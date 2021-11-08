from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
import requests
import time
from get_stock_info import get_info
import asyncio
import json

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("wss://fastapisocket.herokuapp.com/ws/GVR");
            ws.onmessage = function(evt) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }


        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{stock_name}")
async def websocket_endpoint(websocket: WebSocket, stock_name: str):
    await websocket.accept()
    # i = 0

    # asyncio.get_event_loop().run_until_complete(alive())
    await send_m(websocket, stock_name)

    # asyncio.get_event_loop().run_until_complete(asyncio.wait([
    #     send_m(websocket, stock_name)
    # ]))

#
# async def send_mess(stock_name: str):
#     await websocket.send_text(get_info(stock_name))
async def send_m(websocket: WebSocket, stock_name: str):
    i=0
    while True:
        i+=1
        # data = await websocket.receive_text()
        # await websocket.send_text(get_info(stock_name))
        get_info(stock_name)
        await websocket.send_text(f"{stock_name} --{i}")
        await asyncio.sleep(10)

TOKEN = '2120867713:AAF7y9-CqPx0-ZI6MVSARkIv342N0TULTSA'  # Telegram Bot API Key

def send_mess(chat_id,mess:str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    if "checking" in mess:
        stock_name = mess.replace("checking", "")
        mess = get_info(stock_name)
    elif "limit" in mess:
        mess = "i'm checking"
    else:
        mess = "Checking Stock price: STOCK_NAME checking \n Warning price: STOCK_NAME limit your_price"
    payload = json.dumps({
    "chat_id": chat_id,
    "text": mess
    })
    print(payload)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)


@app.post("/webhook")
async def recWebHook(req: Request):
    body = await req.json()
    id = body['message']['chat']['id']
    sender_text = body['message']['text']
    send_mess(id,mess=sender_text)