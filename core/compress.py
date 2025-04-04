from PIL import Image

def compress_image(input_path, output_path, quality, format_, max_size):
    try:
        img = Image.open(input_path)

        if img.mode in ("RGBA", "LA"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        if max_size:
            img.thumbnail(max_size)

        if format_.lower() == "webp":
            img.save(output_path, format_.upper(), quality=quality, lossless=False)
        else:
            img.save(output_path, format_.upper(), quality=quality)

        return True
    except Exception as e:
        return str(e)
