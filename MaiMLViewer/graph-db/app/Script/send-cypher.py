#!/usr/bin/env python3

import sys
from neo4jrestclient.client import GraphDatabase

str = sys.stdin.read()

host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
url = "http://" + host + ":7474/db/data/"
gdb = GraphDatabase(url)

#print("url: " + url)

#results = gdb.query(str, data_contents=True)
results = gdb.query(str)

for r in results:
  print(r)
