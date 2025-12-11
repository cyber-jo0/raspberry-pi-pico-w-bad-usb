raspberry Pi Pico W BadUSB – Advanced DuckyScript Executor

This project turns the Raspberry Pi Pico W into a fully-featured BadUSB device, capable of executing payloads written in Ducky Script 1.0, 2.0, and 3.0.
It provides high reliability, full keyboard-layout support, WiFi control, and greatly extended scripting capabilities compared to the classic USB Rubber Ducky.

✨ Key Features
✔ Full Ducky Script Support (1.0 → 3.0)

The script engine supports every major Ducky Script generation:

Ducky Script 1.0
Basic commands like STRING, DELAY, CTRL ALT DELETE, etc.

Ducky Script 2.0
Includes variables, logic, loops, labels, and flow control:
IF, WHILE, VAR, DEFINE, GOTO, and more.

Ducky Script 3.0
Advanced modern features:

RANDOM

RANDOM_LOWERCASE_LETTER

RANDOM_UPPERCASE_LETTER

RANDOM_SPECIAL

JITTER (randomized typing for realism)

WAIT_FOR_BUTTON
These make the Pico W more flexible than traditional Rubber Ducky hardware.

⌨️ Multi-Language Keyboard Layout Support

The firmware includes dynamic keyboard layout support, allowing payloads to run correctly on systems using various keyboard standards.

Supported layouts:

QWERTY (US)

AZERTY (France/Belgium)

QWERTZ (Germany/Swiss)

You can change the active keyboard layout simply through configuration, without modifying the codebase.
This ensures accurate keystrokes across different regions and system languages.

🌐 WiFi-Enabled Payload Execution (Pico W Only)

Because this project targets the Pico W, it provides WiFi capabilities for remote payload control:

Built-in AP mode

Web interface to browse payloads

Run payloads remotely via a browser

Automatic payload listing inside the /payloads directory

This makes the device dramatically more flexible and powerful than a normal BadUSB.

🖥 Hardware Safety & Controls

The firmware includes useful hardware-level protections:

Execution pause button (GP5 or GP1 depending on configuration)

LED status indicators

Optional input lock/unlock (keyboard + mouse)

Auto-language enforcement (forces host keyboard to English when needed)

📁 Project Structure
boot.py
main.py
command.py
keyboard.py
web.py
layouts/
    qwerty.py
    azerty.py
    qwertz.py
payloads/
    payload.txt


Payloads can be swapped or added freely inside the /payloads folder.

🚀 Summary

This repository provides a complete, feature-rich BadUSB platform for Raspberry Pi Pico W, offering:

Full Ducky Script 1.0 / 2.0 / 3.0 compatibility

Multi-layout keyboard support

WiFi remote execution

Fast, reliable HID injection

More capabilities than the original USB Rubber Ducky

Perfect for developers, security researchers, red teamers, and automation enthusiasts.
