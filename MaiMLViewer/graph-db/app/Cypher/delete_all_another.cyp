// delete all (OPTIONAL ver.)
MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r;
