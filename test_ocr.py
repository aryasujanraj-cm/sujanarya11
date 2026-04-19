from PIL import Image
import pytesseract

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image
img = Image.open("test.png")

# Extract text
text = pytesseract.image_to_string(img)

print("Extracted Text:")
print(text)