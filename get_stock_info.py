import requests
import json

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
            result.append(f"mã cổ phiếu:{i['sym']}\
            Tổng khối lượng giao dịch: {i['lot']}\
            Giá tham chiếu:{i['r']}\
            Giá Trần:{i['c']}\
            Giá sàn:{i['f']}\
            Giá Cao Nhất:{i['highPrice']}\
            Giá Thấp Nhất:{i['lowPrice']}\
            Bên mua:\
            Giá 1:{i['g1']}\
            Giá 2:{i['g2']}\
            Giá 3:{i['g3']}\
            Bên bán:\
            Giá 1:{i['g4']}\
            Giá 2:{i['g5']}\
            Giá 3:{i['g6']}\
                ")
        return result[0]
    except:
        return f"error name :{name}"
