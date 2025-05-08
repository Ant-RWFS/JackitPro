import curses
from JackitPro.UI.UI import UI
from JackitPro.UI import MouseJackUI, ReplayAttackUI, FingerPrintUI


class Main_UI(UI):
    def __init__(self, panel: curses.window, nrf24, nrf24_manager):
        super().__init__(panel, nrf24, nrf24_manager)

    def display_main_menu(self, selected_row):
        self.panel.clear()
        height, width = self.panel.getmaxyx()

        self.display_main_title(width)
        self.display_subtitle(width)
        self.device_info(width, True)
        self.display_options(width, selected_row)

        self.panel.refresh()

    def display_main_title(self, width):
        title_lines = self.titles["MAIN"]

        max_line_length = max(len(line) for line in title_lines)
        start_x = max(0, (width - max_line_length) // 2)

        for i, line in enumerate(title_lines):
            try:
                self.panel.addstr(i, start_x, line)
            except curses.error:
                pass

    def display_subtitle(self, width):
        self.panel.addstr(self.subtitle["y"], width // 2 - len(self.subtitle["content"]) // 2,
                          self.subtitle["content"], curses.A_BOLD)

    def display_options(self, width, selected_row):
        for row_index, option in enumerate(self.options["functions"]):
            y = self.options["y"] + row_index
            x = width // 2 - self.options["width"] // 2

            if row_index == selected_row:
                self.panel.attron(curses.A_REVERSE)
                self.panel.addstr(y, x, option.ljust(self.options["width"]))
                self.panel.attroff(curses.A_REVERSE)
            else:
                self.panel.addstr(y, x, option.ljust(self.options["width"]))

    def activate(self):
        curses.curs_set(0)
        current_row = 0
        self.panel.keypad(True)
        ui = Main_UI(self.panel, self.nrf24, self.nrf24_manager)
        ui.display_main_menu(current_row)

        try:
            while True:
                curses.napms(100)
                key = self.panel.getch()

                match key:
                    case curses.KEY_UP:
                        current_row = (current_row - 1) % len(ui.options["functions"])
                    case curses.KEY_DOWN:
                        current_row = (current_row + 1) % len(ui.options["functions"])
                    case curses.KEY_ENTER | 10 | 13:
                        match ui.options["functions"][current_row]:

                            case "Mouse Jack":
                                mj_ui = MouseJackUI.MJ_UI(self.panel, self.nrf24, self.nrf24_manager)
                                mj_ui.activate()
                            case "Replay Attack":
                                ra_ui = ReplayAttackUI.RA_UI(self.panel, self.nrf24, self.nrf24_manager)
                                ra_ui.activate()
                            case "Finger Print":
                                fp_ui = FingerPrintUI.FP_UI(self.panel, self.nrf24, self.nrf24_manager)
                                fp_ui.activate()
                            case "Exit":
                                break

                ui.display_main_menu(current_row)
        except KeyboardInterrupt:
            pass
        finally:
            self.panel.nodelay(False)
