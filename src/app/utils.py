from PIL.Image import Image as PilImage
from .model import feature_extractor, tokenizer_gpt2, model
from app.constants import promt_dict

def promt_preprocess(user_data: dict) -> str:
    """
    Препроцессинг данных объявления для подачи в качестве промта в модель.
    """
    input_text = (f"{promt_dict['title']}: {user_data.get('title', '')},"
                  f" {promt_dict['cat']}: {user_data.get('cat', '')},"
                  f" {promt_dict['ad_type']}: {user_data.get('ad_type', '')},"
                  f" {promt_dict['location']}: {user_data.get('location', '')},"
                  f" {promt_dict['condition']}: {user_data.get('condition', '')},"
                  f" {promt_dict['color']}: {user_data.get('color', '')},"
                  f" {promt_dict['brand']}: {user_data.get('brand', '')}"
                  f" {promt_dict['size']}. {user_data.get('cat', '')}: {user_data.get('size', '')}")

    if user_data.get('cat', '') != promt_dict['accessories']:
        input_text += f", {promt_dict['sub']}: {user_data.get('sub', '')}"

    input_text += f", {promt_dict['description']}:"

    return input_text


def generate_description_logic(
        input_text: str,
        image: PilImage,
        temperature: float=0.7,
        max_length: int=500
) -> str:
    """
    Генерирует описание для объявления.

    Параметры:
        input_text (str): Текст, содержащий информацию о заголовке,
            категории, подкатегории, состоянии, цвете и т. д.
        image (PilImage): Изображение объявления в формате PIL.Image.

    Возвращает:
        str: Сгенерированное описание объявления.
    """

    pix = feature_extractor(image, return_tensors="pt")
    text = tokenizer_gpt2(input_text, return_tensors="pt")

    generated_text = model.generate(
        pixel_values=pix.pixel_values.cuda(),
        decoder_input_ids=text.input_ids.cuda(),
        max_length=max_length,
        eos_token_id=tokenizer_gpt2.eos_token_id,
        do_sample=True,
        temperature=temperature
    )

    description = tokenizer_gpt2.decode(generated_text[0])
    description = description.split(f"{promt_dict['description']}: ", maxsplit=1)[1].strip()

    return description.strip('</s>')
