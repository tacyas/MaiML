#!/usr/bin/env python3

#import sys
#import uuid
#import os
#from lxml import etree
#import xmlsec
#from signxml import XMLSigner, XMLVerifier

### local packages
import maiml


###

if __name__ == "__main__":
    import argparse
    import cypher_query

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost:7687')
    parser.add_argument('--user', default='')
    parser.add_argument('--password', default='')
    parser.add_argument('--node-id', type=int, required=True)
    parser.add_argument("--output")
    parser.add_argument('--key-file')
    parser.add_argument('--key-passphrase')
    parser.add_argument('--input')
    args = parser.parse_args()

    uri = "bolt://" + args.host
    user = args.user
    password = args.password

    print('Neo4j uri: ', uri)
    print('user: "{}"'.format(user))
    print('pass: "{}"'.format(password))
    query = cypher_query.Cypher_api(uri, auth=(user, password))

    result = query.exec_query('get_xmail')
    xmail_records = result.data()

    infile = None
    for xmail in xmail_records:
        if xmail['nid'] == args.node_id:
            infile = xmail['file']
            break
    if args.input is not None:
        infile = args.input

    #result = query.exec_query('get_updated_PN', args.node_id)
    result = query.exec_query('get_PN_single', args.node_id)
    pn_records = result.data()

    ## node更新リスト作成
    node_ids = []
    updated_node_list = []
    print(pn_records)

    #nodes = pn_records[0]['nodes']
    nodes = result.graph().nodes
    #edges = pn_records[0]['edges']
    edges = result.graph().relationships

    for node in nodes:
        print('scanning node: ', node)
        node_id = node.id
        print('checking node {}: __xmail_nid = {}'.format(node_id, node['__xmail_nid']))
        if node['__xmail_nid'] == args.node_id:
            print('*** found node of own XMAIL')
            node_ids.append(node_id)
            if 'UNREGISTERED' in node.labels:
                #print('Unregistered!')
                name = ''
                desc = ''
                node_info = (node['__tag'], node['id'], name, desc)
                #print('node_id: {}, {}'.format(node_id, node_info))
                #result = query.exec_query('get_template', node_id)
                #print(result.data())
                updated_node_list.append(node_info)

    ## edge更新リスト作成
    edge_list = []
    print('node_ids: ', node_ids)
    for edge in edges:
        if edge.type == 'PN':
            src = edge.start_node
            dst = edge.end_node
            print('checking "{}", src: {}, dst: {}'.format(edge.type, src['id'], dst['id']))
            if src.id in node_ids and dst.id in node_ids:
                print('found PN edges in MaiML')
                #edge_list.append((src['id'], dst['id']))
                edge_list.append(edge)

    del query

    ## XML Signature の鍵情報
    xmlsig_args = {}
    if args.key_file is not None:
        xmlsig_args['key_file'] = args.key_file
    if args.key_passphrase is not None:
        xmlsig_args['passphrase'] = args.key_passphrase

    ## XMAIL ファイル更新処理
    #update_xmail(infile, args.output, (updated_node_list, arc_list), **xmlsig_args)
    mfile = maiml.MaiML_File(infile, xmlsig_args=xmlsig_args)
    mfile.update_PNnodes(updated_node_list)
    mfile.update_PNedges(edge_list)
    mfile.output(args.output)

###
