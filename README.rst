dirtywords - portable text interface framework

So I wanted to create a text interface and ended up creating a framework.  "Why
didn't you just stick with curses?" I hear you ask.  For two good reasons:
First, curses is not very portable.  It does not run on windows.  And it can
not be installed with pip.  The second reason of course is that I had fun with
this project.

So what is this if not curses?  You can think of it as a wrapper around curses
with a different (though similar) API.  But the interesting thing about it is
that it implements a tiny set of functions with curses and builds the rest from
there.  And this tiny core can easily be implemented with other frameworks.

There are currently three implementations of the core: One based on `curses`_,
another one based on `pygame`_, and a minimal implementation without any
dependencies outside of the standard library.

Example
-------

::

    import sys
    from dirtywords import Screen, AttrString

    text = AttrString(u'Hello World!', fg_color=(0, 255, 0))
    screen = Screen(3, len(text) + 4)
    screen.border()
    screen.putstr(1, 2, text)
    screen.refresh()

    while True:
        ch = screen.getch()
        if ch == ord('q'):
            screen.cleanup()
            sys.exit()

Tests
-----

In order to run the tests you need to have ``python-xlib`` installed.  Then
you only need to run the following command::

    tox --sitepackages


.. _curses: https://docs.python.org/2/library/curses.html
.. _pygame: http://pygame.org
