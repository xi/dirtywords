# flake8: noqa

try:
    from curses_core import Screen
except ImportError:
    try:
        from pygame_core import Screen
    except ImportError:
        from stupid_core import Screen

from base import Window
from base import AttrString
