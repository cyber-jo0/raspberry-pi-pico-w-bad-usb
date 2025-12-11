from time import sleep
from random import randint, uniform
from board import LED, GP5
from digitalio import DigitalInOut, Direction, Pull

try:
    import secrets  # optional user config
except ImportError:
    secrets = None

try:
    from .keyboard import Keyboard
except:
    from keyboard import Keyboard

# Enhanced Command handler class supporting DuckyScript 1.0, 2.0, and 3.0
class Command:
    
    # Initial setup
    def __init__(self) -> None:
        self.__keyboard = Keyboard()
        self.__led = DigitalInOut(LED)
        self.__led.direction = Direction.OUTPUT
        self.__typespeed = 0.01  # Small delay helps with reliability
        self.__delay = 0.5
        self.__default_delay = 0.0
        self.__string = ""
        self.__arguments = []
        self.__variables = {}
        self.__defines = {}
        self.__labels = {}
        self.__current_line = 0
        self.__lines = []
        self.__repeat_count = 1
        self.__loop_stack = []
        self.__jitter_enabled = False
        self.__jitter_max = 0
        self.__auto_language_guard = True
        self.__input_lock_default_ms = 0  # optional host input lock duration
        self.__run_box_delay = 0.25
        self.__command_aliases = {
            "waitforbutton": "wait_for_button",
            "wait_for_button_press": "wait_for_button",
            "waitforbuttonpress": "wait_for_button",
            "endif": "end_if",
            "endwhile": "end_while",
            "lang_en": "language_en",
            "ensure_english": "language_en",
            "force_english": "language_en",
            "lockinput": "lock_input",
            "lock_keyboard": "lock_input",
            "lock_mouse": "lock_input",
            "unlockinput": "unlock_input",
            "unlock_keyboard": "unlock_input",
            "unlock_mouse": "unlock_input",
        }
        self.__key_aliases = {
            "CTRL": "CONTROL",
            "CONTROL": "CONTROL",
            "ALT": "ALT",
            "OPTION": "ALT",
            "SHIFT": "SHIFT",
            "GUI": "GUI",
            "WIN": "GUI",
            "WINDOWS": "GUI",
            "CMD": "GUI",
            "COMMAND": "GUI",
            "META": "GUI",
            "SUPER": "GUI",
            "APP": "MENU",
            "APPLICATION": "MENU",
            "ESC": "ESCAPE",
            "DEL": "DELETE",
            "BKSP": "BACKSPACE",
            "RETURN": "ENTER",
            "UPARROW": "UP",
            "DOWNARROW": "DOWN",
            "LEFTARROW": "LEFT",
            "RIGHTARROW": "RIGHT",
        }

        # User overrides (optional)
        if secrets:
            self.__auto_language_guard = getattr(secrets, "AUTO_LANGUAGE_GUARD", self.__auto_language_guard)
            self.__input_lock_default_ms = getattr(secrets, "INPUT_LOCK_DURATION_MS", self.__input_lock_default_ms)
        
        # Blink LED to show we're alive
        self.__led.value = True
        sleep(0.3)
        self.__led.value = False
        sleep(0.2)
        self.__led.value = True
        sleep(0.3)
        self.__led.value = False
        
        # Check GP5 (will auto-skip if not grounded)
        self.__pause()

    # Pauses execution only if GP5 is grounded
    def __pause(self) -> None:
        try:
            gp5 = DigitalInOut(GP5)
            gp5.switch_to_input(pull=Pull.UP)
            
            # If GP5 is LOW (grounded), wait for it to go HIGH
            if not gp5.value:
                # Blink LED while waiting
                while not gp5.value:
                    self.__led.value = not self.__led.value
                    sleep(0.1)
                self.__led.value = False
        except:
            # If any error with GP5, just continue
            pass

    # Run a short hidden PowerShell command using WIN+R
    def __run_powershell(self, script: str, wait: float = 0.5) -> None:
        try:
            command = f"powershell -NoLogo -NoProfile -WindowStyle Hidden -Command \"{script}\""
            self.__keyboard.hotkey(Keyboard.GUI, Keyboard.R)
            sleep(self.__run_box_delay)
            self.__keyboard.string(command, self.__typespeed)
            self.__keyboard.hotkey(Keyboard.ENTER)
            sleep(wait)
        except Exception:
            # If the host rejects the command just keep going
            pass

    # Force the active input language to English without blindly toggling
    def __enforce_english_layout(self) -> None:
        script = (
            "Add-Type -AssemblyName System.Windows.Forms;"
            "$cur=[System.Windows.Forms.InputLanguage]::CurrentInputLanguage;"
            "if($cur.Culture.TwoLetterISOLanguageName -ne 'en'){"
            "$target=[System.Windows.Forms.InputLanguage]::InstalledInputLanguages | "
            "Where-Object { $_.Culture.TwoLetterISOLanguageName -eq 'en' } | Select-Object -First 1;"
            "if($target){[System.Windows.Forms.InputLanguage]::CurrentInputLanguage = $target}"
            "}"
        )
        self.__run_powershell(script, wait=0.8)

    # Lock both keyboard and mouse input on the host for a period
    def __lock_user_input(self, duration_ms: int) -> None:
        if duration_ms <= 0:
            return
        
        script = (
            "Add-Type -Namespace Win32 -Name Native -MemberDefinition "
            "'[DllImport(\"user32.dll\")]public static extern bool BlockInput(bool fBlockIt);';"
            "[Win32.Native]::BlockInput($true);"
            f"Start-Sleep -Milliseconds {duration_ms};"
            "[Win32.Native]::BlockInput($false)"
        )
        wait_time = max(duration_ms / 1000.0, 0) + 0.2
        self.__run_powershell(script, wait=wait_time)

    # Unlock host input immediately
    def __unlock_user_input(self) -> None:
        script = (
            "Add-Type -Namespace Win32 -Name Native -MemberDefinition "
            "'[DllImport(\"user32.dll\")]public static extern bool BlockInput(bool fBlockIt);';"
            "[Win32.Native]::BlockInput($false)"
        )
        self.__run_powershell(script, wait=0.4)
    
    # Expands tokens like CTRL-ALT into ["CTRL", "ALT"]
    def __tokenize_combo(self, parts):
        tokens = []
        for part in parts:
            expanded = self.__replace_vars(part).replace("+", "-")
            for token in expanded.split("-"):
                token = token.strip()
                if token:
                    tokens.append(token)
        return tokens

    # Maps combo tokens to HID keycodes
    def __keys_to_keycodes(self, tokens):
        keycodes = []
        for token in tokens:
            if len(token) == 1:
                ordinal = ord(token)
                if ordinal < 0x80:
                    keycodes.extend(self.__keyboard.ASCII[ordinal])
                continue
            
            token_upper = token.upper()
            token_upper = self.__key_aliases.get(token_upper, token_upper)
            
            if hasattr(Keyboard, token_upper):
                keycodes.append(getattr(Keyboard, token_upper))
        return keycodes

    # Detects if a line is a legacy-style key combo (DuckyScript 1.0)
    def __is_combo_command(self, token) -> bool:
        for part in token.replace("+", "-").split("-"):
            part = part.strip()
            if not part:
                continue
            
            if len(part) == 1:
                return True
            
            part_upper = part.upper()
            if part_upper in self.__key_aliases or hasattr(Keyboard, part_upper):
                return True
        return False

    # Replaces variables and defines in string
    def __replace_vars(self, text: str) -> str:
        for var_name, var_value in self.__variables.items():
            text = text.replace(f"${var_name}", str(var_value))
        for def_name, def_value in self.__defines.items():
            text = text.replace(def_name, def_value)
        return text

    # Evaluates conditional expressions
    def __evaluate_condition(self, condition: str) -> bool:
        condition = self.__replace_vars(condition)
        condition = condition.strip()
        
        # Simple comparison operators
        if "==" in condition:
            left, right = condition.split("==", 1)
            return left.strip() == right.strip()
        elif "!=" in condition:
            left, right = condition.split("!=", 1)
            return left.strip() != right.strip()
        elif ">=" in condition:
            left, right = condition.split(">=", 1)
            try:
                return float(left.strip()) >= float(right.strip())
            except:
                return False
        elif "<=" in condition:
            left, right = condition.split("<=", 1)
            try:
                return float(left.strip()) <= float(right.strip())
            except:
                return False
        elif ">" in condition:
            left, right = condition.split(">", 1)
            try:
                return float(left.strip()) > float(right.strip())
            except:
                return False
        elif "<" in condition:
            left, right = condition.split("<", 1)
            try:
                return float(left.strip()) < float(right.strip())
            except:
                return False
        
        # Boolean evaluation
        return condition.lower() in ["true", "1"]

    # Optional pre-flight setup before running the payload
    def __preflight(self) -> None:
        if self.__auto_language_guard:
            self.language_en()
        if self.__input_lock_default_ms > 0:
            # Locks user input briefly, then continues with the payload
            self.__lock_user_input(self.__input_lock_default_ms)

    # LANGUAGE_EN - ensure host input is set to English
    def language_en(self) -> None:
        self.__enforce_english_layout()

    # LOCK_INPUT - blocks keyboard + mouse input on the host temporarily
    def lock_input(self) -> None:
        duration_ms = self.__input_lock_default_ms
        if len(self.__arguments) > 0:
            try:
                duration_ms = int(self.__replace_vars(self.__arguments[0]))
            except:
                pass
        self.__lock_user_input(duration_ms)

    # UNLOCK_INPUT - releases a stuck lock, if any
    def unlock_input(self) -> None:
        self.__unlock_user_input()

    # REM - Comment (ignored)
    def rem(self) -> None:
        pass

    # Alias to HOTKEY (for both PRESS and standalone keys)
    def press(self) -> None:
        self.hotkey()
    
    # Enters a key combination
    def hotkey(self) -> None:
        keycodes = []
        
        for argument in self.__arguments:
            argument = self.__replace_vars(argument)
            
            if len(argument) == 1:
                ordinal = ord(argument.lower())
                
                if ordinal < 0x80:
                    keycode = self.__keyboard.ASCII[ordinal]
                    keycodes.extend(keycode)
            
            elif hasattr(Keyboard, argument.upper()):
                keycodes.append(getattr(Keyboard, argument.upper()))
        
        if keycodes:
            self.__keyboard.hotkey(*keycodes)
        
        if self.__default_delay > 0:
            sleep(self.__default_delay)

    # Handle single key press (for commands like ENTER, ESCAPE, etc.)
    def __single_key(self, keyname: str) -> None:
        if hasattr(Keyboard, keyname.upper()):
            keycode = getattr(Keyboard, keyname.upper())
            self.__keyboard.hotkey(keycode)
        
        if self.__default_delay > 0:
            sleep(self.__default_delay)

    # All individual key commands
    def enter(self) -> None:
        self.__single_key("ENTER")
    
    def escape(self) -> None:
        self.__single_key("ESCAPE")
    
    def esc(self) -> None:
        self.escape()
    
    def tab(self) -> None:
        self.__single_key("TAB")
    
    def space(self) -> None:
        self.__single_key("SPACE")
    
    def backspace(self) -> None:
        self.__single_key("BACKSPACE")
    
    def delete(self) -> None:
        self.__single_key("DELETE")
    
    def home(self) -> None:
        self.__single_key("HOME")
    
    def end(self) -> None:
        self.__single_key("END")
    
    def pageup(self) -> None:
        self.__single_key("PAGEUP")
    
    def pagedown(self) -> None:
        self.__single_key("PAGEDOWN")
    
    def up(self) -> None:
        self.__single_key("UP")
    
    def down(self) -> None:
        self.__single_key("DOWN")
    
    def left(self) -> None:
        self.__single_key("LEFT")
    
    def right(self) -> None:
        self.__single_key("RIGHT")
    
    def uparrow(self) -> None:
        self.up()
    
    def downarrow(self) -> None:
        self.down()
    
    def leftarrow(self) -> None:
        self.left()
    
    def rightarrow(self) -> None:
        self.right()
    
    def insert(self) -> None:
        self.__single_key("INSERT")
    
    def printscreen(self) -> None:
        self.__single_key("PRINTSCREEN")
    
    def menu(self) -> None:
        self.__single_key("MENU")
    
    def app(self) -> None:
        self.menu()
    
    def f1(self) -> None:
        self.__single_key("F1")
    
    def f2(self) -> None:
        self.__single_key("F2")
    
    def f3(self) -> None:
        self.__single_key("F3")
    
    def f4(self) -> None:
        self.__single_key("F4")
    
    def f5(self) -> None:
        self.__single_key("F5")
    
    def f6(self) -> None:
        self.__single_key("F6")
    
    def f7(self) -> None:
        self.__single_key("F7")
    
    def f8(self) -> None:
        self.__single_key("F8")
    
    def f9(self) -> None:
        self.__single_key("F9")
    
    def f10(self) -> None:
        self.__single_key("F10")
    
    def f11(self) -> None:
        self.__single_key("F11")
    
    def f12(self) -> None:
        self.__single_key("F12")
    
    def capslock(self) -> None:
        self.__single_key("CAPSLOCK")
    
    def numlock(self) -> None:
        self.__single_key("NUMLOCK")
    
    def scrolllock(self) -> None:
        self.__single_key("SCROLLOCK")

    # Enters a string of ASCII characters
    def string(self) -> None:
        text = self.__replace_vars(self.__string)
        
        if self.__jitter_enabled and self.__jitter_max > 0:
            # Add jitter to typing speed
            for char in text:
                ordinal = ord(char)
                if ordinal < 0x80:
                    keycode = self.__keyboard.ASCII[ordinal]
                    self.__keyboard.press(*keycode)
                    self.__keyboard.release()
                    jitter = uniform(0, self.__jitter_max / 1000.0)
                    sleep(self.__typespeed + jitter)
        else:
            self.__keyboard.string(text, self.__typespeed)
        
        if self.__default_delay > 0:
            sleep(self.__default_delay)

    # STRING with ENTER (DuckyScript 2.0)
    def stringln(self) -> None:
        self.string()
        self.__keyboard.hotkey(Keyboard.ENTER)
        
        if self.__default_delay > 0:
            sleep(self.__default_delay)

    # Sets the type speed of strings
    def typespeed(self) -> None:
        if len(self.__arguments) > 0:
            value = self.__replace_vars(self.__arguments[0])
            try:
                self.__typespeed = int(value) / 1000
            except:
                pass

    # Sets the default delay between commands (DuckyScript 1.0)
    def defaultdelay(self) -> None:
        if len(self.__arguments) > 0:
            value = self.__replace_vars(self.__arguments[0])
            try:
                self.__default_delay = int(value) / 1000
            except:
                pass
    
    # Alias for DEFAULTDELAY
    def default_delay(self) -> None:
        self.defaultdelay()

    # Sets the delay between commands
    def delay(self) -> None:
        if len(self.__arguments) > 0:
            value = self.__replace_vars(self.__arguments[0])
            try:
                time = int(value) / 1000
            except:
                time = self.__delay
        else:
            time = self.__delay
        
        sleep(time)

    # REPEAT - Repeats the previous command (DuckyScript 1.0)
    def repeat(self) -> None:
        if len(self.__arguments) > 0:
            value = self.__replace_vars(self.__arguments[0])
            try:
                count = int(value)
                self.__repeat_count = count
            except:
                pass
    
    # QUACK - inline execution helper (DuckyScript 1.0)
    def quack(self) -> None:
        if self.__arguments:
            inline = " ".join(self.__arguments)
            self.__lines.insert(self.__current_line + 1, inline + "\n")

    # VAR - Define/set variable (DuckyScript 2.0)
    def var(self) -> None:
        if len(self.__arguments) >= 2:
            var_name = self.__arguments[0]
            var_value = " ".join(self.__arguments[1:])
            
            # Handle assignment operator
            if "=" in var_value:
                var_value = var_value.split("=", 1)[1].strip()
            
            var_value = self.__replace_vars(var_value)
            self.__variables[var_name] = var_value

    # DEFINE - Define constant (DuckyScript 2.0)
    def define(self) -> None:
        if len(self.__arguments) >= 2:
            def_name = self.__arguments[0]
            def_value = " ".join(self.__arguments[1:])
            def_value = self.__replace_vars(def_value)
            self.__defines[def_name] = def_value

    # IF - Conditional execution (DuckyScript 2.0)
    def if_statement(self, condition: str) -> bool:
        return self.__evaluate_condition(condition)

    # WHILE - Loop (DuckyScript 2.0)
    def while_loop(self, condition: str) -> None:
        if self.__evaluate_condition(condition):
            self.__loop_stack.append({
                'type': 'while',
                'start_line': self.__current_line,
                'condition': condition
            })
        else:
            # Skip to END_WHILE
            self.__skip_to_end('while')

    # Skip to matching END statement
    def __skip_to_end(self, block_type: str) -> None:
        depth = 1
        while self.__current_line < len(self.__lines) - 1:
            self.__current_line += 1
            line = self.__lines[self.__current_line].strip().upper()
            
            if block_type == 'while' and line.startswith('WHILE'):
                depth += 1
            elif block_type == 'if' and line.startswith('IF'):
                depth += 1
            elif line.startswith(f'END_{block_type.upper()}') or line.startswith(f'END{block_type.upper()}'):
                depth -= 1
                if depth == 0:
                    break

    # JITTER - Enable typing randomization (DuckyScript 3.0)
    def jitter(self) -> None:
        if len(self.__arguments) > 0:
            value = self.__replace_vars(self.__arguments[0])
            try:
                self.__jitter_max = int(value)
                self.__jitter_enabled = True
            except:
                pass
        else:
            self.__jitter_enabled = False
            self.__jitter_max = 0

    # RANDOM - Generate random number (DuckyScript 3.0)
    def random(self) -> None:
        if len(self.__arguments) >= 3:
            var_name = self.__arguments[0]
            try:
                min_val = int(self.__replace_vars(self.__arguments[1]))
                max_val = int(self.__replace_vars(self.__arguments[2]))
                self.__variables[var_name] = str(randint(min_val, max_val))
            except:
                pass

    # RANDOM_LOWERCASE_LETTER (DuckyScript 3.0)
    def random_lowercase_letter(self) -> None:
        if len(self.__arguments) >= 1:
            var_name = self.__arguments[0]
            self.__variables[var_name] = chr(randint(97, 122))

    # RANDOM_UPPERCASE_LETTER (DuckyScript 3.0)
    def random_uppercase_letter(self) -> None:
        if len(self.__arguments) >= 1:
            var_name = self.__arguments[0]
            self.__variables[var_name] = chr(randint(65, 90))

    # RANDOM_SPECIAL (DuckyScript 3.0)
    def random_special(self) -> None:
        if len(self.__arguments) >= 1:
            var_name = self.__arguments[0]
            specials = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            self.__variables[var_name] = specials[randint(0, len(specials) - 1)]
    
    # WAIT_FOR_BUTTON (DuckyScript 3.0 hardware pause)
    def wait_for_button(self) -> None:
        self.__pause()

    # COMBO - legacy key combos (CTRL ALT DEL, GUI r, etc.)
    def combo(self) -> None:
        tokens = self.__tokenize_combo(self.__arguments)
        keycodes = self.__keys_to_keycodes(tokens)
        
        if keycodes:
            self.__keyboard.hotkey(*keycodes)
        
        if self.__default_delay > 0:
            sleep(self.__default_delay)

    # Turns on/off the onboard LED diode
    def led(self) -> None:
        if len(self.__arguments) > 0:
            value = self.__replace_vars(self.__arguments[0])
            if value.lower() == "on":
                self.__led.value = True
            else:
                self.__led.value = False

    # Executes instructions and validates them
    def execute(self, path: str) -> None:
        try:
            # First pass: load all lines and find labels
            with open(path, "r", encoding="utf-8") as payload:
                self.__lines = payload.readlines()
            
            # Find all labels
            for idx, line in enumerate(self.__lines):
                clean_line = line.strip()
                if clean_line.startswith(":"):
                    label_name = clean_line[1:].strip()
                    self.__labels[label_name] = idx
        
        except Exception as e:
            # Blink LED rapidly to indicate error
            for _ in range(10):
                self.__led.value = not self.__led.value
                sleep(0.1)
            return

        # Pre-flight: language guard + optional input lock
        self.__preflight()

        # Second pass: execute
        self.__current_line = 0
        previous_command = None
        previous_args = None
        previous_string = None
        
        while self.__current_line < len(self.__lines):
            raw_line = self.__lines[self.__current_line]
            self.__string = raw_line.replace("\n", "").replace("\r", "")
            
            # Skip empty lines and comments
            if not self.__string.strip() or self.__string.strip().startswith("REM"):
                self.__current_line += 1
                continue
            
            # Skip labels
            if self.__string.strip().startswith(":"):
                self.__current_line += 1
                continue
            
            self.__arguments = self.__string.split(" ")
            
            if len(self.__arguments) > 0:
                command = self.__arguments.pop(0).lower()
                command_method = command.replace("-", "_")
                command_method = self.__command_aliases.get(command_method, command_method)
                
                # Handle special flow control
                if command_method == "if":
                    condition = " ".join(self.__arguments)
                    if not self.if_statement(condition):
                        self.__skip_to_end('if')
                    self.__current_line += 1
                    continue
                
                elif command_method == "else":
                    self.__skip_to_end('if')
                    self.__current_line += 1
                    continue
                
                elif command_method == "end_if" or command_method == "endif":
                    self.__current_line += 1
                    continue
                
                elif command_method == "while":
                    condition = " ".join(self.__arguments)
                    self.while_loop(condition)
                    self.__current_line += 1
                    continue
                
                elif command_method == "end_while" or command_method == "endwhile":
                    if self.__loop_stack and self.__loop_stack[-1]['type'] == 'while':
                        loop_info = self.__loop_stack[-1]
                        if self.__evaluate_condition(loop_info['condition']):
                            self.__current_line = loop_info['start_line']
                            continue
                        else:
                            self.__loop_stack.pop()
                    self.__current_line += 1
                    continue
                
                elif command_method == "goto":
                    if len(self.__arguments) > 0:
                        label = self.__arguments[0]
                        if label in self.__labels:
                            self.__current_line = self.__labels[label]
                            continue
                    self.__current_line += 1
                    continue
                
                # Execute command
                if hasattr(Command, command_method):
                    self.__string = self.__string[len(command) + 1:] if len(self.__string) > len(command) else ""
                    
                    try:
                        # Execute main command
                        getattr(Command, command_method)(self)
                        
                        # Handle REPEAT
                        if previous_command and self.__repeat_count > 1:
                            for _ in range(self.__repeat_count - 1):
                                saved_args = self.__arguments[:]
                                saved_string = self.__string
                                
                                self.__arguments = previous_args[:]
                                self.__string = previous_string
                                
                                getattr(Command, previous_command)(self)
                                
                                self.__arguments = saved_args
                                self.__string = saved_string
                            
                            self.__repeat_count = 1
                        
                        # Save for REPEAT
                        if command_method != "repeat":
                            previous_command = command_method
                            previous_args = self.__arguments[:]
                            previous_string = self.__string
                    
                    except Exception as e:
                        self.__keyboard.release()
                
                # Fallback: treat unknown commands as legacy combos
                elif self.__is_combo_command(command):
                    self.__arguments = [command] + self.__arguments
                    self.__string = " ".join(self.__arguments)
                    command_method = "combo"
                    
                    try:
                        getattr(Command, command_method)(self)
                        
                        if previous_command and self.__repeat_count > 1:
                            for _ in range(self.__repeat_count - 1):
                                saved_args = self.__arguments[:]
                                saved_string = self.__string
                                
                                self.__arguments = previous_args[:]
                                self.__string = previous_string
                                
                                getattr(Command, previous_command)(self)
                                
                                self.__arguments = saved_args
                                self.__string = saved_string
                            
                            self.__repeat_count = 1
                        
                        if command_method != "repeat":
                            previous_command = command_method
                            previous_args = self.__arguments[:]
                            previous_string = self.__string
                    
                    except Exception:
                        self.__keyboard.release()
            
            self.__current_line += 1
        
        # Turn on LED when done
        self.__led.value = True
