from flask import Flask, url_for

app = Flask(__name__)


@app.route('/image_sample')
def image():
    return f'''<img src="{url_for('static', filename='img/img.png')}" alt="здесь должна была быть картинка, но не нашлась">'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
