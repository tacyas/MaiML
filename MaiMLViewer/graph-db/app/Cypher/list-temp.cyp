// 指定IDのplaceノードのtemplate情報を抽出
match
  (pr {__tag: 'protocol'})
  -[:XML_Child]->(me {__tag: 'method'})
  -[:XML_Child]->(pg {__tag: 'program'})
  -[:XML_Child]->(pn {__tag: 'pnml'})
  -[:XML_Child]->(pl {__tag: 'place'}),
  (pr)-[:XML_Child*]->(te)-[:XML_Child]->(plR {__tag: 'placeRef'})
where
  id(pl)=0
  and plR.ref = pl.id
with te
optional match
  (te)-[:XML_Child]->(u {__tag: 'uuid'})-[:XML_Data]->(ud)
optional match
  (te)-[:XML_Child]->(n {__tag: 'name'})-[:XML_Data]->(nd)
optional match
  (te)-[:XML_Child]->(d {__tag: 'description'})-[:XML_Data]->(dd)
return
  te.__tag as tag_name,
  te.id as template,
  ud.value as uuid,
  nd.value as name,
  dd.value as description;
