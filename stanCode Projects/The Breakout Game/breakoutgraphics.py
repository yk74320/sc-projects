"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

File: breakoutgraphics.py
Name: Ian Kuo
-------------------------
This program creates a user-defined data structure holding its own variables and methods, 
which can be accessed and used to play a breakout game.
Other than the constructor, the class also contains the ability of drawing colored bricks, starting the game,
moving the paddle, checking bouncing constraints, and reseting ball location and velocity when fail.
"""

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40  # Height of a brick (in pixels).
BRICK_HEIGHT = 15  # Height of a brick (in pixels).
BRICK_ROWS = 10  # Number of rows of bricks.
BRICK_COLS = 10  # Number of columns of bricks.
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10  # Radius of the ball (in pixels).
PADDLE_WIDTH = 75  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels).
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7.0  # Initial vertical speed for the ball.
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        self.pw = paddle_width # Class variable to store paddle width.
        self.pos = paddle_offset # Class variable to store paddle offset.
        self.br = ball_radius # Class variable to store ball radius.
        self.brk_row = brick_rows # Class variable to store the number of brick rows.
        self.brk_col = brick_cols # Class variable to store the number of brick columns.
        self.click = 1 # Class variable as a switch to control game status, where 1 equals to game termination.
        self.brick_count = 0 # Class variable to store the number of bricks being eliminated.

        # Create a graphical window, with some extra space.
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        self.wh = window_height # Class variable to store window height.
        self.ww = window_width # Class variable to store window width.

        # Create a paddle.
        self.paddle = GRect(width=paddle_width, height=paddle_height, x=(window_width - paddle_width) / 2,
                            y=window_height - paddle_offset - paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.paddle.color = 'black'
        self.window.add(self.paddle)

        # Center a filled ball in the graphical window.
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.ball.color = 'black'
        self.set_ball() # Method to set ball place at initial, details shown as below.
        self.window.add(self.ball)

        # Method to set initial velocity of the ball, details shown as below.
        self.set_ball_velocity()

        # Initialize mouse listeners.
        onmousemoved(self.paddle_location) # Method to move paddle while moving the mouse.
        onmouseclicked(self.game_start) # Method to control game status while clicking the mouse.

        # Draw bricks with different colors, which is determined ny the number of rows.
        for i in range(brick_cols):
            for j in range(brick_rows):
                self.brick = GRect(brick_width, brick_height, x=i * (brick_width + brick_spacing),
                                   y=j * (brick_height + brick_spacing) + BRICK_OFFSET)
                self.brick.filled = True
                if j % 10 == 0 or j % 10 == 1:
                    self.brick.fill_color = 'Red'
                    self.brick.color = 'Red'
                elif j % 10 == 2 or j % 10 == 3:
                    self.brick.fill_color = 'Orange'
                    self.brick.color = 'Orange'
                elif j % 10 == 4 or j % 10 == 5:
                    self.brick.fill_color = 'Yellow'
                    self.brick.color = 'Yellow'
                elif j % 10 == 6 or j % 10 == 7:
                    self.brick.fill_color = 'Green'
                    self.brick.color = 'Green'
                else:
                    self.brick.fill_color = 'Blue'
                    self.brick.color = 'Blue'
                self.window.add(self.brick)

    def set_ball(self):
        """
        A method to set ball at initial place.
        """
        self.ball.x = (self.ww - self.br) / 2
        self.ball.y = (self.wh - self.br) / 2

    def set_ball_velocity(self):
        """
        A method to set the initial velocity of the ball speed.
        """
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self.__dx = -self.__dx

    def game_start(self, event):
        """
        :param event: Detect when the user presses the button on their mouse and then minus variable click by 1.
        :return: Continuing the game when the number of click is less than 1.
        """
        self.click -= 1

    def paddle_location(self, event):
        """
        :param event: Detect when the user moves the mouse.
        :return:Move paddle when the mouse is moved and make sure that the paddle completely stays in the window.
        """
        if event.x - (self.pw / 2) < 0:
            self.paddle.x = 0
        elif event.x + (self.pw / 2) >= self.ww:
            self.paddle.x = self.ww - self.pw
        else:
            self.paddle.x = event.x - self.pw / 2
        self.paddle.y = self.wh - self.pos

    def check_for_wall(self):
        """
        A method that changes the direction of the ball when it hits the wall.
        """
        if self.ball.x <= 0 or self.ball.x + self.ball.width >= self.window.width:
            self.__dx = - self.__dx
        if self.ball.y <= 0:
            self.__dy = - self.__dy

    def check_for_collision(self):
        """
        A method that changes the direction of the ball when it hits the paddle.
        """
        ul_obj = self.window.get_object_at(self.ball.x, self.ball.y)
        ur_obj = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)
        ll_obj = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.width)
        lr_obj = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.width)
        if ul_obj is not None and ul_obj is not self.paddle:
            self.window.remove(ul_obj)
            self.brick_count += 1
            self.__dy *= -1
        elif ur_obj is not None and ur_obj is not self.paddle:
            self.window.remove(ur_obj)
            self.brick_count += 1
            self.__dy *= -1
        elif ll_obj is self.paddle:
            self.__dy *= -1
        elif lr_obj is self.paddle:
            self.__dy *= -1

    def get_dx(self):
        """
        Getter function for x velocity.
        """
        return self.__dx

    def get_dy(self):
        """
        Getter function for y velocity.
        """
        return self.__dy
