import pyaudio

p = pyaudio.PyAudio()

# List all audio devices
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if dev['maxOutputChannels'] > 0:
        print(f"ID {i}: {dev['name']}")
