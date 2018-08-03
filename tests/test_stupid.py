from __future__ import absolute_import

from dirtywords.stupid import Screen

from . import shared_core


class TestStupid(shared_core.TestCore):
    def setUp(self):
        super(TestStupid, self).setUp()
        self.scr = Screen(10, 10)

    def tearDown(self):
        self.scr.cleanup()
        super(TestStupid, self).tearDown()
