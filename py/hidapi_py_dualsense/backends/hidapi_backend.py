from typing import Final

from hidapi_py import HidDeviceInfo, HidDevice, get_all_device_infos

from .backend import Backend
from .in_report import InReport, Usb01InReport, Bt01InReport, Bt31InReport, InReportLength, InvalidInReportLengthException
from .out_report import OutReport, Usb01OutReport, Bt01OutReport, Bt31OutReport
from ..mapping import (
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

SONY_VENDOR_ID: int = 0x054C
DS_PRODUCT_ID: int = 0x0CE6


class HidAPIBackend(Backend[HidDeviceInfo]):
    @staticmethod
    def get_available_devices() -> list[HidDeviceInfo]:
        return get_all_device_infos(SONY_VENDOR_ID, DS_PRODUCT_ID)

    __slots__ = (
        "_hid_device",
        "__in_report",
        "__out_report",
    )
    
    def __init__(self, hid_device_info: HidDeviceInfo):
        super().__init__()
        self._hid_device: Final[HidDevice] = HidDevice(hid_device_info.path)
        self.__in_report: InReport | None = None
        self.__out_report: OutReport | None = None

    def before_start(self):
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

    def open(self):
        self._hid_device.open()

    def close(self):
        self._hid_device.close()

    def _read(self):
        if self.__in_report is None:
            return

        self._hid_device.read(self.__in_report.data)

        self._square = uint8_bit_to_bool(self.__in_report.buttons_0, InReport.SQUARE_BIT)
        self._cross = uint8_bit_to_bool(self.__in_report.buttons_0, InReport.CROSS_BIT)
        self._circle = uint8_bit_to_bool(self.__in_report.buttons_0, InReport.CIRCLE_BIT)
        self._triangle = uint8_bit_to_bool(self.__in_report.buttons_0, InReport.TRIANGLE_BIT)
        
        self._dpad_up, self._dpad_right, self._dpad_down, self._dpad_left = uint8_value_mapping(self.__in_report.buttons_0 & 0b1111, InReport.DPAD_MAPPING)
        
        self._l1 = uint8_bit_to_bool(self.__in_report.buttons_1, InReport.L1_BIT)
        self._r1 = uint8_bit_to_bool(self.__in_report.buttons_1, InReport.R1_BIT)
        self._l2 = uint8_bit_to_bool(self.__in_report.buttons_1, InReport.L2_BIT)
        self._r2 = uint8_bit_to_bool(self.__in_report.buttons_1, InReport.R2_BIT)
        self._share = uint8_bit_to_bool(self.__in_report.buttons_1, InReport.SHARE_BIT)
        self._options = uint8_bit_to_bool(self.__in_report.buttons_1, InReport.OPTIONS_BIT)
        self._l3 = uint8_bit_to_bool(self.__in_report.buttons_1, InReport.L3_BIT)
        self._r3 = uint8_bit_to_bool(self.__in_report.buttons_1, InReport.R3_BIT)
        self._ps = uint8_bit_to_bool(self.__in_report.buttons_2, InReport.PS_BIT)
        self._touch = uint8_bit_to_bool(self.__in_report.buttons_2, InReport.TOUCH_BIT)
        self._mikrophone = uint8_bit_to_bool(self.__in_report.buttons_2, InReport.MIKROPHONE_BIT)
        self._left_joy_stick = create_joy_stick(self.__in_report.axes_0, self.__in_report.axes_1)
        self._right_joy_stick = create_joy_stick(self.__in_report.axes_2, self.__in_report.axes_3)
        self._l2_trigger = uint8_to_float(self.__in_report.axes_4, (0.0, 1.0))
        self._r2_trigger = uint8_to_float(self.__in_report.axes_5, (0.0, 1.0))
        self._accelerometer = create_accelerometer(x_0=self.__in_report.accel_x_0, x_1=self.__in_report.accel_x_1, y_0=self.__in_report.accel_y_0, y_1=self.__in_report.accel_y_1, z_0=self.__in_report.accel_z_0, z_1=self.__in_report.accel_z_1)
        self._gyroscope = create_gyroscope(x_0=self.__in_report.gyro_x_0, x_1=self.__in_report.gyro_x_1, y_0=self.__in_report.gyro_y_0, y_1=self.__in_report.gyro_y_1, z_0=self.__in_report.gyro_z_0, z_1=self.__in_report.gyro_z_1)
        self._battery = create_battery(self.__in_report.battery_0, self.__in_report.battery_1)
        self._touch_finger_1 = create_touch_finger(self.__in_report.touch_1_0, self.__in_report.touch_1_1, self.__in_report.touch_1_2, self.__in_report.touch_1_3)
        self._touch_finger_2 = create_touch_finger(self.__in_report.touch_2_0, self.__in_report.touch_2_1, self.__in_report.touch_2_2, self.__in_report.touch_2_3)
        self._left_trigger_feedback = create_trigger_feedback(self.__in_report.left_trigger_feedback)
        self._right_trigger_feedback = create_trigger_feedback(self.__in_report.right_trigger_feedback)
        self._orientation = create_orientation(self._orientation, self._accelerometer, self._gyroscope, (self._read_time - self._last_read_time) if self._last_read_time else 0.0)

    def write(self):
        """
        Write data to the device.
        """
        pass
