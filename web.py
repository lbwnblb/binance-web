import threading
from threading import main_thread

from flask import Flask, jsonify, redirect, url_for, request

import utils
import websocket_binance


app = Flask(__name__)
from flask_cors import CORS  # 导入 flask-cors
CORS(app)
@app.route('/')
def home():
    # 跳转到静态页面
    return redirect(url_for('static', filename='index.html'))

@app.route('/get_data')
def get_data():
    return jsonify(websocket_binance.result_data)
@app.route('/get_options')
def options():
    options_data = []
    for key in utils.intervals.keys():
        options_data.append({'label': key, 'value': key})
    return jsonify(options_data)
@app.route('/set_current_interval')
def set_current_interval():
    interval = request.args.get('interval')  # 获取查询参数 'interval'
    websocket_binance.current_interval = interval
    print(interval)
    return jsonify({"message": f"Interval set to {interval}"})

def run():
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)


if __name__ == "__main__":
    main_thread = threading.Thread(target=run,args=())
    websocket_binance_run = threading.Thread(target=websocket_binance.run,args=())
    main_thread.daemon = True
    websocket_binance_run.daemon = True
    main_thread.start()
    websocket_binance_run.start()
    main_thread.join()
    websocket_binance_run.join()
