import json
from http import HTTPStatus
from azure.core.exceptions import DeserializationError
from botbuilder.schema import Activity
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .bot_logic import *


@csrf_exempt
@require_POST

def BotMessageView(request):
  """
  Respond to an event from Microsoft Teams.
  """
  if request.content_type != "application/json":
    return HttpResponse(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

  payload = json.loads(request.body)

  # React to the activity
  try:
    activity = Activity.deserialize(payload)
  except DeserializationError:
    return HttpResponse(status=HTTPStatus.BAD_REQUEST)

  auth_header = request.headers.get("authorization", "")
  try:
    invoke_response = call_bot(activity, auth_header)
    # Note: more more except blocks may be needed, per:
    # https://github.com/microsoft/botbuilder-python/blob/main/libraries/botbuilder-core/botbuilder/core/integration/aiohttp_channel_service_exception_middleware.py#L19
  except TypeError:
    response = HttpResponse(status=HTTPStatus.BAD_REQUEST)
  else:
    if invoke_response:
      response = JsonResponse(
        data=invoke_response.body, status=invoke_response.status
      )
    else:
      response = JsonResponse({})

  return response