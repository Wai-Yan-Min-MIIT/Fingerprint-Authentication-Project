import serial
import adafruit_fingerprint
import os

# UART setup
uart = serial.Serial("COM3", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# Directory path to store the .dat file
output_directory = r'D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\fingerprint_authentication_system'

def save_fingerprint_data_to_file():
    print("Reading fingerprint templates...")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")

    # Get the number of existing fingerprint templates
    num_templates = len(finger.templates)

    if num_templates == 0:
        print("No fingerprint templates found.")
        return

    print(f"Saving fingerprint data for {num_templates} templates...")

    # Create a list to store fingerprint data and finger IDs
    fingerprint_data = []

    # Loop through each existing finger template and store the data
    for finger_id in range(1, num_templates + 1):
        template_data = finger.get_fpdata("char", finger_id)
        fingerprint_data.append((finger_id, template_data))
        print(fingerprint_data)

    # Construct the full file path including the directory and filename
    filename = os.path.join(output_directory, 'fingerprint_data.dat')

    # Save the fingerprint data to the specified .dat file
    with open(filename, "wb") as file:
        for finger_id, template_data in fingerprint_data:
            file.write(f"Finger ID: {finger_id}\n".encode())
            for byte in template_data:
                file.write(bytearray(byte))
            file.write(b"\n")
    
    print(f"Fingerprint data saved to {filename}")

while True:
    print("----------------")
    print("s) Save fingerprint data to file")
    print("x) Quit")
    print("----------------")
    c = input("> ")

    if c in ("x", "q"):
        print("Exiting fingerprint program")
        raise SystemExit
    elif c == "s":
        save_fingerprint_data_to_file()
    else:
        print("Invalid choice: Try again")
