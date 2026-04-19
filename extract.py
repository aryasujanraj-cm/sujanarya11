import easyocr
import re
from PIL import Image
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image_file):
    image_file.seek(0)
    image = Image.open(image_file).convert("RGB")
    return np.array(image)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def extract_text_and_amount(image_file):
    img = preprocess_image(image_file)

    results = reader.readtext(img, detail=0)

    text = " ".join(results)
    text = clean_text(text)

    nums = re.findall(r'\d+\.\d+|\d+', text)

    values = []

    for n in nums:
        try:
            v = float(n)
            if 10 <= v <= 100000:
                values.append(v)
        except:
            pass

    amount = max(values) if values else 0

    return text, amount