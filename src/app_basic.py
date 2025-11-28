import os
from flask import Flask, render_template, request, send_from_directory, Response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("task.html")


# Обычная страница загрузки - РАБОТАЕТ
@app.route("/upload.html")
def upload_page():
    return render_template("upload.html")


# Iframe с CSP - ЗАПРЕЩАЕТ загрузку
@app.route("/iframe.html")
def iframe_page():
    response = Response(render_template("upload.html"))
    response.headers['Content-Security-Policy'] = "form-action 'none'"
    return response


# Страница со стихотворением
@app.route("/index.html")
def poem_page():
    return render_template("index.html")


# Загрузка файлов
@app.route("/upload", methods=['POST'])
def upload():
    # Создаем папку для изображений
    images_dir = os.path.join(os.path.dirname(__file__), 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    # Сохраняем файлы
    for file in request.files.getlist("file"):
        if file and file.filename:
            file.save(os.path.join(images_dir, file.filename))

    return render_template("complete.html")


if __name__ == "__main__":
    app.run(port=4555, debug=True)