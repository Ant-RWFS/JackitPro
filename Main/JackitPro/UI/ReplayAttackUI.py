import curses
from .UI import UI
from .Animation import Anime


class RA_UI(UI):
    def __init__(self, panel: curses.window, nrf24, nrf24_manager):
        super().__init__(panel, nrf24, nrf24_manager)
        self.running = False

    def activate(self):
        # dot_anim = Anime("dots")
        # sonar_solid_anim = Anime("sonar_solid")
        # sonar_soft_anim = Anime("sonar_soft")
        #
        # self.add_animation("loading1", dot_anim, y=6, x=0)
        # self.add_animation("loading2", sonar_solid_anim, y=5, x=0)
        # self.add_animation("loading3", sonar_soft_anim, y=7, x=0)

        self.panel.nodelay(True)
        self.running = True

        try:
            while self.running:
                curses.napms(100)
                self.panel.clear()
                self.display_title("RA")

                # if "loading2" in self.animations:
                #     self.del_animation("loading2")

                self.update_animations()
                self.panel.refresh()

                key = self.panel.getch()
                if key in (ord('q'), ord('Q')):
                    self.running = False
        finally:
            self.panel.nodelay(False)
