from asgiref.sync import async_to_sync
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext,
)
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import Activity, ActivityTypes, InvokeResponse


class BotHandler(TeamsActivityHandler):
  """
  Determines what to do for incoming events with per-category methods.

  https://learn.microsoft.com/en-us/microsoftteams/platform/bots/bot-basics?tabs=python
  """

  async def on_message_activity(self, turn_context: TurnContext) -> None:
    """
    Handle “message activity” events, which correspond to the bot being
    directly messaged.
    """
    if not turn_context.activity.conversation.is_group:
      # Respond to direct messages only.
      return await turn_context.send_activity(
        Activity(
          type=ActivityTypes.message,
          text_format="markdown",
          text="Beep boop 🤖",
        )
      )


bot = BotHandler()

bot_adapter = BotFrameworkAdapter(
  BotFrameworkAdapterSettings(
    # Replace these with settings from environment variables in a real app.
    # None values allow requests from the Bot Framework Emulator.
    app_id=None,
    app_password=None,
  )
)


@async_to_sync
async def call_bot(activity: Activity, auth_header: str) -> InvokeResponse | None:
  """Call the bot to respond to an incoming activity."""
  return await bot_adapter.process_activity(
    activity,
    auth_header,
    bot.on_turn,
  )
