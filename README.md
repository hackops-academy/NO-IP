# NO-IP — Automatic Tor IP Changer


---

## 📖 Overview
**NO-IP** is a lightweight, professional tool designed to automatically change your IP address using the TOR network.  
It ensures anonymity, privacy, and security while browsing or testing network environments.  

With built-in automation, **NO-IP** handles the process of starting/stopping TOR and refreshing your IP seamlessly — giving you full control with zero hassle.  

---

## ✨ Features
- 🚀 **Auto-start TOR** – No need to start TOR manually, NO-IP does it for you.  
- 🔄 **Automatic IP Rotation** – Changes IP on demand or at intervals.  
- 🛑 **Graceful Exit** – Press `CTRL + C` to stop the tool and cleanly shut down TOR.  
- 🧩 **SOCKS5 Proxy Ready** – Default proxy: `socks5h://127.0.0.1:9050`.  
- 🛡️ **Cross-platform Support** – Works on Linux, macOS, and Termux.  

---

## ⚙️ Requirements
- Python 3.7+  
- TOR installed and accessible in `$PATH`  

> On Debian/Ubuntu:  
```bash
sudo apt update && sudo apt install tor -y
```
> On Termux:
```bash
pkg update && pkg install tor -y
```

## 📥 Installation
Clone the repository and navigate into the directory:
```bash
git clone https://github.com/yourusername/NO-IP.git
cd NO-IP
```
Make the script executable:
```bash
chmod +x noip.py
```

## ▶️ Usage
Run the tool:
```bash
python3 noip.py
```
## Stoping the Tool
Stop the tool anytime with:
```bash
CTRL + C
```
## 🧑‍💻 Author
HackOps Academy
Building tools for security research and ethical hacking.

```bash
STAY LEGAL.
```


































