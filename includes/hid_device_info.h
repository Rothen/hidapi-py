#ifndef _HIDAPI_PY_HID_DEVICE_INFO_H_
#define _HIDAPI_PY_HID_DEVICE_INFO_H_

#include "hid_device.h"

#ifdef _WIN32
    #include <hidapi.h>
#else
    #include <hidapi/hidapi.h>
#endif

#include <string>
#include <locale>
#include <codecvt>
#include <iostream>
#include <algorithm>

#include <pybind11/pybind11.h>

namespace py = pybind11;

class HidDeviceInfo {
public:
    HidDeviceInfo() : device_info({}) {}
    HidDeviceInfo(hid_device_info *ptr) : device_info(*ptr) {}
    HidDeviceInfo(HidDevice &hid_device) : device_info(*hid_get_device_info(hid_device.get_device())) {}

    std::string get_path() {return device_info.path;}
    unsigned short get_vendor_id() { return device_info.vendor_id; }
    unsigned short get_product_id() { return device_info.product_id; }
    std::wstring get_serial_number() { return device_info.serial_number; }
    unsigned short get_release_number() { return device_info.release_number; }
    std::wstring get_manufacturer_string() { return std::wstring(device_info.manufacturer_string); }
    std::wstring get_product_string() { return std::wstring(device_info.product_string); }
    unsigned short get_usage_page() { return device_info.usage_page; }
    unsigned short get_usage() { return device_info.usage; }
    int get_interface_number() { return device_info.interface_number; }
    hid_bus_type get_bus_type() { return device_info.bus_type; }
    hid_device_info *get_device_info_ptr() { return &device_info; }
    hid_device_info &get_device_info() { return device_info; }

private:
    hid_device_info device_info;
};
    
#endif // _HIDAPI_PY_HID_DEVICE_INFO_H_