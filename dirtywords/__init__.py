# flake8: noqa

try:
    from pygame_core import Screen
except ImportError:
    try:
        from curses_core import Screen
    except ImportError:
        from stupid_core import Screen

from base import Window
