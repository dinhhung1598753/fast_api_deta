import requests
import json
import asyncio

def get_info(name):
    # name="VHM"
    # print(name)
    url = f"https://bgapidatafeed.vps.com.vn/getliststockdata/{name}"
    # for i in name:
    #     url.join(i+",")
    try:
        r = requests.get(url)
        x = json.loads(r.text)
        result = []
        for i in x:
            result.append(f"Mã cổ phiếu: {i['sym']} \n Tổng khối lượng giao dịch: {i['lot']}  \n  Giá hiện tại: {i['lastPrice']}\n Giá tham chiếu: {i['r']}\n Giá Trần: {i['c']}\n Giá sàn: {i['f']}\n Giá Cao Nhất: {i['highPrice']}\n Giá Thấp Nhất: {i['lowPrice']}\n Bên mua:\n Giá 1: {i['g1']}\n Giá 2: {i['g2']}\n Giá 3: {i['g3']}\n Bên bán:\n Giá 1: {i['g4']}\n Giá 2: {i['g5']}\n Giá 3: {i['g6']}\n")
        return result[0]
    except:
        return f"error name :{name}"

async def check_limit_price(price:str, name:str):
    url = f"https://bgapidatafeed.vps.com.vn/getliststockdata/{name}"
    # for i in name:
    #     url.join(i+",")
    while True:
        try:
            r = requests.get(url)
            x = json.loads(r.text)
            if price == x[0]['lastPrice']:
                result = []
                for i in x:
                    result.append(f"Mã cổ phiếu: {i['sym']} \n Tổng khối lượng giao dịch: {i['lot']} \n Giá hiện tại: {i['lastPrice']}\n Giá tham chiếu: {i['r']}\n Giá Trần: {i['c']}\n Giá sàn: {i['f']}\n Giá Cao Nhất: {i['highPrice']}\n Giá Thấp Nhất: {i['lowPrice']}\n Bên mua:\n Giá 1: {i['g1']}\n Giá 2: {i['g2']}\n Giá 3: {i['g3']}\n Bên bán:\n Giá 1: {i['g4']}\n Giá 2: {i['g5']}\n Giá 3: {i['g6']}\n")
                return result[0]
            await asyncio.sleep(10)
            
        except:
            return f"error name warrning price :{name}"
