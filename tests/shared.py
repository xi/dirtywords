# flake8: noqa

try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from pykeyboard import PyKeyboard
except ImportError:
    PyKeyboard = None
