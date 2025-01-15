from django.http import JsonResponse
from openai_integration.services import *
from searchai_integration.services import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .services import *


@csrf_exempt
def integrate_search_and_summarize(request):
    responseData = {}
    # Step 1: Search for relevant documents
    index_name='ai-index-1'
    responseData['query'], documents, responseData['formatted_results'] = get_documents_results(request, index_name)

    if not documents:
      return JsonResponse({"error": "No document content available"}, status=404)

    # Summarize using OpenAI
    aiContext = "You are an AI assistant that summarizes search results."
    prompt = f"Summarize the following documents in response to the query: '{responseData['query']}'.\n\nDocuments:\n" + "\n\n".join(documents)
    responseData['summary'] = summarize_results(aiContext, prompt) 
    
    # Return the summary and results
    return JsonResponse(responseData, safe=False)
