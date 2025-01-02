import threading

from flask import Flask, jsonify, redirect, url_for

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
if __name__ == "__main__":
    threading.Thread(target=websocket_binance.run,args=()).start()
    app.run(debug=True, host='0.0.0.0', port=5000)