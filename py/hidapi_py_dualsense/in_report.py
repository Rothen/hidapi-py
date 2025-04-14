from abc import ABC
from typing import Final, TypeAlias

_IndexDict = dict[str, int]
BytesLike: TypeAlias = bytes | bytearray


class InReport(ABC):
    _OFFSET: Final[int] = 1

    @property
    def data(self) -> BytesLike:
        return self._data

    def __init__(self, index_dict: _IndexDict, data: BytesLike):
        self._index_dict: Final[_IndexDict] = index_dict
        self._data: BytesLike = data

    def update(self, data: BytesLike) -> list[str]:
        changes: list[str] = []
        for key in self._index_dict:
            if self._data[InReport._OFFSET + self._index_dict.get(key)] != data[InReport._OFFSET + self._index_dict.get(key)]:
                changes.append(key)
        self._data = data
        return changes

    def _get_uint8(self, key: str) -> int:
        return self._data[InReport._OFFSET + self._index_dict.get(key)]

    def _set_uint8(self, key: str, value: int) -> None:
        self._data[InReport._OFFSET + self._index_dict.get(key)] = value

    # ########################################## GET ##########################################

    @property
    def axes_0(self) -> int:
        return self._get_uint8('axes_0')

    @property
    def axes_1(self) -> int:
        return self._get_uint8('axes_1')

    @property
    def axes_2(self) -> int:
        return self._get_uint8('axes_2')

    @property
    def axes_3(self) -> int:
        return self._get_uint8('axes_3')

    @property
    def axes_4(self) -> int:
        return self._get_uint8('axes_4')

    @property
    def axes_5(self) -> int:
        return self._get_uint8('axes_5')

    @property
    def seq_num(self) -> int:
        return self._get_uint8('seq_num')

    @property
    def buttons_0(self) -> int:
        return self._get_uint8('buttons_0')

    @property
    def buttons_1(self) -> int:
        return self._get_uint8('buttons_1')

    @property
    def buttons_2(self) -> int:
        return self._get_uint8('buttons_2')

    @property
    def buttons_3(self) -> int:
        return self._get_uint8('buttons_3')

    @property
    def timestamp_0(self) -> int:
        return self._get_uint8('timestamp_0')

    @property
    def timestamp_1(self) -> int:
        return self._get_uint8('timestamp_1')

    @property
    def timestamp_2(self) -> int:
        return self._get_uint8('timestamp_2')

    @property
    def timestamp_3(self) -> int:
        return self._get_uint8('timestamp_3')

    @property
    def gyro_x_0(self) -> int:
        return self._get_uint8('gyro_x_0')

    @property
    def gyro_x_1(self) -> int:
        return self._get_uint8('gyro_x_1')

    @property
    def gyro_y_0(self) -> int:
        return self._get_uint8('gyro_y_0')

    @property
    def gyro_y_1(self) -> int:
        return self._get_uint8('gyro_y_1')

    @property
    def gyro_z_0(self) -> int:
        return self._get_uint8('gyro_z_0')

    @property
    def gyro_z_1(self) -> int:
        return self._get_uint8('gyro_z_1')

    @property
    def accel_x_0(self) -> int:
        return self._get_uint8('accel_x_0')

    @property
    def accel_x_1(self) -> int:
        return self._get_uint8('accel_x_1')

    @property
    def accel_y_0(self) -> int:
        return self._get_uint8('accel_y_0')

    @property
    def accel_y_1(self) -> int:
        return self._get_uint8('accel_y_1')

    @property
    def accel_z_0(self) -> int:
        return self._get_uint8('accel_z_0')

    @property
    def accel_z_1(self) -> int:
        return self._get_uint8('accel_z_1')

    @property
    def sensor_timestamp_0(self) -> int:
        return self._get_uint8('sensor_timestamp_0')

    @property
    def sensor_timestamp_1(self) -> int:
        return self._get_uint8('sensor_timestamp_1')

    @property
    def sensor_timestamp_2(self) -> int:
        return self._get_uint8('sensor_timestamp_2')

    @property
    def sensor_timestamp_3(self) -> int:
        return self._get_uint8('sensor_timestamp_3')

    @property
    def touch_1_0(self) -> int:
        return self._get_uint8('touch_1_0')

    @property
    def touch_1_1(self) -> int:
        return self._get_uint8('touch_1_1')

    @property
    def touch_1_2(self) -> int:
        return self._get_uint8('touch_1_2')

    @property
    def touch_1_3(self) -> int:
        return self._get_uint8('touch_1_3')

    @property
    def touch_2_0(self) -> int:
        return self._get_uint8('touch_2_0')

    @property
    def touch_2_1(self) -> int:
        return self._get_uint8('touch_2_1')

    @property
    def touch_2_2(self) -> int:
        return self._get_uint8('touch_2_2')

    @property
    def touch_2_3(self) -> int:
        return self._get_uint8('touch_2_3')

    @property
    def right_trigger_feedback(self) -> int:
        return self._get_uint8('right_trigger_feedback')

    @property
    def left_trigger_feedback(self) -> int:
        return self._get_uint8('left_trigger_feedback')

    @property
    def battery_0(self) -> int:
        return self._get_uint8('battery_0')

    @property
    def battery_1(self) -> int:
        return self._get_uint8('battery_1')
