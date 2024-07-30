docker-compose run --rm graph_db_loader sh -c 'echo "match (n) detach delete (n)" | app/Script/send-cypher.py graph_db'
