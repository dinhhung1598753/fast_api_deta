from typing import Text
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import requests
import time
from get_stock_info import  get_info, get_info_json
import asyncio
import json
import threading

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
            var ws = new WebSocket("ws://127.0.0.1:8000/ws/BSR");
            ws.onmessage = function(evt) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            var ws = new WebSocket("ws://127.0.0.1:8000/ws/MBS");
            ws.onmessage = function(evt) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            
            var ws = new WebSocket("ws://127.0.0.1:8000/ws/VIC");
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
class MessageManager:
    def __init__(self, websocket: WebSocket, stock_name: str):
        self.websocket = websocket
        self.stock_name = stock_name
        self.thread = threading.Timer(10, a)
    def send(self):
        
        # socket_send(self.websocket, self.stock_name)
        self.thread = threading.Timer(10, send_m, args=(self.websocket, self.stock_name)).start()
        send_m(self.websocket, self.stock_name)
    def cancel(self):
        self.thread.cancel()

    

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{stock_name}")
async def websocket_endpoint(websocket: WebSocket, stock_name: str):
    await websocket.accept()
    message =  MessageManager(websocket, stock_name)
    try:
        message.send()
        # socket_send(websocket, stock_name)
        while True:
            # setInterval(10, a)
            await websocket.receive()
    except WebSocketDisconnect:
        message.cancel()
    # i = 0
    # setInterval(10, send_m(websocket, stock_name))
    # asyncio.get_event_loop().run_until_complete(alive())
    # threading.Timer(10, a).start()
    
def a():
    print(time.localtime())

def send_m(websocket: WebSocket, stock_name: str):
    i =0
    while True:
        i+=1
        
        asyncio.run(websocket.send_json(get_info_json(stock_name)))
        time.sleep(10)
    # for i in range(10):
    #     get_info(stock_name)
    #     await websocket.send_text(f"{stock_name} --{time.localtime()}")
    #     time.sleep(10)


# def socket_send(websocket: WebSocket, stock_name: str):
#     # loop = asyncio.get_event_loop()
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(send_m(websocket, stock_name))
#     loop.close()


TOKEN = '2120867713:AAF7y9-CqPx0-ZI6MVSARkIv342N0TULTSA'  # Telegram Bot API Key

# message = ""
# gl_chat_id = ""
# gl_mess = ""

def send_mess(chat_id,mess:str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    if "checking" in mess:
        stock_name = mess.replace("checking", "")
        mess = get_info(stock_name)
    elif "limit" in mess:
        txt = mess.split(" limit ")
        mess = f"Set warning {txt[0]} at price={txt[1]}"
        print(mess)
        payload = json.dumps({
        "chat_id": chat_id,
        "text": mess
        })
        # print(payload)
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        threading.Timer(5, check_limit_price, args=(txt[1], txt[0], chat_id)).start()
        # await check_limit_price(txt[1], txt[0], chat_id)
        return
        
    else:
        mess = "Checking Stock price: STOCK_NAME checking \n Warning price: STOCK_NAME limit your_price"
    payload = json.dumps({
    "chat_id": chat_id,
    "text": mess
    })
    # print(payload)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)


@app.post("/webhook")
async def recWebHook(req: Request):
    body = await req.json()
    try:
        id = body['message']['chat']['id']
        sender_text = body['message']['text']
        send_mess(id,mess=sender_text)

        # await send_mess(123, "GVR limit 40.90")
    except: 
        pass
    


def check_limit_price(price:str, name:str, chat_id):
    url = f"https://bgapidatafeed.vps.com.vn/getliststockdata/{name}"
    # for i in name:
    #     url.join(i+",")
    i=0
    while True:
        try:
            i+=1
            r = requests.get(url)
            x = json.loads(r.text)
            last_price = float(x[0]['lastPrice'])

            now_price = 0.0
            if i == 1:
                now_price = last_price
            if now_price < float(price):
                if float(price) <= last_price:
                    result = []
                    for i in x:
                        result.append(f"Mã cổ phiếu: {i['sym']} \n Tổng khối lượng giao dịch: {i['lot']} \n Giá hiện tại: {i['lastPrice']}\n Giá tham chiếu: {i['r']}\n Giá Trần: {i['c']}\n Giá sàn: {i['f']}\n Giá Cao Nhất: {i['highPrice']}\n Giá Thấp Nhất: {i['lowPrice']}\n Bên mua:\n Giá 1: {i['g1']}\n Giá 2: {i['g2']}\n Giá 3: {i['g3']}\n Bên bán:\n Giá 1: {i['g4']}\n Giá 2: {i['g5']}\n Giá 3: {i['g6']}\n")
                    
                    mes_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

                    payload = json.dumps({
                    "chat_id": chat_id,
                    "text": f"Warning {name} price = {last_price}"
                    })
                    # print(payload)
                    headers = {
                    'Content-Type': 'application/json'
                    }

                    response = requests.request("POST", mes_url, headers=headers, data=payload)

                    
                    payload = json.dumps({
                    "chat_id": chat_id,
                    "text": result[0]
                    })
                    # print(payload)
                    headers = {
                    'Content-Type': 'application/json'
                    }

                    response = requests.request("POST", mes_url, headers=headers, data=payload)
                    break
            else:
                if float(price) >= last_price:
                    result = []
                    for i in x:
                        result.append(f"Mã cổ phiếu: {i['sym']} \n Tổng khối lượng giao dịch: {i['lot']} \n Giá hiện tại: {i['lastPrice']}\n Giá tham chiếu: {i['r']}\n Giá Trần: {i['c']}\n Giá sàn: {i['f']}\n Giá Cao Nhất: {i['highPrice']}\n Giá Thấp Nhất: {i['lowPrice']}\n Bên mua:\n Giá 1: {i['g1']}\n Giá 2: {i['g2']}\n Giá 3: {i['g3']}\n Bên bán:\n Giá 1: {i['g4']}\n Giá 2: {i['g5']}\n Giá 3: {i['g6']}\n")
                    
                    mes_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

                    payload = json.dumps({
                    "chat_id": chat_id,
                    "text": f"Warning {name} price = {last_price}"
                    })
                    # print(payload)
                    headers = {
                    'Content-Type': 'application/json'
                    }

                    response = requests.request("POST", mes_url, headers=headers, data=payload)
                    
                    payload = json.dumps({
                    "chat_id": chat_id,
                    "text": result[0]
                    })
                    # print(payload)
                    headers = {
                    'Content-Type': 'application/json'
                    }

                    response = requests.request("POST", mes_url, headers=headers, data=payload)
                    break
            
            
        except:
            return f"error name warrning price :{name}"