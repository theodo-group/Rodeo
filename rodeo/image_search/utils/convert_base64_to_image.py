import base64
import io

from PIL import Image


def convert_base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)

    return Image.open(io.BytesIO(image_data))
