from PIL.Image import Image as PilImage
from .model import vit, feature_extractor, tokenizer_gpt2, model

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

    pix = feature_extractor(image, return_tensors="pt")
    text = tokenizer_gpt2(input_text, return_tensors="pt")

    generated_text = model.generate(
        pixel_values=pix.pixel_values.cuda(),
        decoder_input_ids=text.input_ids.cuda(),
        max_length=500,
        eos_token_id=tokenizer_gpt2.eos_token_id,
        do_sample=True,
        temperature=1.2
    )

    description = tokenizer_gpt2.decode(generated_text[0]).split('Описание: ', maxsplit=1)[1].strip()

    return description.strip('</s>')
