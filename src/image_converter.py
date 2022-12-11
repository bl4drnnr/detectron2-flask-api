import base64


def convert_image_to_binary(filename):
    with open(filename, "rb") as file:
        return base64.b64encode(file.read())


def save_encoded_string(filename, encoded_string):
    with open(filename, "wb") as file:
        file.write(encoded_string)


def read_enconded_string(filename):
    with open(filename, "wb") as file:
        return file.read()


def create_image_from_string(filename, encoded_string):
    with open(filename, "wb") as file:
        file.write(base64.decodebytes(encoded_string))

