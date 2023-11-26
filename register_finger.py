import time
import adafruit_fingerprint
from finger_storage import *
from verify_finger import *

def register(name):
    for fingerimg in range(1, 3):
        print(f"Place {'same' if fingerimg == 2 else 'your'} finger on sensor...", end="")
        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    if finger.create_model() != adafruit_fingerprint.OK:
        print("Failed to create fingerprint model")
        return False

    model_number = len(fingerprints)+1
    fingerprints[name] = model_number
    save_fingerprints()

    print(f"Storing model for {name} as #{model_number}...")
    m=f"Storing model for {name} as #{model_number}..."
    i = finger.store_model(model_number)
    if i == adafruit_fingerprint.OK: 
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    
    return m


"""if c == "e":
        name = get_name()
        if cf.check_fingerprint():
            fingerprint_name = next((k for k, v in fs.fingerprints.items() if v == finger.finger_id), None)
            if fingerprint_name:
                print("Detected", fingerprint_name, "\nIt is already stored.")
        else:
            enroll_finger(name)"""