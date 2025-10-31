// 全XMAIL内のarc接続を作成
match (a:XMAIL)
  -[:XML_Root]->(d)
  -[:XML_Child]->(pr {__tag: 'protocol'})
  -[:XML_Child]->(me {__tag: 'method'})
  -[:XML_Child]->(pg {__tag: 'program'})
  -[:XML_Child]->(pn {__tag: 'pnml'}),
  (pn)-[:XML_Child]->(ar {__tag: 'arc'})
optional match
  (pn)-[:XML_Child]->(s),
  (pn)-[:XML_Child]->(t)
where
  ar.source=s.id
  and ar.target=t.id
merge (s)-[:PNarc]->(t);
