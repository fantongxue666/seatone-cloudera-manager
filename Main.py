import datetime
import os

from MysqlDB import DataBaseHandle
from StruceHadoop import hadoopStruction
from flask import Flask, render_template, request, json, jsonify, make_response, send_from_directory

app = Flask(__name__)
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

'''
构建hadoop单机版
'''
@app.route('/hadoop_alone', methods=["GET", "POST"])
def hadoop_alone():
    try:
        ip = request.form.get('ip')
        userName = request.form.get('userName')
        passWord = request.form.get('passWord')
        hadoopStruction().hadoop_alone(ip=ip, username=userName, passwd=passWord)
        return json.dumps({"code":200,"msg":"success"})
    except Exception as e:
        print(e)
        return json.dumps({"code":500,"msg":"error"})

'''
构建hadoop集群
'''
@app.route('/hadoop_cluster', methods=["GET", "POST"])
def hadoop_cluster():
    hadoopStruction().hadoop_cluster()

'''
查看日志列表
'''
@app.route('/logList', methods=["GET"])
def getLogList():
    db = DataBaseHandle()  # 数据库操作类 全局
    data = db.selectDB("select * from mg_log where log_type='构建Hadoop单机版' order by log_time desc")
    list=[]
    for obj in data:
        list.append({
            'target_ip':obj[1],
            'log_url':obj[2],
            'log_type':obj[3],
            'log_status':obj[4],
            'log_time':obj[5]
        })
    return json.dumps(list,cls=MyEncoder)

'''
查看某个txt日志，在线预览
'''
@app.route("/download", methods=['GET'])
def download_file():
    fileName = request.args.get("fileName")
    BASE_DIR = os.path.dirname(__file__)
    file_path = BASE_DIR + "/shell/logs/"
    if not os.path.exists(file_path + fileName):
        return "文件不存在，八成被删除了！"
    response = make_response(send_from_directory(file_path,fileName,as_attachment=False))
    response.headers['Content-Type'] = 'text/html'
    response.headers["Content-Disposition"] = "inline; filename=" + fileName
    return response

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
