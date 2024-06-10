from transformers import (VisionEncoderDecoderModel,
                          ViTFeatureExtractor, GPT2Tokenizer)
from peft import LoraConfig, get_peft_model
import torch

model_path = "tuman/vit-rugpt2-image-captioning"

vit = VisionEncoderDecoderModel.from_pretrained(model_path)
feature_extractor = ViTFeatureExtractor.from_pretrained(model_path)
tokenizer_gpt2 = GPT2Tokenizer.from_pretrained(model_path)

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules='all-linear',
    lora_dropout=0.1
)

model = get_peft_model(vit, lora_config)

vit.load_state_dict(torch.load(r'app/static/state_dict'))

vit.decoder.config.pad_token_id = 0
vit.decoder.config.bos_token_id = 1
vit.decoder.config.eos_token_id = 2

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
