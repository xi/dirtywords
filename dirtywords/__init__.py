# flake8: noqa

from __future__ import absolute_import
from __future__ import unicode_literals

try:
    from .curses import Screen
except ImportError:
    try:
        from .pygame import Screen
    except ImportError:
        from .stupid import Screen

from .base import Window
from .base import AttrString
