import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
from finger_storage import *
from verify_finger import *
import threading


csv_table = None
stop_event = threading.Event()
stop_flag = False

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

# creat csv file
now = datetime.now()
current_date = now.strftime("%Y_%m_%d_%H_%M_%S")
file_path = os.path.join(
    "D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\finger_record_sheets", current_date + ".csv")

with open(file_path, "w", newline="") as f:
    lnwriter = csv.writer(f)
    lnwriter.writerow(["Fingerprint Record"])
    lnwriter.writerow(["No.", "Name", "Time"])

n = 1
# def get_name():


def click_display_button():
    clear()
    display_frame.configure(
        text="Display CSV", foreground="white", background="#030335", font=('ariel', 30))
    display_csv()


def click_register_button():
    clear()
    display_frame.configure(text="Register Finger", foreground="white",
                            background="#030335", font=('ariel', 30))
    text_widget.pack()
    frame.pack(side="left", padx=20)

    entry.pack(side="left")
    confirm_button.pack(side="left", padx=20)


def click_verify_button():
    clear()
    display_frame.configure(text="Verify Finger", foreground="white",
                            background="#030335", font=('ariel', 30))
    text_widget.pack()
    verify_button.pack(side="left", padx=20)


def click_attendance_button():
    clear()
    display_frame.configure(
        text="Attendance", foreground="white", background="#030335", font=('ariel', 30))

    text_widget.pack()
    start_button.pack(side="left", padx=20)
    stop_button.pack(side="right", padx=20)


def click_delete_button():
    clear()
    display_frame.configure(text="Delete Finger", foreground="white",
                            background="#030335", font=('Helvetica', 30))
    text_widget.pack()
    frame.pack(side="left", padx=20)

    entry.pack(side="left")
    confirm_button.pack(side="left", padx=20)


def clear():
    text_widget.delete("1.0", tk.END)  # Clear the text widget
    text_widget.pack_forget()
    confirm_button.pack_forget()
    verify_button.pack_forget()
    start_button.pack_forget()
    stop_button.pack_forget()
    entry.pack_forget()
    frame.pack_forget()


def start():
    global stop_flag
    stop_flag = False
    thread = threading.Thread(target=check_finger)
    thread.start()


def stop():
    global stop_flag
    stop_flag = True


def get_name():
    global entry, user_input
    user_input = entry.get()
    print("User input:", user_input)
    return user_input


def register():
    get_name()
    if verify_finger():
        fingerprint_name = next(
            (k for k, v in fingerprints.items() if v == finger.finger_id), None)
        if fingerprint_name:
            output_text = f"Detected {fingerprint_name} \nIt is already stored.\n"
            print(output_text)
            text_widget.insert(tk.END, output_text)
    else:
        for fingerimg in range(1, 3):
            message = f"Place {'same' if fingerimg == 2 else 'your'} finger on sensor..."
            text_widget.insert(tk.END, message + "\n")
            while True:
                i = finger.get_image()
                if i == adafruit_fingerprint.OK:
                    message = "Image taken"
                    text_widget.insert(tk.END, message + "\n")
                    break
                if i == adafruit_fingerprint.NOFINGER:
                    message = "."
                    text_widget.insert(tk.END, message)
                elif i == adafruit_fingerprint.IMAGEFAIL:
                    message = "Imaging error"
                    text_widget.insert(tk.END, message + "\n")
                    return False
                else:
                    message = "Other error"
                    text_widget.insert(tk.END, message + "\n")
                    return False

            message = "Templating..."
            text_widget.insert(tk.END, message + "\n")
            i = finger.image_2_tz(fingerimg)
            if i == adafruit_fingerprint.OK:
                message = "Templated"
                text_widget.insert(tk.END, message + "\n")
            else:
                if i == adafruit_fingerprint.IMAGEMESS:
                    message = "Image too messy"
                    text_widget.insert(tk.END, message + "\n")
                elif i == adafruit_fingerprint.FEATUREFAIL:
                    message = "Could not identify features"
                    text_widget.insert(tk.END, message + "\n")
                elif i == adafruit_fingerprint.INVALIDIMAGE:
                    message = "Image invalid"
                    text_widget.insert(tk.END, message + "\n")
                else:
                    message = "Other error"
                    text_widget.insert(tk.END, message + "\n")
                return False

        message = "Creating model..."
        text_widget.insert(tk.END, message + "\n")
        i = finger.create_model()
        if i == adafruit_fingerprint.OK:
            message = "Created"
            text_widget.insert(tk.END, message + "\n")
        else:
            if i == adafruit_fingerprint.ENROLLMISMATCH:
                message = "Prints did not match"
                text_widget.insert(tk.END, message + "\n")
            else:
                message = "Other error"
                text_widget.insert(tk.END, message + "\n")
            return False

        if finger.create_model() != adafruit_fingerprint.OK:
            message = "Failed to create fingerprint model"
            text_widget.insert(tk.END, message + "\n")
            return False

        model_number = len(fingerprints) + 1
        fingerprints[user_input] = model_number
        save_fingerprints()

        message = f"Storing model for {user_input} as #{model_number}..."
        text_widget.insert(tk.END, message + "\n")
        i = finger.store_model(model_number)
        if i == adafruit_fingerprint.OK:
            message = "Stored"
            text_widget.insert(tk.END, message + "\n")
        else:
            if i == adafruit_fingerprint.BADLOCATION:
                message = "Bad storage location"
                text_widget.insert(tk.END, message + "\n")
            elif i == adafruit_fingerprint.FLASHERR:
                message = "Flash storage error"
                text_widget.insert(tk.END, message + "\n")
            else:
                message = "Other error"
                text_widget.insert(tk.END, message + "\n")
            return False

        return True


