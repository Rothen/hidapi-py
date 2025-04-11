#ifndef _HIDAPI_PY_HID_DEVICE_H_
#define _HIDAPI_PY_HID_DEVICE_H_

#ifdef _WIN32
    #include <hidapi.h>
#else
    #include <hidapi/hidapi.h>
#endif

#include <string>
#include <locale>
#include <codecvt>
#include <vector>

#include <pybind11/pybind11.h>

#include <iostream>
#include <utility>

namespace py = pybind11;

#define MAX_BUFFER_SIZE 255

class HidDevice {
public:
    HidDevice(unsigned short vendor_id, unsigned short product_id, std::wstring serial_number, bool blocking = true) : HidDevice(false, blocking) {
        this->vendor_id = vendor_id;
        this->product_id = product_id;
        this->serial_number = std::move(serial_number);
    }

    HidDevice(std::string path, bool blocking = true) : HidDevice(true, blocking) {
        this->path = std::move(path);
    }

    ~HidDevice()
    {
        close();
    }

    int open()
    {
        if (is_opened())
            return -1;

        if (open_by_path)
        {
            hid_device_ptr = hid_open_path(path.c_str());
        }
        else
        {
            hid_device_ptr = hid_open(vendor_id, product_id, serial_number.c_str());
        }

        if (!is_opened())
        {
            return 1;
        }
        if (!blocking)
        {
            hid_set_nonblocking(hid_device_ptr, 1);
        }
        return 0;
    }

    int close()
    {
        if (is_opened())
        {
            hid_close(hid_device_ptr);
            hid_device_ptr = nullptr; // Ensure the pointer is null after closing
            return 0;
        }
        return 1;
    }

    int write(std::string &data)
    {
        const unsigned char *data_ptr = reinterpret_cast<const unsigned char *>(data.c_str());
        return hid_write(hid_device_ptr, data_ptr, data.size());
    }

    int write(py::bytes &data)
    {
        py::buffer_info info(py::buffer(data).request(true));
        return hid_write(hid_device_ptr, reinterpret_cast<unsigned char *>(info.ptr), info.size);
    }

    py::bytes read(size_t length, int timeout_ms = 0, bool blocking = false)
    {
        unsigned char *buffer = new unsigned char[length];
        int rv = read(buffer, length, timeout_ms, blocking);
        auto result = py::bytes(reinterpret_cast<const char *>(buffer), rv);
        delete[] buffer;
        return result;
    }

    py::bytes read(int timeout_ms = 0, bool blocking = false)
    {
        int rv = read(temp_read_data, MAX_BUFFER_SIZE, timeout_ms, blocking);
        return py::bytes(reinterpret_cast<const char *>(temp_read_data), rv);
    }

    int read(py::bytearray &buffer, int timeout_ms = 0, bool blocking = false)
    {
        py::buffer_info info(py::buffer(buffer).request(true));
        return read(reinterpret_cast<unsigned char *>(info.ptr), info.size, timeout_ms, blocking);
    }

    int set_nonblocking(int nonblock)
    {
        return hid_set_nonblocking(hid_device_ptr, nonblock);
    }
    
    int send_feature_report(std::string data, uint8_t report_id=0x0)
    {
        unsigned char *data_ptr = new unsigned char[data.size() + 1];
        data_ptr[0] = report_id;
        std::memcpy(data_ptr + 1, data.c_str(), data.size());
        int result = hid_send_feature_report(hid_device_ptr, data_ptr, data.size() + 1);
        delete[] data_ptr;
        return result;
    }

    int get_feature_report(uint8_t report_id, size_t length) {
        unsigned char *data_ptr = new unsigned char[length + 1];
        data_ptr[0] = report_id;
        return hid_get_feature_report(hid_device_ptr, data_ptr, length);
    }

    int get_input_report(uint8_t report_id, size_t length)
    {
        unsigned char *data_ptr = new unsigned char[length + 1];
        data_ptr[0] = report_id;
        return hid_get_input_report(hid_device_ptr, data_ptr, length);
    }

    std::string get_error() {
        std::wstring ws(hid_error(hid_device_ptr));
        return std::string(ws.begin(), ws.end());
    }

    std::wstring get_manufacturer() {
        hid_get_manufacturer_string(hid_device_ptr, temp_wchar_buffer, MAX_BUFFER_SIZE);
        return std::wstring(temp_wchar_buffer);
    }

    std::wstring get_product() {
        hid_get_product_string(hid_device_ptr, temp_wchar_buffer, MAX_BUFFER_SIZE);
        return std::wstring(temp_wchar_buffer);
    }

    std::wstring get_serial_number() {
        hid_get_serial_number_string(hid_device_ptr, temp_wchar_buffer, MAX_BUFFER_SIZE);
        return std::wstring(temp_wchar_buffer);
    }

    std::wstring get_indexed_string(int string_index) {
        hid_get_indexed_string(hid_device_ptr, string_index, temp_wchar_buffer, MAX_BUFFER_SIZE);
        return std::wstring(temp_wchar_buffer);
    }

    std::string get_report_descriptor()
    {
        hid_get_report_descriptor(hid_device_ptr, temp_char_buffer, MAX_BUFFER_SIZE);
        return std::string(reinterpret_cast<char *>(temp_char_buffer));
    }

    bool is_opened() const { return hid_device_ptr != nullptr; }

    hid_device *get_device() const { return hid_device_ptr; }

private:
    HidDevice(bool open_by_path, bool blocking) : open_by_path(open_by_path), blocking(blocking), hid_device_ptr(nullptr)
    {
    }

    int read(unsigned char *buffer, size_t length, int timeout_ms = 0, bool blocking = false)
    {
        if (timeout_ms == 0 && blocking)
        {
            timeout_ms = -1;
        }
        int rv;
        if (timeout_ms)
        {
            rv = hid_read_timeout(hid_device_ptr, buffer, length, timeout_ms);
        }
        else
        {
            rv = hid_read(hid_device_ptr, buffer, length);
        }
        return rv;
    }

    bool open_by_path;
    bool blocking;

    std::string path;
    unsigned short vendor_id;
    unsigned short product_id;
    std::wstring serial_number;

    hid_device *hid_device_ptr;
    unsigned char temp_read_data[MAX_BUFFER_SIZE];
    wchar_t temp_wchar_buffer[MAX_BUFFER_SIZE];
    unsigned char temp_char_buffer[MAX_BUFFER_SIZE];
};

#endif // _HIDAPI_PY_HID_DEVICE_H_