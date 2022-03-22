from flask import Flask, url_for

app = Flask(__name__)


@app.route('/sample_page')
def return_sample_page():
    return f"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}"/>
                    <title>Шедевры</title>
                  </head>
                  <body>
                    <h1>Шедевры</h1>
                    <div id="carouselExampleSlidesOnly" class="carousel slide" data-bs-ride="carousel">
                      <div class="carousel-inner">
                        <div class="carousel-item">
                          <img src="{url_for('static', filename='img/img_1.png')} class="d-block w-100">
                        </div>
                        <div class="carousel-item">
                          <img src="{url_for('static', filename='img/img_2.png')} class="d-block w-100">
                        </div>
                        <div class="carousel-item">
                          <img src="{url_for('static', filename='img/img_3.png')} class="d-block w-100">
                        </div>
                      </div>
                    </div>
                  </body>
                </html>"""


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
