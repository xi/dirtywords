try:
    from ncurses import curses
except ImportError:
    import curses

import base
from attr_string import AttrString


class Screen(base.Screen):
    def __init__(self, height, width):
        super(Screen, self).__init__(height, width)

        curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.curs_set(0)  # hide cursor

        # use black background everywhere
        for i in range(1, 8):
            curses.init_pair(i, i, 0)

        self.curses_window = curses.newwin(height, width, 0, 0)

    def getch(self, blocking=True):
        if blocking:
            self.curses_window.timeout(-1)
        else:
            self.curses_window.timeout(100)

        ch = self.curses_window.getch()
        if ch != -1:
            return ch

    def _get_color(self, color):
        r, g, b = color
        r = int(round(r / 255.0)) * 255
        g = int(round(g / 255.0)) * 255
        b = int(round(b / 255.0)) * 255

        if (r, g, b) == (0, 0, 0):
            return 0
        elif (r, g, b) == (255, 0, 0):
            return 1
        elif (r, g, b) == (0, 255, 0):
            return 2
        elif (r, g, b) == (255, 255, 0):
            return 3
        elif (r, g, b) == (0, 0, 255):
            return 4
        elif (r, g, b) == (255, 0, 255):
            return 5
        elif (r, g, b) == (0, 255, 255):
            return 6
        elif (r, g, b) == (255, 255, 255):
            return 7

    def putstr(self, y, x, s):
        for i, ch in enumerate(s):
            ch = AttrString(ch)
            if ch.bold:
                self.curses_window.attron(curses.A_BOLD)
            if ch.underline:
                self.curses_window.attron(curses.A_UNDERLINE)
            color = self._get_color(ch.fg_color)
            self.curses_window.attron(curses.color_pair(color))

            try:
                self.curses_window.addstr(y, x + i, ch)
            except:
                pass

            self.curses_window.attroff(curses.A_BOLD)
            self.curses_window.attroff(curses.A_UNDERLINE)

    def refresh(self):
        self.curses_window.refresh()

    def cleanup(self):
        curses.endwin()
