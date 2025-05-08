import curses
from JackitPro.UI.MainUI import Main_UI
from JackitPro.Attack.Mousejack import MouseJack
from JackitPro.Manager.ProcessManager import NRF24ProcessManager


def main(panel: curses.window):
    mousejack = MouseJack()
    nrf24PM = NRF24ProcessManager(mousejack)
    ui = Main_UI(panel, mousejack, nrf24PM)
    ui.activate()


if __name__ == "__main__":
    curses.wrapper(main)
