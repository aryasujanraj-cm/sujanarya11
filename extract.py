import easyocr
import re
import cv2
import numpy as np

# Load EasyOCR model once
reader = easyocr.Reader(['en'])


# ---------------- IMAGE PREPROCESSING ----------------
def preprocess_image(image_file):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    return gray


# ---------------- OCR ----------------
def extract_text_and_amount(image_file):
    try:
        image_file.seek(0)
        processed = preprocess_image(image_file)

        results = reader.readtext(processed)

        text = " ".join([res[1] for res in results])

        print("OCR TEXT:", text)  # debug

        return text, 0  # ❌ we DON'T trust raw amount anymore

    except Exception as e:
        print("OCR Error:", e)
        return "", 0


# ---------------- SMART EXTRACTION ----------------
def extract_details(text):

    text_upper = text.upper()

    # -------- Currency --------
    currency = "₹"
    if "$" in text:
        currency = "$"
    elif "€" in text:
        currency = "€"

    # -------- Merchant --------
    merchant = "Unknown"
    lines = text.split()

    for word in lines:
        if len(word) > 3 and not word.isdigit():
            merchant = word
            break

    # -------- Amount Detection (SMART) --------

    # Priority 1 → TOTAL / AMOUNT keywords
    patterns = [
        r"TOTAL\s*[:\-]?\s*(\d+\.?\d*)",
        r"AMOUNT\s*[:\-]?\s*(\d+\.?\d*)",
        r"GRAND\s*TOTAL\s*[:\-]?\s*(\d+\.?\d*)",
        r"TOTAL\s*₹?\s*(\d+\.?\d*)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text_upper)
        if match:
            return merchant, float(match.group(1)), currency

    # Priority 2 → ₹ or currency values
    currency_matches = re.findall(r"[₹$€]\s?(\d+\d*)", text)
    if currency_matches:
        return merchant, float(max(currency_matches, key=float)), currency

    # Priority 3 → Filtered numbers
    numbers = re.findall(r"\d+\.?\d*", text)

    filtered = []
    for num in numbers:
        val = float(num)

        # Ignore unrealistic values
        if 1 < val < 100000:
            filtered.append(val)

    if filtered:
        return merchant, max(filtered), currency

    return merchant, 0, currency