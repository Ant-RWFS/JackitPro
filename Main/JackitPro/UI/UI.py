import curses

TITLES = {
    "MAIN":
        [
            "   █ █▀▀▄ █▀▀▄ █ ▄▀ ▀█▀ ▀▀█▀▀    █▀▀█ █▀▀▄ █▀▀▀█",
            "   █ █▄▄█ █    █▀▄   █    █  ▀▀▀ █▄▄█ █▄▄▀ █   █",
            "█▄▄█ █  █ █▄▄▀ █  █ ▄█▄   █      █    █  █ █▄▄▄█"
        ],

    "MJ":
        [
            "█▀▄▀█ █▀▀▀█ █  █ █▀▀▀█ █▀▀▀    █ █▀▀▄ █▀▀▄ █ ▄▀",
            "█ █ █ █   █ █  █ ▀▀▀▄▄ █▀▀▀    █ █▄▄█ █    █▀▄ ",
            "█   █ █▄▄▄█ ▀▄▄▀ █▄▄▄█ █▄▄▄ █▄▄█ █  █ █▄▄▀ █  █"
        ],

    "RA":
        [
            "█▀▀▄ █▀▀▀ █▀▀█ █    █▀▀▄ █   █ █▀▀▄ ▀▀█▀▀ ▀▀█▀▀ █▀▀▄ █▀▀▄ █ ▄▀",
            "█▄▄▀ █▀▀▀ █▄▄█ █    █▄▄█ ▀▄▄▄▀ █▄▄█   █     █   █▄▄█ █    █▀▄ ",
            "█  █ █▄▄▄ █    █▄▄█ █  █   █   █  █   █     █   █  █ █▄▄▀ █  █"
        ],

    "FP":
        [
            "█▀▀▀ ▀█▀ █▄  █ █▀▀█ █▀▀▀ █▀▀▄ █▀▀█ █▀▀▄ ▀█▀ █▄  █ ▀▀█▀▀",
            "█▀▀   █  █ █ █ █ ▄▄ █▀▀▀ █▄▄▀ █▄▄█ █▄▄▀  █  █ █ █   █  ",
            "█    ▄█▄ █  ▀█ █▄▄▀ █▄▄▄ █  █ █    █  █ ▄█▄ █  ▀█   █  "
        ]
}

SUBTITLE = {
    "content": "Provided by Ant-RWFS",
    "y": len(TITLES["MAIN"]) + 1
}

OPTIONS = {
    "functions": ["Mouse Jack", "Replay Attack", "Finger Print", "Exit"],
    "width": 20,
    "y": SUBTITLE["y"] + 2
}


def init_font_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

    return {
        'RED': curses.color_pair(1),
        'GREEN': curses.color_pair(2),
        'BLUE': curses.color_pair(3),
        'YELLOW': curses.color_pair(4),
        'CYAN': curses.color_pair(5),
        'MAGENTA': curses.color_pair(6),
        'WHITE': curses.color_pair(7),
        'DEFAULT': curses.A_NORMAL
    }


class UI:
    def __init__(self, panel: curses.window, nrf24, nrf24_manager):
        self.nrf24 = nrf24
        self.nrf24_manager = nrf24_manager
        self.panel = panel
        self.animations = {}
        self.titles = TITLES
        self.subtitle = SUBTITLE
        self.options = OPTIONS
        self.font_color = init_font_colors()

    def add_animation(self, name, anim_instance, y=0, x=0):
        self.animations[name] = (anim_instance, y, x)

    def del_animation(self, name):
        del self.animations[name]

    def update_animations(self):
        for name, (anim, y, x) in self.animations.items():
            current_frame = anim.update()
            self.panel.addstr(y, x, current_frame)

    def display_title(self, module):
        for i, line in enumerate(TITLES[module]):
            try:
                self.panel.addstr(i, 0, line)
            except curses.error:
                pass

    def device_info(self, width, main):
        if self.nrf24.crazy_radio.device:
            device_info = "NRF24 Connected"
            if main:
                self.panel.addstr(self.subtitle["y"] + 1, width // 2 - len(device_info) // 2,
                                  device_info, self.font_color['GREEN'])
            else:
                self.panel.addstr(0, width - len(device_info),
                                  device_info, self.font_color['GREEN'])

        else:
            device_info = "ERROR:NRF24 Disconnected!"
            if main:
                self.panel.addstr(self.subtitle["y"] + 1, width // 2 - len(device_info) // 2,
                                  device_info, self.font_color['YELLOW'])
            else:
                self.panel.addstr(0, width - len(device_info),
                                  device_info, self.font_color['YELLOW'])