def new_finger():
    get_name()
    if verify_finger():
        fingerprint_name = next(
            (k for k, v in fingerprints.items() if v == finger.finger_id), None)
        if fingerprint_name:
            output_text = f"Detected {fingerprint_name} \nIt is already stored.\n"
            print(output_text)
            text_widget.insert(tk.END, output_text)
    else:
        register(user_input)


def check_finger():
    global n
    global stop_flag
    while not stop_flag:
        if verify_finger():
            fingerprint_name = next(
                (k for k, v in fingerprints.items() if v == finger.finger_id), None)
            if fingerprint_name:
                output_text = f"Detected {fingerprint_name} with confidence {finger.confidence} finger-id {finger.finger_id}\n"
                print(output_text)
                text_widget.insert(tk.END, output_text)
                # Write to the CSV file
                current_second = datetime.now()
                current_time = current_second.strftime("%H:%M:%S")
                with open(file_path, "a", newline="") as f:
                    lnwriter = csv.writer(f)
                    lnwriter.writerow([n, fingerprint_name, current_time])
                f.close()
                n += 1
            else:
                output_text = "Unknown fingerprint\n"
                print(output_text)
                text_widget.insert(tk.END, output_text)
        else:
            output_text = "Finger not found\n"
            print(output_text)
            text_widget.insert(tk.END, output_text)


def verify():
    global n
    if verify_finger():
        fingerprint_name = next(
            (k for k, v in fingerprints.items() if v == finger.finger_id), None)
        if fingerprint_name:
            output_text = f"Detected {fingerprint_name} with confidence {finger.confidence} finger-id {finger.finger_id}\n"
            print(output_text)
            text_widget.insert(tk.END, output_text)
            # Write to the CSV file
            current_second = datetime.now()
            current_time = current_second.strftime("%H:%M:%S")
            with open(file_path, "a", newline="") as f:
                lnwriter = csv.writer(f)
                lnwriter.writerow([n, fingerprint_name, current_time])
            f.close()
            n += 1
        else:
            output_text = "Unknown fingerprint\n"
            print(output_text)
            text_widget.insert(tk.END, output_text)
    else:
        output_text = "Finger not found\n"
        print(output_text)
        text_widget.insert(tk.END, output_text)


def fingerprint_clicked(event):
    clear()
    display_frame.configure(text="Main Frame", foreground="white",
                            background="#030335", font=('Helvetica', 30))
    # Add the logic to display the main frame (blank) in the left frame when the fingerprint image is clicked


