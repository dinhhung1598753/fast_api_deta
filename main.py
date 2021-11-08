from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
import requests
import time
from get_stock_info import  get_info
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
        await websocket.send_text(f"{stock_name} --{i*10}")
        # await asyncio.sleep(10)

TOKEN = '2120867713:AAF7y9-CqPx0-ZI6MVSARkIv342N0TULTSA'  # Telegram Bot API Key

message = ""
async def send_mess(chat_id,mess:str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": mess
        })
        # print(payload)
    headers = {
        'Content-Type': 'application/json'
        }
    response = requests.request("POST", url, headers=headers, data=payload)
    if mess == "clear":
        message = "clear"
    else:
        message = ""
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
        await check_limit_price(txt[1], txt[0], chat_id)
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
        await send_mess(id,mess=sender_text)

        # await send_mess(123, "GVR limit 40.90")
    except: 
        pass
    


async def check_limit_price(price:str, name:str, chat_id):
    url = f"https://bgapidatafeed.vps.com.vn/getliststockdata/{name}"
    # for i in name:
    #     url.join(i+",")
    i=0
    while True:
        if message == "clear":
            return

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
            
            await asyncio.sleep(10)
            
        except:
            return f"error name warrning price :{name}"