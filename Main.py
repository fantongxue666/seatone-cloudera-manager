from flask import Flask,render_template
app=Flask(__name__)

@app.route('/index')
def index():
    return "this is index"


@app.route('/test')
def test():
    return render_template("index.html")

app.run(port=8080)