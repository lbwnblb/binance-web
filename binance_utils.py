import requests

import utils

hr24_map = {}
def hr24_init():

    response = requests.get(utils.binance_fapi + "/fapi/v1/ticker/24hr")
    datas = response.json()
    for data in datas:
        utils.convert_to_float(data)
        symbol = data['symbol']
        data['quoteVolume'] = round(data['quoteVolume']/10000, 2)
        hr24_map[symbol] = data

    # return datas

if __name__ == '__main__':
    pass
