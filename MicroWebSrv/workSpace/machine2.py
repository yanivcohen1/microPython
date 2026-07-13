import serial
import time
import threading  # <--- הוספנו את זה למניעת התנגשויות
import user_lib.settings as settings

class _SerialRPC:
    def __init__(self, port='COM3', baudrate=115200):
        self.lock = threading.Lock() # יצירת מנעול לתקשורת
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self._enter_raw_repl()
        self.execute("import machine")

    def _enter_raw_repl(self):
        self.ser.write(b'\r\x03\x03')  # Ctrl+C
        time.sleep(0.1)
        self.ser.write(b'\x01')        # Ctrl+A (Raw REPL)
        time.sleep(0.1)
        self.ser.read_all()

    def execute(self, command, retries=3):
        # המנעול דואג שרק חוט אחד מתקשר בכל רגע נתון
        with self.lock:
            for attempt in range(retries):
                # 1. ניקוי החוצץ הטורי משאריות לפני שליחת הפקודה
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
                
                # 2. שליחת הפקודה
                self.ser.write(command.encode('utf-8'))
                self.ser.write(b'\x04') 
                
                # 3. קריאת התשובה
                response = b''
                while not response.endswith(b'\x04>'):
                    chunk = self.ser.read(1)
                    if not chunk:
                        break # קרה Timeout
                    response += chunk
                    
                try:
                    if response.startswith(b'OK'):
                        response = response[2:]
                        
                    parts = response.split(b'\x04')
                    stdout = parts[0].decode('utf-8').strip()
                    
                    if len(parts) > 1 and parts[1].strip():
                        stderr = parts[1].decode('utf-8').strip()
                        print(f"[MicroPython Error] {stderr}")
                        
                    # אם התשובה ריקה לחלוטין (ולא התקבלה שגיאה מהבקר), ננסה שוב
                    if not stdout and not response:
                        if attempt < retries - 1:
                            time.sleep(0.05) # המתנה קלה לפני הניסיון הבא
                            continue
                            
                    return stdout
                    
                except Exception as e:
                    print(f"[PC Error] {e}")
                    return ""
                    
            return "" # אם כל הניסיונות נכשלו

    def __del__(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.write(b'\x02') # יציאה מ-Raw REPL
            self.ser.close()

# אל תשכח לוודא שה-port נכון
env_data = settings.readEnvData()  # קבלת הפורט מהגדרות 
rpc = _SerialRPC(port=env_data["port"]) # 'COM3'


# ==========================================
# 2. פונקציות מערכת של machine
# ==========================================
def reset():
    """מבצע ריסט לחומרה"""
    rpc.execute("machine.reset()")

def freq(freq_hz=None):
    """קריאה או הגדרה של תדר המעבד"""
    if freq_hz is None:
        res = rpc.execute("print(machine.freq())")
        return int(res) if res.isdigit() else None
    else:
        rpc.execute(f"machine.freq({freq_hz})")


# ==========================================
# 3. מחלקות חומרה - Hardware Classes
# ==========================================
class Pin:
    IN = 1
    OUT = 3
    PULL_NONE = None
    PULL_UP = 2
    PULL_DOWN = 1
    
    def __init__(self, id, mode=-1, pull=-1):
        self.id = id
        self._name = f"pin_{self.id}" # השם של המשתנה שיווצר בבקר
        
        args = [str(self.id)]
        if mode != -1: args.append(str(mode))
        if pull != -1: args.append(str(pull))
            
        code = f"{self._name} = machine.Pin({', '.join(args)})"
        rpc.execute(code)

    def value(self, val=None):
        if val is None:
            res = rpc.execute(f"print({self._name}.value())")
            return int(res) if res.isdigit() else None
        else:
            rpc.execute(f"{self._name}.value({val})")

    def on(self):
        self.value(1)

    def off(self):
        self.value(0)


class ADC:
    ATTN_0DB = 0
    ATTN_2_5DB = 1
    ATTN_6DB = 2
    ATTN_11DB = 3
    
    def __init__(self, pin):
        self.pin_id = pin.id if isinstance(pin, Pin) else pin
        self._name = f"adc_{self.pin_id}"
        
        pin_obj = f"machine.Pin({self.pin_id})"
        rpc.execute(f"{self._name} = machine.ADC({pin_obj})")

    def read(self):
        res = rpc.execute(f"print({self._name}.read())")
        try:
            return int(res)
        except (ValueError, TypeError):
            # אם קיבלנו אשפה במקום מספר, נדפיס אזהרה ונחזיר 0 כדי לא להקריס את הקוד
            print(f"[ADC read Warning] Invalid response: {repr(res)}")
            return 0 

    def read_u16(self):
        res = rpc.execute(f"print({self._name}.read_u16())")
        try:
            return int(res)
        except (ValueError, TypeError):
            print(f"[ADC read_u16 Warning] Invalid response: {repr(res)}")
            return 0
        
    def atten(self, attenuation):
        rpc.execute(f"{self._name}.atten({attenuation})")


# ==========================================
# 4. מודולים נוספים: WDT, Timer, I2C, PWM
# ==========================================

def time_pulse_us(pin, pulse_level, timeout_us=1000000):
    """
    מודד כמה זמן (במיקרו-שניות) הפין נמצא במצב הנתון (0 או 1).
    """
    pin_name = pin._name if isinstance(pin, Pin) else f"machine.Pin({pin})"
    res = rpc.execute(f"print(machine.time_pulse_us({pin_name}, {pulse_level}, {timeout_us}))")
    try:
        return int(res)
    except:
        return -1 # מיקרופייטון מחזיר -1 או -2 במקרה של Timeout

class WDT:
    def __init__(self, id=0, timeout=5000):
        self.id = id
        self._name = f"wdt_{self.id}"
        # בחלק מהבקרים כמו ESP8266 אי אפשר להעביר timeout לאתחול, 
        # אבל זהו התקן הרשמי של מיקרופייטון.
        rpc.execute(f"{self._name} = machine.WDT(id={self.id}, timeout={timeout})")

    def feed(self):
        """מאכיל את כלב השמירה כדי למנוע ריסט"""
        rpc.execute(f"{self._name}.feed()")


class Timer:
    PERIODIC = 1
    ONE_SHOT = 0
    
    def __init__(self, id):
        self.id = id
        self._name = f"timer_{abs(self.id)}" # ESP32 משתמש לעיתים ב--1
        rpc.execute(f"{self._name} = machine.Timer({self.id})")

    def init(self, mode=PERIODIC, period=-1, callback=None):
        """
        אתחול הטיימר.
        הערה חשובה: מכיוון שהקוד רץ על המחשב, אי אפשר להעביר פונקציית פייתון רגילה ל-callback.
        יש להעביר את הפונקציה כמחרוזת טקסט של קוד מיקרופייטון.
        לדוגמה: callback="lambda t: pin_2.value(not pin_2.value())"
        """
        cb_str = "None"
        if isinstance(callback, str):
            cb_str = callback
        elif callback is not None:
            print("[Warning] PC-side callbacks are not supported. Pass MicroPython code as a string.")
            return

        code = f"{self._name}.init(mode={mode}, period={period}, callback={cb_str})"
        rpc.execute(code)

    def deinit(self):
        rpc.execute(f"{self._name}.deinit()")


class PWM:
    def __init__(self, pin, freq=None, duty_u16=None):
        self.pin_id = pin.id if isinstance(pin, Pin) else pin
        self._name = f"pwm_{self.pin_id}"
        
        pin_obj = f"machine.Pin({self.pin_id})"
        rpc.execute(f"{self._name} = machine.PWM({pin_obj})")
        
        if freq is not None:
            self.freq(freq)
        if duty_u16 is not None:
            self.duty_u16(duty_u16)

    def freq(self, freq=None):
        if freq is None:
            res = rpc.execute(f"print({self._name}.freq())")
            return int(res) if res.isdigit() else None
        else:
            rpc.execute(f"{self._name}.freq({freq})")

    def duty_u16(self, duty=None):
        if duty is None:
            res = rpc.execute(f"print({self._name}.duty_u16())")
            return int(res) if res.isdigit() else None
        else:
            rpc.execute(f"{self._name}.duty_u16({duty})")

    def duty(self, duty=None):
        # תמיכה לאחור ב-duty הישן (0-1023) הקיים בבקרי ESP
        if duty is None:
            res = rpc.execute(f"print({self._name}.duty())")
            return int(res) if res.isdigit() else None
        else:
            rpc.execute(f"{self._name}.duty({duty})")

    def deinit(self):
        rpc.execute(f"{self._name}.deinit()")


class I2C:
    def __init__(self, id, scl, sda, freq=400000):
        self.id = id
        self._name = f"i2c_{self.id}"
        
        scl_name = scl._name if isinstance(scl, Pin) else f"machine.Pin({scl})"
        sda_name = sda._name if isinstance(sda, Pin) else f"machine.Pin({sda})"
        
        code = f"{self._name} = machine.I2C({self.id}, scl={scl_name}, sda={sda_name}, freq={freq})"
        rpc.execute(code)

    def scan(self):
        res = rpc.execute(f"print({self._name}.scan())")
        try:
            import ast
            return ast.literal_eval(res) if res else []
        except Exception as e:
            print(f"[I2C Scan Warning] Invalid response: {repr(res)}")
            return []

    def writeto(self, addr, buf):
        # המרה בטוחה: אם המשתמש שלח רשימה (למשל [0x00, 0xFF]), נמיר ל-bytes במחשב 
        # כדי שה-repr יפיק מחרוזת של בייטים (כמו b'\x00\xff') שהבקר יבין
        if isinstance(buf, (list, tuple)):
            buf = bytes(buf)
        buf_repr = repr(buf) 
        rpc.execute(f"{self._name}.writeto({addr}, {buf_repr})")

    def readfrom(self, addr, nbytes):
        res = rpc.execute(f"print(repr({self._name}.readfrom({addr}, {nbytes})))")
        try:
            import ast
            return ast.literal_eval(res) if res else b''
        except Exception as e:
            print(f"[I2C readfrom Warning] Invalid response: {repr(res)}")
            return b''
            
    def readfrom_mem(self, addr, memaddr, nbytes):
        res = rpc.execute(f"print(repr({self._name}.readfrom_mem({addr}, {memaddr}, {nbytes})))")
        try:
            import ast
            return ast.literal_eval(res) if res else b''
        except Exception as e:
            print(f"[I2C readfrom_mem Warning] Invalid response: {repr(res)}")
            return b''

    def writeto_mem(self, addr, memaddr, buf):
        if isinstance(buf, (list, tuple)):
            buf = bytes(buf)
        buf_repr = repr(buf)
        rpc.execute(f"{self._name}.writeto_mem({addr}, {memaddr}, {buf_repr})")