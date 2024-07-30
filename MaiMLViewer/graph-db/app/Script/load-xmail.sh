f=$@
echo "### XMAIL: $f"

result=$( \
<<<<<<< HEAD
  ./app/Script/xml2cypher.py "$f" \
=======
  python ./app/Script/xml2cypher.py "$f" \
>>>>>>> 06ad53fa34db96c372a6ef94cae120abb4d7eb8f
   | docker exec -i graph-db cypher-shell --format plain
  )
echo "### create_node:" ${result}
node_id=$( echo ${result} | awk -v FS='[\]\[ ]' '{print$2}' )
echo "### node_id:" ${node_id}

cypher_str="
match (a:XMAIL)
  -[:XML_Root]->(d)
  -[:XML_Child]->(pr {__tag: 'protocol'})
  -[:XML_Child]->(me {__tag: 'method'})
  -[:XML_Child]->(pg {__tag: 'program'})
  -[:XML_Child]->(pn {__tag: 'pnml'}),
  (pn)-[:XML_Child]->(ar {__tag: 'arc'}),
  (pn)-[:XML_Child]->(s),
  (pn)-[:XML_Child]->(t)
where
  id(a)=${node_id}
  and ar.source=s.id
  and ar.target=t.id
merge (s)-[:PNarc]->(t);
"

#echo "### Cypher BEGIN <<<"
#echo "${cypher_str}"
#echo "### >>>"

echo "${cypher_str}" \
 | docker exec -i graph-db cypher-shell --format plain
