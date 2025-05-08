import curses
from .UI import UI
from .Animation import Anime


class FP_UI(UI):
    def __init__(self, panel: curses.window, nrf24, nrf24_manager):
        super().__init__(panel, nrf24, nrf24_manager)
        self.running = False

    def activate(self):
        self.panel.nodelay(True)
        self.running = True

        try:
            while self.running:
                curses.napms(100)
                self.panel.clear()
                self.display_title("FP")

                self.update_animations()
                self.panel.refresh()

                key = self.panel.getch()
                if key in (ord('q'), ord('Q')):
                    self.running = False
        finally:
            self.panel.nodelay(False)
