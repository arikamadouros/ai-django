## Spin up Docker
docker compose up --build
docker exec -it django_ai_project-web-1 /bin/bash

## Command line tests 
curl -X POST "http://127.0.0.1:8000/api/integration/" \
    -H "Content-Type: application/json" \
    -d '{"query": "tell me about django"}'\

curl -X POST "http://127.0.0.1:8000/api/openai/" \     
     -H "Content-Type: application/json" \
     -d '{"query": "Tell me about Django"}'\

curl -X POST "http://127.0.0.1:8000/api/searchai/" \   
     -H "Content-Type: application/json" \
     -d '{"query": "Tell me about Django"}' 

curl -X POST http://localhost:8000/api/openai/ \
-H "Content-Type: application/json" \
-d '{
  "type": "message",
  "query": "hello",
  "from": {"id": "user1"},
  "conversation": {"id": "conv1"},
  "recipient": {"id": "bot"},
  "channelId": "directline",
  "serviceUrl": "http://localhost:8000"
}'# ai-django
