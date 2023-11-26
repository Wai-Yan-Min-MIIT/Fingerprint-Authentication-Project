import time
import adafruit_fingerprint
import serial
import json
import csv
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Serial communication
uart = serial.Serial('COM3', baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
fingerprints = {}
n=1
 
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

# Fingerprint operations
def verify_finger():
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

    return True

def delete_finger(name):
    if name in fingerprints:
        if finger.delete_model(fingerprints[name]) == adafruit_fingerprint.OK:
            del fingerprints[name]
            save_fingerprints()
            print("Deleted!")
        else:
            print("Failed to delete")
    else:
        print("Fingerprint not found")

def delete_all_fingerprints():
    # Read the current fingerprint templates
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
        
    templates = finger.templates
    if not templates:
        print("No more fingerprint templates to delete.")

    for template in templates:
        if finger.delete_model(template) == adafruit_fingerprint.OK:
            print("Fingerprint template", template, "deleted.")
        else:
            print("Failed to delete fingerprint template", template)

    print("All fingerprint templates deleted.")

    """fingerprints.clear()  # Clear the fingerprints dictionary
    save_fingerprints()   # Save the updated dictionary to the JSON file
"""
def send_email(subject, to, body, attachment_path):
    gmail_user = 'testerwaiyan@gmail.com'
    gmail_password = 'epxemhusdamumqbm'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, 'rb') as f:
        part = MIMEApplication(
            f.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(
            attachment_path)
        msg.attach(part)

    server.sendmail(gmail_user, to, msg.as_string())
    server.quit()
    
# User input functions
def get_name():
    return input("Enter the name of the fingerprint: ")

now = datetime.now()
current_date = now.strftime("%Y_%m_%d_%H_%M_%S")
file_path = os.path.join(
    "D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\finger_record_sheets", current_date + ".csv")


with open(file_path, "w", newline="") as f:
    lnwriter = csv.writer(f)
    lnwriter.writerow(["Fingerprint Record"])
    lnwriter.writerow(["No.", "Name", "Time"])

while True:
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Fingerprint templates:", finger.templates)
    print("e) Collect new fingerprint")
    print("f) Check fingerprint")
    print("d) Delete fingerprint")
    print("r) Reset all fingerprints")
    print("q) Quit the program")

    
    print("----------------")
    c = input("> ")

    if c == "e":
        name = get_name()
        if verify_finger():
            fingerprint_name = next((k for k, v in fingerprints.items() if v == finger.finger_id), None)
            if fingerprint_name:
                print("Detected", fingerprint_name, "\nIt is already stored.")
        else:
            register(name)

    elif c == "f":
        if verify_finger():
            fingerprint_name = next((k for k, v in fingerprints.items() if v == finger.finger_id), None)
            if fingerprint_name:
                print("Detected", fingerprint_name, "with confidence", finger.confidence, "fingerid",finger.finger_id)
                #write in csv file
                current_second = datetime.now()
                current_time = current_second.strftime("%H:%M:%S")
                with open(file_path, "a", newline="") as f:
                    lnwriter = csv.writer(f)
                    lnwriter.writerow([n, fingerprint_name, current_time])
                n += 1
            else:
                print("Unknown fingerprint")
        else:
            print("Finger not found")
        
    elif c == "d":
        name = get_name()
        delete_finger(name)
        
    elif c == "q":
        f.close()
        subject = 'Finger Record'
        to = 'waiyanminmiit@gmail.com'
        body = 'Please find the attached CSV file.'
        attachment_path = os.path.join('D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\finger_record_sheets', current_date + '.csv')
        send_email(subject, to, body, attachment_path)
        print("Your email is successfully sent.")
        break

    else:
        print("Invalid option")
        
    """elif c == "r":
        delete_all_fingerprints()"""

