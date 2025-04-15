import signal
from typing import Any
from threading import Event

from hidapi_py import HidDevice, get_all_device_infos

from py.hidapi_py_dualsense import DualSenseController
from py.hidapi_py_dualsense.states import Orientation
from py.hidapi_py_dualsense.mapping import (
    uint8_value_mapping,
    uint8_bit_to_bool,
    create_battery,
    create_touch_finger,
    uint8_to_float,
    create_accelerometer,
    create_gyroscope,
    create_trigger_feedback,
    create_orientation
)

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

dpad_mapping: list[list[int]] = [
    [dpad_up_bit_mask, dpad_ne_bit_mask, dpad_nw_bit_mask],
    [dpad_right_bit_mask, dpad_ne_bit_mask, dpad_se_bit_mask],
    [dpad_down_bit_mask, dpad_se_bit_mask, dpad_sw_bit_mask],
    [dpad_left_bit_mask, dpad_nw_bit_mask, dpad_sw_bit_mask]
]
last_read_time: float | None = None
orientation: Orientation = Orientation()    

if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, controller))

    controller = DualSenseController(device)
    controller.open()
    controller.cross_pressed(lambda: print("Cross pressed!"))
    controller.cross_released(lambda: print("Cross released!"))
    while not exit_event.is_set():
        '''start = time.perf_counter()
        read_time = time.perf_counter()
        device.read(report.data)

        buttons_0 = report.buttons_0
        buttons_1 = report.buttons_1
        buttons_2 = report.buttons_2
        buttons_3 = report.buttons_3
        axes_0 = report.axes_0
        axes_1 = report.axes_1
        axes_2 = report.axes_2
        axes_3 = report.axes_3
        axes_4 = report.axes_4
        axes_5 = report.axes_5
        
        accel_x_0 = report.accel_x_0
        accel_x_1 = report.accel_x_1
        accel_y_0 = report.accel_y_0
        accel_y_1 = report.accel_y_1
        accel_z_0 = report.accel_z_0
        accel_z_1 = report.accel_z_1

        gyro_x_0 = report.gyro_x_0
        gyro_x_1 = report.gyro_x_1
        gyro_y_0 = report.gyro_y_0
        gyro_y_1 = report.gyro_y_1
        gyro_z_0 = report.gyro_z_0
        gyro_z_1 = report.gyro_z_1

        square = uint8_bit_to_bool(buttons_0, square_bit)
        cross = uint8_bit_to_bool(buttons_0, cross_bit)
        circle = uint8_bit_to_bool(buttons_0, circle_bit)
        triangle = uint8_bit_to_bool(buttons_0, triangle_bit)
        
        dpad_up, dpad_right, dpad_down, dpad_left = uint8_value_mapping(buttons_0 & 0b1111, dpad_mapping)
        
        l1 = uint8_bit_to_bool(buttons_1, l1_bit)
        r1 = uint8_bit_to_bool(buttons_1, r1_bit)
        l2 = uint8_bit_to_bool(buttons_1, l2_bit)
        r2 = uint8_bit_to_bool(buttons_1, r2_bit)
        share = uint8_bit_to_bool(buttons_1, share_bit)
        options = uint8_bit_to_bool(buttons_1, options_bit)
        l3 = uint8_bit_to_bool(buttons_1, l3_bit)
        r3 = uint8_bit_to_bool(buttons_1, r3_bit)
        ps = uint8_bit_to_bool(buttons_2, ps_bit)
        touch = uint8_bit_to_bool(buttons_2, touch_bit)
        mikrophone = uint8_bit_to_bool(buttons_2, mikrophone_bit)
        
        left_joy_stick_x = uint8_to_float(axes_0, (-1.0, 1.0))
        
        left_joy_stick_y = uint8_to_float(axes_1, (-1.0, 1.0))

        right_joy_stick_x = uint8_to_float(axes_2, (-1.0, 1.0))

        right_joy_stick_y = uint8_to_float(axes_3, (-1.0, 1.0))
        
        l2_trigger = uint8_to_float(axes_4, (0.0, 1.0))
                
        r2_trigger = uint8_to_float(axes_5, (0.0, 1.0))
                
        accelerometer = create_accelerometer(x_0=accel_x_0, x_1=accel_x_1, y_0=accel_y_0, y_1=accel_y_1, z_0=accel_z_0, z_1=accel_z_1)
                
        gyroscope = create_gyroscope(x_0=gyro_x_0, x_1=gyro_x_1, y_0=gyro_y_0, y_1=gyro_y_1, z_0=gyro_z_0, z_1=gyro_z_1)
                
        battery = create_battery(report.battery_0, report.battery_1)
                
        touch_finger_1 = create_touch_finger(report.touch_1_0, report.touch_1_1, report.touch_1_2, report.touch_1_3)
                
        touch_finger_2 = create_touch_finger(report.touch_2_0, report.touch_2_1, report.touch_2_2, report.touch_2_3)
                
        left_trigger_feedback = create_trigger_feedback(report.left_trigger_feedback)
                
        right_trigger_feedback = create_trigger_feedback(report.right_trigger_feedback)
        
        orientation = create_orientation(orientation, accelerometer, gyroscope, read_time - last_read_time) if last_read_time else create_orientation(orientation, accelerometer, gyroscope, 0.0)
        
        # print('□, x, o, ∆:', square, cross, circle, triangle)
        # print('DPAD:', dpad_up, dpad_right, dpad_down, dpad_left)
        # print('L1, R1, L2, R2, Share, Options, L3, R3:', l1, r1, l2, r2, share, options, l3, r3)
        # print('PS, Touch Pad, Mikrophone:', ps, touch, mikrophone)
        # print('Left Joy Stick X:', left_joy_stick_x)  # left: -1.0, right: 1.0
        # print('Left Joy Stick Y:', left_joy_stick_y)  # top: -1.0, bottom: 1.0
        # print('Right Joy Stick X:', right_joy_stick_x)  # left: -1.0, right: 1.0
        # print('Right Joy Stick Y:', right_joy_stick_y)  # top: -1.0, bottom: 1.0
        # print('L2 Trigger:', l2_trigger)
        # print('R2 Trigger:', r2_trigger)
        # print('Accelerometer:', accelerometer)
        # print('Gyroscope:', gyroscope)
        # print('Battery:', battery)
        # print("Touch Finger 1", touch_finger_1)
        # print("Touch Finger 2", touch_finger_2)
        # print("Left Trigger Feedback", left_trigger_feedback)
        # print("Right Trigger Feedback", right_trigger_feedback)
        # print('Orientation:', orientation)
        
        last_read_time = read_time
        end = time.perf_counter()
        # print('Time taken:', "%.1f ms" % ((end - start) * 1000))'''
