from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps


class ImagePreprocessor:
    """
    Local production preprocessing:
    - normalize format
    - fix EXIF rotation
    - convert to RGB
    - resize tiny source images before AI
    - place product on clean studio-like canvas
    """

    def prepare_for_ai(self, input_path: str) -> bytes:
        image = Image.open(input_path)
        image = ImageOps.exif_transpose(image).convert("RGB")

        image = self._resize_if_too_small(image)
        image = self._studio_canvas(image)

        temp_path = Path(input_path).with_suffix(".prepared.png")
        image.save(temp_path, format="PNG", optimize=True)

        return temp_path.read_bytes()

    def postprocess_output(self, image_bytes: bytes, output_path: str) -> str:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        image.save(
            output_path,
            format="PNG",
            optimize=True,
            compress_level=6,
        )

        return output_path

    def _resize_if_too_small(self, image: Image.Image) -> Image.Image:
        width, height = image.size
        min_side = min(width, height)

        if min_side >= 768:
            return image

        scale = 768 / min_side
        new_size = (int(width * scale), int(height * scale))

        return image.resize(new_size, Image.Resampling.LANCZOS)

    def _studio_canvas(self, image: Image.Image) -> Image.Image:
        max_size = 1024
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        canvas = Image.new("RGB", (1024, 1024), (248, 248, 248))
        x = (1024 - image.width) // 2
        y = (1024 - image.height) // 2

        canvas.paste(image, (x, y))
        return canvas
