#!/usr/bin/env python3

import sys
import uuid
import os
import itertools
from lxml import etree
#import xmlsec
from signxml import XMLSigner, XMLVerifier



def delete_node(node):
    parent = node.getparent()
    prev = node.getprevious()
    if prev is None:
        parent.text = node.tail
    else:
        prev.tail = node.tail
    parent.remove(node)


def create_node(node, tag, namespaces=None):
    def get_indent(node):
        prev = node.getprevious()
        if prev is None:
            return node.getparent().text
        else:
            return prev.tail

    def set_indent(node, indent):
        prev = node.getprevious()
        if prev is None:
            node.getparent().text = indent
        else:
            prev.tail = indent

    indent_parent = get_indent(node)
    sub = etree.SubElement(node, tag, nsmap=namespaces)

    prev = sub.getprevious()
    if prev is None:
        indent = get_indent(node)
        #print('parent: {}, text: "{}"'.format(node.tag, indent))
        set_indent(sub, indent + ' ' * 2)
        sub.tail = indent
    else:
        indent = get_indent(prev)
        tail = prev.tail
        #print('prev: {}, tail: "{}"'.format(prev.tag, indent))
        set_indent(sub, indent)
        sub.tail = tail

    return sub


def sign_xml(root, key_file='example.key', passphrase=b'secret'):
    import os
    from signxml import XMLSigner, XMLVerifier

    key_path = os.path.join(os.path.dirname(__file__), key_file)
    #cert = open("example.pem").read()
    key = open(key_path).read()
    #root = etree.fromstring(data_to_sign)
    #signed_root = XMLSigner().sign(root, key=key, cert=cert,
    #    passphrase=b'secret')
    signed_root = XMLSigner().sign(root, key=key,
        passphrase=passphrase)
    #verified_data = XMLVerifier().verify(signed_root).signed_xml

    return signed_root



