from PIL.Image import Image as PilImage

user_data = {}


def generate_description_logic(input_text: str, image: PilImage) -> str:
    """
    Генерирует описание для объявления.

    Параметры:
        input_text (str): Текст, содержащий информацию о заголовке, категории, подкатегории, состоянии, цвете и т. д.
        image (PilImage): Изображение объявления в формате PIL.Image.

    Возвращает:
        str: Сгенерированное описание объявления.
    """
    return f"{input_text}"
