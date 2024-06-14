import serial
import threading
import tkinter as tk
from tkinter import ttk
from serial.tools import list_ports
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import subprocess
import cv2

# Spotify Credentials
SPOTIPY_CLIENT_ID = '1e37564d1d0#############'
SPOTIPY_CLIENT_SECRET = 'b7e02bfd54ae#################'
SPOTIPY_REDIRECT_URI = 'http://localhost:3333/callback' ## 'http://localhost:8888/callback' ## https://developer.spotify.com/dashboard

# Set up Spotify authorization
sp = Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                       client_secret=SPOTIPY_CLIENT_SECRET,
                                       redirect_uri=SPOTIPY_REDIRECT_URI,
                                       scope="user-read-playback-state,user-modify-playback-state"))

# Define functions to be executed
def launch_calculator():
    try:
        subprocess.Popen('calc.exe')
    except FileNotFoundError:
        print("Calculator not found")

def launch_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam not found")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def launch_google_chrome():

        webbrowser.open('https://www.youtube.com/')

def open_google():
    webbrowser.open('http://www.google.com')

def open_notepad():
    try:
        subprocess.Popen('notepad.exe')
    except FileNotFoundError:
        print("Notepad not found")

def open_paint():
    try:
        subprocess.Popen('mspaint.exe')
    except FileNotFoundError:
        print("Paint not found")

def open_messenger():
    try:
        subprocess.Popen(r"C:\Users\eeean\AppData\Local\Programs\Messenger\Messenger.exe") 
    except FileNotFoundError:
        print("Messenger not found")

def open_email():
    webbrowser.open('https://outlook.office365.com/mail/')

# Spotify control functions
def spotify_play():
    try:
        sp.start_playback()
    except Exception as e:
        print(f"Error starting playback: {e}")

def spotify_pause():
    try:
        sp.pause_playback()
    except Exception as e:
        print(f"Error pausing playback: {e}")

def spotify_next():
    try:
        sp.next_track()
    except Exception as e:
        print(f"Error skipping to next track: {e}")

def spotify_previous():
    try:
        sp.previous_track()
    except Exception as e:
        print(f"Error skipping to previous track: {e}")

# Function dictionaries
functions = {
    "Calculator": launch_calculator,
    "Webcam": launch_webcam,
    "Youtube": launch_google_chrome,
    "Google": open_google,
    "Notepad": open_notepad,
    "Paint": open_paint,
    "Messenger": open_messenger,
    "Email": open_email,
    "Spotify Play": spotify_play,
    "Spotify Pause": spotify_pause,
    "Spotify Next": spotify_next,
    "Spotify Previous": spotify_previous
}

# Function to handle Arduino input
def handle_serial_input():
    global ser
    while True:
        if 'ser' in globals() and ser and ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line == "BUTTON1_PRESSED":
                selected_func1 = dropdown_var1.get()
                if selected_func1 in functions:
                    functions[selected_func1]()
            elif line == "BUTTON2_PRESSED":
                selected_func2 = dropdown_var2.get()
                if selected_func2 in functions:
                    functions[selected_func2]()
            elif line == "BUTTON3_PRESSED":
                selected_func3 = dropdown_var3.get()
                if selected_func3 in functions:
                    functions[selected_func3]()

# Function to list available COM ports
def list_serial_ports():
    ports = list_ports.comports()
    port_list = [port.device for port in ports]
    return port_list

# Create the main window
root = tk.Tk()
root.title("Launchpad")

# Create dropdown variables
dropdown_var1 = tk.StringVar(root)
dropdown_var2 = tk.StringVar(root)
dropdown_var3 = tk.StringVar(root)

# Set default values
dropdown_var1.set("Calculator")
dropdown_var2.set("Webcam")
dropdown_var3.set("Notepad")

# Create dropdown menus
options = ["Calculator", "Webcam", "Youtube", "Google", "Notepad", "Paint", "Messenger", "Email", "Spotify Play", "Spotify Pause", "Spotify Next", "Spotify Previous"]

dropdown_menu1 = ttk.Combobox(root, textvariable=dropdown_var1, values=options)
dropdown_menu2 = ttk.Combobox(root, textvariable=dropdown_var2, values=options)
dropdown_menu3 = ttk.Combobox(root, textvariable=dropdown_var3, values=options)

# Place dropdown menus on the window
dropdown_menu1.pack(pady=10)
dropdown_menu2.pack(pady=10)
dropdown_menu3.pack(pady=10)

# Function to update serial port dropdown with available ports
def update_serial_dropdown():
    port_list = list_serial_ports()
    serial_port_dropdown['values'] = port_list
    if port_list:
        serial_port_dropdown.current(0)  # Select the first port by default

# Create serial port dropdown
serial_port_label = tk.Label(root, text="Select Arduino Port:")
serial_port_label.pack(pady=5)
serial_port_dropdown = ttk.Combobox(root, values=[], state="readonly")
serial_port_dropdown.pack(pady=5)

# Update serial port dropdown initially
update_serial_dropdown()

# Set up serial communication based on selected port
def connect_to_serial():
    global ser
    port = serial_port_dropdown.get()
    try:
        ser = serial.Serial(port, 9600)
        connect_button.config(bg="green")
        print(f"Connected to Arduino on {port}")
    except serial.SerialException as e:
        connect_button.config(bg="red")
        print(f"Failed to connect to Arduino on {port}: {e}")

# Button to connect to selected serial port
connect_button = tk.Button(root, text="Connect", command=connect_to_serial)
connect_button.pack(pady=5)

# Button to refresh the list of available serial ports
refresh_button = tk.Button(root, text="Refresh Ports", command=update_serial_dropdown)
refresh_button.pack(pady=5)

# Start a thread to handle serial input
serial_thread = threading.Thread(target=handle_serial_input)
serial_thread.daemon = True
serial_thread.start()

# Run the application
root.mainloop()
