#include "hid_device_info.h"
#include "hid_device.h"
#include "config.h"

#ifdef _WIN32
    #include <hidapi.h>
#else
    #include <hidapi/hidapi.h>
#endif

#include <string>
#include <locale>
#include <codecvt>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(hidapi_py, m) {
    m.doc() = "HIDAPI C++ bindings";

    m.attr("__version__") = "1.0.0";
#ifdef HID_API_VERSION_STR
    m.attr("__hid_version__") = HID_API_VERSION_STR;
#else
    m.attr("__hid_version__") = "Unknown";
#endif
    
#ifdef HID_API_HAS_BUS_TYPE
    py::enum_<hid_bus_type>(m, "HidBusType")
        .value("UNKNOWN", HID_API_BUS_UNKNOWN)
        .value("USB", HID_API_BUS_USB)
        .value("BLUETOOTH", HID_API_BUS_BLUETOOTH)
        .value("I2C", HID_API_BUS_I2C)
        .value("SPI", HID_API_BUS_SPI);
#endif

    py::class_<HidDeviceInfo>(m, "HidDeviceInfo")
        .def(py::init<>())
        .def_property_readonly("path", &HidDeviceInfo::get_path, "Platform-specific device path")
        .def_property_readonly("vendor_id", &HidDeviceInfo::get_vendor_id, "Device Vendor ID")
        .def_property_readonly("product_id", &HidDeviceInfo::get_product_id, "Device Product ID")
        .def_property_readonly("serial_number", &HidDeviceInfo::get_serial_number, "Serial Number")
        .def_property_readonly("release_number", &HidDeviceInfo::get_release_number, "Device Release Number in binary-coded decimal")
        .def_property_readonly("manufacturer_string", &HidDeviceInfo::get_manufacturer_string, "Manufacturer String")
        .def_property_readonly("product_string", &HidDeviceInfo::get_product_string, "Product String")
        .def_property_readonly("usage_page", &HidDeviceInfo::get_usage_page, "Usage Page for this Device/Interface")
        .def_property_readonly("usage", &HidDeviceInfo::get_usage, "Usage for this Device/Interface")
        .def_property_readonly("interface_number", &HidDeviceInfo::get_interface_number, "USB interface which this logical device represents")
        .def_property_readonly("bus_type", &HidDeviceInfo::get_bus_type, "Underly bus type");

    py::class_<HidDevice>(m, "HidDevice")
        .def(py::init<unsigned short, unsigned short, std::wstring, bool>(),
             py::arg("vendor_id"), py::arg("product_id"), py::arg("serial_number"), py::arg("blocking") = true)
        .def(py::init<std::string, bool>(), py::arg("path"), py::arg("blocking") = true)
        .def("open", &HidDevice::open)
        .def("close", &HidDevice::close)
        .def("write", py::overload_cast<std::string &>(&HidDevice::write), py::arg("data"), "Write string data to the device")
        .def("write", py::overload_cast<py::bytes &>(&HidDevice::write), py::arg("data"), "Write bytes data to the device")
        .def("read", py::overload_cast<size_t, int, bool>(&HidDevice::read), py::arg("length"), py::arg("timeout_ms") = 0, py::arg("blocking") = false)
        .def("read", py::overload_cast<int, bool>(&HidDevice::read), py::arg("timeout_ms") = 0, py::arg("blocking") = false)
        .def("read", py::overload_cast<py::bytearray &, int, bool>(&HidDevice::read), py::arg("buffer"), py::arg("timeout_ms") = 0, py::arg("blocking") = false)
        .def("set_nonblocking", &HidDevice::set_nonblocking, py::arg("nonblocking"), "Set non-blocking mode")
        .def("send_feature_report", &HidDevice::send_feature_report, py::arg("data"), py::arg("report_id") = 0x0, "Send feature report to the device")
        .def("get_feature_report", &HidDevice::get_feature_report, py::arg("report_id"), py::arg("length"), "Get feature report from the device")
        .def("get_manufacturer", &HidDevice::get_manufacturer, "Get manufacturer string from the device")
        .def("get_product", &HidDevice::get_product, "Get product string from the device")
        .def("get_serial_number", &HidDevice::get_serial_number, "Get serial number string from the device")
        .def("get_indexed_string", &HidDevice::get_indexed_string, py::arg("string_index"), "Get indexed string from the device")
        .def("get_report_descriptor", &HidDevice::get_report_descriptor, "Get report descriptor from the device")
        .def("get_error", &HidDevice::get_error, "Get error string from the device")
        .def("is_opened", &HidDevice::is_opened, "Check if the device is opened");

    m.def("hid_init", &hid_init, "Initialize the HIDAPI library");
    m.def("hid_exit", &hid_exit, "Finalize the HIDAPI library");
    m.def("get_all_device_infos", [](unsigned short vendor_id, unsigned short product_id)
        {
            hid_device_info *first_device_info = hid_enumerate(vendor_id, product_id);
            hid_device_info *device_info{first_device_info};
            std::vector<HidDeviceInfo> device_info_list;

            while (device_info != nullptr) {
                device_info_list.push_back(HidDeviceInfo(device_info));
                device_info = device_info->next;
            }

            hid_free_enumeration(first_device_info);

            return device_info_list;
            
        }, py::arg("vendor_id"), py::arg("product_id"), "Enumerate HID devices");
}