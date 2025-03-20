# 🔄 SyncX-Server - Remote 🖥️ Control & Monitoring

## 🌍 Overview
SyncX is a remote 🖥️ control & monitoring app that lets users do various actions using a Flask-SocketIO server. It supports:

- 📸 Real-time screen capture
- 🖱️ Remote mouse control
- ⌨️ Remote keyboard input
- 📋 Clipboard access
- 📊 System resource monitoring (💾 CPU, 🔋 memory, 💽 disk, 🔌 battery)
- ⚡ System power control (📴 shutdown, 🔄 restart)
- 🔒 Authentication-based access
- 🔔 Desktop notifications for connection events

## 🚀 Features
- **🖥️ Screen Sharing**: Captures & streams screen images in real-time.
- **🖱️ Mouse Control**: Move, click & double-click remotely.
- **⌨️ Keyboard Input**: Type text & send ⌫ backspace events.
- **📋 Clipboard Access**: Copy & retrieve clipboard content.
- **📊 System Monitoring**: Get 💾 CPU, 🔋 memory, 💽 disk & 🔌 battery stats.
- **⚡ System Control**: 📴 Shutdown or 🔄 restart remotely.
- **🔒 User Authentication**: Secure with a 🔑 password.
- **🔔 Desktop Notifications**: Get 🔔 alerts for connection, disconnection & errors.
- **🖼️ GUI Interface**: Tkinter-based server 🏠 window showing IP & password settings.

## 🛠️ Technologies Used
- **🐍 Python**
  - 🏗️ Flask-SocketIO
  - 🎨 Tkinter
  - 🖱️ PyAutoGUI
  - 📸 OpenCV
  - 🔢 NumPy
  - 📊 Psutil
  - 📋 Pyperclip
  - 🔔 Plyer
- **🌐 Flask & SocketIO**
  - Handles 🔗 WebSocket connections for real-time 📡 communication.
- **🖼️ PIL (Pillow)**
  - Used for 📸 screen capturing.
- **📸 OpenCV & 🔢 NumPy**
  - Image 🖼️ processing for efficient screen 📡 streaming.

## 🏗️ Installation & Setup
### 📋 Prerequisites
Ensure 🐍 Python 3 is installed.

### ⚙️ Setting Up
1. 📥 Clone the repo:
```sh
git clone https://github.com/DevzYash/SyncX-Server.git
```
2. 📦 Install dependencies using the `requirements.txt` file:
```sh
pip install -r requirements.txt
```
3. ▶️ Run the server:
```sh
python syncx.py
```
The server will launch with a 🏠 GUI showing local 🌐 IP & 🔑 password options.

## 🔄 Converting to EXE
To convert this script into an executable, use **Nuitka**:
```sh
nuitka --standalone --onefile --enable-plugin=tk-inter --include-package=flask --include-package=flask_socketio --include-package=pyautogui --include-package=psutil --include-package=pyperclip --include-package=plyer --include-package=cv2 --include-package=PIL --include-package=numpy --windows-console-mode=disable syncX-server.py
```
This will create a standalone `.exe` file.

## 🔗 WebSocket Events
### 📤 Client-to-Server Events
| 📡 Event | 📝 Description |
|------------|--------------|
| `auth` | 🔒 Authenticate with a 🔑 password |
| `start_screen_capture` | 📸 Start real-time screen sharing |
| `stop_screen_capture` | 🛑 Stop screen sharing |
| `mouseEvent` | 🖱️ Move mouse via coordinates |
| `mouseAction` | 🖱️ Click or double-click |
| `write` | ⌨️ Type text remotely |
| `backspace` | ⌫ Simulate backspace |
| `copy` | 📋 Retrieve clipboard content |
| `restart` | 🔄 Restart system |
| `shutdown` | 📴 Shutdown system |

### 📥 Server-to-Client Events
| 📡 Event | 📝 Description |
|------------|--------------|
| `screen_capture` | 📸 Sends base64 screen image |
| `resource_usage` | 📊 CPU, 💽 memory & disk usage |
| `battery_level` | 🔋 Battery % |
| `auth_success` | ✅ Authentication success |
| `auth_failure` | ❌ Authentication failed |

## 📲 Client Side
The client side is developed in **Flutter**. You can check the repository here:
🔗 [SyncX Client (Flutter)](https://github.com/DevzYash/syncx)

## 🔒 Security Considerations
- Requires 🔑 authentication before actions.
- Password must be set manually in 🏠 GUI before connection.
- Runs in `production` mode for 🛡️ security & 🔄 stability.

## 📸 Screenshots
![image](https://github.com/user-attachments/assets/f82a4e5c-3e09-463f-9b57-5c68fbe531ac)

## 🔮 Future Improvements
- 🔐 Implement encrypted 🔗 communication.
- 👤 Add user role-based access control.
- 🌍 Introduce a web 🏠 dashboard for easy control.

## 📜 License
📂 Open-source under the 📝 MIT License.

## 👤 Author
Developed by **Yash Agarwal**. 🤝 Contributions & 💬 collaborations welcome!

