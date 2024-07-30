docker run \
  --name neo4j_kyutech \
  --detach \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=none \
  neo4j:3.4
