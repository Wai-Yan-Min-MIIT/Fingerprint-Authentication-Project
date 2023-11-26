"""import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

def click_display_button():
    display_frame.configure(text="Display CSV")
    display_csv()

def click_register_button():
    display_frame.configure(text="Register Finger")
    # Add the logic to display the output of the "Register Finger" button in the left frame

def click_verify_button():
    display_frame.configure(text="Verify Finger")
    # Add the logic to display the output of the "Verify Finger" button in the left frame

def click_attendance_button():
    display_frame.configure(text="Attendance")
    # Add the logic to display the output of the "Attendance" button in the left frame

def click_delete_button():
    display_frame.configure(text="Delete Finger")
    # Add the logic to display the output of the "Delete Finger" button in the left frame

def fingerprint_clicked(event):
    display_frame.configure(text="Main Frame (Blank)")
    # Add the logic to display the main frame (blank) in the left frame when the fingerprint image is clicked

def display_csv():
    file_path = "D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\finger_record_sheets\\test.csv"  # Replace with the actual path to your CSV file
    df = pd.read_csv(file_path)  # Read the CSV file using pandas
    text_widget.delete("1.0", tk.END)  # Clear the text widget
    text_widget.insert(tk.END, df.to_string())

window = tk.Tk()
window.state('zoomed')  # Set the window state to 'zoomed' (full screen)
window.title("Fingerprint Authentication System")

# Add custom style and theme
style = ttk.Style()
style.theme_use("clam")  # Choose a theme (e.g., 'clam', 'winnative', 'default')

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
main_frame = tk.Frame(window, bg="white")
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the right frame
right_frame = tk.Frame(window, bg="#030335")
right_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

# Convert image to GIF format with transparency
image = Image.open("D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\fingerprint.png")  # Replace with the actual path to your image
image = image.resize((150, 150))  # Resize the image as needed
image = image.convert("RGBA")  # Convert to RGBA mode to support transparency
image_with_alpha = ImageTk.PhotoImage(image)

# Create buttons
button_frame = tk.Frame(right_frame, bg="#030335")
button_frame.grid(row=1, column=0, padx=10, pady=10)

# Create a transparent label for the image
image_label = tk.Label(button_frame, image=image_with_alpha, bg="#030335")
image_label.grid(row=0, column=0, pady=25)
image_label.bind("<Button-1>", lambda event: fingerprint_clicked())  # Bind the left mouse button click event to the function

button1 = ttk.Button(button_frame, text="Register Finger", command=click_register_button)
button1.grid(row=1, column=0, pady=12)

button2 = ttk.Button(button_frame, text="Verify Finger", command=click_verify_button)
button2.grid(row=2, column=0, pady=12)

button3 = ttk.Button(button_frame, text="Attendance", command=click_attendance_button)
button3.grid(row=3, column=0, pady=12)

button4 = ttk.Button(button_frame, text="Delete Finger", command=click_delete_button)
button4.grid(row=4, column=0, pady=12)

display_button = ttk.Button(button_frame, text="Display CSV", command=click_display_button)
display_button.grid(row=5, column=0, pady=12)

# Create the display frame in the main frame
display_frame = ttk.Label(main_frame, text="Main Frame (Blank)", font=("Helvetica", 16), background="white")
display_frame.pack(padx=10, pady=10)

# Create a scrollbar for the display frame
scrollbar = ttk.Scrollbar(main_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a text widget for displaying the output
text_widget = tk.Text(main_frame, font=("Courier", 12), wrap=tk.WORD, yscrollcommand=scrollbar.set)
text_widget.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

scrollbar.configure(command=text_widget.yview)

# Create a label for copyright information
copyright_label = tk.Label(button_frame,
                           text="Developed by Wai Yan Min   Copyright © 2023 MIIT. All rights reserved.",
                           font=("Helvetica", 10), fg="white", bg="#030335")
copyright_label.grid(row=6, column=0, pady=12)

window.mainloop()
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

text_widget = None
table_frame = None

def click_display_button():
    global text_widget, table_frame
    if text_widget:
        text_widget.destroy()  # Remove the previous text widget if it exists
    text_widget = tk.Text(table_frame, font=("Courier", 12))
    text_widget.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
    display_csv()

def display_csv():
    file_path = "D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\finger_record_sheets\\test.csv"  # Replace with the actual path to your CSV file
    df = pd.read_csv(file_path)  # Read the CSV file using pandas
    text_widget.delete("1.0", tk.END)  # Clear the text widget
    text_widget.insert(tk.END, df.to_string())

def fingerprint_clicked(event):
    global table_frame
    if table_frame:
        table_frame.destroy()  # Remove the table frame if it exists
    table_frame = tk.Frame(main_frame, bg="#030335")
    table_frame.pack(fill=tk.BOTH, expand=True)
    main_frame.configure(background="#030335")  # Set the background color of the main frame to "#030335"

def quit_program():
    window.destroy()

window = tk.Tk()
window.state('zoomed')  # Set the window state to 'zoomed' (full screen)
window.title("Fingerprint Authentication System")

# Add custom style and theme
style = ttk.Style()
style.theme_use("clam")  # Choose a theme (e.g., 'clam', 'winnative', 'default')

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

# Convert image to GIF format with transparency
image = Image.open("D:\\Wai_yan_folder\\programming\\fingerprint_recognition\\fingerprint.png")  # Replace with the actual path to your image
image = image.resize((150, 150))  # Resize the image as needed
image = image.convert("RGBA")  # Convert to RGBA mode to support transparency
image_with_alpha = ImageTk.PhotoImage(image)

# Create buttons
button_frame = tk.Frame(window, bg="#030335")
button_frame.pack(side=tk.RIGHT, padx=10)

# Create a transparent label for the image
image_label = tk.Label(button_frame, image=image_with_alpha, bg="#030335")
image_label.grid(row=0, column=1, pady=25)
image_label.bind("<Button-1>", fingerprint_clicked)  # Bind the left mouse button click event to the function

button1 = ttk.Button(button_frame, text="Register Finger")
button1.grid(row=1, column=1, pady=12)

button2 = ttk.Button(button_frame, text="Verify Finger")
button2.grid(row=2, column=1, pady=12)

button3 = ttk.Button(button_frame, text="Attendance")
button3.grid(row=3, column=1, pady=12)

button4 = ttk.Button(button_frame, text="Delete finger")
button4.grid(row=4, column=1, pady=12)

display_button = ttk.Button(button_frame, text="Display CSV", command=click_display_button)
display_button.grid(row=5, column=1, pady=12)

# Create a label for copyright information
copyright_label = tk.Label(button_frame, text="Developed by Wai Yan Min   Copyright © 2023 MIIT. All rights reserved.", font=("Helvetica", 10), fg="white", bg="#030335")
copyright_label.grid(row=6, column=1, pady=12)

# Create the main frame
main_frame = tk.Frame(window, bg="#030335")
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

window.mainloop()
