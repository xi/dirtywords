# flake8: noqa

from __future__ import absolute_import

try:
    from .curses import Screen
except ImportError:
    try:
        from .pygame import Screen
    except ImportError:
        from .stupid import Screen

from .base import Window
from .base import AttrString
