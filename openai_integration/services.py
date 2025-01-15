import inspect
import json
import requests
from django.conf import settings

openai_api_base = settings.AZURE_OPENAI_API_BASE
openai_api_key = settings.AZURE_OPENAI_API_KEY
openai_api_version = settings.AZURE_OPENAI_API_VERSION
openai_deployment = settings.AZURE_OPENAI_DEPLOYMENT_NAME
openai_content_type = settings.AZURE_OPENAI_CONTENT_TYPE
openai_completion = settings.AZURE_OPENAI_COMPLETION

class OpenAI:
  def __init__(self):
    self.openai_api_base = openai_api_base
    self.openai_api_key = openai_api_key
    self.openai_api_version = openai_api_version
    self.openai_deployment = openai_deployment
    self.openai_completion = openai_completion
    self.openai_content_type = openai_content_type
    self.openai_context = "You are an AI assistant that summarizes search results."
    self.openai_headers =  {
      "Content-Type": openai_content_type,
      "api-key": openai_api_key,
    }
    self.openai_url = f"{self.openai_api_base}openai/deployments/{self.openai_deployment}/{self.openai_completion}?api-version={self.openai_api_version}"
  
  """
  Get OpenAI API Headers
  """
  def headers(self):
    return self.openai_headers
  
  """
  Get and Re-Set OpenAI API Endpoint URL
  """
  def url(self, newVal=False):    
    if newVal:
      self.openai_url = newVal
    else:
      return self.openai_url
    
  """
  Get and Re-Set OpenAI Content Type
  """
  def contentType(self, newVal=False):    
    if newVal:
      self.openai_content_type = newVal
    else:
      return self.openai_content_type

  """
  Get and Set OpenAI Deployment Name
  """
  def deployment(self, newVal=False):
    if newVal:
      self.openai_deployment = newVal
    else:
      return self.openai_deployment

  """
  Get and Set OpenAI API Version
  """
  def apiVersion(self, newVal=False):
    if newVal:
      self.openai_api_version = newVal
    else:
      return self.openai_api_version

  """
  Get and Set OpenAI API Key
  """  
  def api_key(self, newVal=False):
    if newVal:
      self.openai_api_key = newVal
    else:
      return self.openai_api_key

  """
  Get and Set OpenAI API URL Base
  """  
  def api_base(self, newVal=False):
    if newVal:
      self.openai_api_base = newVal
    else:
      return self.openai_api_base
    
  """
  Get and Set OpenAI AI Context
  """  
  def aiContext(self, newVal=False):
    if newVal:
      self.openai_context = newVal
    else:
      return self.openai_context
  
  """
  Receive Django request and index. Return the prompt.
  """
  def ask(self, request):
    badMethod = self.checkMethod(request.method)
    if badMethod:
      return badMethod

    prompt = self.getPrompt(request.body)
    return self.getResponse(prompt['prompt']['query'])

  """
  Send a prompt to OpenAI and return the response.
  """
  def getResponse(self, prompt):
    responseData = {}

    try:
      responseData['prompt'] = prompt
      payload = self.buildPayload(prompt)

      received = requests.post(self.url(), headers=self.headers(), json=payload)
      received.raise_for_status()

      if received.status_code:
        responseData['code'] = received.status_code

      responseData['response'] = received.json()['choices'][0]['message']['content']
      
    except Exception as e:
      responseData['code'] = received.status_code
      responseData[type(e).__name__] = str(e)
      responseData['context'] = self.getContext()

    return responseData

  """
  Parse Django request for prompt.
  """
  def getPrompt(self, requestBody):
    responseData = {}

    try:
      responseData['code'] = 200
      responseData['prompt'] = json.loads(requestBody)

    except Exception as e:
      responseData['code'] = 500
      responseData[type(e).__name__] = str(e)
      responseData['context'] = self.getContext()
    return responseData

  """
  Build Payload
  """  
  def buildPayload(self, prompt, max_tokens=500, temperature=0.7, top_p=0.95):
    payload = {
      "messages": [
          {"role": "system", "content": self.aiContext()},
          {"role": "user", "content": prompt}
      ],
      "max_tokens": max_tokens,
      "temperature": temperature,
      "top_p": top_p,
    }
    return payload

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
