import json
import time

import requests
import websocket

import binance_utils
import utils
from binance_utils import hr24_init

symbol_all_usdt = []
def init():
    hr24_init()
    # global current_interval
    url = utils.binance_fapi + '/fapi/v1/exchangeInfo'
    exchangeInfos = requests.get(url).json()
    for exchangeInfo in exchangeInfos['symbols']:
        symbol =  exchangeInfo['symbol']
        if 'USDT' in symbol and '_' not in symbol:
            symbol_all_usdt.append(symbol)
    change_init()
    starting_price_init()
    # current_interval = utils.current_interval()


subscribe = {
        "method": "SUBSCRIBE"
        ,"params":[]
        , "id": 1
    }

# {
#   "e": "aggTrade",  // 事件类型
#   "E": 123456789,   // 事件时间
#   "s": "BNBUSDT",    // 交易对
#   "a": 5933014,		// 归集成交 ID
#   "p": "0.001",     // 成交价格
#   "q": "100",       // 成交量
#   "f": 100,         // 被归集的首个交易ID
#   "l": 105,         // 被归集的末次交易ID
#   "T": 123456785,   // 成交时间
#   "m": true         // 买方是否是做市方。如true，则此次成交是一个主动卖出单，否则是一个主动买入单。
# }

change = {'next': utils.get_current_timestamp_ms()}
starting_price = {}

result_data = {}


def change_init():
    for interval in utils.intervals:
        change[interval] = {}


def starting_price_init():
    for interval in utils.intervals.keys():
        starting_price[interval] = {}

current_interval = '5m'

def on_message(ws, message):
    global current_interval
    message = json.loads(message)
    utils.convert_to_float(message)
    E = message['E']
    symbol = message['s']
    price = message['p']
    if price != 0:
        starting_price_map = starting_price[current_interval]

        if symbol not in starting_price_map:
            starting_price_map[symbol] = klines(symbol, current_interval)
        else:
            starting_price_symbol = starting_price_map[symbol]
            if E - utils.intervals[current_interval] >= starting_price_symbol[0]:
                # 如果大于的话，就是新的一根K线，把这个开盘价设置为新的开盘价
                starting_price_map[symbol] = klines(symbol, current_interval)
        change[current_interval][symbol] = {'change':round((price - starting_price_map[symbol][1]) / starting_price_map[symbol][1] * 100, 2),'price':price,'current_interval':current_interval}

        if E > change['next']:
            change['next'] = E + 1000 * 1
            current_interval_change = change[current_interval]
            # current_interval_change = dict(sorted(current_interval_change.items(), key=lambda x: x[1], reverse=True))
            # keys = current_interval_change.keys()
            # print('开始时间:',utils.convert_timestamp_to_date(starting_price_map[symbol][0]))

            # for key in keys:
            #     print(key,current_interval,'涨幅:',current_interval_change[key])
            result_data['time'] =  utils.convert_timestamp_to_date(starting_price_map[symbol][0])
            result_data['data'] =  []
            keys = current_interval_change.keys()
            # 平均涨幅
            avg_change = round(sum([current_interval_change[key]['change'] for key in keys]) / len(keys),2)
            for key in keys:
                result_data['data'].append({'symbol':key,'change':current_interval_change[key]['change'],'price':current_interval_change[key]['price'],'current_interval':current_interval_change[key]['current_interval']
                                            ,'url':f'https://www.binance.com/zh-CN/futures/{key}?_from=markets'
                                            })
            result_data['avg_change'] = avg_change
            # current_interval = utils.current_interval()
            # print(end='\n\n\n')

# def on_message(ws, message):
#     global current_interval
#     message = json.loads(message)
#     utils.convert_to_float(message)
#     E = message['E']
#     symbol = message['s']
#     price = message['p']
#     if price != 0:
#         pass

def on_error(ws, error):
    print(error)
def on_close(ws,close_status_code, close_msg):
    print("### closed ###")
    print(close_status_code, close_msg)
    retry()

def on_open(ws):
    for symbol in symbol_all_usdt:
    # symbol = 'BTCUSDT'
        if symbol in binance_utils.hr24_map:
            if binance_utils.hr24_map[symbol]['quoteVolume']>2000:
                subscribe['params'].append(f'{symbol.lower()}@aggTrade')
    # front = subscribe['params'][:199]
    # after = subscribe['params'][-199:]
    # subscribe['params'] = subscribe['params'][:10]

    # subscribe['params'].append(f'{symbol.lower()}@aggTrade')
    ws.send(json.dumps(subscribe))
    print("### open ###")



