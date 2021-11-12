import requests
import json
import asyncio


TOKEN = '2120867713:AAF7y9-CqPx0-ZI6MVSARkIv342N0TULTSA' 

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



def get_info_json(name):
    # name="VHM"
    # print(name)
    url = f"https://bgapidatafeed.vps.com.vn/getliststockdata/{name}"
    # for i in name:
    #     url.join(i+",")
    try:
        r = requests.get(url)
        # x = json.loads(r.text)
        return f"{json.loads(r.text)[0]}"
    except:
        return f"error name :{name}"

