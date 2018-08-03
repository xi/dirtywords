import sys
from time import sleep

from dirtywords import Screen, AttrString
from dirtywords.constants import KEYS


class Player(object):
    def __init__(self, win):
        self.win = win
        self.y = win.height / 2
        self.x = win.width / 2
        self.direction = 'stop'

    def move(self):
        self.win.putstr(self.y, self.x, ' ')

        if self.direction == 'up':
            self.y -= 1
        elif self.direction == 'right':
            self.x += 1
        elif self.direction == 'down':
            self.y += 1
        elif self.direction == 'left':
            self.x -= 1

        s = AttrString('X', strong=True, fg_color=(0, 0, 255))
        self.win.putstr(self.y, self.x, s)
        self.win.refresh()
        sleep(0.05)


if __name__ == '__main__':
    scr = Screen(32, 100)

    try:
        scr.border()

        player = Player(scr)
        player.move()  # initial refresh

        while 1:
            for event in scr.get_key_events():
                if event['type'] == 'keydown':
                    if event['key'] in [ord('h'), KEYS['Left']]:
                        player.direction = 'left'
                    elif event['key'] in [ord('j'), KEYS['Down']]:
                        player.direction = 'down'
                    elif event['key'] in [ord('k'), KEYS['Up']]:
                        player.direction = 'up'
                    elif event['key'] in [ord('l'), KEYS['Right']]:
                        player.direction = 'right'
                    elif event['key'] == ord('q'):
                        scr.cleanup()
                        sys.exit()
                elif event['type'] == 'keyup':
                    player.direction = 'stop'
            player.move()
    except Exception:
        scr.cleanup()
        raise
