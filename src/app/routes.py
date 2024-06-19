from flask import (Blueprint, render_template, request, jsonify)
from werkzeug import Response
from app.utils import generate_description_logic, promt_preprocess
from PIL import Image
import io


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def category_select() -> str:
    """
    Отображает главную страницу.
    """

    return render_template('category_select.html')


@main_bp.route('/ad_details')
def ad_details() -> str:
    """
    Отображает страницу с заполнением данных.
    """

    return render_template('ad_details.html')


@main_bp.route('/generate_description', methods=['POST'])
def generate_description() -> Response:
    """Генерирует описание."""
    input_text = promt_preprocess(request.form)
    file = request.files['image']
    image = io.BytesIO(file.read())
    pil_image = Image.open(image).convert('RGB')

    description = generate_description_logic(input_text, pil_image)
    return jsonify({'description': description})
