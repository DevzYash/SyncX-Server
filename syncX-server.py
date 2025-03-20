import tkinter as tk
from flask import Flask
from flask_socketio import SocketIO, emit
import logging
import pyautogui
import psutil
import threading
import queue
import cv2
import numpy as np
from PIL import ImageGrab
import io
import base64
import os
import sys
import socket
import pyperclip
from plyer import notification
from threading import Thread

app = Flask(__name__)
app.config['DEBUG'] = False
os.environ['FLASK_ENV'] = 'production'
socketio = SocketIO(app, async_mode='threading', logging=False, engineio_logger=False)
pyautogui.FAILSAFE = False 

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

resource_queue = queue.Queue()
battery_queue = queue.Queue()
screen_capture_running = False
screen_capture_thread = None

def capture_screen():
    global screen_capture_running
    while screen_capture_running:
        img = ImageGrab.grab()
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        _, buffer = cv2.imencode('.jpg', frame)
        img_str = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('screen_capture', {'image': img_str}, namespace='/')
        threading.Event().wait(1)  # Update every second

@socketio.on('start_screen_capture')
def handle_start_screen_capture():
    global screen_capture_running, screen_capture_thread
    if not screen_capture_running:
        screen_capture_running = True
        screen_capture_thread = threading.Thread(target=capture_screen)
        screen_capture_thread.start()
        emit('screen_capture_started', {'message': 'Screen capture started'})

@socketio.on('stop_screen_capture')
def handle_stop_screen_capture():
    global screen_capture_running
    if screen_capture_running:
        screen_capture_running = False
        emit('screen_capture_stopped', {'message': 'Screen capture stopped'})

def monitor_resources():
    while True:
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        resource_queue.put({'cpu': cpu_usage, 'memory': memory_usage, 'disk': disk_usage})
        threading.Event().wait(1)  # Update every second

def emit_resources():
    while True:
        try:
            resources = resource_queue.get(timeout=1)
            socketio.emit('resource_usage', resources, namespace='/')
        except queue.Empty:
            pass

def monitor_battery():
    while True:
        battery_percent = psutil.sensors_battery().percent if psutil.sensors_battery() else None
        battery_queue.put({'battery': battery_percent})
        threading.Event().wait(20)  # Update every minute

def emit_battery():
    while True:
        try:
            battery = battery_queue.get(timeout=60)
            socketio.emit('battery_level', battery, namespace='/')
        except queue.Empty:
            pass

@socketio.on('connect')
def handle_connect():
    notification.notify(
        title="Connection",
        message="Connection established",
        app_name="SyncX",
        timeout=3  # Notification will stay for 10 seconds
    )
    print('Client connected')

    
@socketio.on('disconnect')
def handle_disconnect(reason):
    try:
        print('Client disconnected')
        notification.notify(
        title="Connection",
        message="Client disconnected",
        app_name="SyncX",
        timeout=10  # Notification will stay for 10 seconds
    )
    except Exception as e:
        print(f"Error during disconnection: {e}")

@socketio.on('auth')
def handle_auth(data):
    global password
    # logging.info(f"User authenticated with data: {data}")
    try:
        if data['password'] == password:
            print('User authenticated successfully')
            emit('auth_success', {'message': 'Authenticated successfully'})
            logging.info('User authenticated successfully')
            notification.notify(
                title="Connection",
                message="Client connected successfully",
                app_name="SyncX",
                timeout=10  
            )
            threading.Thread(target=monitor_resources).start()
            threading.Thread(target=emit_resources).start()
            threading.Thread(target=monitor_battery).start()
            threading.Thread(target=emit_battery).start()
        else:
            emit('auth_failure', {'message': 'Authentication failed'})
            logging.info('User authentication failed')
    except Exception as e:
        logging.error(f"Error during authentication: {e}")

@socketio.on('mouseEvent')
def handle_mouse_event(data):
    # logging.info(f"Mouse event: {data}")
    try:
        if data['event'] == 'move':
            dx = data['dx']
            dy = data['dy']
            current_position = pyautogui.position()
            # logging.info(f"Moving mouse to ({current_position[0] + dx}, {current_position[1] + dy})")
            pyautogui.moveTo(current_position[0] + dx, current_position[1] + dy, _pause=False)
    except Exception as e:
        logging.error(f"Error handling mouse event: {e}")

@socketio.on('mouseAction')
def handle_mouse_action(data):
    # logging.info(f"Mouse action: {data}")
    try:
        if data['action'] == 'left_click':
            # logging.info('Simulating left click')
            pyautogui.click()
        elif data['action'] == 'right_click':
            # logging.info('Simulating right click')
            pyautogui.click(button='right')
        elif data['action'] == 'double_click':
            # logging.info('Simulating double click')
            pyautogui.doubleClick()
    except Exception as e:
        logging.error(f"Error handling mouse action: {e}")

@socketio.on('write')
def handle_write(data):
    # logging.info(f"Typing: {data}")
    try:
        pyautogui.typewrite(data['text'])
    except Exception as e:
        logging.error(f"Error handling typing: {e}")

