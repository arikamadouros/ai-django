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

  def test(self, query, index):
    return {"query": query, "summary": "this is a systems searchai test", "results": [
      'endpoint: '+self.endpoint(),
      'api_key: '+self.api_key(),
      'searchVersion: '+self.searchVersion(),
      'contentType: '+self.contentType(),
      'url: '+self.url(),
      'headers: '+str(self.headers()),
      'testConnect: '+str(self.runQuery(query, index))
    ]}

  """
  Parse Django request for query.
  """
  def getQuery(self, request, index='query'):
    responseData = {}
    badMethod = self.checkMethod(request.method)
    if badMethod:
      return badMethod

    try:
      query = json.loads(request.body)
      responseData['query'] = query.get(index, "")
      responseData['code'] = 200

    except Exception as e:
      responseData['code'] = 500
      responseData['context'] = self.getContext()
      responseData['response'] = [{f"{type(e).__name__}":f"{str(e)}"}]
    return responseData
  
  """
  Send a prompt to Search and return the response.
  """
  def runQuery (self, query, index):
    responseData = {}
    responseData['query'] = query

    try:
      payload = {'search':responseData['query']}
      received = requests.post(self.url(index), headers=self.headers(), json=payload)
      received.raise_for_status()

      if received.status_code:
        responseData['code'] = received.status_code
      
      response = self.parseQueryResult(received)
      
      responseData['context'] =  response.get("context")
      responseData['response'] =  response.get("documents")

    except Exception as e:
      responseData['code'] = 500
      responseData['context'] = self.getContext()
      responseData['response'] = [{f"{type(e).__name__}":f"{str(e)}"}]

    return responseData
  
  """
  Receives result and returns parsed data
  """
  def parseQueryResult (self, result):
    responseData = {}
    try:
      response = result.json()
      if response.get('@odata.context'):
        responseData['context'] = response.get('@odata.context')

      if response.get('value'):
        responseData['documents'] = [
        {
          "id": doc.get("id"),
          "title": doc.get("title"),
          "content": doc.get("content"),
          "score": doc.get("@search.score")
        }
        for doc in response.get('value')
      ]

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
