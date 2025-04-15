import math
import time
import signal
from typing import Any
from threading import Event
from dataclasses import dataclass

from hidapi_py import HidDevice, get_all_device_infos

from py.hidapi_py_dualsense import Usb01InReport, InReport, DualSenseController

# buttons 0
dpad_up_bit_mask = 0b0000
dpad_right_bit_mask = 0b0010
dpad_down_bit_mask = 0b0100
dpad_left_bit_mask = 0b0110
dpad_ne_bit_mask = 0b0001
dpad_se_bit_mask = 0b0011
dpad_sw_bit_mask = 0b0101
dpad_nw_bit_mask = 0b0111
square_bit = 4
cross_bit = 5
circle_bit = 6
triangle_bit = 7

# buttons 1
l1_bit = 0
r1_bit = 1
l2_bit = 2
r2_bit = 3
share_bit = 4
options_bit = 5
l3_bit = 6
r3_bit = 7

# buttons 2
ps_bit = 0
touch_bit = 1
mikrophone_bit = 2

def signal_handler(sig: int, frame: Any, device: HidDevice) -> None:
    """Handles Ctrl+C to stop the session gracefully."""
    print("\nCtrl+C detected! Stopping controller...")
    device.close()
    exit_event.set()

exit_event = Event()

sony_vendor_id: int = 0x054C
ds_product_id: int = 0x0CE6

ms_vendor_id: int = 0x045E
xbox_controller_product_id: int = 0x028E

# sony_device_infos = get_all_device_infos(sony_vendor_id, ds_product_id)
sony_device_infos = get_all_device_infos(ms_vendor_id, xbox_controller_product_id)
device = HidDevice(sony_device_infos[0].path)
device.open()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda sig,
                    frame: signal_handler(sig, frame, device))

    report = Usb01InReport(bytearray(100))
    while not exit_event.is_set():
        start = time.perf_counter()
        data = device.read()
        print(data)
        changes = report.update(data)
        # if 'buttons_0' in changes:            
        #     buttons_0 = report.buttons_0
        #     dpad_data = buttons_0 & 0b1111
        #     dpad_up = dpad_data == dpad_up_bit_mask or dpad_data == dpad_ne_bit_mask or dpad_data == dpad_nw_bit_mask
        #     dpad_right = dpad_data == dpad_right_bit_mask or dpad_data == dpad_ne_bit_mask or dpad_data == dpad_se_bit_mask
        #     dpad_down = dpad_data == dpad_down_bit_mask or dpad_data == dpad_se_bit_mask or dpad_data == dpad_sw_bit_mask
        #     dpad_left = dpad_data == dpad_left_bit_mask or dpad_data == dpad_nw_bit_mask or dpad_data == dpad_sw_bit_mask

        #     end = time.perf_counter()
        #     print('□, x, o, ∆, DPAD:', (buttons_0 >> square_bit) & 1, (buttons_0 >> cross_bit) & 1, (buttons_0 >> circle_bit) & 1, (buttons_0 >>
        #           triangle_bit) & 1, int(dpad_up), int(dpad_right), int(dpad_down), int(dpad_left), f"Time taken: {(end - start)*1000:.0f} ms")
        # if 'buttons_1' in changes:
        #     buttons_1 = report.buttons_1
        #     print('L1, R1, L2, R2, Share, Options, L3, R3:', (buttons_1 >> l1_bit) & 1, (buttons_1 >> r1_bit) & 1, (buttons_1 >> l2_bit) & 1,
        #           (buttons_1 >> r2_bit) & 1, (buttons_1 >> share_bit) & 1, (buttons_1 >> options_bit) & 1, (buttons_1 >> l3_bit) & 1, (buttons_1 >> r3_bit) & 1)
        # if 'buttons_2' in changes:
        #     buttons_2 = report.buttons_2
        #     print('PS, Touch Pad, Mikrophone:', (buttons_2 >> ps_bit) & 1, (buttons_2 >> touch_bit) & 1, (buttons_2 >> mikrophone_bit) & 1)
        # if 'buttons_3' in changes:
        #     buttons_3 = report.buttons_3
        #     print(buttons_3)
        # if 'axes_0' in changes:
        #     axes_0 = report.axes_0
        #     print('Left Analog X:', axes_0 / 127.5 - 1) # left: -1.0, right: 1.0
        # if 'axes_1' in changes:
        #     axes_1 = report.axes_1
        #     print('Left Analog Y:', axes_1 / 127.5 - 1) # top: -1.0, bottom: 1.0
        # if 'axes_2' in changes:
        #     axes_2 = report.axes_2
        #     print('Right Analog X:', axes_2 / 127.5 - 1) # left: -1.0, right: 1.0
        # if 'axes_3' in changes:
        #     axes_3 = report.axes_3
        #     print('Right Analog Y:', axes_3 / 127.5 - 1) # top: -1.0, bottom: 1.0
        # if 'axes_4' in changes:
        #     axes_4 = report.axes_4
        #     print('L2 Trigger:', axes_4 / 255)
        # if 'axes_5' in changes:
        #     axes_5 = report.axes_5
        #     print('R2 Trigger:', axes_5 / 255)
        # if 'accel_x_0' in changes or 'accel_x_1' in changes:
        #     accel_x: int = ((report.accel_x_1 << 8) | report.accel_x_0)
        #     if accel_x > 0x7FFF:
        #         accel_x -= 0x10000
        #     print('Accel X:', accel_x)
        # if 'accel_y_0' in changes or 'accel_y_1' in changes:
        #     accel_y: int = ((report.accel_y_1 << 8) | report.accel_y_0)
        #     if accel_y > 0x7FFF:
        #         accel_y -= 0x10000
        #     print('Accel Y:', accel_y)
        # if 'accel_z_0' in changes or 'accel_z_1' in changes:
        #     accel_z: int = ((report.accel_z_1 << 8) | report.accel_z_0)
        #     if accel_z > 0x7FFF:
        #         accel_z -= 0x10000
        #     print('Accel Y:', accel_z)
        # if 'gyro_x_0' in changes or 'gyro_x_1' in changes:
        #     gyro_x: int = ((report.gyro_x_1 << 8) | report.gyro_x_0)
        #     if gyro_x > 0x7FFF:
        #         gyro_x -= 0x10000
        #     print('Accel X:', gyro_x)
        # if 'gyro_y_0' in changes or 'gyro_y_1' in changes:
        #     gyro_y: int = ((report.gyro_y_1 << 8) | report.gyro_y_0)
        #     if gyro_y > 0x7FFF:
        #         gyro_y -= 0x10000
        #     print('Accel Y:', gyro_y)
        # if 'gyro_z_0' in changes or 'gyro_z_1' in changes:
        #     gyro_z: int = ((report.gyro_z_1 << 8) | report.gyro_z_0)
        #     if gyro_z > 0x7FFF:
        #         gyro_z -= 0x10000
        #     print('Accel Y:', gyro_z)
        dual_sense_controller: DualSenseController = DualSenseController()
        dual_sense_controller.circle_pressed(lambda: print("Circle pressed!"))
        dual_sense_controller.square_pressed(lambda: print("Square pressed!"))
