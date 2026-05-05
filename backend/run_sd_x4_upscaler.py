import os
from pathlib import Path
from tkinter import Tk, filedialog
from datetime import datetime

import torch
from PIL import Image, ImageOps
from diffusers import StableDiffusionUpscalePipeline


MODEL_ID = "stabilityai/stable-diffusion-x4-upscaler"
OUTPUT_DIR = "outputs"

PROMPT = (
    "professional ecommerce studio product photo, sharp details, realistic texture, "
    "clean white studio background, soft commercial lighting, high quality"
)

NEGATIVE_PROMPT = (
    "blurry, distorted, low quality, watermark, text, deformed, duplicate, bad edges"
)


def choose_image_file() -> str:
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        title="Select a low-resolution product image",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.webp"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("WEBP files", "*.webp"),
        ],
    )

    root.destroy()

    if not file_path:
        raise RuntimeError("No image selected.")

    return file_path


def prepare_image(path: str, max_size: int = 192) -> Image.Image:
    image = Image.open(path)
    image = ImageOps.exif_transpose(image).convert("RGB")

    width, height = image.size
    longest_side = max(width, height)

    if longest_side > max_size:
        scale = max_size / longest_side
        new_size = (int(width * scale), int(height * scale))
        image = image.resize(new_size, Image.Resampling.LANCZOS)

    return image


def load_pipeline() -> StableDiffusionUpscalePipeline:
    if not torch.cuda.is_available():
        print("CUDA not found. Running on CPU. This will be very slow.")
        dtype = torch.float32
        device = "cpu"
    else:
        print(f"CUDA found: {torch.cuda.get_device_name(0)}")
        dtype = torch.float16
        device = "cuda"

    pipe = StableDiffusionUpscalePipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        variant="fp16" if device == "cuda" else None,
        use_safetensors=True,
    )

    if device == "cuda":
        pipe.enable_attention_slicing()
        pipe.enable_model_cpu_offload()
    else:
        pipe = pipe.to(device)

    return pipe


def upscale_image(pipe: StableDiffusionUpscalePipeline, image: Image.Image) -> Image.Image:
    generator = torch.Generator(
        device="cuda" if torch.cuda.is_available() else "cpu").manual_seed(42)

    result = pipe(
        prompt=PROMPT,
        negative_prompt=NEGATIVE_PROMPT,
        image=image,
        num_inference_steps=30,
        guidance_scale=7.5,
        generator=generator,
    ).images[0]

    return result


def save_output(image: Image.Image, source_path: str) -> str:
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    source_name = Path(source_path).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(OUTPUT_DIR) / \
        f"{source_name}_x4_upscaled_{timestamp}.png"

    image.save(output_path, format="PNG", optimize=True)
    return str(output_path)


def main():
    print("Select an image...")
    input_path = choose_image_file()

    print(f"Selected: {input_path}")
    print("Preparing image...")
    image = prepare_image(input_path, max_size=192)

    print(f"Prepared image size: {image.size}")
    print("Loading Stable Diffusion x4 Upscaler...")
    pipe = load_pipeline()

    print("Upscaling image...")
    output = upscale_image(pipe, image)

    output_path = save_output(output, input_path)

    print("\nDone!")
    print(f"Saved output to: {output_path}")


if __name__ == "__main__":
    main()