def display_csv():
    global csv_table
    df = pd.read_csv(file_path)  # Read the CSV file using pandas
    text_widget.delete("1.0", tk.END)  # Clear the text widget
    text_widget.insert(tk.END, df.to_string())
    text_widget.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
    csv_table = True


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


window = tk.Tk()
window.state('zoomed')  # Set the window state to 'zoomed' (full screen)
window.title("Fingerprint Authentication System")

# Add custom style and theme
style = ttk.Style()
# Choose a theme (e.g., 'clam', 'winnative', 'default')
style.theme_use("clam")

# Customize colors
style.configure("TButton",
                foreground="#030335",
                background="#2196F3",
                font=("Helvetica", 25),
                padding=15,
                width=15,  # Set the width of the buttons
                height=3)  # Set the height of the buttons

# Change button color
style.map("TButton",
          foreground=[('pressed', 'white'), ('active', '#01001F')],
          background=[('pressed', '!disabled', 'dark blue'), ('active', 'dark blue')])

# Change window background color
window.configure(background="#030335")

# Create the main frame
left_frame = tk.Frame(window, bg="#030335")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the right frame
right_frame = tk.Frame(window, bg="#030335")
right_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

# Convert image to GIF format with transparency
# Replace with the actual path to your image
image = Image.open(
    "D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\fingerprint.png")
image = image.resize((150, 150))  # Resize the image as needed
image = image.convert("RGBA")  # Convert to RGBA mode to support transparency
image_with_alpha = ImageTk.PhotoImage(image)

# Create buttons
button_frame = tk.Frame(right_frame, bg="#030335")
button_frame.grid(row=1, column=0, padx=10, pady=10)

# Create a transparent label for the image
image_label = tk.Label(button_frame, image=image_with_alpha, bg="#030335")
image_label.grid(row=0, column=0, pady=25)
# Bind the left mouse button click event to the function
image_label.bind("<Button-1>", lambda event: fingerprint_clicked())

button1 = ttk.Button(button_frame, text="Register Finger",
                     command=click_register_button)
button1.grid(row=1, column=0, pady=12)

button2 = ttk.Button(button_frame, text="Verify Finger",
                     command=click_verify_button)
button2.grid(row=2, column=0, pady=12)

button3 = ttk.Button(button_frame, text="Attendance",
                     command=click_attendance_button)
button3.grid(row=3, column=0, pady=12)

button4 = ttk.Button(button_frame, text="Delete Finger",
                     command=click_delete_button)
button4.grid(row=4, column=0, pady=12)

display_button = ttk.Button(
    button_frame, text="Display CSV", command=click_display_button)
display_button.grid(row=5, column=0, pady=12)

# Create the display frame in the main frame
display_frame = ttk.Label(left_frame, text="Fingerprint Authentication System", font=(
    "Helvetica", 20), background="#030335", foreground="white")
display_frame.pack(padx=20, pady=20)

"""# Create a scrollbar for the display frame
scrollbar = ttk.Scrollbar(left_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)"""

frame = tk.Frame(left_frame)
entry = tk.Entry(frame)


# Create a text widget and buttons for displaying the output
text_widget = tk.Text(left_frame, font=("Helvetica", 14),
                      wrap=tk.WORD, bg="#030335", fg="white")
start_button = tk.Button(left_frame, text="Start", command=start,
                         bg="#2196F3", fg="#030335", font=("Helvetica", 25))
stop_button = tk.Button(left_frame, text="Stop", command=stop,
                        bg="#2196F3", fg="#030335", font=("Helvetica", 25))
verify_button = tk.Button(left_frame, text="Verify", command=verify,
                          bg="#2196F3", fg="#030335", font=("Helvetica", 25))
confirm_button = tk.Button(left_frame, text="Confirm", command=register,
                           bg="#2196F3", fg="#030335", font=("Helvetica", 25))

# scrollbar.configure(command=text_widget.yview)

# Create a label for copyright information
copyright_label = tk.Label(button_frame,
                           text="Developed by Wai Yan Min   Copyright © 2023 MIIT. All rights reserved.",
                           font=("Helvetica", 10), fg="white", bg="#030335")
copyright_label.grid(row=6, column=0, pady=12)

window.mainloop()
