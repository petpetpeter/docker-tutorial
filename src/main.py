import sys
import time
import os
from pyzbar.pyzbar import decode
from PIL import Image

BARCODE_IMAGE = "qr.png"
API_KEY_THAT_WILL_MAKE_YOU_BANKRUPT = os.getenv("API_KEY_THAT_WILL_MAKE_YOU_BANKRUPT","default_key")

def decode_qr(image_path):
    try:
        print(f"API Key: {API_KEY_THAT_WILL_MAKE_YOU_BANKRUPT}")
        img = Image.open(image_path)
        decoded_objects = decode(img)
        if not decoded_objects:
            print(f"No QR code found in {image_path}")
            return
        
        for obj in decoded_objects:
            print(f"Type: {obj.type}")
            print(f"Data: {obj.data.decode('utf-8')}\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        decode_qr(f"./data/{BARCODE_IMAGE}")
        time.sleep(3)
        
    
