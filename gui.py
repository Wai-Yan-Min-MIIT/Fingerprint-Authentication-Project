import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
from finger_storage import *
from verify_finger import *
from email_sender import *
import threading
from tkinter import font

csv_table = None
stop_event = threading.Event()
stop_flag = False

attendance = set()
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


def click_csv_button():
    clear()
    stop()
    display_frame.configure(
        text="Display CSV", foreground="white", background="#030335", font=('ariel', 30))
    display_csv()


def click_register_button():
    clear()
    stop()
    display_frame.configure(text="Register Finger", foreground="white",
                            background="#030335", font=('ariel', 30))
    text_widget.pack()
    confirm_button.pack(side="right", padx=10)
    frame.pack(side="right", padx=20)
    text_widget.delete("1.0", tk.END)  # Clear the text widget
    output_text = "\n\n   Enter  Name or Roll No. in textbox.\n\n   Click  \"Confirm\"  and place your finger on sensor until finger model is stored!\n\n\n\n\n"
    text_widget.insert(tk.END, output_text)
    entry.pack(side="right")


def click_verify_button():
    clear()
    stop()
    display_frame.configure(text="Verify Finger", foreground="white",
                            background="#030335", font=('ariel', 30))
    text_widget.pack()
    text_widget.delete("1.0", tk.END)  # Clear the text widget
    output_text = "\n\n   Click  \"Check\"  and Place Your Finger on Sensor!\n\n\n\n\n"
    text_widget.insert(tk.END, output_text)
    verify_button.pack(side="right", padx=10)


def click_attendance_button():
    clear()
    stop()
    display_frame.configure(
        text="Attendance", foreground="white", background="#030335", font=('ariel', 30))
    text_widget.pack()
    text_widget.delete("1.0", tk.END)  # Clear the text widget
    output_text = "\n\n   Click  \"Start\"  to record attendance and click  \"Stop\"  to stop recording.\n\n\n\n\n"
    text_widget.insert(tk.END, output_text)
    start_button.pack(side="left", padx=10)
    stop_button.pack(side="right", padx=10)


def click_delete_button():
    clear()
    stop()
    display_frame.configure(text="Delete Finger", foreground="white",
                            background="#030335", font=('Helvetica', 30))
    text_widget.pack()
    text_widget.delete("1.0", tk.END)
    output_text = "\n\n   Enter your Name or Roll No. in textbox. Click  \"Delete\"  to delete your fingerprint from database.\n\n\n\n\n"
    text_widget.insert(tk.END, output_text)
    delete_button.pack(side="right", padx=10)
    frame.pack(side="right", padx=10)
    entry.pack(side="right")


def click_email_button():
    clear()
    stop()
    display_frame.configure(text="Send Email", foreground="white",
                            background="#030335", font=('Helvetica', 30))
    text_widget.pack()
    text_widget.delete("1.0", tk.END)
    frame.pack(side="left", padx=10)
    output_text = "\n\n   You can enter  Email  you want in textbox and click \"Send\" to send attendance data\n\n   but you must be a admin.\n\n   If you're not admin, click \"Default\".\n\n\n\n\n"
    text_widget.insert(tk.END, output_text)
    entry.pack(side="left")
    send_button.pack(side="left", padx=20)
    default_button.pack(side="right", padx=10)


def clear():
    text_widget.delete("1.0", tk.END)
    text_widget.pack_forget()
    confirm_button.pack_forget()
    verify_button.pack_forget()
    start_button.pack_forget()
    stop_button.pack_forget()
    entry.pack_forget()
    frame.pack_forget()
    delete_button.pack_forget()
    send_button.pack_forget()
    default_button.pack_forget()
    miit_label.pack_forget()
    text.pack_forget()
    display_frame.pack(pady=30)


def display_csv():
    global csv_table
    df = pd.read_csv(file_path)  # Read the CSV file using pandas
    text_widget.delete("1.0", tk.END)  # Clear the text widget
    text_widget.insert(tk.END, df.to_string())
    text_widget.pack()
    csv_table = True


def start():
    global stop_flag
    stop_flag = False
    output_text = "Place Your Finger on Sensor!"
    text_widget.insert(tk.END, output_text)
    thread = threading.Thread(target=check_finger)
    thread.start()


def stop():
    global stop_flag
    stop_flag = True


