import hashlib
import platform
import os
import time
import datetime
from urllib.parse import quote

# from datetime import datetime

import pytz
import requests

system = platform.system()

binance_fapi = 'https://fapi.binance.com'
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


proxy = "http://127.0.0.1:10808"
if system == "Windows":
    # # 设置代理地址和端口
     # 替换为实际的代理地址和端口
    os.environ['HTTP_PROXY'] = proxy
    os.environ['HTTPS_PROXY'] = proxy

def convert_to_beijing_time(time_str):
    # 解析时间字符串
    dt_utc = datetime.datetime.strptime(time_str, "%a %b %d %H:%M:%S %z %Y")
    # 转换为北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    dt_beijing = dt_utc.astimezone(beijing_tz)
    # 返回格式化后的时间
    return dt_beijing.strftime("%Y-%m-%d %H:%M:%S")
def translate_a(q):
    # 定义接口 URL
    url = f'https://translate.googleapis.com/translate_a/single?client=gtx&dt=t&sl=auto&tl=zh&q={quote(q)}'
    # 发送 GET 请求
    res = requests.get(url)
    # 提取翻译结果
    text = [te[0] for te in res.json()[0]]
    str_txt = ''
    for t in text:
        str_txt += str(t)
    return str_txt


def calculate_md5(input_string):
    # 创建 MD5 对象
    md5_hash = hashlib.md5()

    # 更新 MD5 对象，将字符串编码成字节流
    md5_hash.update(input_string.encode('utf-8'))

    # 获取 MD5 值（返回的是十六进制字符串）
    return md5_hash.hexdigest()
def baidu_translate(q,type_='list'):
    # 设置代理字典
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    # 定义接口 URL
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    params = {
        'q':q,
        'from':'auto',
        'to':'zh',
        'appid':'20250106002246903',
        'salt':get_current_timestamp_ms()

    }
    params['sign'] = calculate_md5(params['appid']+params['q']+str(params['salt'])+'oCJBrRSSVe7ERCKFkVlt')
    if type_ == 'list':
        trans_result = requests.get(url,params=params).json()['trans_result']
        return [trans['dst'] for trans in trans_result]
    elif type_ == 'one':
        trans_result = requests.get(url, params=params).json()['trans_result']
        return trans_result[0]['dst']


if __name__ == '__main__':
    print(baidu_translate('my\nhello\nworld\n'))

