import cv2
import numpy as np
import pytesseract

# ------------------------------
# Convert Y position to price
# ------------------------------
def y_to_price(y, y1, p1, y2, p2):
    if y2 == y1:
        return None
    ratio = (y - y1) / (y2 - y1)
    return p1 + ratio * (p2 - p1)

# ------------------------------
# Simple OCR reader
# ------------------------------
def try_ocr_read(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        text = pytesseract.image_to_string(blur)
        return text.strip()
    except:
        return ""

# ------------------------------
# BASIC OB / FVG DETECTORS
# ------------------------------
def detect_ob_fvg(img):
    h, w, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 60, 140)

    edge_density = np.sum(edges == 255)

    order_block = edge_density % 2 == 0
    fair_value_gap = edge_density % 3 == 0

    return {
        "ob": order_block,
        "fvg": fair_value_gap,
        "density": int(edge_density)
    }