def get_name():
    global entry, user_input
    user_input = entry.get()
    print("User input:", user_input)
    entry.delete(0, tk.END)


def register():
    get_name()
    text_widget.delete("1.0", tk.END)  # Clear the text widget
    if Verify_finger():
        fingerprint_name = next(
            (k for k, v in fingerprints.items() if v == finger.finger_id), None)
        if fingerprint_name:
            output_text = f"\n\n\n\n\n\n\n\n\n\t\t\tDetected {fingerprint_name} \n\n\t\t\tIt is already stored.\n\n\t\t\tRegister another finger\n"
            """print(output_text)"""
            text_widget.insert(tk.END, output_text)
    else:
        for fingerimg in range(1, 3):
            message = f"Place {'same' if fingerimg == 2 else 'your'} finger on sensor..."
            # text_widget.insert(tk.END, message + "\n")
            while True:
                i = finger.get_image()
                if i == adafruit_fingerprint.OK:
                    message = "Image taken"
                    # text_widget.insert(tk.END, message + "\n")
                    break
                if i == adafruit_fingerprint.NOFINGER:
                    message = "."
                    # text_widget.insert(tk.END, message)
                elif i == adafruit_fingerprint.IMAGEFAIL:
                    message = "Imaging error"
                    # text_widget.insert(tk.END, message + "\n")
                    return False
                else:
                    message = "Other error"
                    # text_widget.insert(tk.END, message + "\n")
                    return False

            message = "Templating..."
            # text_widget.insert(tk.END, message + "\n")
            i = finger.image_2_tz(fingerimg)
            if i == adafruit_fingerprint.OK:
                message = "Templated"
                # text_widget.insert(tk.END, message + "\n")
            else:
                if i == adafruit_fingerprint.IMAGEMESS:
                    message = "Image too messy"
                    # text_widget.insert(tk.END, message + "\n")
                elif i == adafruit_fingerprint.FEATUREFAIL:
                    message = "Could not identify features"
                    # text_widget.insert(tk.END, message + "\n")
                elif i == adafruit_fingerprint.INVALIDIMAGE:
                    message = "Image invalid"
                    # text_widget.insert(tk.END, message + "\n")
                else:
                    message = "Other error"
                    # text_widget.insert(tk.END, message + "\n")
                return False

        message = "Creating model..."
        # text_widget.insert(tk.END, message + "\n")
        i = finger.create_model()
        if i == adafruit_fingerprint.OK:
            message = "Created"
            # text_widget.insert(tk.END, message + "\n")
        else:
            if i == adafruit_fingerprint.ENROLLMISMATCH:
                message = "Prints did not match"
                # text_widget.insert(tk.END, message + "\n")
            else:
                message = "Other error"
                # text_widget.insert(tk.END, message + "\n")
            return False

        if finger.create_model() != adafruit_fingerprint.OK:
            message = "Failed to create fingerprint model"
            # text_widget.insert(tk.END, message + "\n")
            return False

        model_number = len(fingerprints)+2
        fingerprints[user_input] = model_number
        save_fingerprints()

        message = f"\n\n\n\n\n\n\n\n\n\t\t\tStoring model for {user_input} as #{model_number}...\n"
        text_widget.insert(tk.END, message + "\n")
        i = finger.store_model(model_number)
        if i == adafruit_fingerprint.OK:
            message = "\t\t\tStored"
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


def check_finger():
    global n
    global stop_flag
    while not stop_flag:
        if check():
            text_widget.delete("1.0", tk.END)  # Clear the text widget
            fingerprint_name = next(
                (k for k, v in fingerprints.items() if v == finger.finger_id), None)
            if fingerprint_name:
                text_widget.delete(tk.END)
                output_text = f"\n\n\n\n\n\n\n\n\n\n\t\t\t\tDetected Name:   {fingerprint_name}\n"
                """print(output_text)"""
                text_widget.insert(tk.END, output_text)
                if fingerprint_name in attendance:
                    print("You attendance recorded!")
                else:
                    attendance.add(fingerprint_name)
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
                """print(output_text)"""
                text_widget.insert(tk.END, output_text)
        else:
            # text_widget.delete("1.0", tk.END)
            output_text = f"\n\n\n\n\n\n\n\n\n\n\t\t\t\tDetected Name:   \n"
            """print(output_text)"""
            # text_widget.insert(tk.END, output_text)


