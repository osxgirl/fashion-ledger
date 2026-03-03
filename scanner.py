import cv2
import pytesseract
from storage import load_items, save_items
import re
from models.item import FashionItem


def normalize(text):
    return text.lower().strip()


def preprocess_image(image_path):
    img = cv2.imread(image_path)

    # upscale
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    # isolate bright pixels (white text)
    lower = (200, 200, 200)
    upper = (255, 255, 255)

    mask = cv2.inRange(img, lower, upper)

    return mask


def extract_text(processed_image):
    text = pytesseract.image_to_string(
        processed_image,
        config="--psm 6"
    )
    return text


def clean_ocr_text(text):
    text = re.sub(r"[^A-Za-z0-9| \n]", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" | ", "|")
    return text.strip()


def extract_items(text):
    # Look for sequences of capitalized words
    matches = re.findall(r"[A-Z][a-z]+(?: [A-Z][a-z]+){0,2}", text)

    items = []

    for match in matches:
        # Filter obvious junk fragments
        if len(match) < 4:
            continue

        # Skip known OCR noise fragments
        if match.lower() in ["rl", "nal"]:
            continue

        items.append(match.strip())

    return items


def run_scan(image_path):
    items = load_items()

    img = cv2.imread(image_path)

    if img is None:
        print("❌ Image failed to load.")
        return

    print("✅ Image loaded successfully.")

    processed = preprocess_image(image_path)
    cv2.imwrite("debug_processed.png", processed)
    print("🧪 Saved processed image as debug_processed.png")

    text = extract_text(processed)

    cleaned = clean_ocr_text(text)
    detected_items = extract_items(cleaned)

    print("\n📦 DETECTED ITEMS:\n")
    for item in detected_items:
        print("-", item)

    # Normalize for comparison
    existing_normalized = {normalize(i.name) for i in items}

    new_items = []
    for item in detected_items:
        if normalize(item) not in existing_normalized:
            new_item = FashionItem(
                name=item,
                item_type="Unknown",
                platform="Roblox",
                acquisition_type="DTI Unlock",
                price=0,
                currency_name="Unknown",
                currency_type="Unknown",
            )
            items.append(new_item)
            new_items.append(item)

    if new_items:
        print("\n✨ NEW ITEMS ADDED:")
        for item in new_items:
            print("+", item)
    else:
        print("\n✔ No new items found.")

    save_items(items)

    print("\n🔎 OCR RAW OUTPUT:\n")
    print(repr(text))

    cleaned = clean_ocr_text(text)

    print("\n✨ CLEANED TEXT:\n")
    print(cleaned)

    detected = extract_items(cleaned)

    print("\n📦 DETECTED ITEMS:\n")
    for item in detected:
        print("-", item)

    save_items(items)
    print("\nDTI OCR scan complete.")