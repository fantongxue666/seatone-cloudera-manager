import datetime

from StruceHadoop import hadoopStruction
from flask import Flask, render_template, request, json, jsonify
app = Flask(__name__)

'''
构建hadoop单机版
'''

import json
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            print("MyEncoder-datetime.datetime")
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        if isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, float):
            return float(obj)
        #elif isinstance(obj, array):
        #    return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

@app.route('/hadoop_alone', methods=["GET", "POST"])
def hadoop_alone():
    try:
        ip = request.form.get('ip')
        userName = request.form.get('userName')
        passWord = request.form.get('passWord')
        hadoopStruction().hadoop_alone(ip=ip, username=userName, passwd=passWord)
        return 200
    except Exception as e:
        print(e)
        return 500

'''
构建hadoop集群
'''


@app.route('/hadoop_cluster', methods=["GET", "POST"])
def hadoop_cluster():
    hadoopStruction().hadoop_cluster()


'''
首页页面
'''


@app.route('/index')
def index():
    return render_template('index.html')


'''
构建hadoop单机版页面
'''


@app.route('/struction')
def struction():
    return render_template('struction.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
