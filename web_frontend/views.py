import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ai_integration.services import *
from openai_integration.services import *
from searchai_integration.services import *


@csrf_exempt
def webchat(request):
  index_name='ai-index-1'
  responseData={}
  searchAI = SearchAI()
  query = searchAI.getQuery(request)['query']
  response=searchAI.runQuery(query, index_name)
  responseData['summary']='summary'
  responseData['query']=str(response['query'])
  responseData['results']=response['response']


  if not responseData['results']:
    return JsonResponse({"error": "No document content available"}, status=404)

  # Summarize using OpenAI
  aiContext = "You are an AI assistant that summarizes search results."
  prompt = f"Summarize the following documents in response to the query: '{responseData['query']}'.\n\nDocuments:\n" + str(responseData['results'])
  responseData['summary'] = summarize_results(aiContext, prompt)['response']

  return JsonResponse(responseData)
