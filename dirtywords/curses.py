from __future__ import absolute_import
from __future__ import unicode_literals

import locale

try:
    from ncurses import curses
except ImportError:
    import curses

from . import base
from .constants import KEYS


class Screen(base.Screen):
    def __init__(self, height, width):
        super(Screen, self).__init__(height, width)

        curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.meta(1)
        curses.cbreak()
        curses.curs_set(0)  # hide cursor
        locale.setlocale(locale.LC_ALL, '')

        # use black background everywhere
        for i in range(1, 8):
            curses.init_pair(i, i, 0)

        self.curses_window = curses.newwin(height, width, 0, 0)
        self.curses_window.keypad(1)

    def _convert_ch(self, ch):
        mapping = {
            'Pause': curses.KEY_BREAK,
            'Down': curses.KEY_DOWN,
            'Up': curses.KEY_UP,
            'Left': curses.KEY_LEFT,
            'Right': curses.KEY_RIGHT,
            'Home': curses.KEY_HOME,
            'Backspace': curses.KEY_BACKSPACE,
            'Delete': curses.KEY_DC,
            'Insert': curses.KEY_IC,
            'PageDown': curses.KEY_NPAGE,
            'PageUp': curses.KEY_PPAGE,
            'Return': 10,
            'Print': curses.KEY_PRINT,
            'End': curses.KEY_END,
        }

        for key, curses_ch in mapping.items():
            if ch == curses_ch:
                return KEYS[key]

        if 0 <= ch < 256:
            return ch

    def getch(self, blocking=True):
        if blocking:
            self.curses_window.timeout(-1)
        else:
            self.curses_window.timeout(100)

        ch = self.curses_window.getch()
        return self._convert_ch(ch)

    def _get_color(self, color):
        r, g, b = color
        r = int(round(r / 255.0))
        g = int(round(g / 255.0))
        b = int(round(b / 255.0))

        return {
            '000': 0,
            '100': 1,
            '010': 2,
            '110': 3,
            '001': 4,
            '101': 5,
            '011': 6,
            '111': 7,
        }.get('%i%i%i' % (r, g, b))

    def putstr(self, y, x, s):
        for i, ch in enumerate(s):
            ch = base.AttrString(ch)
            if ch.strong:
                self.curses_window.attron(curses.A_BOLD)
            if ch.underline:
                self.curses_window.attron(curses.A_UNDERLINE)
            color = self._get_color(ch.fg_color)
            self.curses_window.attron(curses.color_pair(color))

            try:
                self.curses_window.addstr(y, x + i, ch.encode('utf8'))
            except Exception:
                pass

            self.curses_window.attroff(curses.A_BOLD)
            self.curses_window.attroff(curses.A_UNDERLINE)

    def refresh(self):
        self.curses_window.refresh()

    def cleanup(self):
        curses.endwin()
