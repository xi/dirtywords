"""
dirtywords is based on multiple implementations of the :py:class:`Core` class.
On top of that, the :py:class:`Screen`-API is implemented. This is what you
work with most of the time.

The screen API is accompanied by :py:class:`Window` (a screen implementation
that uses an existing screen object rather than an external framework) and
:py:class:`AttrString` for easy string formatting.

A new core implementation should be derived from :py:class:`Screen` and
must provide implementations for all low-level functions.  It may also provide
optimised implementations of high-level functionality.

When importing directly from :py:mod:`dirtywords`, the "best" available
implementation is chosen.

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from time import time
import string

import six

from .constants import KEYS


class AttrString(six.text_type):
    """String with additional attributes.

    Rather than specifying formatting information with :py:meth:`Core.putstr`,
    it is saved with the string object itself. This way the formatting can be
    used for further computation before printing it to the screen.

    :py:class:`AttrString` is derived from :py:class:`unicode`. You need to
    take care of proberly decoding byte-strings yourself.

    ========= ========= ================
    name      type      description
    ========= ========= ================
    emph      bool      emphasis
    strong    bool      strong emphasis
    underline bool      underline text
    fg_color  (r, g, b) foreground color
    bg_color  (r, g, b) background color
    ========= ========= ================

    Example::

        AttrString(u'Hello World!', strong=True, fg_color=(0, 255, 0))


    """

    def __new__(cls, s, **kwargs):
        self = super(AttrString, cls).__new__(cls, s)
        self.set_attrs(s, **kwargs)
        return self

    def set_attrs(self, reference='', **kwargs):
        defaults = {
            'strong': False,
            'emph': False,
            'underline': False,
            'fg_color': (255, 255, 255),
            'bg_color': (0, 0, 0),
        }

        for attr in kwargs:
            if attr not in defaults:
                raise TypeError('No such attribute: %s' % attr)

        for attr in defaults.keys():
            if attr in kwargs:
                value = kwargs[attr]
            elif isinstance(reference, AttrString):
                value = getattr(reference, attr)
            else:
                value = defaults[attr]

            setattr(self, attr, value)

    def get_attrs(self):
        return {
            'strong': self.strong,
            'emph': self.emph,
            'underline': self.underline,
            'fg_color': self.fg_color,
            'bg_color': self.bg_color,
        }

    def __iter__(self):
        return (self[i] for i in range(len(self)))

    def __getitem__(self, i):
        ch = super(AttrString, self).__getitem__(i)
        return AttrString(ch, **self.get_attrs())


class Core(object):
    """Minimal core on which everything else is based."""

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.data = [[' ' for xx in range(width)] for yy in range(height)]

    def getch(self, blocking=True):
        """Get a character from ``stdin``."""
        # TODO: There should be some kind of abstraction for modifiers and
        # more general any non-ascii keys.
        raise NotImplementedError

    def putstr(self, y, x, s):
        """Write string to position."""
        for i, ch in enumerate(s):
            try:
                self.data[y][x + i] = ch
            except IndexError:
                pass

    def refresh(self):
        """Print the current state to the screen."""
        raise NotImplementedError

    def cleanup(self):
        """Deinitialize screen."""
        pass


class Screen(Core):
    """Additional text interface utilities build on top of :py:class:`Core`."""

    def __init__(self, height, width):
        super(Screen, self).__init__(height, width)
        self._pressed_keys = {}

    def get_key_events(self):
        """Get iterator of keyup/-down events.

        The events are dictionaries of the form::

            {
                'type': 'keyup',
                'key': 32,
            }

        The default implementation tries to emulate these using
        :py:meth:`getch`.  It includes a short delay so that only one keydown
        and one keyup event is triggered on repeated key presses.

        """

        # 0.  The key is not pressed. Nothing happens.
        # 1.  The key is initially pressed.
        #     -   trigger keydown event
        #     -   enter phase 0
        # 2.  if Key is pressed again:
        #     -   enter phase 2
        #     else:
        #     -   trigger keyup event
        #     -   enter phase 1
        #     2.1   Key is pressed again
        #         -   trigger key down event
        #         -   enter phase 2
        # 3.  key is pressed again
        #     -   update timestamp
        # 4.  Timeout
        #     -   trigger keyup event
        #     -   enter phase -1

        now = time()
        threshold = now - 0.1

        for ch, detail in list(self._pressed_keys.items()):
            t, phase = detail
            if t < threshold:
                del self._pressed_keys[ch]
                if phase != 1:
                    yield {
                        'type': 'keyup',
                        'key': ch,
                        'phase': phase,
                    }
            # TODO if ch is pressed this will generate a redundant up/down pair
            elif phase == 0:
                yield {
                    'type': 'keyup',
                    'key': ch,
                    'phase': phase,
                }
                self._pressed_keys[ch] = (now, 1)

        ch = self.getch(blocking=False)
        if ch is not None:
            if ch not in self._pressed_keys:
                yield {
                    'type': 'keydown',
                    'key': ch,
                    'phase': -1,
                }
                self._pressed_keys[ch] = (now, 0)
            else:
                t, phase = self._pressed_keys[ch]
                if phase == 1:
                    yield {
                        'type': 'keydown',
                        'key': ch,
                        'phase': phase,
                    }
                self._pressed_keys[ch] = (now, 2)

    def getkey(self, blocking=True):
        """Wrapper around :py:meth:`getch` that returns unicode if possible."""
        ch = self.getch(blocking=blocking)

        if ch is not None:
            if ch in KEYS.values():
                return ch

            elif 127 < ch < 256:  # interpret as utf8
                nbytes = bin(ch)[3:].find('0')
                chars = [ch]
                for i in range(nbytes):
                    chars.append(self.getch())
                s = ''.join([chr(c) for c in chars])
                return s.decode('utf8')

            elif ch < 256 and chr(ch) in string.printable:
                return six.text_type(chr(ch))

        if blocking:
            return self.getkey(blocking=blocking)

    def delch(self, y, x):
        """Delete character at position."""
        self.putstr(y, x, ' ')

    def fill_row(self, y, ch):
        """Fill a complete row with character."""
        self.putstr(y, 0, ch * self.width)

    def fill_column(self, x, ch):
        """Fill a complete column with character."""
        for y in range(self.height):
            self.putstr(y, x, ch)

    def fill(self, ch):
        """Fill whole screen with character."""
        for y in range(self.height):
            self.fill_row(y, ch)

    def clear(self):
        """Clear whole screen."""
        self.fill(' ')

    def border(self, ls='|', rs='|', ts='-', bs='-',
               tl='+', tr='+', bl='+', br='+'):
        """Draw border around screen."""
        self.fill_column(0, ls)
        self.fill_column(self.width - 1, rs)
        self.fill_row(0, ts)
        self.fill_row(self.height - 1, bs)
        self.putstr(0, 0, tl)
        self.putstr(0, self.width - 1, tr)
        self.putstr(self.height - 1, 0, bl)
        self.putstr(self.height - 1, self.width - 1, br)


class Window(Screen):
    """A screen that is rendered onto another screen."""

    def __init__(self, parent, height, width, y, x):
        super(Window, self).__init__(height, width)
        self.parent = parent
        self.y = y
        self.x = x

    def getch(self, blocking=True):
        return self.parent.getch(blocking=blocking)

    def get_key_events(self):
        return self.parent.get_key_events()

    def refresh(self):
        for y in range(self.height):
            for x in range(self.width):
                self.parent.putstr(self.y + y, self.x + x, self.data[y][x])
        self.parent.refresh()
