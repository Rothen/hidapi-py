import time
import signal
from typing import Any
from threading import Event

from hidapi_py import HidDevice, get_all_device_infos

from py.hidapi_py_dualsense import Usb01InReport

dpad_up_bit_mask = 0b0000  # buttons_0
dpad_right_bit_mask = 0b0010  # buttons_0
dpad_down_bit_mask = 0b0100  # buttons_0
dpad_left_bit_mask = 0b0110  # buttons_0

dpad_ne_bit_mask = 0b0001  # buttons_0
dpad_se_bit_mask = 0b0011  # buttons_0
dpad_sw_bit_mask = 0b0101  # buttons_0
dpad_nw_bit_mask = 0b0111  # buttons_0

square_bit = 4 # buttons_0
cross_bit = 5 # buttons_0
circle_bit = 6 # buttons_0
triangle_bit = 7 # buttons_0

def signal_handler(sig: int, frame: Any, device: HidDevice) -> None:
    """Handles Ctrl+C to stop the session gracefully."""
    print("\nCtrl+C detected! Stopping controller...")
    device.close()
    exit_event.set()

exit_event = Event()

vendor_id: int = 0x054C
product_id: int = 0x0CE6

sony_device_infos = get_all_device_infos(vendor_id, product_id)
device = HidDevice(sony_device_infos[0].path)
device.open()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda sig,
                    frame: signal_handler(sig, frame, device))

    report = Usb01InReport(bytearray(100))
    while not exit_event.is_set():
        start = time.perf_counter()
        changes = report.update(device.read())
        if 'buttons_0' in changes:            
            buttons_0 = report.buttons_0
            dpad_data = buttons_0 & 0b1111
            dpad_up = dpad_data == dpad_up_bit_mask or dpad_data == dpad_ne_bit_mask or dpad_data == dpad_nw_bit_mask
            dpad_right = dpad_data == dpad_right_bit_mask or dpad_data == dpad_ne_bit_mask or dpad_data == dpad_se_bit_mask
            dpad_down = dpad_data == dpad_down_bit_mask or dpad_data == dpad_se_bit_mask or dpad_data == dpad_sw_bit_mask
            dpad_left = dpad_data == dpad_left_bit_mask or dpad_data == dpad_nw_bit_mask or dpad_data == dpad_sw_bit_mask

            end = time.perf_counter()
            print('□, x, o, ∆, DPAD:', (buttons_0 >> square_bit) & 1, (buttons_0 >> cross_bit) & 1, (buttons_0 >> circle_bit) & 1, (buttons_0 >>
                  triangle_bit) & 1, int(dpad_up), int(dpad_right), int(dpad_down), int(dpad_left), f"Time taken: {(end - start)*1000:.0f} ms")
