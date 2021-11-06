from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import time
from get_stock_info import get_info

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
            var ws = new WebSocket("wss://hif4vg.deta.dev/ws/GVR");
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
    i = 0
    while True:
        # data = await websocket.receive_text()
        i=0
        while True:
            i += 1
            await websocket.send_text(get_info(stock_name))