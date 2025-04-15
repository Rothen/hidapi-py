import signal
import time
from typing import Any
from threading import Event

from hidapi_py import HidDevice, get_all_device_infos

from py.hidapi_py_dualsense import DualSenseController

def signal_handler(sig: int, frame: Any, controller: DualSenseController) -> None:
    """Handles Ctrl+C to stop the session gracefully."""
    print("\nCtrl+C detected! Stopping controller...")
    controller.close()
    exit_event.set()

exit_event = Event()

sony_vendor_id: int = 0x054C
ds_product_id: int = 0x0CE6

ms_vendor_id: int = 0x045E
xbox_controller_product_id: int = 0x028E

sony_device_infos = get_all_device_infos(sony_vendor_id, ds_product_id)
# sony_device_infos = get_all_device_infos(ms_vendor_id, xbox_controller_product_id)
device = HidDevice(sony_device_infos[0].path)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, controller))

    controller = DualSenseController(device)
    controller.open()
    controller.cross_pressed(lambda: print("Cross pressed!", controller.loop_time))
    controller.cross_released(lambda: print("Cross released!"))
    while not exit_event.is_set():
        time.sleep(0.1)
