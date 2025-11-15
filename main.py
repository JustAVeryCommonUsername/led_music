import serial
import serial.tools.list_ports
from music import AudioBeatAnalyzer
from web_server import start_server_in_thread
import threading

class LEDSerialInteface:
    def __init__(self, baudrate=115200):
        self.arduino = self.connect_arduino(baudrate)

    def connect_arduino(self, baudrate):
        ports = serial.tools.list_ports.comports()
        if not ports:
            return None
        port = ports[0].device
        try:
            return serial.Serial(port, baudrate, timeout=None, write_timeout=None)
        except Exception:
            return None

    def send_rgb(self, r, g, b):
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.write(bytes([r, g, b]))
                self.arduino.flush()
            except serial.SerialException as e:
                pass
            except Exception as e:
                pass

DEVICE_NAME = "CABLE Output (VB-Audio Virtual Cable), Windows WASAPI"
SAMPLE_RATE = 48000
BLOCK_SIZE = 1024

music_enabled = True
music_lock = threading.Lock()

def set_music_enabled(state: bool):
    global music_enabled
    with music_lock:
        music_enabled = state

def get_music_enabled():
    with music_lock:
        return music_enabled

def music_callback(r, g, b):
    if get_music_enabled():
        interface.send_rgb(r, g, b)

def web_callback(r, g, b):
    interface.send_rgb(r, g, b)

if __name__ == "__main__":
    interface = LEDSerialInteface()
    analyzer = AudioBeatAnalyzer(DEVICE_NAME, callback=music_callback)
    analyzer.start()

    start_server_in_thread(
        interface,
        port=5000,
        static_dir='static',
        music_toggle_callback=set_music_enabled,
        rgb_callback=web_callback
    )
    print("Web server running at http://localhost:5000")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        analyzer.stop()