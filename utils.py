import platform
import os
import time

system = platform.system()
import datetime

intervals = {
    '1m': 60000,
    '3m': 180000,
    '5m': 300000,
    '15m': 900000,
    '30m': 1800000,
    '1h': 3600000,
    '2h': 7200000,
    '4h': 14400000,
    '6h': 21600000,
    '8h': 28800000,
    '12h': 43200000,
    '1d': 86400000,
    '3d': 259200000,
    '1w': 604800000,
    '1M': 2592000000
}


def arr_to_float(arr):
    result = []
    for x in arr:
        if isinstance(x, str):  # Only apply replace() to strings
            if x.replace('.', '', 1).isdigit():
                result.append(float(x))
            else:
                result.append(x)
        elif isinstance(x, (int, float)):  # Directly append numbers
            result.append(float(x))
        else:
            result.append(x)  # For other types, just append as is
    return result
def convert_to_float(d):
    for key, value in d.items():
        if isinstance(value, str) and value.replace('.', '', 1).replace('-', '', 1).isdigit():
            d[key] = float(value)
        elif isinstance(value, dict):
            convert_to_float(value)

# def current_interval():
#     return open('current_interval.txt').read().replace('\n','')


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

