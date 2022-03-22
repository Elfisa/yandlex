from flask import Flask, url_for

app = Flask(__name__)


@app.route('/choice')
def bootstrap():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet" 
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                    crossorigin="anonymous">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                    <title>Привет, Марс!</title>
                  </head>
                  <body>
                    <h1>Жди нас, Марс!</h1>
                    <img src="{url_for('static', filename='img/img.png')}">
                    <div class="alert alert-dark" role="alert">
                      <h5>Человечество вырастает из детства.</h5>
                    </div>
                    <div class="alert alert-success" role="alert">
                      <h5>Человечеству мала одна планета.</h5>
                    </div>
                    <div class="alert alert-secondary" role="alert">
                      <h5>Мы сделаем обитаемыми безжизненные пока планеты.</h5>
                    </div>
                    <div class="alert alert-warning" role="alert">
                      <h5>И начнём с Марса!</h5>
                    </div>
                    <div class="alert alert-danger" role="alert">
                      <h5>Присоединяйся!</h5>
                    </div>
                  </body>
                </html>'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
