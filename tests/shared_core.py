from __future__ import absolute_import

import threading
from time import sleep

from .shared import unittest
from .shared import PyKeyboard

from dirtywords.constants import KEYS


class KeyboardUser(threading.Thread):
    def __init__(self, keyboard, keys=[], offset=0.05):
        super(KeyboardUser, self).__init__()
        self.k = keyboard
        self.keys = []
        self.offset = offset

    def add_key(self, key):
        self.keys.append(key)

    def run(self):
        for key in self.keys:
            sleep(self.offset)
            self.k.tap_key(key)


@unittest.skipIf(PyKeyboard is None, 'PyUserInput not available')
class TestCore(unittest.TestCase):
    def setUp(self):
        self.k = PyKeyboard()
        self.user = KeyboardUser(self.k)

    def tearDown(self):
        self.user.join()

    def test_getch_lower_ascii(self):
        self.user.add_key('a')
        self.user.add_key('b')
        self.user.add_key('1')
        self.user.start()

        self.assertEqual(chr(self.scr.getch()), 'a')
        self.assertEqual(chr(self.scr.getch()), 'b')
        self.assertEqual(chr(self.scr.getch()), '1')

    def test_getch_upper_ascii(self):
        self.user.add_key('A')
        self.user.start()

        self.assertEqual(chr(self.scr.getch()), 'A')

    def test_getch_arrow_controls(self):
        self.user.add_key(self.k.up_key)
        self.user.add_key(self.k.down_key)
        self.user.add_key(self.k.left_key)
        self.user.add_key(self.k.right_key)
        self.user.start()

        self.assertEqual(self.scr.getch(), KEYS['Up'])
        self.assertEqual(self.scr.getch(), KEYS['Down'])
        self.assertEqual(self.scr.getch(), KEYS['Left'])
        self.assertEqual(self.scr.getch(), KEYS['Right'])

    def test_getch_controls(self):
        self.user.add_key(self.k.backspace_key)
        self.user.add_key(self.k.return_key)
        self.user.add_key(self.k.end_key)
        self.user.add_key(self.k.home_key)
        self.user.add_key(self.k.page_up_key)
        self.user.add_key(self.k.page_down_key)
        self.user.add_key(self.k.delete_key)
        self.user.add_key(self.k.insert_key)
        self.user.start()

        self.assertEqual(self.scr.getch(), KEYS['Backspace'])
        self.assertEqual(self.scr.getch(), KEYS['Return'])
        self.assertEqual(self.scr.getch(), KEYS['End'])
        self.assertEqual(self.scr.getch(), KEYS['Home'])
        self.assertEqual(self.scr.getch(), KEYS['PageUp'])
        self.assertEqual(self.scr.getch(), KEYS['PageDown'])
        self.assertEqual(self.scr.getch(), KEYS['Delete'])
        self.assertEqual(self.scr.getch(), KEYS['Insert'])