def verify():
    global n
    text_widget.delete("1.0", tk.END)  # Clear the text widget
    if Verify_finger():
        fingerprint_name = next(
            (k for k, v in fingerprints.items() if v == finger.finger_id), None)
        if fingerprint_name:
            output_text = f"\n\n\n\n\n\n\n\n\n\n\t\t\t\tDetected:   {fingerprint_name}\n"
            """print(output_text)"""
            text_widget.insert(tk.END, output_text)
            if fingerprint_name in attendance:
                print("Your attendance has already been recorded!")
                print(attendance)
            else:
                attendance.add(fingerprint_name)
                # Write to the CSV file
                current_time = datetime.now().strftime("%H:%M:%S")
                with open(file_path, "a", newline="") as f:
                    lnwriter = csv.writer(f)
                    lnwriter.writerow([n, fingerprint_name, current_time])
                n += 1
        else:
            output_text = "Unknown fingerprint\n"
            """print(output_text)"""
            text_widget.insert(tk.END, output_text)
    else:
        output_text = "Finger not found\n"
        """print(output_text)"""
        text_widget.insert(tk.END, output_text)


def delete_finger():
    get_name()
    text_widget.delete("1.0", tk.END)
    if user_input in fingerprints:
        if finger.delete_model(fingerprints[user_input]) == adafruit_fingerprint.OK:
            del fingerprints[user_input]
            save_fingerprints()
            output_text = f"\n\n\n\n\n\n\n\n\n\n\t\t\t\t{user_input} is  Deleted!\n"
            text_widget.insert(tk.END, output_text)
        else:
            output_text = "Failed to delete\n"
            text_widget.insert(tk.END, output_text)
    else:
        output_text = "\n\n\n\n\n\n\n\n\n\n\t\t\t\tFingerprint not found\n"
        text_widget.insert(tk.END, output_text)


def email(gmail):
    f.close()
    text_widget.delete("1.0", tk.END)
    subject = 'Finger Record'
    body = 'Please find the attached CSV file.'
    send_email(subject, gmail, body, file_path)
    output_text = f"\n\n\n\n\n\n\n\n\n\n\t\tEmail is successfully sent to {gmail}\n"
    text_widget.insert(tk.END, output_text)


def send():
    get_name()
    email(user_input)


def default():
    mail = 'waiyanminmiit@gmail.com'
    text_widget.delete("1.0", tk.END)
    output_text = "\n\n\n\n\n\n\n\n\n\n\t\tSending Email ....."
    text_widget.insert(tk.END, output_text)
    text_widget.update_idletasks()  # Force GUI update
    email(mail)


def home():
    clear()
    stop()
    display_frame.pack_forget()
    miit_label.pack(padx=30, pady=50)
    text.pack()


def delete():
    text_widget.delete("1.0", tk.END)
    output_text = "\n\n\n\n\n\n\n\n\n\n\t\tAre you admin?  Verify with your fingerprint ..."
    text_widget.insert(tk.END, output_text)
    text_widget.update_idletasks()  # Force GUI update

    if Verify_finger():
        fingerprint_name = next(
            (k for k, v in fingerprints.items() if v == finger.finger_id), None)
        if fingerprint_name == "Wai Yan Min":
            delete_finger()
        else:
            text_widget.delete("1.0", tk.END)
            output_text = "\n\n\n\n\n\n\n\n\n\n\t\tYou're not admin. You can't delete data."
            text_widget.insert(tk.END, output_text)
    else:
        text_widget.delete("1.0", tk.END)
        output_text = "\n\n\n\n\n\n\n\n\n\n\t\tYou're not admin. You can't delete data."
        text_widget.insert(tk.END, output_text)


def secure():
    text_widget.delete("1.0", tk.END)
    output_text = "\n\n\n\n\n\n\n\n\n\n\t\tAre you admin?  Verify with your fingerprint ..."
    text_widget.insert(tk.END, output_text)
    text_widget.update_idletasks()  # Force GUI update

    if Verify_finger():
        fingerprint_name = next(
            (k for k, v in fingerprints.items() if v == finger.finger_id), None)
        if fingerprint_name == "Wai Yan Min":
            text_widget.delete("1.0", tk.END)
            output_text = "\n\n\n\n\n\n\n\n\n\n\t\tSending Email ....."
            text_widget.insert(tk.END, output_text)
            text_widget.update_idletasks()  # Force GUI update
            send()  # Call the send() function to send the email
        else:
            text_widget.delete("1.0", tk.END)
            output_text = "\n\n\n\n\n\n\n\n\n\n\t\tYou're not admin. You can only send default."
            text_widget.insert(tk.END, output_text)


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
                font=("Helvetica", 20),
                padding=10,
                width=15,  # Set the width of the buttons
                height=2)  # Set the height of the buttons

