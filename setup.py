from setuptools import setup


setup(
    name='dirtywords',
    version='0.0.0',
    description="portable text interface framework",
    long_description=open('README.rst').read(),
    url='https://github.com/xi/dirtywords',
    author='Tobias Bengfort',
    author_email='tobias.bengfort@posteo.de',
    packages=['dirtywords'],
    extras_require={
        'curses_core': ['curses'],
        'pygame_core': ['pygame'],
    },
    license='GPLv2+',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers'
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v2 or later '
            '(GPLv2+)',
        'Topic :: Software Development :: User Interfaces',
    ])
