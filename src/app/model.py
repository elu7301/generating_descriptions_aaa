from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, GPT2Tokenizer
from peft import LoraConfig, get_peft_model
import torch

vit = VisionEncoderDecoderModel.from_pretrained("tuman/vit-rugpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("tuman/vit-rugpt2-image-captioning")
tokenizer_gpt2 = GPT2Tokenizer.from_pretrained("tuman/vit-rugpt2-image-captioning")

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules='all-linear',
    lora_dropout=0.1
)

model = get_peft_model(vit, lora_config)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

vit.load_state_dict(torch.load(r'static/state_dict'))

vit.decoder.config.pad_token_id = 0
vit.decoder.config.bos_token_id = 1
vit.decoder.config.eos_token_id = 2
