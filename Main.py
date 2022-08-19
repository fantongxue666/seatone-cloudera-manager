from StruceHadoop import hadoopStruction
from flask import Flask, render_template

app = Flask(__name__)
'''
构建hadoop单机版
'''
def hadoop_alone():
    hadoopStruction().hadoop_alone(ip="192.168.195.128",username="root",passwd="aini12345")


'''
构建hadoop集群
'''
def hadoop_cluster():
    hadoopStruction().hadoop_cluster()

'''
首页
'''
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/struction')
def struction():
    return render_template('struction.html')

if __name__ == '__main__':
    app.run(port=8080)
