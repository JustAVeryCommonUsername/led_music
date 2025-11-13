import sounddevice as sd
import numpy as np
import aubio

class AudioBeatAnalyzer:
    def __init__(self, device_name, callback, samplerate=48000, block_size=1024):
        self.device_name = device_name
        self.callback = callback
        self.samplerate = samplerate
        self.block_size = block_size

        self.beat_detector = aubio.tempo("default", 2048, 1024, samplerate)

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

        mono = np.mean(indata, axis=1).astype(np.float32)
        beat = self.beat_detector(mono)
        if beat:
            self.callback(1, 1, 1)  # Trigger callback on beat

    def start(self):
        self.stream.start()  # Fixed: added parentheses

    def stop(self):
        self.stream.stop()
        self.stream.close()