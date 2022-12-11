import base64
from src.image_converter import *

"""
Step 1 - convertion of an imange to base64 encoded string
"""
enconded_string = convert_image_to_base64('')

"""
Step 2 - save base64 encoded string to txt file
"""
save_encoded_string('', encoded_string)

"""
Step 3 - create new image from encoded string
"""
create_image_from_string('', encoded_string)
