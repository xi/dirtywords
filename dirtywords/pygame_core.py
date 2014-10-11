import string

import pygame
from pygame.locals import KEYDOWN, KEYUP

import base
from constants import KEYS


class Screen(base.Screen):
    def __init__(self, height, width):
        super(Screen, self).__init__(height, width)

        pygame.init()
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont('monospace', 12)
        reference_char = 'M'  # some arbitrary char to measure the fontsize
        self.fontwidth, self.fontheight = self.font.size(reference_char)

        self.pygame_screen = pygame.display.set_mode(
            (self.fontwidth * width, self.fontheight * height))

    def _convert_ch(self, ch):
        # key constants
        for key, value in KEYS.iteritems():
            if ch == getattr(pygame, 'K_' + key.upper()):
                return value

        if 0 <= ch < 256:
            if chr(ch) in string.letters:
                # capital letters on shift
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    ch ^= 32
            return ch

    def getch(self, blocking=True):
        while blocking or pygame.event.peek(KEYDOWN):
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                ch = self._convert_ch(event.key)
                if ch is not None:
                    return ch

    def get_key_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                yield {
                    'type': 'keydown',
                    'key': self._convert_ch(event.key),
                    'modifier': event.mod,
                }
            elif event.type == KEYUP:
                yield {
                    'type': 'keyup',
                    'key': self._convert_ch(event.key),
                    'modifier': event.mod,
                }

    def _render_ch(self, ch):
        ch = base.AttrString(ch)
        self.font.set_bold(ch.strong)
        self.font.set_italic(ch.emph)
        self.font.set_underline(ch.underline)

        s = self.font.render(ch, False, ch.fg_color, ch.bg_color)

        # make sure the returned surface has the right dimensions
        surface = pygame.Surface((self.fontwidth, self.fontheight))
        surface.fill(ch.bg_color)
        surface.blit(s, (0, 0))
        return surface

    def putstr(self, y, x, s):
        super(Screen, self).putstr(y, x, s)
        for i, ch in enumerate(s):
            self.pygame_screen.blit(
                self._render_ch(ch),
                ((x + i) * self.fontwidth, y * self.fontheight),
                area=(0, 0, self.fontwidth, self.fontheight))

    def refresh(self):
        self.clock.tick()
        pygame.display.flip()

    def cleanup(self):
        pygame.quit()
