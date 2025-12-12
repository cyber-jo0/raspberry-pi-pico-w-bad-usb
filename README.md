<h1 align="center">raspberry pi pico w badusb</h1>
<h3 align="center">make your raspberry pi pico w support all 3 versions of ducky script</h3>

<p align="center"> 
  <img src="https://komarev.com/ghpvc/?username=cyber-jo0&label=Profile%20views&color=blueviolet&style=flat" alt="cyber-jo0" />
</p>

<p align="center"> 
  <a href="https://github.com/ryo-ma/github-profile-trophy">
    <img src="https://github-profile-trophy.vercel.app/?username=cyber-jo0&theme=dracula&margin-w=10&margin-h=10" alt="cyber-jo0" />
  </a>
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

php-template
Copy code

Payloads can be added or modified freely inside /payloads.

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
<h3>5️⃣ Plug In & Execute</h3> Your Pico W now behaves as a full BadUSB device.
<h2>🚀 Summary</h2>
This project provides:

Full Ducky Script 1.0 / 2.0 / 3.0 support

Multi-language keyboard layouts

High-speed HID injection

WiFi-based remote payload execution

More features than the original USB Rubber Ducky

Perfect for developers, testers, cybersecurity researchers, automation engineers, and more.

<h3 align="left">Connect with me:</h3> <p align="left"> <a href="https://instagram.com/cybe_rjo" target="blank"> <img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="cybe_rjo" height="30" width="40" /> </a> <a href="https://www.youtube.com/@cyber-jo" target="blank"> <img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/youtube.svg" alt="@cyber-jo" height="30" width="40" /> </a> </p>
<h3 align="center">Languages and Tools</h3> <p align="center"> <a href="https://www.arduino.cc/" target="_blank"> <img src="https://cdn.worldvectorlogo.com/logos/arduino-1.svg" alt="arduino" width="40" height="40"/> </a> <a href="https://git-s-scm.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://www.linux.org/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>
<p align="center"> <img src="https://github-readme-stats.vercel.app/api/top-langs?username=cyber-jo0&show_icons=true&locale=en&layout=compact&theme=tokyonight" /> </p> <p align="center"> <img src="https://github-readme-stats.vercel.app/api?username=cyber-jo0&show_icons=true&locale=en&theme=tokyonight" /> </p> <p align="center"> <img src="https://github-readme-streak-stats.herokuapp.com/?user=cyber-jo0&theme=tokyonight" /> </p> ```
