from flask import Flask, request
from .bot import Bot

app = Flask(__name__)

@app.route('/webhook/github', methods=['POST'])
def github():
    data = request.get_json()
    bot = Bot()
    bot.send({
    "sessionKey": bot.session,
        "target":946063184,
        "messageChain":[
            { "type":"Plain", "text":f"GitHub Push at {data.get('repository').get('name')}\n" },
            { "type":"Plain", "text":f"ref: {data.get('ref')}\n" },
            { "type":"Plain", "text":f"commit: {data.get('head_commit').get('id')[-8:]}\n" },
            { "type":"Plain", "text":f"message: {data.get('head_commit').get('message')}\n" },
            { "type":"Plain", "text":f"author: {data.get('head_commit').get('author').get('name')}\n" },
        ]
    }, 'sendGroupMessage')