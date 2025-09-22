#!/usr/bin/env python3
import requests
import time
import os
import random
import signal
import sys
from shutil import which

# ---------------- Configuration ----------------
TOR_PROXY = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

MESSAGES = {
    'welcome': "=== Automatic Tor IP Changer ===",
    'interval_prompt': "Enter time interval in seconds (e.g. 30): ",
    'count_prompt': "Enter how many times to change IP (0 = infinite): ",
    'invalid_number': "Invalid number entered.",
    'infinite_mode': "Starting infinite mode. Press Ctrl+C to stop.",
    'changing_ip': "[+] Reloading Tor service...",
    'ip_output': "New IP address: ",
    'error': "Failed to get IP: "
}

#ASCII ART
ASCII_BANNER = r"""
                                              
@@@  @@@   @@@@@@              @@@  @@@@@@@   
@@@@ @@@  @@@@@@@@             @@@  @@@@@@@@  
@@!@!@@@  @@!  @@@             @@!  @@!  @@@  
!@!!@!@!  !@!  @!@             !@!  !@!  @!@  
@!@ !!@!  @!@  !@!  @!@!@!@!@  !!@  @!@@!@!   
!@!  !!!  !@!  !!!  !!!@!@!!!  !!!  !!@!!!    
!!:  !!!  !!:  !!!             !!:  !!:       
:!:  !:!  :!:  !:!             :!:  :!:       
::   ::  ::::: ::              ::   ::       
::    :    : :  :              :     :        
                                             
"""

# ---------------- Utility functions ----------------
def colorize(text, color_code="\033[92m"):
    return f"{color_code}{text}\033[0m"

def is_systemctl_available():
    return which("systemctl") is not None

def manage_tor(action):
    """
    action: 'start', 'stop', 'reload', 'status'
    Returns (returncode, stdout+stderr) as tuple from os.popen read.
    """
    if not is_systemctl_available():
        # Fallback to 'service' command if systemctl is missing
        cmd = f"sudo service tor {action}"
    else:
        if action == 'status':
            cmd = "systemctl is-active --quiet tor"
            # for status we want return code only
            return os.system(cmd) == 0
        cmd = f"sudo systemctl {action} tor"
    return os.system(cmd)

def get_ip():
    """Fetch current IP through Tor proxy."""
    try:
        response = requests.get("https://checkip.amazonaws.com", proxies=TOR_PROXY, timeout=10)
        return response.text.strip()
    except Exception as e:
        return f"{MESSAGES['error']} {e}"

def reload_tor():
    print(MESSAGES['changing_ip'])
    # try systemctl reload; if fails, try restart; finally sleep to allow new circuit
    rc = manage_tor('reload')
    # if reload returned non-zero (os.system returns exit code), try restart
    if rc != 0:
        manage_tor('restart')
    # give Tor time to build new circuits
    time.sleep(5)

def print_banner():
    os.system("clear")
    print(ASCII_BANNER)

# ---------------- Cleanup & Signal Handling ----------------
def cleanup_and_exit(signum=None, frame=None):
    """Stop Tor service and exit cleanly."""
    try:
        print("\n[!] Caught exit signal — stopping Tor and exiting...")
        # Attempt to stop Tor unconditionally (per user request).
        manage_tor('stop')
        time.sleep(1)
    except Exception:
        pass
    finally:
        sys.exit(0)

# register SIGINT and SIGTERM
signal.signal(signal.SIGINT, cleanup_and_exit)
signal.signal(signal.SIGTERM, cleanup_and_exit)

# ---------------- Main ----------------
def main():
    print_banner()
    print(MESSAGES['welcome'])

    # Auto-start Tor
    print("[*] Ensuring Tor service is running...")
    # If systemctl exists, check active; else assume service command will start it
    if is_systemctl_available():
        # If 'systemctl is-active --quiet tor' returns non-zero, start tor
        status_ok = manage_tor('status')
        if not status_ok:
            print("[*] Tor is not active — starting Tor (requires sudo)...")
            manage_tor('start')
            # wait for Tor to initialize
            time.sleep(4)
        else:
            print("[*] Tor appears to be active.")
    else:
        # Try to start with service command (best effort)
        print("[*] systemctl not found — trying 'service tor start' (requires sudo)...")
        manage_tor('start')
        time.sleep(4)

    try:
        interval = int(input(MESSAGES['interval_prompt']))
        count = int(input(MESSAGES['count_prompt']))
    except ValueError:
        print(MESSAGES['invalid_number'])
        # Stop Tor before exit (user wanted Tor closed on Ctrl+C; be consistent)
        manage_tor('stop')
        return

    try:
        if count == 0:
            print(MESSAGES['infinite_mode'])
            while True:
                reload_tor()
                print(MESSAGES['ip_output'], colorize(get_ip()))
                # randomized sleep around the interval, minimum 5 seconds
                sleep_time = random.randint(max(5, interval - 5), interval + 5)
                time.sleep(sleep_time)
        else:
            for i in range(count):
                reload_tor()
                new_ip = get_ip()
                print(f"[{i+1}/{count}] {MESSAGES['ip_output']}{colorize(new_ip)}")
                time.sleep(interval)
    except SystemExit:
        # cleanup handled in signal handler
        pass
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        # On normal completion stop Tor (per your request to close Tor on Ctrl+C/exit)
        print("[*] Task finished or interrupted — stopping Tor (requires sudo)...")
        manage_tor('stop')

if __name__ == "__main__":
    main()
