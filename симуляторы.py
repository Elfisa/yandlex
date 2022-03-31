from flask import Flask, render_template

app = Flask(__name__)


@app.route('/page2')
def index2():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