def klines(symbol,interval,limit=1):
    response_json =  requests.get(utils.binance_fapi + '/fapi/v1/klines',
                 params={'symbol': symbol, 'interval': interval, 'limit': limit}).json()
    if limit == 1:
        # return utils.arr_to_float(requests.get(utils.binance_fapi + '/fapi/v1/klines', params={'symbol':symbol, 'interval':interval, 'limit':limit}).json()[0])
        return utils.arr_to_float(response_json[0])
    else:
        # for data in response_json:
        utils.arr_to_float_s(response_json)
        return response_json
def retry():
    print('重试')
    binance_utils.hr24_init()
    time.sleep(1)
    ws = websocket.WebSocketApp("wss://fstream.binance.com/ws", on_close=on_close, on_open=on_open,
                                on_message=on_message,
                                on_error=on_error)
    ws.run_forever()

def run():
    init()

    ws = websocket.WebSocketApp("wss://fstream.binance.com/ws", on_close=on_close, on_open=on_open,
                                on_message=on_message,
                                on_error=on_error)
    ws.run_forever()
# klines_map_8h = {}
if __name__ == '__main__':
    # run()
    init()
    # data_s = klines('BTCUSDT','1h',10)
    # symbol_all_usdt.for

    symbol_filter = []
    for symbol in symbol_all_usdt:
        if symbol in binance_utils.hr24_map:
            if binance_utils.hr24_map[symbol]['quoteVolume'] > 20000:
                symbol_filter.append(symbol)
    klines_map = {}
    limit = 4*24
    klines_map_h = {}
    for symbol in symbol_filter:
        klines_map[symbol] = klines(symbol,'15m',limit=limit)
        # klines_map_h[symbol] = klines(symbol,'8h',limit=limit)
    print('limit:',limit)
    avg_map = {}
    for key in klines_map.keys():
        klines_data = klines_map.get(key)
        for data in klines_data:
            if data[0] not in avg_map:
                avg_map[data[0]] = []
            avg_map[data[0]].append({'change':utils.price_change(data[1], data[4]),'symbol':key,'low':data[3],'high':data[2],'close':data[4],'open':data[1]})
    # avg_map_h = {}
    # for key in klines_map_h.keys():
    #     klines_data = klines_map_h.get(key)
    #     for data in klines_data:
    #         if data[0] not in avg_map_h:
    #             avg_map_h[data[0]] = []
    #         avg_map_h[data[0]].append({'change':utils.price_change(data[1], data[4]),'symbol':key,'low':data[3],'high':data[2],'close':data[4],'open':data[1]})
    last = None
    total_income = 0
    # for key in avg_map_h.keys():
    #     sum_number_h = sum([item['change'] for item in avg_map_h[key]])
    #     sum_change_h = round(sum_number_h / len(avg_map_h[key]), 2)

    for key in avg_map.keys():
        if last:
            item = [item for item in avg_map[key] if item['symbol'] == last['symbol']][0]
            k = 0
            if last['side'] in 'BUY' and item['open']+k > item['low']:
                flag = False #(utils.price_change(item['open'],item['low']) < -1)
                print('收益:','-1' if flag else item['change'])
                total_income += (-1 if flag else item['change'])
                total_income-=0.1
                # pass
            # else:
            #     if item['open']+k < item['high']:
            #         flag = False #(utils.price_change(item['open'], item['high']) > 1)
            #         print('收益:','-1' if flag else -item['change'])
            #         total_income -= (1 if flag else item['change'])
            #         total_income -= 0.1

        sum_number = sum([item['change'] for item in avg_map[key]])
        sum_change = round(sum_number / len(avg_map[key]), 2)

        length = len(avg_map[key])
        # print(key,avg_map[key])
        print(utils.convert_timestamp_to_date(key),sum_change,end='')
        # print(key, sum_change,end='')
        symbol = sorted(avg_map[key], key=lambda x: x['change'], reverse=(False if sum_change > 0 else True))[0]['symbol']
        last = {'symbol': symbol, 'side': 'BUY' if sum_change > 0 else 'SELL'}


        print('选择:', last)
        # if sum_change > 0:
        #     print('选择:',sorted(avg_map[key], key=lambda x: x['change'], reverse=False)[0]['symbol'])
        # else:
        #     print('选择:', sorted(avg_map[key], key=lambda x: x['change'], reverse=True)[0]['symbol'])
    # exit()

    print('盈亏',total_income)
    # print(data_s)

