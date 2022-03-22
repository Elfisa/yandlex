from flask import Flask, url_for

app = Flask(__name__)


@app.route('/carousel')
def carousel():
    return f"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <link rel="stylesheet" 
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" 
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" 
                    crossorigin="anonymous">
                    <title>Шедевры</title>
                  </head>
                  <body>
                    <h1>Шедевры</h1>
                    <div id="carouselExampleSlidesOnly" class="carousel slide" data-bs-ride="carousel">
                      <div class="carousel-inner">
                        <div class="carousel-item" active>
                          <img src="{url_for('static', filename='img/img_1.png')}">
                        </div>
                        <div class="carousel-item">
                          <img src="{url_for('static', filename='img/img_2.png')}">
                        </div>
                        <div class="carousel-item">
                          <img src="{url_for('static', filename='img/img_3.png')}">
                        </div>
                      </div>
                    </div>
                  </body>
                </html>"""


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
