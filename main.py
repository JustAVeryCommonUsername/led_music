import serial
import serial.tools.list_ports
from music import AudioBeatAnalyzer
from worker import LEDWorker
import sounddevice as sd

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

#DEVICE_NAME = "Microphone Array (Intel® Smart Sound Technology for Digital Microphones), Windows WASAPI"
DEVICE_NAME = "CABLE Output (VB-Audio Virtual Cable), Windows WASAPI"
SAMPLE_RATE = 48000
BLOCK_SIZE = 1024

if __name__ == "__main__":
    interface = LEDSerialInteface()
    worker = LEDWorker(interface)
    analyzer = AudioBeatAnalyzer(DEVICE_NAME, callback=interface.send_rgb, worker=worker)
    analyzer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        analyzer.stop()