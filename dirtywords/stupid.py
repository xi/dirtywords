"""Minimal dirtywords implementation.

Simply prints to ``stdout`` with some lines space at the top.

The :py:meth:`Screen.getch` implementation should be more or less
cross-platform.

"""

from __future__ import absolute_import
from __future__ import print_function

from . import base
from .constants import KEYS


class Screen(base.Screen):
    def __init__(self, height, width):
        super(Screen, self).__init__(height, width)

        self._pressed_keys = {}

    def _getch(self, blocking=True):
        # http://code.activestate.com/recipes/134892/

        try:  # windows
            import msvcrt

            if blocking or msvcrt.kbhit():
                return ord(msvcrt.getch())

        except ImportError:  # unix
            import sys
            import termios
            import tty
            import select

            fd = sys.stdin.fileno()

            old_settings = termios.tcgetattr(fd)
            tty.setraw(sys.stdin.fileno())

            try:
                if blocking or sys.stdin in select.select(
                        [sys.stdin], [], [], 0.1)[0]:
                    return ord(sys.stdin.read(1))
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    def _codes2key(self, l):
        codes = {
            '13': KEYS['Return'],
            '127': KEYS['Backspace'],
            '27, 27': 27,
            '27, 91, 70': KEYS['End'],
            '27, 91, 72': KEYS['Home'],
            '27, 91, 50, 126': KEYS['Insert'],
            '27, 91, 51, 126': KEYS['Delete'],
            '27, 91, 53, 126': KEYS['PageUp'],
            '27, 91, 54, 126': KEYS['PageDown'],
            '27, 91, 65': KEYS['Up'],
            '27, 91, 66': KEYS['Down'],
            '27, 91, 67': KEYS['Right'],
            '27, 91, 68': KEYS['Left'],
        }
        key = ', '.join([str(i) for i in l])
        if key in codes:
            return codes[key]
        elif len(l) == 1:
            return l[0]

    def getch(self, blocking=True):
        # Convert ANSI escape sequences to key constants
        # This is implemented as a wrapper around :py:meth:`_getch` because
        # it needs to get a variable number of bytes from stdin.
        chars = [self._getch(blocking=blocking)]

        if chars == [27]:
            # TODO: single ESC is valid, so this should not block
            chars.append(self._getch())
        elif chars == [155]:
            chars = [27, 91]

        if chars[0] == 27:
            if chars[1] == 91:
                chars.append(self._getch())
                while chars[-1] not in range(64, 127):
                    chars.append(self._getch())
            elif chars[1] == 79:
                chars.append(self._getch())
            elif chars[-1] in range(64, 96):
                pass
            else:
                # invalid?
                pass

        return self._codes2key(chars)

    def refresh(self):
        spacing = '\n' * self.height * 2
        s = '\n'.join([''.join(row) for row in self.data])
        print(spacing + s.encode('utf8'))
