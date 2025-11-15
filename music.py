import colorsys
import sounddevice as sd
import numpy as np
import aubio
import time as tm

class AudioBeatAnalyzer:
    def __init__(self, device_name, callback, samplerate=48000, block_size=1024):
        self.device_name = device_name
        self.callback = callback
        self.samplerate = samplerate
        self.block_size = block_size

        self.beat_detector = aubio.onset("default", 2048, 1024, samplerate)
        self.beat_detector.set_threshold(0.03)
        self.pitch_detector = aubio.pitch("default", 2048, 1024, samplerate)

        self.beat_active = False
        self.last_beat_time = 0

        self.stream = sd.InputStream(
            device=device_name,
            channels=2,
            samplerate=samplerate,
            blocksize=block_size,
            callback=self._audio_callback,
            dtype='float32'
        )

        self.last_color = [0, 0, 0]

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print("Audio stream status:", status)
        mono = np.mean(indata, axis=1).astype(np.float32)

        # Intensity / Amplitude
        rms = np.sqrt(np.mean(mono ** 2))
        intensity = rms * 5
        intensity = max(0.0, min(intensity, 1.0))

        # Beat detection
        is_beat = self.beat_detector(mono)
        now = tm.time()
        if is_beat:
            self.last_beat_time = now
        self.beat_active = (now - self.last_beat_time) < 0.1

        if not self.beat_active:
            intensity = 1 / ((now - self.last_beat_time) * 40)
        if intensity < 0.05:
            intensity = 0

        # Pitch / Hue
        pitch = self.pitch_detector(mono)[0]
        hue = min(max((pitch - 50) / (2000 - 50), 0), 1) if pitch > 0 else 0
        hue = (hue * 3) % 1

        # Smoothing
        alpha = 0.3
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, intensity)
        r = alpha * r + (1 - alpha) * self.last_color[0]
        g = alpha * g + (1 - alpha) * self.last_color[1]
        b = alpha * b + (1 - alpha) * self.last_color[2]

        self.last_color = [r, g, b]

        # Directly call the callback with the color
        self.callback(int(r * 255), int(g * 255), int(b * 255))

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()
        self.stream.close()