class MaiML_File:

    def __init__(self, infile, xmlsig_args=None) -> None:
        self.default_ns = ''
        self.xmlsig_args = xmlsig_args or {}

        ## 親XMAIL入力
        self.xml_tree = etree.parse(infile)
        self.xml_root = self.xml_tree.getroot()

        ## 名前空間の定義
        ns = self.xml_root.nsmap[None]
        print('namespace: ', ns)
        self.default_ns = ns
        self.nsmap = {
            'ns': ns,
            'ds': 'http://www.w3.org/2000/09/xmldsig#'
        }

        ## 編集対象ノード検索
        self.xml_node_doc = self.xml_root.find('ns:document', namespaces=self.nsmap)
        self.xml_node_pnml = self.xml_root.xpath('/*/ns:protocol/ns:method//ns:pnml', namespaces=self.nsmap)[0]
        #self.xml_node_results = self.xml_root.xpath('/*/ns:data/ns:results', namespaces=self.nsmap)[0]
        # 2023/4/19 edit
        if len(self.xml_root.xpath('/*/ns:data/ns:results', namespaces=self.nsmap)) != 0:
            self.xml_node_results = self.xml_root.xpath('/*/ns:data/ns:results', namespaces=self.nsmap)[0]
        
        self.reset_signature()

    def output(self, outfile):
        self.set_uuid()
        self.set_signature()

        ## 更新済みXMAIL出力
        if outfile is not None:
            with open(outfile, 'wb') as f:
                f.write(etree.tostring(self.xml_signed_root,
                        xml_declaration=True,
                        encoding='utf-8'))

    def get_nstag(self, tag, ns=None):
        if ns is None:
            ns = self.default_ns
        return '{' + ns + '}' + tag

    def create_node_ns(self, node, tag, tag_ns=None, namespaces=None):
        return create_node(node, self.get_nstag(tag, ns=tag_ns), namespaces=namespaces)

    def create_parent_node(self, elm, uuid, svalue):
        elm_parent = self.create_node_ns(elm, 'parent')
        elm_uuid = self.create_node_ns(elm_parent, 'uuid')
        elm_uuid.text = uuid
        elm_hash = self.create_node_ns(elm_parent, 'hash')
        elm_hash.text = svalue

    def create_signature_node(self, elm):
        ns_ds = 'http://www.w3.org/2000/09/xmldsig#'

        nsmap_ds = {
            'ds': ns_ds
        }
        nsmap_default = {
            None: ns_ds
        }
        nsmap = nsmap_ds

        alg_can = 'http://www.w3.org/2001/10/xml-exc-c14n#'
        alg_sign = 'http://www.w3.org/2000/09/xmldsig#rsa-sha1'
        alg_tf = 'http://www.w3.org/2000/09/xmldsig#enveloped-signature'
        alg_dig = 'http://www.w3.org/2000/09/xmldsig#sha1'

        elm_sig = self.create_node_ns(elm, 'Signature', tag_ns=ns_ds, namespaces=nsmap)

        return elm_sig

    def reset_signature(self):
        ## 親のXML署名の取得
        xml_node_sign = self.xml_node_doc.find('ds:Signature', namespaces=self.nsmap)
        #print('Signature: ', node_sign)
        orig_svalue = None
        if xml_node_sign is not None:
            node_svalue = self.xml_root.xpath('//ds:SignatureValue', namespaces=self.nsmap)[0]
            node_dvalue = self.xml_root.xpath('//ds:DigestValue', namespaces=self.nsmap)[0]
            self.orig_SignatureValue = node_svalue.text
            self.orig_DigestValue = node_dvalue.text
            print('original SignatureValue: ', self.orig_SignatureValue)
            print('original DigestValue: ', self.orig_DigestValue)
            delete_node(xml_node_sign)
        else:
            ## DigestValue算出（仮のXML署名作成により取得）
            node_sign = self.create_signature_node(self.xml_node_doc)
            node_sign.set('Id', 'placeholder')
            signed_root = sign_xml(self.xml_tree, **self.xmlsig_args)
            node_dvalue = signed_root.xpath('//ds:DigestValue', namespaces=self.nsmap)[0]
            self.orig_DigestValue = node_dvalue.text
            print('calculated DigestValue: ', self.orig_DigestValue)
            delete_node(node_sign)

    def set_uuid(self):
        ## UUID新規設定
        node_uuid = self.xml_node_doc.find('ns:uuid', namespaces=self.nsmap)
        self.orig_uuid = node_uuid.text
        node_uuid.text = str(uuid.uuid4())
        print('original uuid: ', self.orig_uuid)
        print('new uuid: ', node_uuid.text)

    def set_signature(self):
        ## 親のXML署名リンク作成
        node_parent = self.xml_node_doc.find('ns:parent', namespaces=self.nsmap)
        #print('parent: ', node_parent)
        if node_parent is not None:
            delete_node(node_parent)
        self.create_parent_node(self.xml_node_doc, self.orig_uuid, self.orig_DigestValue)

        ## 新規XML署名の作成
        node_sign = self.create_signature_node(self.xml_node_doc)
        node_sign.set('Id', 'placeholder')

        self.xml_signed_root = sign_xml(self.xml_tree, **self.xmlsig_args)
        node_svalue = self.xml_signed_root.xpath('//ds:SignatureValue', namespaces=self.nsmap)[0]
        node_dvalue = self.xml_signed_root.xpath('//ds:DigestValue', namespaces=self.nsmap)[0]
        orig_svalue = node_svalue.text
        orig_dvalue = node_dvalue.text
        print('new SignatureValue: ', orig_svalue)
        print('new DigestValue: ', orig_dvalue)

    def create_pnml_node(self, type, id, source=None, target=None, name=None, description=None):
        elm_arc = self.create_node_ns(self.xml_node_pnml, type)
        elm_arc.set('id', id)
        if source:
            elm_arc.set('source', source)
        if target:
            elm_arc.set('target', target)
        elm_name = self.create_node_ns(elm_arc, 'name')
        elm_name.text = name
        elm_desc = self.create_node_ns(elm_arc, 'description')
        elm_desc.text = description

    def create_ref_node(self, node, type, id, ref):
        elm_ref = self.create_node_ns(node, type)
        elm_ref.set('id', id)
        elm_ref.set('ref', ref)

    def create_edge(self, source_n4j, target_n4j, name=None, description=None):
        tag_type_table = {
            'place': 0,
            'transition': 0,
            'materialTemplate': 1,
            'conditionTemplate': 1,
            'resultTemplate': 1,
            'material': 2,
            'condition': 2,
            'result': 2,
        }
        edge_type_table = [
            [('ARC', 'arc'), None, None],
            [('XXREF', 'placeRef'), ('XXREF', 'templateRef'), None],
            [None, ('REF', 'ref'), ('XXREF', 'instanceRef')]
        ]

        source = source_n4j['id']
        target = target_n4j['id']
        node = self.xml_node_doc.xpath("//*[@id='{}']".format(source), namespaces=self.nsmap)[0]
        tag_src = source_n4j['__tag']
        tag_tgt = target_n4j['__tag']
        print('create_edges: <{}>-<{}> src:{}, tgt:{}'.format(tag_src, tag_tgt, source, target))

        edge_type, tag = edge_type_table[tag_type_table[tag_src]][tag_type_table[tag_tgt]]

        id = tag + '_' + source + '_' + target

        if edge_type == 'ARC':
            print('  * <arc>')
            self.create_pnml_node('arc', id,
                    source=source,
                    target=target,
                    name=name,
                    description=description)
        elif edge_type == 'XXREF':
            print('  * <{}>'.format(tag))
            self.create_ref_node(node, tag, id, target)
        elif edge_type == 'REF':
            print('  * @ref')
            node.set('ref', target)
        else:
            raise
        print('  * src:{} tgt:{}'.format(source, target))

    def delete_edge(self, node, type):
        print('delete type: {}'.format(type))
        if type == 'REF':
            print('  * reset attribute "ref"')
            node.set('ref', '')
        else:
            print('  * delete_node()')
            delete_node(node)

    def get_arc(self):
        return self.xml_node_pnml.xpath("ns:arc", namespaces=self.nsmap)

    def update_PNedges(self, edge_list):

        ## MaiMLデータ中の arc を辞書に登録
        dict_xmail_edges = {}
        for xmail_arc in self.xml_node_pnml.xpath("ns:arc", namespaces=self.nsmap):
            id = xmail_arc.get('id')
            src = xmail_arc.get('source')
            tgt = xmail_arc.get('target')
            print('MaiML <arc> ', id, src, tgt)
            dict_xmail_edges[src, tgt] = (xmail_arc, 'ARC')

        print('## dict ##: ', dict_xmail_edges.keys())

        ## MaiMLデータ中の xxRef を辞書に登録
        it_xxxRef = itertools.chain(
            self.xml_node_doc.xpath("//ns:placeRef", namespaces=self.nsmap),
            self.xml_node_doc.xpath("//ns:templateRef", namespaces=self.nsmap),
            self.xml_node_doc.xpath("//ns:instanceRef", namespaces=self.nsmap)
        )
        for xmail_edge in it_xxxRef:
            id = xmail_edge.get('id')
            pnode = xmail_edge.getparent()
            src = pnode.get('id')
            tgt = xmail_edge.get('ref')
            tag = pnode.tag.rpartition('}')
            print('MaiML <{}> id:{}, src:{}, tgt:{}'.format(tag, id, src, tgt))
            dict_xmail_edges[src, tgt] = (xmail_edge, 'XXREF')

        print('## dict ##: ', dict_xmail_edges.keys())

        ## MaiMLデータ中のインスタンス ref を辞書に登録
        it_ref = itertools.chain(
            self.xml_node_results.xpath("//ns:material", namespaces=self.nsmap),
            self.xml_node_results.xpath("//ns:condition", namespaces=self.nsmap),
            self.xml_node_results.xpath("//ns:result", namespaces=self.nsmap)
        )
        for xmail_edge in it_ref:
            id = xmail_edge.get('id')
            src = id
            tgt = xmail_edge.get('ref')
            print('MaiML <{}> id:{}, src:{}, tgt:{}'.format(xmail_edge.tag, id, src, tgt))
            dict_xmail_edges[src, tgt] = (xmail_edge, 'REF')

        print('## dict ##: ', dict_xmail_edges.keys())

        ## edge更新リストをスキャンして既存分は辞書から削除、追加分のみのリストを作成する
        new_edges = []
        for edge in edge_list:
            src_n4j = edge.start_node
            tgt_n4j = edge.end_node
            src = src_n4j['id']
            tgt = tgt_n4j['id']
            if (src, tgt) in dict_xmail_edges:
                print('already exists: ', src, tgt)
                del dict_xmail_edges[src, tgt]
            else:
                new_edges.append(edge)
                #print('*** add new arc: ', src, tgt)
                #id = 'arc_' + src + '_' + tgt
                #self.create_edge(id, src_n4j, tgt_n4j)

        print('## dict ##: ', dict_xmail_edges.keys())

        ## edge更新リストに存在せず辞書に残っている edge を削除
        for edge_node, edge_type in dict_xmail_edges.values():
            print('*** delete edge: ', edge_node.items())
            self.delete_edge(edge_node, edge_type)

        ## edge更新リスト新規追加分についてMaiMLに新規作成
        for edge in new_edges:
            src_n4j = edge.start_node
            tgt_n4j = edge.end_node
            src = src_n4j['id']
            tgt = tgt_n4j['id']
            print('*** add new edge: ', src, tgt)
            self.create_edge(src_n4j, tgt_n4j)

    def update_PNnodes(self, node_list):
        ## 新規placeの作成
        for type, id, name, description in node_list:
            print('*** create node: ', type, id, name, description)
            self.create_pnml_node(type, id,
                    name=name,
                    description=description
                    )

