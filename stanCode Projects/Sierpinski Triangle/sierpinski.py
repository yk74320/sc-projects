"""
File: sierpinski.py
Name: Ian Kuo
---------------------------
This file recursively prints the Sierpinski triangle on GWindow.
The Sierpinski triangle is a fractal described in 1915 by Waclaw Sierpinski.
It is a self similar structure that occurs at different levels of iterations.
"""

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GLine
from campy.gui.events.timer import pause

# Constants
ORDER = 6                # Controls the order of Sierpinski Triangle
LENGTH = 600               # The length of order 1 Sierpinski Triangle
UPPER_LEFT_X = 150		   # The upper left x coordinate of order 1 Sierpinski Triangle
UPPER_LEFT_Y = 100         # The upper left y coordinate of order 1 Sierpinski Triangle
WINDOW_WIDTH = 950         # The width of the GWindow
WINDOW_HEIGHT = 700        # The height of the GWindow

# Global Variable
window = GWindow(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)  # The canvas to draw Sierpinski Triangle


def main():
	"""
	The aim of this function is to print out a Sierpinski triangle on GWindow. The number of triangle layers can also
	be determined by user, using the variable ORDER.
	"""
	sierpinski_triangle(ORDER, LENGTH, UPPER_LEFT_X, UPPER_LEFT_Y)


def sierpinski_triangle(order, length, upper_left_x, upper_left_y):
	"""
	:param order: the order of Sierpinski Triangle
	:param length: length of order 1 Sierpinski Triangle
	:param upper_left_x: upper left x coordinate of order 1 Sierpinski Triangle
	:param upper_left_y: upper left y coordinate of order 1 Sierpinski Triangle
	:return: Sierpinski Triangle drawn by the recursive function
	"""
	pause(50)
	if order == 0:
		return
	else:
		# upper left
		sierpinski_triangle(order - 1, length / 2, upper_left_x, upper_left_y)

		# upper right
		sierpinski_triangle(order - 1, length / 2, upper_left_x + 0.5 * length, upper_left_y)

		# lower
		sierpinski_triangle(order - 1, length / 2, upper_left_x + 0.25 * length, upper_left_y + 0.433 * length)

		S1 = GLine(upper_left_x, upper_left_y, upper_left_x + length, upper_left_y)
		window.add(S1)
		S2 = GLine(upper_left_x, upper_left_y, upper_left_x + 0.5 * length, upper_left_y + 0.866 * length)
		window.add(S2)
		S3 = GLine(upper_left_x + 0.5 * length, upper_left_y + 0.866 * length, upper_left_x + length, upper_left_y)
		window.add(S3)


if __name__ == '__main__':
	main()