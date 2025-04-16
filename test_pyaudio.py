import pyaudio
import numpy as np

p = pyaudio.PyAudio()

# Parameters
fs = 44100
duration = 2.0
freq = 440.0  # Hz (A4 tone)
device_index = 31  # <- Replace with your USB speaker's device ID

# Generate waveform
samples = (np.sin(2 * np.pi * np.arange(fs * duration)
           * freq / fs)).astype(np.float32)

# Open stream
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True,
                output_device_index=device_index)

# Play audio
stream.write(samples.tobytes())

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
