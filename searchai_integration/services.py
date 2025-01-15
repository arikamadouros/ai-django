import requests
import json
import inspect
from django.conf import settings

search_content_type = settings.SEARCH_CONTENT_TYPE
search_endpoint = settings.SEARCH_ENDPOINT
search_api_key = settings.SEARCH_API_KEY
search_version = settings.SEARCH_VERSION

class SearchAI:
  def __init__(self):
    self.search_endpoint = search_endpoint
    self.search_api_key = search_api_key
    self.content_type = search_content_type
    self.search_version = search_version

    self.headers_search =  {
      "Content-Type": search_content_type,
      "api-key": search_api_key,
    }
  
  """
  Get Search AI API Headers
  """
  def headers(self):
    return self.headers_search
  
  """
  Generate Search AI API Endpoint URL
  """
  def url(self, index="placeholder"):
    return f"{self.search_endpoint}/indexes/{index}/docs/search?api-version={self.search_version}"

  """
  Get and Re-Set OpenAI Content Type
  """
  def contentType(self, newVal=False):    
    if newVal:
      self.content_type = newVal
    else:
      return self.content_type
    
  """
  Get and Set Search API Version
  """
  def searchVersion(self, newVal=False):
    if newVal:
      self.search_version = newVal
    else:
      return self.search_version

  """
  Get and Set Search API Key
  """  
  def api_key(self, newVal=False):
    if newVal:
      self.search_api_key = newVal
    else:
      return self.search_api_key

  """
  Get and Set Search API Endpoint
  """  
  def endpoint(self, newVal=False):
    if newVal:
      self.search_endpoint = newVal
    else:
      return self.search_endpoint

  """
  Receive Django request and index. Return the prompt.
  """
  def query(self, request, index):
    badMethod = self.checkMethod(request.method)
    if badMethod:
      return badMethod

    query = self.getQuery(request.body)
    responseData = self.getResults(query, index)
    return responseData

  """
  Parse Django request for query.
  """
  def getQuery(self, requestBody, index='query'):
    responseData = {}

    try:
      responseData['code'] = 200
      query = json.loads(requestBody)
      responseData['query'] = query.get(index, "")

    except Exception as e:
      responseData['code'] = 500
      responseData[type(e).__name__] = str(e)
      responseData['context'] = self.getContext()
    return responseData
  
  """
  Send a prompt to Search and return the response.
  """
  def getResults (self, query, index):
    responseData = {}

    try:
      responseData['query'] = query['query']
      payload = {'search':responseData['query']}

      received = requests.post(self.url(index), headers=self.headers(), json=payload)
      received.raise_for_status()

      if received.status_code:
        responseData['code'] = received.status_code

      responseData['response'] = received.json()
      
    except Exception as e:
      responseData[type(e).__name__] = str(e)
      responseData['context'] = self.getContext()

    return responseData

  """
  Enforce POST.
  """
  def checkMethod(self, method):
    responseData = {}
    try:
      if method != "POST":
        raise BadMethod(method)
      else:
        return False
    
    except BadMethod as e:
      responseData['code'] = e.status_code
      responseData[type(e).__name__] = str(e)
      responseData['context'] = self.getContext()
      return responseData

  """
  Returns traceback information for error handler
  """
  def getContext (self):
    return inspect.getouterframes( inspect.currentframe() )[3][3] + "() -> " + inspect.getouterframes( inspect.currentframe() )[2][3] + "() -> " + inspect.getouterframes( inspect.currentframe() )[1][3]  + "()"

"""
Custom Exceptions
"""
class BadMethod(Exception):
  def __init__(self, method):
    self.message = "Received "+ method+ ". Must Use POST."
    self.status_code = 405
        
  def __str__(self):
    return self.message
