from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .services import *

@csrf_exempt
def query_search_ai(request):
    index_name='ai-index-1'

    searchAI = SearchAI()
    responseData = searchAI.query(request, index_name)

    return JsonResponse(responseData, safe=False)