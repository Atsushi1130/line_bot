from flask import Flask, request, abort
import os
import scrape as sc

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    print("Hello World")

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)    # get request body as text

    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # result1,result2 = sc.get_news
    result = sc.get_news()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result),
    )

    # for i in range(len(result1)):
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=result1[i] + "\n" + "https://www.nishinippon.co.jp/" + result2[i]),
    #     )
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=result1[i+1] + "\n" + "https://www.nishinippon.co.jp/" + result2[i+1]),
    #     )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0", port=port)
