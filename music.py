import colorsys
import sounddevice as sd
import numpy as np
import aubio

class AudioBeatAnalyzer:
    def __init__(self, device_name, callback, worker, samplerate=48000, block_size=1024):
        self.device_name = device_name
        self.callback = callback
        self.worker = worker
        self.samplerate = samplerate
        self.block_size = block_size

        self.beat_detector = aubio.onset("default", 2048, 1024, samplerate)
        self.pitch_detector = aubio.pitch("default", 2048, 1024, samplerate)

        self.stream = sd.InputStream(
            device=device_name,
            channels=2,
            samplerate=samplerate,
            blocksize=block_size,
            callback=self._audio_callback,
            dtype='float32'
        )

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print("Audio stream status:", status)

        # Intensity / Amplitude
        mono = np.mean(indata, axis=1).astype(np.float32)
        rms = np.sqrt(np.mean(mono ** 2))
        intensity = rms * 5
        intensity = max(0.0, min(intensity, 1.0))

        # Pitch / Hue
        pitch = self.pitch_detector(mono)[0]
        hue = min(max((pitch - 50) / (2000 - 50), 0), 1) if pitch > 0 else 0

        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, intensity)

        self.worker.schedule([int(r * 255), int(g * 255), int(b * 255)], 0)

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()
        self.stream.close()