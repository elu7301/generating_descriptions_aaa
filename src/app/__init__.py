from flask import Flask
from app.routes import main_bp
import os

def create_app() -> Flask:
    """
    Создает и настраивает экземпляр Flask-приложения.

    Returns:
        Flask: Экземпляр Flask-приложения.
    """

    app = Flask(__name__)
    app.config.from_object('config.Config')

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(main_bp)

    return app
