from __future__ import absolute_import

from .shared import unittest
from .shared import PyKeyboard
from . import shared_core

try:
    from dirtywords.stupid import Screen
    stupid = True
except ImportError:
    stupid = None


@unittest.skipIf(stupid is None, 'stupid not available')
@unittest.skipIf(PyKeyboard is None, 'PyUserInput not available')
class TestStupid(shared_core.TestCore):
    def setUp(self):
        super(TestStupid, self).setUp()
        self.scr = Screen(10, 10)

    def tearDown(self):
        self.scr.cleanup()
        super(TestStupid, self).tearDown()
