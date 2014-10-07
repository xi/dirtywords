from time import time


class AttrString(unicode):
    """Unicode string with additional attributes."""

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

        for attr in defaults.iterkeys():
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
        ch = unicode.__getitem__(self, i)
        return AttrString(ch, **self.get_attrs())


class Core(object):
    def __init__(self, height, width):
        """Initialize screen."""
        self.height = height
        self.width = width
        self.data = [[' ' for xx in range(width)] for yy in range(height)]
        self._pressed_keys = {}

    def getch(self, blocking=True):
        # TODO: There should be some kind of abstraction for modifiers and
        # more general any non-ascii keys.
        raise NotImplementedError

    def get_key_events(self):
        """Get iterator of keyup/down events."""

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

        for ch, detail in self._pressed_keys.items():
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

    def putstr(self, y, x, s):
        """Write string to position."""
        # TODO: handle newlines
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
    """Additional utility functions for :py:class:`Core`."""

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

    def get_key_events(self):
        return self.parent.get_key_events()

    def refresh(self):
        for y in range(self.height):
            for x in range(self.width):
                self.parent.putstr(self.y + y, self.x + x, self.data[y][x])
        self.parent.refresh()
