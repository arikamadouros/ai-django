from django.http import JsonResponse
from openai_integration.services import *
from searchai_integration.services import *
import os
appname = os.path.dirname(os.path.abspath(__file__))

def get_documents_results(request, index_name):
    searchAI = SearchAI()
    query = searchAI.getQuery(request.body)['query']
    
    # Extract the search results from the response
    search_results = searchAI.runQuery(query, index_name)
    response_data = search_results.get("response", {})
    documents = response_data.get("value", [])

    # Check if documents were found
    if not documents:
      return JsonResponse({"error": "No documents found"}, status=404)

    # Prepare documents for summarization, including relevant fields like content
    document_texts = [doc["content"] for doc in documents]
    
    # Prepare the results with scores and metadata
    formatted_results = [
      {
        "id": doc.get("id"),
        "title": doc.get("title"),
        "content": doc.get("content"),
        "score": doc.get("@search.score")
      }
      for doc in documents
    ]

    return query, document_texts, formatted_results

def summarize_results(aiContext, prompt):
  openAI = OpenAI()
  openAI.aiContext(aiContext)
  return openAI.getResponse(prompt)
