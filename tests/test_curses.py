from __future__ import absolute_import

from .shared import unittest
from .shared import PyKeyboard
from . import shared_core

try:
    from dirtywords.curses_core import Screen
    from dirtywords.curses_core import curses
except ImportError:
    curses = None


@unittest.skipIf(curses is None, 'curses not available')
@unittest.skipIf(PyKeyboard is None, 'PyUserInput not available')
class TestCurses(shared_core.TestCore):
    def setUp(self):
        super(TestCurses, self).setUp()
        self.scr = Screen(10, 10)

        # clear input stream
        while True:
            ch = self.scr.getch(blocking=False)
            if ch is None:
                break

    def tearDown(self):
        self.scr.cleanup()
        super(TestCurses, self).setUp()
