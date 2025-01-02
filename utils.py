import platform
import os
import time

system = platform.system()
import datetime

intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

def convert_to_float(d):
    for key, value in d.items():
        if isinstance(value, str) and value.replace('.', '', 1).replace('-', '', 1).isdigit():
            d[key] = float(value)
        elif isinstance(value, dict):
            convert_to_float(value)

def current_interval():
    return open('current_interval.txt').read()


def get_current_timestamp_ms():
    return int(time.time() * 1000)


def convert_timestamp_to_date(timestamp_ms):
    # Convert to seconds
    timestamp_s = timestamp_ms / 1000

    # Convert to datetime
    date_time = datetime.datetime.fromtimestamp(timestamp_s)

    # Format the datetime
    formatted_date = date_time.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_date
if system == "Windows":
    # # 设置代理地址和端口
    proxy = "http://127.0.0.1:10808"  # 替换为实际的代理地址和端口
    os.environ['HTTP_PROXY'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
if __name__ == '__main__':
    v = {'e': 'continuous_kline', 'E': '2025-01-02 13:00:16', 'ps': 'AMBUSDT', 'ct': 'PERPETUAL',
     'k': {'t': '2025-01-02 13:00:00', 'T': '2025-01-02 13:04:59', 'i': '5m', 'f': 6306341673087, 'L': 6306344126600,
           'o': '0.0076420', 'c': '0.0076400', 'h': '0.0076450', 'l': '0.0076380', 'v': '262761', 'n': 47, 'x': False,
           'q': '2007.7661670', 'V': '77258', 'Q': '590.2733980', 'B': '0'}}

    convert_to_float(v)
    print(v)

