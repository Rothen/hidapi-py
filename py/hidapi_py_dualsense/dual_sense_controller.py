from typing import Final
import time
from threading import Thread, Event

from reactivex.abc import DisposableBase
from hidapi_py import HidDevice, HidDeviceInfo

from .readable_value import ReadableValue, ButtonValue, ChangeCallable, ButtonPressedCallable, ButtonReleasedCallable
from .in_report import InReport, Usb01InReport, Bt01InReport, Bt31InReport, InReportLength, InvalidInReportLengthException
from .out_report import OutReport, Usb01OutReport, Bt01OutReport, Bt31OutReport
from .states import (
    Accelerometer,
    Battery,
    Gyroscope,
    JoyStick,
    Orientation,
    TouchFinger,
    TriggerFeedback
)
from .mapping import (
    uint8_value_mapping,
    uint8_bit_to_bool,
    create_battery,
    create_touch_finger,
    uint8_to_float,
    create_accelerometer,
    create_gyroscope,
    create_trigger_feedback,
    create_orientation,
    create_joy_stick
)


class DualSenseController:
    __slots__ = (
        "_hid_device",
        "__in_report",
        "__out_report",
        "_read_thread",
        "_exit_event",
        "__last_read_time",
        "_square",
        "_cross",
        "_circle",
        "_triangle",
        "_dpad_up",
        "_dpad_right",
        "_dpad_down",
        "_dpad_left",
        "_l1",
        "_r1",
        "_l2",
        "_r2",
        "_share",
        "_options",
        "_l3",
        "_r3",
        "_ps",
        "_touch",
        "_mikrophone",
        "_left_joy_stick",
        "_right_joy_stick",
        "_l2_trigger",
        "_r2_trigger",
        "_accelerometer",
        "_gyroscope",
        "_battery",
        "_touch_finger_1",
        "_touch_finger_2",
        "_left_trigger_feedback",
        "_right_trigger_feedback",
        "_orientation",
        "__read_time",
        "__loop_time"
    )

    @property
    def read_time(self) -> float:
        return self.__read_time
    
    @property
    def loop_time(self) -> float:
        return self.__loop_time

    def __init__(self, hid_device_info: HidDeviceInfo) -> None:
        self._hid_device: Final[HidDevice] = HidDevice(hid_device_info.path)
        self._read_thread: Final[Thread] = Thread(target=self._read_loop, daemon=True)
        self._exit_event: Final[Event] = Event()

        self.__in_report: InReport | None = None
        self.__out_report : OutReport | None = None
        self.__last_read_time: float = 0.0
        self.__loop_time: float = -1.0
    
        self._square: Final[ButtonValue] = ButtonValue()
        self._cross: Final[ButtonValue] = ButtonValue()
        self._circle: Final[ButtonValue] = ButtonValue()
        self._triangle: Final[ButtonValue] = ButtonValue()
        self._dpad_up: Final[ButtonValue] = ButtonValue()
        self._dpad_right: Final[ButtonValue] = ButtonValue()
        self._dpad_down: Final[ButtonValue] = ButtonValue()
        self._dpad_left: Final[ButtonValue] = ButtonValue()
        self._l1: Final[ButtonValue] = ButtonValue()
        self._r1: Final[ButtonValue] = ButtonValue()
        self._l2: Final[ButtonValue] = ButtonValue()
        self._r2: Final[ButtonValue] = ButtonValue()
        self._share: Final[ButtonValue] = ButtonValue()
        self._options: Final[ButtonValue] = ButtonValue()
        self._l3: Final[ButtonValue] = ButtonValue()
        self._r3: Final[ButtonValue] = ButtonValue()
        self._ps: Final[ButtonValue] = ButtonValue()
        self._touch: Final[ButtonValue] = ButtonValue()
        self._mikrophone: Final[ButtonValue] = ButtonValue()
        self._left_joy_stick: Final[ReadableValue[JoyStick]] = ReadableValue[JoyStick](JoyStick())
        self._right_joy_stick: Final[ReadableValue[JoyStick]] = ReadableValue[JoyStick](JoyStick())
        self._l2_trigger: Final[ReadableValue[float]] = ReadableValue[float](0.0)
        self._r2_trigger: Final[ReadableValue[float]] = ReadableValue[float](0.0)
        self._accelerometer: Final[ReadableValue[Accelerometer]] = ReadableValue[Accelerometer](Accelerometer())
        self._gyroscope: Final[ReadableValue[Gyroscope]] = ReadableValue[Gyroscope](Gyroscope())
        self._battery: Final[ReadableValue[Battery]] = ReadableValue[Battery](Battery())
        self._touch_finger_1: Final[ReadableValue[TouchFinger]] = ReadableValue[TouchFinger](TouchFinger())
        self._touch_finger_2: Final[ReadableValue[TouchFinger]] = ReadableValue[TouchFinger](TouchFinger())
        self._left_trigger_feedback: Final[ReadableValue[TriggerFeedback]] = ReadableValue[TriggerFeedback](TriggerFeedback())
        self._right_trigger_feedback: Final[ReadableValue[TriggerFeedback]] = ReadableValue[TriggerFeedback](TriggerFeedback())
        self._orientation: Final[ReadableValue[Orientation]] = ReadableValue[Orientation](Orientation())
    
    def open(self):
        self._hid_device.open()
        self._read_thread.start()

    def close(self):
        self._exit_event.set()
        self._read_thread.join()
    
    def _read_loop(self) -> None:
        data = self._hid_device.read()
        
        match len(data):
            case InReportLength.USB_01:
                self.__in_report = Usb01InReport()
                self.__out_report = Usb01OutReport()
            case InReportLength.BT_31:
                self.__in_report = Bt31InReport()
                self.__out_report = Bt31OutReport()
            case InReportLength.BT_01:
                self.__in_report = Bt01InReport()
                self.__out_report = Bt01OutReport()
            case _:
                raise InvalidInReportLengthException
        
        while not self._exit_event.is_set():
            start = time.perf_counter()
            self._hid_device.read(self.__in_report.data)
            self.__read_time = (time.perf_counter() - start) * 1000.0

            self._square.set_value(uint8_bit_to_bool(self.__in_report.buttons_0, InReport.SQUARE_BIT))
            self._cross.set_value(uint8_bit_to_bool(self.__in_report.buttons_0, InReport.CROSS_BIT))
            self._circle.set_value(uint8_bit_to_bool(self.__in_report.buttons_0, InReport.CIRCLE_BIT))
            self._triangle.set_value(uint8_bit_to_bool(self.__in_report.buttons_0, InReport.TRIANGLE_BIT))
            
            for button_value, value in zip(
                    [self._dpad_up, self._dpad_right, self._dpad_down, self._dpad_left],
                    uint8_value_mapping(self.__in_report.buttons_0 & 0b1111, InReport.DPAD_MAPPING)
                ):
                button_value.set_value(value)
            
            
            self._l1.set_value(uint8_bit_to_bool(self.__in_report.buttons_1, InReport.L1_BIT))
            self._r1.set_value(uint8_bit_to_bool(self.__in_report.buttons_1, InReport.R1_BIT))
            self._l2.set_value(uint8_bit_to_bool(self.__in_report.buttons_1, InReport.L2_BIT))
            self._r2.set_value(uint8_bit_to_bool(self.__in_report.buttons_1, InReport.R2_BIT))
            self._share.set_value(uint8_bit_to_bool(self.__in_report.buttons_1, InReport.SHARE_BIT))
            self._options.set_value(uint8_bit_to_bool(self.__in_report.buttons_1, InReport.OPTIONS_BIT))
            self._l3.set_value(uint8_bit_to_bool(self.__in_report.buttons_1, InReport.L3_BIT))
            self._r3.set_value(uint8_bit_to_bool(self.__in_report.buttons_1, InReport.R3_BIT))
            self._ps.set_value(uint8_bit_to_bool(self.__in_report.buttons_2, InReport.PS_BIT))
            self._touch.set_value(uint8_bit_to_bool(self.__in_report.buttons_2, InReport.TOUCH_BIT))
            self._mikrophone.set_value(uint8_bit_to_bool(self.__in_report.buttons_2, InReport.MIKROPHONE_BIT))
            self._left_joy_stick.set_value(create_joy_stick(self.__in_report.axes_0, self.__in_report.axes_1))
            self._right_joy_stick.set_value(create_joy_stick(self.__in_report.axes_2, self.__in_report.axes_3))
            self._l2_trigger.set_value(uint8_to_float(self.__in_report.axes_4, (0.0, 1.0)))
            self._r2_trigger.set_value(uint8_to_float(self.__in_report.axes_5, (0.0, 1.0)))
            self._accelerometer.set_value(create_accelerometer(x_0=self.__in_report.accel_x_0, x_1=self.__in_report.accel_x_1, y_0=self.__in_report.accel_y_0, y_1=self.__in_report.accel_y_1, z_0=self.__in_report.accel_z_0, z_1=self.__in_report.accel_z_1))
            self._gyroscope.set_value(create_gyroscope(x_0=self.__in_report.gyro_x_0, x_1=self.__in_report.gyro_x_1, y_0=self.__in_report.gyro_y_0, y_1=self.__in_report.gyro_y_1, z_0=self.__in_report.gyro_z_0, z_1=self.__in_report.gyro_z_1))
            self._battery.set_value(create_battery(self.__in_report.battery_0, self.__in_report.battery_1))
            self._touch_finger_1.set_value(create_touch_finger(self.__in_report.touch_1_0, self.__in_report.touch_1_1, self.__in_report.touch_1_2, self.__in_report.touch_1_3))
            self._touch_finger_2.set_value(create_touch_finger(self.__in_report.touch_2_0, self.__in_report.touch_2_1, self.__in_report.touch_2_2, self.__in_report.touch_2_3))
            self._left_trigger_feedback.set_value(create_trigger_feedback(self.__in_report.left_trigger_feedback))
            self._right_trigger_feedback.set_value(create_trigger_feedback(self.__in_report.right_trigger_feedback))
            self._orientation.set_value(create_orientation(self._orientation.value, self._accelerometer.value, self._gyroscope.value, (start - self.__last_read_time) if self.__last_read_time else 0.0))

            self.__last_read_time = start
            self.__loop_time = (time.perf_counter() - start) * 1000.0

        self._hid_device.close()

    def square_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._square.pressed(callback)

    def cross_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._cross.pressed(callback)

    def circle_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._circle.pressed(callback)

    def triangle_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._triangle.pressed(callback)

    def dpad_up_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._dpad_up.pressed(callback)

    def dpad_right_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._dpad_right.pressed(callback)

    def dpad_down_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._dpad_down.pressed(callback)

    def dpad_left_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._dpad_left.pressed(callback)

    def l1_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._l1.pressed(callback)

    def r1_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._r1.pressed(callback)

    def l2_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._l2.pressed(callback)

    def r2_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._r2.pressed(callback)

    def share_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._share.pressed(callback)

    def options_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._options.pressed(callback)

    def l3_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._l3.pressed(callback)

    def r3_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._r3.pressed(callback)

    def ps_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._ps.pressed(callback)

    def touch_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._touch.pressed(callback)

    def mikrophone_pressed(self, callback: ButtonPressedCallable) -> DisposableBase:
        return self._mikrophone.pressed(callback)

    def square_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._square.released(callback)

    def cross_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._cross.released(callback)

    def circle_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._circle.released(callback)

    def triangle_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._triangle.released(callback)

    def dpad_up_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._dpad_up.released(callback)

    def dpad_right_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._dpad_right.released(callback)

    def dpad_down_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._dpad_down.released(callback)

    def dpad_left_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._dpad_left.released(callback)

    def l1_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._l1.released(callback)

    def r1_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._r1.released(callback)

    def l2_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._l2.released(callback)

    def r2_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._r2.released(callback)

    def share_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._share.released(callback)

    def options_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._options.released(callback)

    def l3_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._l3.released(callback)

    def r3_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._r3.released(callback)

    def ps_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._ps.released(callback)

    def touch_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._touch.released(callback)

    def mikrophone_released(self, callback: ButtonReleasedCallable) -> DisposableBase:
        return self._mikrophone.released(callback)

    def left_joy_stick_changed(self, callback: ChangeCallable[JoyStick]) -> DisposableBase:
        return self._left_joy_stick.subscribe(callback)

    def right_joy_stick_changed(self, callback: ChangeCallable[JoyStick]) -> DisposableBase:
        return self._right_joy_stick.subscribe(callback)

    def l2_trigger_changed(self, callback: ChangeCallable[float]) -> DisposableBase:
        return self._l2_trigger.subscribe(callback)

    def r2_trigger_changed(self, callback: ChangeCallable[float]) -> DisposableBase:
        return self._r2_trigger.subscribe(callback)

    def accelerometer_changed(self, callback: ChangeCallable[Accelerometer]) -> DisposableBase:
        return self._accelerometer.subscribe(callback)

    def gyroscope_changed(self, callback: ChangeCallable[Gyroscope]) -> DisposableBase:
        return self._gyroscope.subscribe(callback)

    def battery_changed(self, callback: ChangeCallable[Battery]) -> DisposableBase:
        return self._battery.subscribe(callback)

    def touch_finger_1_changed(self, callback: ChangeCallable[TouchFinger]) -> DisposableBase:
        return self._touch_finger_1.subscribe(callback)

    def touch_finger_2_changed(self, callback: ChangeCallable[TouchFinger]) -> DisposableBase:
        return self._touch_finger_2.subscribe(callback)

    def left_trigger_feedback_changed(self, callback: ChangeCallable[TriggerFeedback]) -> DisposableBase:
        return self._left_trigger_feedback.subscribe(callback)

    def right_trigger_feedback_changed(self, callback: ChangeCallable[TriggerFeedback]) -> DisposableBase:
        return self._right_trigger_feedback.subscribe(callback)

    def orientation_changed(self, callback: ChangeCallable[Orientation]) -> DisposableBase:
        return self._orientation.subscribe(callback)
