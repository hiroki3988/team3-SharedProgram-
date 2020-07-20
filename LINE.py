from __future__ import unicode_literals

import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# 環境変数からchannel_secretとchannel_access_tokenを所得する
channel_secret = "YOUR_CHANNEL_SECRET"
channel_access_token = "YOUR_CHANNEL_ACCESS"
if channel_secret is None: #LINE_CHANNEL_SECRETが指定されていないとき
    print('環境変数としてLINE_CHANNEL_SECRETを指定してください。')
    sys.exit(1)
if channel_access_token is None: #LINE_CHANNEL_SECRETが指定されていないとき
    print('環境変数としてLINE_CHANNEL_ACCESS_TOKENを指定してください。')
    sys.exit(1)

# 各クライアントライブラリのインスタンス作成
line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # イベントがMessageEvent(メッセージが送られた場合のイベント)であり,かつメッセージがTextMessage(文字)であるとき,オウム返しをする
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
　　　　# ↓テキストのオウム返し部分
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
