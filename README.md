# hidapi-py

`hidapi-py` provides Python bindings for the HIDAPI library, enabling interaction with HID-class USB devices.

## Usage

You can use the `hidapi_py` module in your Python scripts (listing all connected DualSense controllers):

```python
from hidapi_py import get_all_device_infos

print(hidapi_py.__version__)
print(hidapi_py.__hid_version__)

SONY_VENDOR_ID: int = 0x054C
DS_PRODUCT_ID: int = 0x0CE6

devices = get_all_device_infos(SONY_VENDOR_ID, DS_PRODUCT_ID)

print(devices)
```

## Features

- Access HID device information such as vendor ID, product ID, and serial number.
- Communicate with HID devices using Python.

## Building from Source

### Windows

Ensure you have the following installed:

- CMake
- Ninja
- Visual Studio Build Tools
- HID API dll from [https://github.com/libusb/hidapi](https://github.com/libusb/hidapi)

Use the following commands to build the project on Windows:

```powershell
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release --clean-first --target hidapi-py
```

### Mac OSx

Install the HIDAPI library using Homebrew:

```bash
brew install hidapi
```

To build the project on macOS for x86_64 architecture, run:

```bash
./scripts/build_macosx_x86_64.sh
```

### Ubuntu

Install the HIDAPI library using your package manager. For example, on Ubuntu:

```bash
sudo apt-get install libhidapi-dev
```

Run the following commands to build the project on Linux:

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release --clean-first --target hidapi-py
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any bugs or feature requests.

## License

This project is licensed under the terms of the [LICENSE.txt](LICENSE.txt) file.
