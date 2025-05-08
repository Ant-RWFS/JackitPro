from JackitPro.Attack import Mousejack

if __name__ == '__main__':
    mj = Mousejack.MouseJack()

    while 1:
        mj.scan()
        mj.clear_devices()
        # if mj.devices:
        #     first_device_address = list(mj.devices.keys())[0]
        #     # print(f"Sniffing device with address: {first_device_address}")
        #     mj.sniff(0.01, first_device_address)
        #     payload = list(mj.devices[first_device_address]['payload'])
        #     if payload:
        #         payload_hex = ':'.join(f'{byte:02X}' for byte in payload)
        #         print(payload_hex)
        #         mj.devices = {}
        #     else:
        #         print('no payload received')
