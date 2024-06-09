from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from app.utils import generate_description_logic, user_data
from PIL import Image
import io


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index() -> str:
    """Отображает главную страницу."""
    return render_template('category_select.html')


@main_bp.route('/select_category', methods=['POST'])
def select_category() -> str:
    """Обрабатывает выбор категории."""
    category = request.form['category']
    subcategory = request.form.get('subcategory', '')
    user_data['Вид одежды'], user_data['Предмет одежды'] = category, subcategory

    if category == "Аксессуары":
        return redirect(url_for('main.ad_details', category=category, subcategory=''))
    return render_template('ad_details.html', category=category, subcategory=subcategory)


@main_bp.route('/ad_details', methods=['GET'])
def ad_details() -> str:
    """Отображает детали объявления."""
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    return render_template('ad_details.html', category=category, subcategory=subcategory)


@main_bp.route('/save_data', methods=['POST'])
def save_data() -> dict:
    """Сохраняет данные."""
    field_name = request.form['field_name']
    field_value = request.form['field_value']
    user_data[field_name] = field_value
    return jsonify({'status': 'success'})


@main_bp.route('/create_ad', methods=['POST'])
def create_ad() -> str:
    """Создает объявление."""
    title = request.form['title']
    ad_type = request.form['ad_type']
    condition = request.form['condition']
    color = request.form['color']
    brand = request.form['brand']
    description = request.form['description']
    category = request.form['category']
    subcategory = request.form['subcategory']
    price = request.form['price']
    image = request.files['image']
    location = request.form['location']

    user_data['Заголовок'], user_data['Вид обьявления'], user_data['Состояние'], user_data['Место сделки'], user_data['Цвет'], user_data['Бренд'] = title, ad_type, condition, location, color, brand

    if image and image.filename != '':
        filename = secure_filename(image.filename)
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        flash('Объявление успешно создано!', 'success')
    else:
        flash('Ошибка при загрузке изображения', 'error')

    return redirect(url_for('main.index'))


@main_bp.route('/generate_description', methods=['POST'])
def generate_description() -> dict:
    """Генерирует описание."""
    input_text = f"Заголовок: {user_data['Заголовок']}, Вид одежды: {user_data['Вид одежды']}, Вид обьявления: {user_data['Вид обьявления']}, Место сделки: {user_data['Место сделки']}, Состояние: {user_data['Состояние']}, Цвет: {user_data['Цвет']}, Бренд одежды: {user_data['Бренд']}"

    if user_data['Вид одежды'] != 'Аксессуары':
        input_text += f", Предмет одежды: {user_data['Предмет одежды']}"

    input_text += ', Описание:'

    file = request.files['image']
    image = io.BytesIO(file.read())
    pil_image = Image.open(image).convert('RGB')

    description = generate_description_logic(input_text, pil_image)

    return jsonify({'description': description})
