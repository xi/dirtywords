from __future__ import absolute_import

from .shared import unittest
from .shared import PyKeyboard
from . import shared_core

try:
    from dirtywords.pygame import Screen
    from dirtywords.pygame import pygame
except ImportError:
    pygame = None


@unittest.skipIf(pygame is None, 'pygame not available')
@unittest.skipIf(PyKeyboard is None, 'PyUserInput not available')
class TestPygame(shared_core.TestCore):
    def setUp(self):
        super(TestPygame, self).setUp()
        self.scr = Screen(10, 10)

    def tearDown(self):
        self.scr.cleanup()
        super(TestPygame, self).setUp()

    @unittest.expectedFailure
    def test_getch_upper_ascii(self):
        super(TestPygame, self).test_getch_upper_ascii()
