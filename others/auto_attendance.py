import adafruit_fingerprint
import serial
import json
import csv
from datetime import datetime
import os
from finger_storage import *

n=1

# Fingerprint operations
def get_fingerprint():
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True

now = datetime.now()
current_date = now.strftime("%Y_%m_%d_%H_%M_%S")
file_path = os.path.join(
    "D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\finger_record_sheets", current_date + ".csv")


while True:

    if get_fingerprint():
        fingerprint_name = next((k for k, v in fingerprints.items() if v == finger.finger_id), None)
        if fingerprint_name:
            print("Detected", fingerprint_name, "with confidence", finger.confidence, "fingerid",finger.finger_id)
            #write in csv file
            current_time = now.strftime("%H:%M:%S")
            with open(file_path, "a", newline="") as f:
                lnwriter = csv.writer(f)
                lnwriter.writerow([n, fingerprint_name, current_time])
            n += 1
        else:
            print("Unknown fingerprint")
    else:
        print("Finger not found")