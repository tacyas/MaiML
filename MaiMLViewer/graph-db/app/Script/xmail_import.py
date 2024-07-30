#!/usr/bin/env python3

import sys
import io
from pathlib import Path
import tempfile
import shutil
import os


def move_file_to_working_directory(path, dir_base):
    tmpdir = tempfile.mkdtemp(dir=dir_base)
    os.chmod(tmpdir, 0o755)
    in_name = Path(path).name
    dst_path = Path(tmpdir) / in_name
    shutil.move(path, dst_path)
    return dst_path


def convert_xml(fname):
    import xml2cypher

    io_str = io.StringIO()
    xml2cypher.xml2cypher(fname, output=io_str)
    cypher = io_str.getvalue()

    return cypher


###

if __name__ == "__main__":
    import argparse
    import cypher_query
    import xml2cypher

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost:7687')
    parser.add_argument('--user', default='')
    parser.add_argument('--password', default='')
    #parser.add_argument('--node-id', type=int, required=True)
    #parser.add_argument("--output")
    parser.add_argument('--work-dir', default=os.getenv('MAIML_TMP_DIR', '/opt/app/xmail-viewer/models/tmp'))
    parser.add_argument('input')
    args = parser.parse_args()

    #uri = "bolt://" + args.host
    uri = "neo4j://" + args.host
    user = args.user
    password = args.password

    #print('Neo4j uri: ', uri)
    #print('user: "{}"'.format(user))
    #print('pass: "{}"'.format(password))
    query = cypher_query.Cypher_api(uri, auth=(user, password))

    ###
    ### 1st query: XMAIL import
    ###
    dst_path = move_file_to_working_directory(args.input, args.work_dir)
    cypher = convert_xml(dst_path)
    params = {}
    result = query.exec_cypher(cypher, params)
    record = result.data()[0]
    print(record, file=sys.stderr)
    print('"XMAIL import" result-counters: ', result.consume().counters, file=sys.stderr)
    nid = record['xmail_nid']

    ###
    ### 2nd query: update arc connection
    ###
    result = query.exec_query('import_arc', nid)
    print('"import_arc" result-counters: ', result.consume().counters, file=sys.stderr)

    result = query.exec_query('import_placeRef', nid)
    print('"import_placeRef" result-counters: ', result.consume().counters, file=sys.stderr)

    result = query.exec_query('import_ref', nid)
    print('"import_ref" result-counters: ', result.consume().counters, file=sys.stderr)

    result = query.exec_query('import_templateRef', nid)
    print('"import_templateRef" result-counters: ', result.consume().counters, file=sys.stderr)

    result = query.exec_query('import_instanceRef', nid)
    print('"import_instanceRef" result-counters: ', result.consume().counters, file=sys.stderr)

    result = query.exec_query('import_same_template', nid)
    print('"import_same_template" result-counters: ', result.consume().counters, file=sys.stderr)

    result = query.exec_query('import_nodes', nid)
    print('"import_nodes" result-counters: ', result.consume().counters, file=sys.stderr)

    print('return {} as xmail_nid;'.format(nid))

    del query



###
