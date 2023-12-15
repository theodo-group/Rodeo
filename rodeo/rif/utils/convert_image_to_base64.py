import base64


def convert_image_to_base64(image):
    img_str = base64.b64encode(image)
    return img_str.decode("utf-8")
