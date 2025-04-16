from __future__ import annotations
from typing import Type

from hidapi_py import get_all_device_infos

from .hidapi_device_info import HidDeviceInfo
from .backend import Backend


SONY_VENDOR_ID: int = 0x054C
DS_PRODUCT_ID: int = 0x0CE6


class HidAPIBackend(Backend[HidDeviceInfo]):
    @staticmethod
    def _get_available_devices() -> list[HidDeviceInfo]:
        return [HidDeviceInfo(hid_device_info.path, hid_device_info) for hid_device_info in get_all_device_infos(SONY_VENDOR_ID, DS_PRODUCT_ID)]

    @staticmethod
    def _init() -> Type[HidAPIBackend]:
        return HidAPIBackend

    @staticmethod
    def _quit() -> None:
        pass
