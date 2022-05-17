from email import message
import sys,os,logging,psycopg2,json
from datetime import datetime, date, timedelta,timezone
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction
)
from linebot.exceptions import LineBotApiError

LINE_CHANNEL_ACCESS_TOKEN   = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET         = os.environ['LINE_CHANNEL_SECRET']
LINE_BOT_API = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
LINE_HANDLER = WebhookHandler(LINE_CHANNEL_SECRET)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def handler(event, context):
    logger.info(event)
    body_str = event["body"]
    body_dict = json.loads(body_str)
    logger.info(type(body_dict))
    line_user_id = body_dict["events"][0]["source"]["userId"]
    logger.info(f"line_user_id:{line_user_id}")
    signature = event["headers"]["x-line-signature"]
    body = event["body"]
    
    """textメッセージを受信"""
    @LINE_HANDLER.add(MessageEvent, message=TextMessage)
    def on_message(line_event):
        LINE_BOT_API.reply_message(line_event.reply_token, TextSendMessage("test message"))
    
    """"Followイベントを受信"""
    @LINE_HANDLER.add(FollowEvent)
    def account_linkage(event):
        user_id = event.source.user_id
        logger.debug(f"user_id:{user_id}")
        link_token_response = LINE_BOT_API.issue_link_token(user_id)
        buttons_template_message = TemplateSendMessage(
            alt_text='Account Link',
            template=ButtonsTemplate(
                title='Menu',
                text='Account Link',
                actions=[
                    URIAction(
                        label='uri',
                        uri="https://shiftmanagementapp-heroku.herokuapp.com/account_linkage?linkToken="+str(link_token_response.link_token)
                    )
                ]
            )
        )
        LINE_BOT_API.push_message(user_id, buttons_template_message)

        
    
    LINE_HANDLER.handle(body, signature)
    return 0
    