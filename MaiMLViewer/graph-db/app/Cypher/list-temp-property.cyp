// 指定IDのplaceノードに関連するtemplateのproperty情報を出力
//
//   usage: where句 'id(pl)=xxx' のxxxにplaceノードのID値を指定
//
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
match
  (te)-[:XML_Child*]->(prop {__tag: 'property'})
optional match
  (prop)-[:XML_Child]->(v {__tag: 'value'})-[:XML_Data]->(vd)
optional match
  (prop)-[:XML_Child]->(d {__tag: 'description'})-[:XML_Data]->(dd)
optional match
  (prop)<-[:XML_Child]-(parent {__tag: 'property'})
return
  te.__tag as tag_name,
  te.id as template,
  id(prop) as nid,
  id(parent) as parent_nid,
  dd.value as description,
  vd.value as value,
  properties(prop) as attrib;
