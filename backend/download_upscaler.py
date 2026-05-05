from diffusers import StableDiffusionUpscalePipeline
import torch

MODEL_ID = "stabilityai/stable-diffusion-x4-upscaler"

pipe = StableDiffusionUpscalePipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    use_safetensors=True,
)

print("Model downloaded and cached successfully.")