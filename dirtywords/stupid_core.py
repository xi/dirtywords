"""Minimal dirtywords implementation.

Simply prints to ``stdout`` with some lines space at the top.

The :py:meth:`Screen.getch` implementation should be more or less
cross-platform.

"""

import base
from constants import KEYS


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

    def getch(self, blocking=True):
        # Convert ANSI escape sequences to key constants
        # This is implemented as a wrapper around :py:meth:`_getch` because
        # it needs to get a variable number of bytes from stdin.
        l = [self._getch()]

        if l == [27]:
            # TODO: single ESC is valid, so this should not block
            l.append(self._getch())
        elif l == [155]:
            l = [27, 91]

        if l[0] == 27:
            if l[1] == 91:
                l.append(self._getch())
                while l[-1] not in range(64, 127):
                    l.append(self._getch())
            elif l[1] == 79:
                l.append(self._getch())
            elif l[-1] in range(64, 96):
                pass
            else:
                # invalid?
                pass

        if l == [27, 27]:
            return 27
        if l == [27, 91, 68]:
            return KEYS['Left']
        elif l == [27, 91, 67]:
            return KEYS['Right']
        elif l == [27, 91, 66]:
            return KEYS['Down']
        elif l == [27, 91, 65]:
            return KEYS['Up']
        elif l == [27, 91, 54, 126]:
            return KEYS['PageDown']
        elif l == [27, 91, 53, 126]:
            return KEYS['PageUp']
        elif l == [27, 91, 51, 126]:
            return KEYS['Delete']
        elif l == [27, 91, 50, 126]:
            return KEYS['Insert']
        elif l == [127]:
            return KEYS['Backspace']
        elif l == [13]:
            return KEYS['Return']
        elif len(l) == 1:
            return l[0]
        elif l == [27, 79, 70]:
            return KEYS['End']
        elif l == [27, 79, 72]:
            return KEYS['Home']

    def refresh(self):
        spacing = '\n' * self.height * 2
        s = '\n'.join([''.join(row) for row in self.data])
        print(spacing + s.encode('utf8'))
