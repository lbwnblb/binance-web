import json

import requests
import websocket

import utils
binance_fapi = 'https://fapi.binance.com'
symbol_all_usdt = []
def init():
    url = binance_fapi + '/fapi/v1/exchangeInfo'
    exchangeInfos = requests.get(url).json()
    for exchangeInfo in exchangeInfos['symbols']:
        symbol =  exchangeInfo['symbol']
        if 'USDT' in symbol:
            symbol_all_usdt.append(symbol)
    change_init()

subscribe = {
        "method": "SUBSCRIBE"
        ,"params":[]
        , "id": 1
    }
unsubscribe = {
        "method": "UNSUBSCRIBE",
        "params":[],
        "id": 312
    }

# {
#   "e":"continuous_kline",	// 事件类型
#   "E":1607443058651,		// 事件时间
#   "ps":"BTCUSDT",			// 标的交易对
#   "ct":"PERPETUAL",			// 合约类型
#   "k":{
#     "t":1607443020000,		// 这根K线的起始时间
#     "T":1607443079999,		// 这根K线的结束时间
#     "i":"1m",				// K线间隔
#     "f":116467658886,		// 这根K线期间第一笔更新ID
#     "L":116468012423,		// 这根K线期间末一笔更新ID
#     "o":"18787.00",			// 这根K线期间第一笔成交价
#     "c":"18804.04",			// 这根K线期间末一笔成交价
#     "h":"18804.04",			// 这根K线期间最高成交价
#     "l":"18786.54",			// 这根K线期间最低成交价
#     "v":"197.664",			// 这根K线期间成交量
#     "n":543,				// 这根K线期间成交笔数
#     "x":false,				// 这根K线是否完结(是否已经开始下一根K线)
#     "q":"3715253.19494",	// 这根K线期间成交额
#     "V":"184.769",			// 主动买入的成交量
#     "Q":"3472925.84746",	// 主动买入的成交额
#     "B":"0"					// 忽略此参数
#   }
# }

change = {'next': utils.get_current_timestamp_ms()}


def change_init():
    for interval in utils.intervals:
        change[interval] = {}



def on_message(ws, message):
    message = json.loads(message)
    utils.convert_to_float(message)
    k = message['k']
    symbol = message['ps']
    i = k['i']
    change[i][symbol] = round((k['c']-k['o'])/k['o']*100,2)

    if message['E'] > change['next']:
        change['next'] = message['E'] + 1000*3
        current_interval = utils.current_interval()
        if i not in current_interval:
            # 取消订阅
            unsubscribe['params'] = [s[:-2]+i for s in subscribe['params']]
            ws.send(json.dumps(unsubscribe))
            # 订阅
            subscribe['params'] = [s[:-2]+current_interval for s in subscribe['params']]
            ws.send(json.dumps(subscribe))

        for change_key in change.keys():
            if change_key in current_interval:
                interval_map = change[change_key]
                sorted_interval_map = dict(sorted(interval_map.items(), key=lambda x: x[1], reverse=True))
                print(f"开始时间:{utils.convert_timestamp_to_date(k['t'])}")
                for interval_map_key in sorted_interval_map.keys():
                    print(f"{interval_map_key} {change_key} 涨幅:{sorted_interval_map[interval_map_key]}%")
                print(end='\n\n\n')

def on_error(ws, error):
    print(error)
def on_close(ws,close_status_code, close_msg):
    print("### closed ###")
    print(close_status_code, close_msg)

def on_open(ws):


    for symbol in symbol_all_usdt:
        # symbol = 'BTCUSDT'
        subscribe['params'].append(f'{symbol.lower()}_perpetual@continuousKline_5m')

    subscribe['params'] = subscribe['params'][-10:]

    ws.send(json.dumps(subscribe))
    print("### open ###")



if __name__ == '__main__':
    init()

    ws = websocket.WebSocketApp("wss://fstream.binance.com/ws", on_close=on_close, on_open=on_open,
                                on_message=on_message,
                                on_error=on_error)
    ws.run_forever()
