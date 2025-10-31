// 指定IDのXMAILを削除
//
// (*) L.4 --> "where id(a)=" + node_ID
//
match p=(a:XMAIL)
  -[:XML_Root]->(r)
  -[:XML_Child|XML_Data*1..]->(n)
where id(a)=0
detach delete p;