# Change button color
style.map("TButton",
          foreground=[('pressed', 'white'), ('active', '#01001F')],
          background=[('pressed', '!disabled', 'dark blue'), ('active', 'dark blue')])

# Change window background color
window.configure(background="#030335")

# Create the main frame
left_frame = tk.Frame(window, bg="#030335")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the display frame in the main frame
display_frame = ttk.Label(left_frame, text="", font=(
    "Helvetica", 20), background="#030335", foreground="#2196F3")
display_frame.pack(padx=30, pady=20)

frame = tk.Frame(left_frame)
font_style = font.Font(size=25)  # Adjust the font size as per your requirement
entry = tk.Entry(frame, width=20, font=font_style)

# MIIt logo
# Replace with the actual path to your image
miit = Image.open(
    "D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\fingerprint_authentication_system\\icon\\miit_logo.png")
miit = miit.resize((150, 150))  # Resize the image as needed
miit = miit.convert("RGBA")  # Convert to RGBA mode to support transparency
miit_with_alpha = ImageTk.PhotoImage(miit)

miit_label = tk.Label(left_frame, image=miit_with_alpha, bg="#030335")
miit_label.pack(padx=30, pady=30)

text = tk.Label(left_frame, text="Fingerprint Authentication System", font=(
    "Helvetica", 30), background="#030335", fg="white")
text.pack()

# Create a text widget and buttons for displaying the output
text_widget = tk.Text(left_frame, font=("Helvetica", 14),
                      wrap=tk.WORD, background="#030335", fg="white")
# Create buttons with custom style
start_button = ttk.Button(left_frame, text="Start",
                          command=start, style="TButton", width=8)
stop_button = ttk.Button(left_frame, text="Stop",
                         command=stop, style="TButton", width=8)
verify_button = ttk.Button(left_frame, text="Check",
                           command=verify, style="TButton", width=8)
confirm_button = ttk.Button(
    left_frame, text="Confirm", command=register, style="TButton", width=8)
delete_button = ttk.Button(left_frame, text="Delete",
                           command=delete, style="TButton", width=8)
default_button = ttk.Button(
    left_frame, text="Default", command=default, style="TButton", width=8)
send_button = ttk.Button(left_frame, text="Send",
                         command=secure, style="TButton", width=8)
# Create the right frame
right_frame = tk.Frame(window, bg="#030335")
right_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

# Create buttons
button_frame = tk.Frame(right_frame, bg="#030335")
button_frame.grid(row=1, column=0, padx=10, pady=10)

# Fingerprint Icon
# Convert image to GIF format with transparency
# Replace with the actual path to your image
image = Image.open(
    "D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\fingerprint_authentication_system\\icon\\fingerprint_icon.png")
image = image.resize((150, 150))  # Resize the image as needed
image = image.convert("RGBA")  # Convert to RGBA mode to support transparency
image_with_alpha = ImageTk.PhotoImage(image)

# Create a transparent label for the image
# Create a transparent label for the image
image_label = tk.Label(button_frame, image=image_with_alpha, bg="#030335")
image_label.grid(row=0, column=0, pady=25)
image_label.bind("<Button-1>", lambda event: home())

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

csv_button = ttk.Button(button_frame, text="Display CSV",
                        command=click_csv_button)
csv_button.grid(row=5, column=0, pady=12)

send_email_button = ttk.Button(
    button_frame, text="Send Email", command=click_email_button)
send_email_button.grid(row=6, column=0, pady=12)

# Create a label for copyright information
copyright_label = tk.Label(button_frame,
                           text="Developed by Wai Yan Min   Copyright © 2023 MIIT. All rights reserved.",
                           font=("Helvetica", 10), fg="white", bg="#030335")
copyright_label.grid(row=7, column=0, pady=12)

"""# Create a scrollbar for the display frame
scrollbar = ttk.Scrollbar(left_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#scrollbar.configure(command=text_widget.yview)"""

window.mainloop()