@socketio.on('backspace')
def handle_backspace():
    # logging.info('Backspace pressed')
    try:
        pyautogui.press('backspace')
    except Exception as e:
        logging.error(f"Error handling backspace: {e}")

@socketio.on('copy')
def handle_copy():
    try:
        clipboard_text = pyperclip.paste()
        emit('clipboard_text', {'text': clipboard_text}, namespace='/')
    except Exception as e:
        logging.error(f"Error handling copy: {e}")

@socketio.on('restart')
def handle_restart():
    try:
        os.system('shutdown /r /t 1')
    except Exception as e:
        logging.error(f"Error handling restart: {e}")

@socketio.on('shutdown')
def handle_shutdown():
    try:
        os.system('shutdown /s /t 1')
    except Exception as e:
        logging.error(f"Error handling shutdown: {e}")

@socketio.on_error()
def error_handler(e):
    notification.notify(
        title="Connection",
        message="Error on server",
        app_name="SyncX",
        timeout=10  # Notification will stay for 10 seconds
    )
    logging.error(f"An error occurred: {e}")

def start_server():
    try:
        socketio.run(app, host='0.0.0.0', port=6969,debug=False)
        logging.info('Server started on port 6969')
        notification.notify(
        title="Connection",
        message="Server Started",
        app_name="SyncX",
        timeout=4  # Notification will stay for 10 seconds
    )
    except KeyboardInterrupt:
        logging.info("Server stopped manually.")
    except Exception as e:
        logging.error(f"Server error: {e}")


    global password, end_button
    root = tk.Tk()
    root.title("Sync X Server")
    root.geometry("600x250")  # Set window size
    root.resizable(False, False)  # Disable resizing
    # Get IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()

    # Display IP address
    ip_label = tk.Label(root, text=f"IP Address: {ip_address}", font=('Arial', 24, 'bold'))
    ip_label.pack(pady=(20, 10), padx=20)  # Add padding

    # Password field
    password_frame = tk.Frame(root)
    password_label = tk.Label(password_frame, text="Set Password:")
    password_label.pack(side='left')
    password_entry = tk.Entry(password_frame, show='*', width=20)
    password_entry.pack(side='left')
    password_button = tk.Button(password_frame, text="Set Password", command=lambda: set_password(password_entry))
    password_button.pack(side='left')
    password_frame.pack(pady=(0, 20), padx=20)  # Add padding

    # Start and End server buttons
    button_frame = tk.Frame(root)
    start_button = tk.Button(button_frame, text="Start Server", bg= 'green',fg='white', command=lambda: Thread(target=start_server).start())
    start_button.pack(side='left', padx=10)  # Add horizontal padding
    end_button = tk.Button(button_frame, text="End Server", bg='red', fg='white', command=lambda: os._exit(0))
    end_button.pack(side='left', fill='x', expand=True, padx=10)  # Add horizontal padding
    button_frame.pack(pady=(0, 20), padx=20)  # Add padding

    root.mainloop()
def create_gui():
    global password, end_button
    root = tk.Tk()
    root.title("Sync X Server")
    root.geometry("600x250")
    root.resizable(False, False)  
    root.config(bg='#f0f0f0') 

    image_icon = tk.PhotoImage(file = 'C:\\Users\\yasha\\Desktop\\Codes\\SyncX-Server\\SYNC.png') 
    root.iconphoto(False, image_icon,image_icon)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()

    ip_label = tk.Label(root, text=f"IP Address: {ip_address}", font=('Arial', 24, 'bold'), bg='#f0f0f0')
    ip_label.pack(pady=(20, 10), padx=20)  

    password_frame = tk.Frame(root, bg='#f0f0f0')
    password_label = tk.Label(password_frame, text="Set Password:", bg='#f0f0f0')
    password_label.pack(side='left')
    password_entry = tk.Entry(password_frame, show='*', width=20, font=('Arial', 12))
    password_entry.pack(side='left')
    password_button = tk.Button(password_frame, text="Set Password", command=lambda: set_password(password_entry), bg='#007bff', fg='white', font=('Arial', 10))
    password_button.pack(side='left')
    password_frame.pack(pady=(0, 20), padx=20)  

    button_frame = tk.Frame(root, bg='#f0f0f0')
    start_button = tk.Button(button_frame, text="Start Server", bg='#28a745', fg='white', command=lambda: Thread(target=start_server).start(), font=('Arial', 12))
    start_button.pack(side='left', padx=10)  
    end_button = tk.Button(button_frame, text="End Server", bg='#dc3545', fg='white', command=lambda: os._exit(0), font=('Arial', 12))
    end_button.pack(side='left', fill='x', expand=True, padx=10) 
    button_frame.pack(pady=(0, 20), padx=20)  

    root.mainloop()

def set_password(entry):
    global password
    password = entry.get()
    entry.config(state='disabled')

if __name__ == '__main__':
    create_gui()
    
