from flask import Flask, render_template, request, redirect, url_for
from transformations import transform_image
from qr_code import generate_qr_code
from database import save_image_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Отримуємо завантажене зображення
    uploaded_image = request.files['image']

    # Виконуємо трансформацію зображення
    transformed_image = transform_image(uploaded_image)

    # Генеруємо QR-код для зображення
    qr_code = generate_qr_code(transformed_image)

    # Зберігаємо дані про зображення в базі даних
    save_image_data(uploaded_image.filename, qr_code)

    return render_template('result.html', qr_code=qr_code)

if __name__ == '__main__':
    app.run(debug=True)
