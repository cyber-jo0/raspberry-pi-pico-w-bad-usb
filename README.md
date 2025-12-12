<h1 align="center">raspberry pi pico w badusb</h1>
<h3 align="center">make your raspberry pi pico w support all 3 versions of ducky script</h3>

<p align="center"> 
  <img src="https://komarev.com/ghpvc/?username=cyber-jo0&label=Profile%20views&color=blueviolet&style=flat" alt="cyber-jo0" />
</p>

---

- hi im mouhmed → 
  <a href="https://github.com/cyber-jo0/raspberry-pi-pico-w-bad-usb">
    <b>Pico W BadUSB – Advanced DuckyScript Executor</b>
  </a>

---

<h2 align="center">🔥 Raspberry Pi Pico W BadUSB – Advanced DuckyScript Executor</h2>

<p align="left">
This project transforms the <b>Raspberry Pi Pico W</b> into a powerful, fully-featured <b>BadUSB device</b> capable of executing Ducky Script 1.0 → 3.0, with WiFi control, layout switching, advanced logic, and high-speed HID injection.

It offers far more flexibility and power than the classic USB Rubber Ducky.
</p>

---

<h2>✨ Key Features</h2>

<h3>✔ Full Ducky Script Support (1.0 → 3.0)</h3>

<b>Ducky Script 1.0</b>
<ul>
  <li>STRING</li>
  <li>DELAY</li>
  <li>CTRL / ALT / SHIFT / GUI combinations</li>
  <li>Basic hotkeys</li>
</ul>

<b>Ducky Script 2.0</b>
<ul>
  <li>VAR, DEFINE</li>
  <li>IF / ELSE / END_IF</li>
  <li>WHILE / END_WHILE</li>
  <li>REPEAT</li>
  <li>GOTO</li>
  <li>Labels (:label)</li>
</ul>

<b>Ducky Script 3.0</b>
<ul>
  <li>RANDOM</li>
  <li>RANDOM_LOWERCASE_LETTER</li>
  <li>RANDOM_UPPERCASE_LETTER</li>
  <li>RANDOM_SPECIAL</li>
  <li>JITTER (randomized typing)</li>
  <li>WAIT_FOR_BUTTON</li>
</ul>

---

<h2>⌨️ Multi-Language Keyboard Layout Support</h2>

<ul>
  <li><b>QWERTY</b> (US)</li>
  <li><b>AZERTY</b> (France/Belgium)</li>
  <li><b>QWERTZ</b> (Germany/Swiss)</li>
</ul>

<p>Layouts can be changed via <code>secrets.py</code> without editing the firmware.</p>

---

<h2>🌐 WiFi-Enabled Payload Execution (Pico W Only)</h2>

<ul>
  <li>Built-in Access Point mode</li>
  <li>Web interface to run payloads</li>
  <li>Remote execution from any browser</li>
  <li>Auto payload listing inside /payloads</li>
</ul>

---

<h2>🖥 Hardware Safety & Controls</h2>

<ul>
  <li>Execution pause button (GP5)</li>
  <li>Boot-level USB storage disable (GP1)</li>
  <li>LED status indicators</li>
  <li>Optional keyboard/mouse lock</li>
  <li>Automatic English layout enforcement</li>
</ul>

---

<h2>📁 Project Structure</h2>

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

---

<h2>⚙️ Installation Guide (Pico W)</h2>

<h3>1️⃣ Download CircuitPython</h3>
Official UF2 firmware:  
https://circuitpython.org/board/raspberry_pi_pico_w/

<h3>2️⃣ Flash the UF2</h3>
1. Hold <b>BOOTSEL</b>  
2. Plug the Pico W into USB  
3. Drop the UF2 file into <b>RPI-RP2</b>

The board reboots into <b>CIRCUITPY</b>.

<h3>3️⃣ Copy the Project Files</h3>

Copy into CIRCUITPY:
- boot.py  
- main.py  
- command.py  
- keyboard.py  
- web.py  
- layouts/  
- payloads/  

<h3>4️⃣ (Optional) Configure WiFi + Layout</h3>

```python
SSID = "PicoW_AP"
PASSWORD = "12345678"
LAYOUT = "QWERTY"
