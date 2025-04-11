from hidapi_py import HidDevice, get_all_device_infos

vendor_id: int = 0x054C
product_id: int = 0x0CE6

device_infos = get_all_device_infos(vendor_id, product_id)
# device_infos = get_all_device_infos(0, 0)

for i, device_info in enumerate(device_infos):
    if device_info.vendor_id in [5426, 2821, 1133]:
        continue
    try:
        device = HidDevice(device_info.path)
        if device.open() != 0:
            continue
        print(device.get_manufacturer())
        print(device.get_product())
        device.close()
        print('###########################################')
    except Exception as e:
        pass
