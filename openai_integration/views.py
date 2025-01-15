from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import *

@csrf_exempt
def get_ai_response(request):

  #try:
  openAI = OpenAI()
  # Force POST
  responseData = openAI.ask(request)

  return JsonResponse(responseData, safe=False)