"""Minimal dirtywords implementation.

Simply prints to ``stdout`` with some lines space at the top.

The :py:meth:`Screen.getch` implementation should be more or less
cross-platform.

"""

import base


class Screen(base.Screen):
    def __init__(self, height, width):
        super(Screen, self).__init__(height, width)

        self._pressed_keys = {}

    def getch(self, blocking=True):
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

    def refresh(self):
        spacing = '\n' * self.height * 2
        s = '\n'.join([''.join(row) for row in self.data])
        print(spacing + s.encode('utf8'))
