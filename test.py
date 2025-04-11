import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build'))

from hidapi_py import HidDevice, hid_enumerate

vendor_id: int = 0x054C
product_id: int = 0x0CE6

def enumerate(vendor_id: int, product_id: int):
    """
    Enumerate HID devices with the given vendor and product IDs.
    """
    devices: list[HidDevice] = []
    info = hid_enumerate(vendor_id, product_id)
    if info is None or info.has() is False:
        return devices
    devices.append(info)
    while info.has_next():
        info = info.next()
        devices.append(info)

    return devices

print(enumerate(vendor_id, product_id))