###

if __name__ == "__main__":
    import argparse
    import cypher_query

    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument("--output")
    parser.add_argument('--key-file')
    parser.add_argument('--key-passphrase')
    args = parser.parse_args()


    ## XML Signature の鍵情報
    xmlsig_args = {}
    if args.key_file is not None:
        xmlsig_args['key_file'] = args.key_file
    if args.key_passphrase is not None:
        xmlsig_args['passphrase'] = args.key_passphrase

    ### !!!TODO DBから取得
    node_list = [
        ###
        ### (type, id, name, description)
        ###
        ('place', 'place9001', 'hoge_place001', 'hogehoge'),
        ('place', 'place9002', 'hoge_place002', 'hogehogehoge'),
        ('transition', 'transition9001', 'hoge_transition001', 'hoge')
    ]
    arc_list = [
        ('place5', 'transition_b'),
        ('place6', 'transition_b'),
        ('transition_b', 'place7'),
        ('transition_b', 'place9001'),
        ('place9001', 'transition9001'),
        ('transition9001', 'place9002')
    ]

    ## XMAIL ファイル更新処理
    #update_xmail(infile, args.output, (updated_node_list, arc_list), **xmlsig_args)
    mfile = MaiML_File(args.infile, xmlsig_args=xmlsig_args)
    mfile.update_PNnodes(node_list)
    mfile.update_PNedges(arc_list)
    mfile.output(args.output)


###
