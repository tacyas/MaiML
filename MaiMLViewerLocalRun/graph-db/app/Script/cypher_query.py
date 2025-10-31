import os
import json
from neo4j import GraphDatabase



class Cypher_api():

    def __init__(self, uri, auth=(None, None), api_file='cypher_api.json'):
        self.driver = GraphDatabase.driver(uri, auth=auth, encrypted=False)
        self.session = self.driver.session()

        api_path = os.path.join(os.path.dirname(__file__), api_file)

        with open(api_path) as f:
            self.query_list = json.load(f)


    def __del__(self):
        try:
            self.session
        except:
            pass
        else:
            self.session.close()
        finally:
            try:
                self.driver
            except:
                pass
            else:
                self.driver.close()


    def exec_cypher(self, cypher, params):
        result = self.session.run(cypher, params)
        return result


    def exec_query(self, name, *param_args):
        query = self.query_list[name]
        cypher = query['cypher_str']

        params = {}
        for i, key in enumerate(query['params']):
            params[key] = param_args[i]

        #print('** api name: ', name)
        #print('cypher: ', cypher)
        #print('params: ', params)

        result = self.session.run(cypher, params)
        #print('== result:')
        #for row in result:
        #    print(row)
        #print('== counters: ', result.consume().counters)

        return result


    def do_test(self, dry_run=True):

        print('option "dry_run": ', dry_run)


        print('\n** TEST: "get_xmail"')
        result = self.exec_query('get_xmail')
        for row in result:
            print(row)
            xmail_info = row.get('xmail_info')
            if xmail_info[1] == 'MaiML-A':
                xmail_nid = row.get('nid')
                print('selected XMAIL : ', xmail_nid, xmail_info)


        print('\n** TEST: "get_PNall"')
        result = self.exec_query('get_PNall', xmail_nid)
        record = result.single()
        nodes = record.get('nodes')
        edges = record.get('edges')
        print("--- PN nodes ---")
        nodes_IdByNID = {}
        nodes_byId = {}
        edges_dict = {}
        for node in nodes:
            nid = node.id
            id = node.get('id')
            print(nid, id)
            nodes_IdByNID[nid] = id
            nodes_byId[id] = node
        print("--- PN edges (start, end) ---")
        for edge in edges:
            src_id = nodes_IdByNID[edge.start_node.id]
            dst_id = nodes_IdByNID[edge.end_node.id]
            kind = edge.get('__edge_kind')
            edges_dict[src_id, dst_id] = edge
            print('{:12} : {:24} --> {}'.format(kind, src_id, dst_id))

        #print('## nodes: ', nodes_byId)
        #print('## edges: ', edges_dict)

        place1 = nodes_byId.get('place1')
        place2 = nodes_byId.get('place2')
        place3 = nodes_byId.get('place3')
        place4 = nodes_byId.get('place4')
        tr = nodes_byId.get('transition_a')
        temp1 = nodes_byId.get('materialTemplate1')
        temp2 = nodes_byId.get('conditionTemplate2')
        temp4 = nodes_byId.get('materialTemplate4')
        inst1 = nodes_byId.get('material1')
        inst2 = nodes_byId.get('condition2')
        inst4 = nodes_byId.get('material4')

        if dry_run:
            return

        #result = self.exec_query('get_template', place_nid)
        #for row in result:
        #    print(row)
        #    template_nid = row['template_nid']

        #result = self.exec_query('get_properties', template_nid)
        #for row in result:
        #    print(row)


        def check_result(result, no_record=False):
            record = result.single()
            success = result.consume().counters.contains_updates
            print('  >> ', 'OK' if success else 'NG')
            return no_record or record[0]


        print('\n** TEST: "create_PNnode"')

        print('  * new <place> "place_new" ==> OK')
        result = self.exec_query('create_PNnode', xmail_nid, 'place_new', 'place')
        nid_place_new = check_result(result)
        print('  >> nid: ', nid_place_new)

        print('  * new <transition> "transition_new" ==> OK')
        result = self.exec_query('create_PNnode', xmail_nid, 'transition_new', 'transition')
        nid_transition_new = check_result(result)
        print('  >> nid: ', nid_transition_new)

        print('  * new <place> with same id "place_new" ==> NG')
        result = self.exec_query('create_PNnode', xmail_nid, 'place1', 'place_new')
        check_result(result, no_record=True)

        #result = self.exec_query('test_PNarc', place3.id, nid_transition_new)
        #for row in result:
        #    print(' result : ', row['matched'])


        print('\n** TEST: "create_PNedge"')
        print('  * place to transition ==> OK, <arc>')
        result = self.exec_query('create_PNedge', place3.id, nid_transition_new)
        edge_kind = check_result(result)
        print('  >> edge_kind: ', edge_kind)

        print('  * transition to place ==> OK, <arc>')
        result = self.exec_query('create_PNedge', nid_transition_new, nid_place_new)
        edge_kind = check_result(result)
        print('  >> edge_kind: ', edge_kind)

        print('  * place to place ==> NG')
        result = self.exec_query('create_PNedge', place3.id, nid_place_new)
        check_result(result, no_record=True)

        print('  * transition to transition ==> NG')
        result = self.exec_query('create_PNedge', tr.id, nid_transition_new)
        check_result(result, no_record=True)

        print('  * transition to place (another) ==> NG')
        result = self.exec_query('create_PNedge', tr.id, nid_place_new)
        check_result(result, no_record=True)

        print('  * place to transition (reversed) ==> NG')
        result = self.exec_query('create_PNedge', nid_place_new, nid_transition_new)
        check_result(result, no_record=True)

        print('  * template to place ==> OK, <placeRef>')
        result = self.exec_query('create_PNedge', temp1.id, place2.id)
        edge_kind = check_result(result)
        print('  >> edge_kind: ', edge_kind)

        print('  * template to template ==> OK, <templateRef>')
        result = self.exec_query('create_PNedge', temp1.id, temp2.id)
        edge_kind = check_result(result)
        print('  >> edge_kind: ', edge_kind)

        print('  * instance to instance ==> OK, <instanceRef>')
        result = self.exec_query('create_PNedge', inst1.id, inst2.id)
        edge_kind = check_result(result)
        print('  >> edge_kind: ', edge_kind)

        print('  * instance to template (2nd) ==> NG')
        result = self.exec_query('create_PNedge', inst1.id, temp4.id)
        check_result(result, no_record=True)


        print('\n** TEST: "delete_PNedge"')

        print('  * <arc> ==> OK')
        result = self.exec_query('delete_PNedge', place3.id, nid_transition_new)
        check_result(result, no_record=True)

        print('  * <placeRef> ==> OK')
        result = self.exec_query('delete_PNedge', temp1.id, place1.id)
        check_result(result, no_record=True)

        print('  * <templateRef> ==> OK')
        result = self.exec_query('delete_PNedge', temp1.id, temp4.id)
        check_result(result, no_record=True)

        print('  * <instanceRef> ==> OK')
        result = self.exec_query('delete_PNedge', inst1.id, inst4.id)
        check_result(result, no_record=True)

        print('  * ref ==> OK')
        result = self.exec_query('delete_PNedge', inst1.id, temp1.id)
        check_result(result, no_record=True)


        print('\n** TEST: "create_PNedge" (instance to template)')

        print('  * instance to template (different type) ==> NG')
        result = self.exec_query('create_PNedge', inst1.id, temp2.id)
        check_result(result, no_record=True)

        print('  * instance to template (same type) ==> OK, ref')
        result = self.exec_query('create_PNedge', inst1.id, temp4.id)
        edge_kind = check_result(result)
        print('  >> edge_kind: ', edge_kind)


        result = self.exec_query('get_PNall', xmail_nid)
        record = result.single()
        nodes = record.get('nodes')
        print("--- PN nodes ---")
        for node in nodes:
            nid = node.id
            id = node.get('id')
            print(nid, id)



if __name__ == "__main__":

    import argparse
    import uuid

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost:7687')
    parser.add_argument('--user', default='')
    parser.add_argument('--password', default='')
    parser.add_argument('--test', nargs='*')
    parser.add_argument('--api')
    parser.add_argument('api_args', nargs='*')
    args = parser.parse_args()

    uri = "bolt://" + args.host
    user = args.user
    password = args.password

    query = Cypher_api(uri, auth=(user, password))

    if args.test is not None:
        query.do_test(dry_run=('dry_run' in args.test))
    if args.api:
        converted_args = list(map(lambda x: int(x) if x.isdigit() else x, args.api_args))
        print('api: ', args.api)
        print('args: ', converted_args)
        result = query.exec_query(args.api, *converted_args)
        print('result-keys: ', result.keys())
        print('result-data: ', result.data())
        print('result-counters: ', result.consume().counters)

    del query
