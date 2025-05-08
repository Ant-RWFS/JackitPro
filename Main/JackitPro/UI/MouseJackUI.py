import os
import curses
import multiprocessing
from six import iteritems
from JackitPro.UI.UI import UI
from JackitPro.Mapper.Parser import Parser

BAR_OPTIONS = {
    "Auto-PWN": {"active": True, "selectable": True},
    "All-Channels": {"active": False, "selectable": True},
    "Snipe": {"active": False, "selectable": True},
    "MalCode": {"active": False, "selectable": True},
    "Scan": {"active": False, "selectable": True},
    "Confirm": {"active": False, "selectable": True},
}


class MJ_UI(UI):
    def __init__(self, panel: curses.window, nrf24, nrf24_manager):
        super().__init__(panel, nrf24, nrf24_manager)
        self.running = False
        self.selected_option = 0
        self.bar_options = BAR_OPTIONS
        self.option_keys = list(BAR_OPTIONS.keys())
        self.first_line_options = ["Auto-PWN", "All-Channels", "Snipe"]
        self.second_line_options = ["MalCode", "Scan", "Confirm"]

        self.selected_file_content = None
        self.selected_malcode_file = None
        self.malcode_files = []
        self.selected_file_index = 0
        self.is_browsing_files = False

    def activate(self):
        self.panel.nodelay(True)
        self.running = True
        self.refresh_malcode_files()  # load file list

        try:
            while self.running:
                curses.napms(100)
                key = self.panel.getch()
                height, width = self.panel.getmaxyx()

                self.panel.clear()
                self.display_title("MJ")
                self.device_info(width, False)
                self.display_help_info(width)
                self.display_control_bar(width)
                self.handle_input(key)
                self.mouse_jack_activate(key)
                self.update_animations()
                self.panel.refresh()
        finally:
            self.panel.nodelay(False)

    def display_help_info(self, width):
        self.panel.addstr(len(self.titles["MJ"]) - 1, width - len("Q:QUIT"),
                          "Q:QUIT", curses.A_DIM)

    def display_control_bar(self, width):
        self.panel.addstr(len(self.titles["MJ"]), 0, "━" * width)

        # display first line
        for index, key in enumerate(self.first_line_options):
            option = self.bar_options[key]
            effect = curses.A_REVERSE if (index == self.selected_option and not self.is_browsing_files) else \
                curses.A_BLINK if option["active"] else curses.A_DIM
            status = " [ON]" if option["active"] else "[OFF]"
            self.panel.addstr(len(self.titles["MJ"]) + 1, index * 20,
                              f"{key.ljust(12)} {status.rjust(5)}", effect)

        # display second line
        for index, key in enumerate(self.second_line_options):
            option = self.bar_options[key]
            second_line_selected = (self.selected_option - len(self.first_line_options)) == index

            effect = curses.A_REVERSE if (second_line_selected and not self.is_browsing_files) else \
                curses.A_BLINK if (key == "Confirm" and option["active"]) else curses.A_DIM

            if key == "MalCode" and hasattr(self, 'selected_malcode_file') and self.selected_malcode_file:
                filename = os.path.basename(self.selected_malcode_file)

                display_name = filename[:5] + "..." if len(filename) > 5 else filename
                self.panel.addstr(len(self.titles["MJ"]) + 2, index * 20,
                                  f"{key.ljust(7)} {display_name.rjust(10)}", effect)

            elif key == "Scan" or "Confirm":
                info = " [ON]" if option["active"] else "[OFF]"
                self.panel.addstr(len(self.titles["MJ"]) + 2, index * 20,
                                  f"{key.ljust(13)}{info.rjust(5)}", effect)

            else:
                self.panel.addstr(len(self.titles["MJ"]) + 2, index * 20,
                                  f"{key.ljust(13)}", effect)

                # display file list
            if key == "MalCode" and second_line_selected:
                self.display_malcode_files()

    def handle_input(self, key):
        if key == -1:
            return

        if key in (ord('q'), ord('Q')):
            self.running = False

        if self.is_browsing_files:
            if key == curses.KEY_UP:
                self.selected_file_index = max(0, self.selected_file_index - 1)
            elif key == curses.KEY_DOWN:
                self.selected_file_index = min(len(self.malcode_files) - 1, self.selected_file_index + 1)
            elif key in (curses.KEY_ENTER, 10, 13):
                # select file confirmation
                selected_file = self.malcode_files[self.selected_file_index]
                if not selected_file.startswith(("No", "MalCode")):
                    self.process_selected_file(selected_file)
                self.is_browsing_files = False
            elif key == 27:
                self.is_browsing_files = False
            return

        if key == curses.KEY_LEFT:
            self.selected_option = (self.selected_option - 1) % len(self.option_keys)
        elif key == curses.KEY_RIGHT:
            self.selected_option = (self.selected_option + 1) % len(self.option_keys)
        elif key == curses.KEY_UP:
            if self.selected_option >= len(self.first_line_options):
                self.selected_option %= len(self.first_line_options)
        elif key == curses.KEY_DOWN:
            if self.selected_option < len(self.first_line_options):
                self.selected_option += len(self.first_line_options)
        elif key in (curses.KEY_ENTER, 10, 13):
            current_key = self.option_keys[self.selected_option]
            if current_key == "MalCode":
                self.refresh_malcode_files()
                self.is_browsing_files = True
                self.selected_file_index = 0
            elif current_key != "MalCode":
                self.bar_options[current_key]["active"] = not self.bar_options[current_key]["active"]

    def functions_mutex(self, key):
        if key in (curses.KEY_ENTER, 10, 13):
            current_key = self.option_keys[self.selected_option]

            if current_key in self.first_line_options:
                if self.bar_options["Auto-PWN"]["active"] and current_key != "Auto-PWN":
                    self.bar_options["Auto-PWN"]["active"] = False
                if self.bar_options["All-Channels"]["active"] and current_key != "All-Channels":
                    self.bar_options["All-Channels"]["active"] = False
                if self.bar_options["Snipe"]["active"] and current_key != "Snipe":
                    self.bar_options["Snipe"]["active"] = False

    def display_malcode_files(self):
        start_row = len(self.titles["MJ"]) + 3
        for i, filename in enumerate(self.malcode_files):
            effect = curses.A_REVERSE if (i == self.selected_file_index and self.is_browsing_files) else curses.A_DIM
            self.panel.addstr(start_row + i, 0, f"▶ {filename}" if i == self.selected_file_index else f"  {filename}",
                              effect)

    def refresh_malcode_files(self):
        malcode_dir = "JackitPro/MalCode"
        try:
            self.malcode_files = [f for f in os.listdir(malcode_dir)
                                  if f.endswith('.txt')]
            if not self.malcode_files:
                self.malcode_files = ["No .txt files found"]
        except FileNotFoundError:
            self.malcode_files = ["MalCode directory not found!"]

    def process_selected_file(self, filename):
        self.selected_malcode_file = f"./MalCode/{filename}"
        with open(f"JackitPro/MalCode/{filename}", 'r') as f:
            self.selected_file_content = f.read()

    def mouse_jack_activate(self, key):
        self.functions_mutex(key)

        try:
            if self.bar_options["Auto-PWN"]["active"]:
                self.display_detected_devices()

                if self.selected_malcode_file is None and self.option_keys[self.selected_option] != "MalCode":
                    self.panel.addstr(len(self.titles["MJ"]) + 3, 0, "No File Selected", self.font_color['YELLOW'])
                elif self.selected_malcode_file and self.nrf24.crazy_radio.device:
                    try:
                        if self.option_keys[self.selected_option] == "Scan" and key in (curses.KEY_ENTER, 10, 13):
                            self.nrf24_manager.subprocess_scan()

                        if self.nrf24_manager.process and not self.bar_options["Scan"]["active"]:
                            self.nrf24_manager.clean_subprocess()

                        if self.option_keys[self.selected_option] == "Confirm" and key in (curses.KEY_ENTER, 10, 13):
                            self.nrf24_manager.subprocess_attack(self.selected_file_content)
                            self.nrf24_manager.clean_subprocess()

                    except KeyboardInterrupt:
                        self.bar_options["Scan"]["active"] = False

        finally:
            self.nrf24.close()

    def display_detected_devices(self):
        if self.nrf24.devices:
            headers = ["KEY", "TYPE", "ADDRESS", "CHANNELS", "PAYLOAD"]
            for index, content in enumerate(headers):
                self.panel.addstr(len(self.titles["MJ"]) + 4, 15 + index * 15, str(headers[index]).ljust(15))

            detected_devices = []
            for device_address, device in iteritems(self.nrf24.devices):
                if device['device']:
                    device_type = device['device'].description()
                else:
                    device_type = 'Unknown'

                detected_devices.append([
                    device['index'],
                    device_type,
                    device_address,
                    ",".join(str(x) for x in device['channels']),
                    self.nrf24.hex_to_str(device['payload'])
                ])

                for row_index, device_data in enumerate(detected_devices):
                    for col_index, data in enumerate(device_data):
                        self.panel.addstr(len(self.titles["MJ"]) + 6 + row_index, 15 + col_index * 15,
                                          str(data).ljust(15))
        else:
            pass
