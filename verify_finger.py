import time
import adafruit_fingerprint
import serial
import json
import csv
from datetime import datetime
import os
from matplotlib import pyplot as plt
import numpy as np
from finger_storage import *

"""now = datetime.now()
current_date = now.strftime("%Y_%m_%d_%H_%M_%S")
file_path = os.path.join(
    "D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\finger_record_sheets", current_date + ".csv")
n=1
"""

#check fingerprint
def check():
    print("Waiting for image...")
    if finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True

# def check():
#     """Get a finger print image, show it, template it, and see if it matches!"""
#     print("Waiting for image...")
#     while finger.get_image() != adafruit_fingerprint.OK:
#         pass
#     print("Got image...Transferring image data...")
#     imgList = finger.get_fpdata("image", 2)
#     imgArray = np.zeros(73728, np.uint8)
#     for i, val in enumerate(imgList):
#         imgArray[(i * 2)] = val & 240
#         imgArray[(i * 2) + 1] = (val & 15) * 16
#     imgArray = np.reshape(imgArray, (288, 256))
#     plt.title("Fingerprint Image")
#     plt.imshow(imgArray)
#     plt.show(block=False)
#     print("Templating...")
#     if finger.image_2_tz(1) != adafruit_fingerprint.OK:
#         return False
#     print("Searching...")
#     if finger.finger_search() != adafruit_fingerprint.OK:
#         return False
#     return True

# def Verify_finger():
#     """Get a finger print image, show it, template it, and see if it matches!"""
#     print("Waiting for image...")
#     while finger.get_image() != adafruit_fingerprint.OK:
#         pass
#     print("Got image...Transferring image data...")
#     imgList = finger.get_fpdata("image", 2)
#     imgArray = np.zeros(73728, np.uint8)
#     for i, val in enumerate(imgList):
#         imgArray[(i * 2)] = val & 240
#         imgArray[(i * 2) + 1] = (val & 15) * 16
#     imgArray = np.reshape(imgArray, (288, 256))
#     plt.title("Fingerprint Image")
#     plt.imshow(imgArray)
#     plt.show(block=False)
#     print("Templating...")
#     if finger.image_2_tz(1) != adafruit_fingerprint.OK:
#         return False
#     print("Searching...")
#     if finger.finger_search() != adafruit_fingerprint.OK:
#         return False
#     return True
def Verify_finger():
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

"""if verify_finger():
            fingerprint_name = next((k for k, v in fs.fingerprints.items() if v == finger.finger_id), None)
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
    print("Finger not found")"""