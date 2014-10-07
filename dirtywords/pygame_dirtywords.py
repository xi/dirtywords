import pygame
from pygame.locals import KEYDOWN, KEYUP

import base
from attr_string import AttrString


class Screen(base.Screen):
    def __init__(self, height, width):
        super(Screen, self).__init__(height, width)

        pygame.init()
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont('monospace', 12)
        self.fontwidth, self.fontheight = self.font.size(' ')

        self.pygame_screen = pygame.display.set_mode(
            (self.fontwidth * width, self.fontheight * height))

    def getch(self, blocking=True):
        while blocking or pygame.event.peek(KEYDOWN):
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                return event.key

    def get_key_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                yield {
                    'type': 'keydown',
                    'key': event.key,
                    'modifier': event.mod,
                }
            elif event.type == KEYUP:
                yield {
                    'type': 'keyup',
                    'key': event.key,
                    'modifier': event.mod,
                }

    def _render_ch(self, ch):
        ch = AttrString(ch)
        self.font.set_bold(ch.bold)
        self.font.set_italic(ch.italic)
        self.font.set_underline(ch.underline)
        return self.font.render(ch, False, ch.fg_color, ch.bg_color)

    def putstr(self, y, x, s):
        super(Screen, self).putstr(y, x, s)
        for i, ch in enumerate(s):
            self.pygame_screen.blit(
                self._render_ch(ch),
                ((x + i) * self.fontwidth, y * self.fontheight))

    def refresh(self):
        self.clock.tick()
        pygame.display.flip()

    def cleanup(self):
        pygame.quit()
