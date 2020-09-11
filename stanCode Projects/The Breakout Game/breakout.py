"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

File: breakout.py
Name: Ian Kuo
-------------------------
The objective of this program is to create a breakout game. In this game, a layer of bricks lines the top third of the
screen and the goal is to destroy them all. A ball moves straight around the screen, bouncing off the top and two
sides of the screen. When a brick is hit, the ball bounces back and the brick is destroyed.
The player loses a turn when the ball touches the bottom of the screen. To prevent this from happening,
the player has a horizontally movable paddle to bounce the ball upward, keeping it in play.
"""

from campy.gui.events.timer import pause
from breakoutgraphics_ext import BreakoutGraphics

FRAME_RATE = 1000 / 60  # 120 frames per second.
NUM_LIVES = 3 # Number of turns which the player can play game.


def main():
    graphics = BreakoutGraphics()
    for i in range(NUM_LIVES):
        while True:
            pause(FRAME_RATE)
            if graphics.click < 1:
                graphics.ball.move(graphics.get_dx(), graphics.get_dy())
                graphics.check_for_wall()
                graphics.check_for_collision()
                if graphics.ball.y >= graphics.window.height or graphics.brick_count == \
                        (graphics.brk_row * graphics.brk_col):
                    graphics.set_ball()
                    graphics.set_ball_velocity()
                    graphics.click = 1
                    break


if __name__ == '__main__':
    main()
