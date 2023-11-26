import json
import adafruit_fingerprint
import serial

# Serial communication
uart = serial.Serial('COM3', baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

fingerprints = {}
 
# File operations
def save_fingerprints():
    with open("D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\fingerprint_templates.json", "w") as file:
        json.dump(fingerprints, file)

def load_fingerprints():
    try:
        with open("D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\fingerprint_templates.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

fingerprints = load_fingerprints()
