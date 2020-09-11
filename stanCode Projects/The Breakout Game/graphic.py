from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel, GLine
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import time
import random

COLUMNS = 10						# columns of the bricks
ROWS = 5							# rows of the bricks
BRICK_HEIGHT_FRACTION = 0.3  		# brick total height(include middle spacing) / window height
BRICK_OFFSET_FRACTION = 0.05  		# brick offset region / window height
BRICK_SPACE = 4  					# space between bricks
MAX_SPEED = 8  						# maximum ball speed
MIN_SPEED = 5						# minimum ball speed
MAX_LIFE = 3						# lives in a game
MAX_BALL_AMOUNT = 10				# maximun amount of balls
GIFT_CHANCE = 0.5					# the chance a brick contains a gift
GIFT_COLOR = [						# gift colors and explanations
["blue", "expand paddle width"], 
["black", "add one more ball"], 
["lime", "slow down the speed"], 
["darkblue", "shorten paddle width"]
]
HIGHSCORE_AMOUNT = 5				# the amount of highscore shown

def color_set(obj, color):  # set the object color a specific color
	"""
	obj : the object wanted to change color
	color : the color to change
	"""
	obj.filled = True
	obj.fill_color = color
	obj.color = color


class Graphics:
	def __init__(self, width=500, height=500):
		"""
		width : the window's width
		height : the window's height
		"""
		# Setting variables
		self.brick_width = (width + BRICK_SPACE) // COLUMNS - BRICK_SPACE
		self.brick_height = int((height * BRICK_HEIGHT_FRACTION + BRICK_SPACE) / ROWS - BRICK_SPACE)
		self.brick_offset = int(height * BRICK_OFFSET_FRACTION)
		self.paddle_width = width // 4
		self.paddle_height = self.brick_height//2
		self.paddle_offset = height // 8
		self.ball_size = min(self.brick_width, self.brick_height)
		self.gift_speed = width // 200
		self.gift_size = self.ball_size

		# Create a graphical window.
		self.window = GWindow(width=width, height=height, title="Breakout")

		# Create a paddle.

		self.paddle = GRect(self.paddle_width, self.paddle_height)
		self.paddle.x = (self.window.width - self.paddle_width) // 2
		self.paddle.y = self.window.height - self.paddle_offset
		color_set(self.paddle, "blue")

		# Draw balls.
		self.ball_list = [GOval(0, 0)] * MAX_BALL_AMOUNT
		self.ball_set()
		self.lives = MAX_LIFE
		self.ball_lives = [0] * MAX_BALL_AMOUNT
		self.ball_amount = 1
		self.fake_ball_x = (self.window.width - self.ball_size) // 2
		self.fake_ball_y = self.paddle.y - self.ball_size

		# Default initial velocity for the ball.
		self.vx_list = [0] * MAX_BALL_AMOUNT
		self.vy_list = [0] * MAX_BALL_AMOUNT
		self.speed_set()
		self.slow_fraction = 1

		# Draw bricks.
		self.brick_list = [GRect(0, 0)] * (ROWS * COLUMNS)
		self.brick_score_list = [0] * (ROWS * COLUMNS)
		self.brick_lives = [1] * (ROWS * COLUMNS)
		self.brick_gift = [0] * (ROWS * COLUMNS)

		# Initial gift boxes
		self.gift_vy = [0] * (ROWS * COLUMNS)
		self.gift_switch = [0] * (ROWS * COLUMNS)
		self.gift_list = [GRect(0, 0)] * (ROWS * COLUMNS)
		self.example_gift = [GRect(0, 0)] * len(GIFT_COLOR)
		self.gift_explanation = [GLabel(0, 0)] * len(GIFT_COLOR)
		self.brick_set()
		self.gift_set()

		# Graphics label
		self.intro_text = GLabel("Breakout")
		self.intro_click_text = GLabel("Click to Start")
		self.loading_text = GLabel("Loading")
		self.progress_bar = GLabel("                       ")
		self.menu_text = GLabel("Symbols")
		self.ending_text = GLabel("")
		self.highscore_text = GLabel("Highscore")
		self.highscore = [GLabel("")] * HIGHSCORE_AMOUNT
		self.highscore_eg = GLabel("0.   "+str(sum(self.brick_score_list)))
		self.highscore_eg.font = "-25"
		self.highscore_eg.x = self.window.width//2 - self.highscore_eg.width//2
		self.retry_click_text = GLabel("Click to Restart ( 3 sec left )")

		# Score label
		self.score = 0
		self.score_text = GLabel("Score : " + str(self.score))
		self.score_text.font = "-20"
		self.score_text.x = 0
		self.score_text.y = self.window.height - 1
		self.life_score = 0

		# Life label
		self.life_label = GLabel("")
		for i in range(MAX_LIFE):
			self.life_label.text += "♥"
		self.life_label.font = "-30"
		self.life_label.x = self.window.width - self.life_label.width
		self.life_label.y = self.window.height - 1

		# mouse listener
		onmouseclicked(self.start)
		self.game_start = False
		onmousemoved(self.paddle_move)

	def full_reset(self):
		"""
		reset all the variables
		"""
		self.paddle_width = self.window.width // 4
		self.ball_size = min(self.brick_width, self.brick_height)
		self.paddle = GRect(self.paddle_width, self.paddle_height)
		self.paddle.x = (self.window.width - self.paddle_width) // 2
		self.paddle.y = self.window.height - self.paddle_offset
		color_set(self.paddle, "blue")
		self.ball_set()
		self.lives = MAX_LIFE
		self.ball_lives = [0] * MAX_BALL_AMOUNT
		self.ball_amount = 1
		self.fake_ball_x = (self.window.width - self.ball_size) // 2
		self.fake_ball_y = self.paddle.y - self.ball_size
		self.speed_set()
		self.slow_fraction = 1
		self.brick_lives = [1] * (ROWS * COLUMNS)
		self.brick_gift = [0] * (ROWS * COLUMNS)
		self.gift_vy = [0] * (ROWS * COLUMNS)
		self.gift_switch = [0] * (ROWS * COLUMNS)
		self.brick_set()
		self.gift_set()
		self.score = 0
		self.score_text.text = "Score : 0"
		self.score_text.x = 0
		self.score_text.y = self.window.height - 1
		self.life_score = 0
		self.life_label.text = ""
		for i in range(MAX_LIFE):
			self.life_label.text += "♥"
		self.life_label.x = self.window.width - self.life_label.width

	def speed_set(self):
		"""
		set a random speed for every ball, y direction is always negative
		"""
		for index in range(MAX_BALL_AMOUNT):
			self.vx_list[index] = random.randint(0, MAX_SPEED*2)-MAX_SPEED
			while abs(self.vx_list[index]) < MIN_SPEED:
				self.vx_list[index] = random.randint(0, MAX_SPEED*2)-MAX_SPEED
			self.vy_list[index] = -random.randint(MIN_SPEED, MAX_SPEED)

	def speed_change(self):
		"""
		change the speed by the effect of the score and the gifts
		"""
		vx = [0] * MAX_BALL_AMOUNT
		vy = [0] * MAX_BALL_AMOUNT
		gvy = [0] * (ROWS * COLUMNS)
		multiplier = (1 + min((self.score - self.life_score) / sum(self.brick_score_list)*4, 2)) * self.slow_fraction
		for index in range(MAX_BALL_AMOUNT):
			vx[index] = int(self.vx_list[index] * multiplier)
			vy[index] = int(self.vy_list[index] * multiplier)
		for num in range(ROWS*COLUMNS):
			gvy[num] = int(self.gift_vy[num] * multiplier)
		return vx, vy, gvy

	def object_show(self):
		"""
		show the object in the correct order 
		"""
		self.window.add(self.paddle)
		self.window.add(self.score_text)
		self.window.add(self.life_label)
		for index in range(self.ball_amount):
			self.window.add(self.ball_list[index])
			self.ball_lives[index] = 1
		for index in range(ROWS * COLUMNS):
			self.window.add(self.brick_list[index])

	def paddle_reset(self):
		"""
		reset the paddle
		"""
		self.paddle_width = self.window.width // 4
		self.window.remove(self.paddle)
		xcor = self.paddle.x
		ycor = self.paddle.y
		self.paddle = GRect(self.paddle_width, self.paddle_height, x=xcor, y=ycor)
		color_set(self.paddle, "blue")
		self.window.add(self.paddle)

	def paddle_resize(self):
		"""
		change the paddle width by replacing a new one
		"""
		self.window.remove(self.paddle)
		xcor = self.paddle.x
		ycor = self.paddle.y
		self.paddle = GRect(self.paddle_width, self.paddle_height, x=xcor, y=ycor)
		color_set(self.paddle, "blue")
		self.window.add(self.paddle)

	def ball_show(self):
		"""
		show the balls on the window for self.ball_amount of balls
		"""
		for index in range(self.ball_amount):
			self.window.add(self.ball_list[index])
			self.ball_lives[index] = 1

	def ball_set(self):
		"""
		setting the balls' graphics
		"""
		for index in range(MAX_BALL_AMOUNT):
			self.ball_list[index] = GOval(self.ball_size, self.ball_size)
			self.ball_list[index].x = (self.window.width - self.ball_size) // 2
			self.ball_list[index].y = self.window.height - self.paddle_offset - self.ball_size
			color_set(self.ball_list[index], "black")

	def ball_resize(self):
		"""
		changing the balls' size by replacing a new one
		"""
		self.fake_ball_y = self.paddle.y - self.ball_size
		for index in range(MAX_BALL_AMOUNT):
			self.window.remove(self.ball_list[index])
			xcor = self.ball_list[index].x
			ycor = self.ball_list[index].y
			self.ball_list[index] = GOval(self.ball_size, self.ball_size, x=xcor, y=ycor)
			color_set(self.ball_list[index], "black")
			self.window.add(self.ball_list[index])

	def ball_add(self):
		"""
		add one more ball to the game (maximum 10)
		"""
		self.window.add(self.ball_list[self.ball_amount-1])
		self.ball_lives[self.ball_amount-1] = 1

	def ball_amount_reset(self):
		"""
		set the ball amount to 1
		"""
		for index in range(1, self.ball_amount):
			self.window.remove(self.ball_list[index])
			self.ball_lives[index] = 0
		self.ball_amount = 1

	def ball_reset(self):
		"""
		reset all the balls position
		"""
		for index in range(MAX_BALL_AMOUNT):
			self.ball_list[index].x = self.fake_ball_x
			self.ball_list[index].y = self.fake_ball_y

	def brick_set(self):
		"""
		bricks' initial setting
		"""
		for by in range(ROWS):
			for bx in range(COLUMNS):
				index = bx + by * COLUMNS
				self.brick_list[index] = GRect(self.brick_width, self.brick_height)
				self.brick_list[index].x = bx * (self.brick_width + BRICK_SPACE)
				self.brick_list[index].y = self.brick_offset + by * (self.brick_height + BRICK_SPACE)
				color = (0xFFFFFF // ROWS) * (index // COLUMNS)
				self.brick_score_list[index] = (ROWS - by) * 10
				color_set(self.brick_list[index], color)
				if random.randint(1, int(1/GIFT_CHANCE)) == 1:
					self.brick_gift[index] = random.randint(1, 4)

	def gift_set(self):
		"""
		gifts' initial setting
		"""
		for num in range(ROWS*COLUMNS):
			self.gift_list[num] = GRect(self.gift_size, self.gift_size)
			color_set(self.gift_list[num], GIFT_COLOR[self.brick_gift[num]-1][0])
			self.gift_list[num].x = self.brick_list[num].x + self.brick_width // 2 - self.gift_size // 2
			self.gift_list[num].y = self.brick_list[num].y + self.brick_height // 2 - self.gift_size // 2

	def clear_gift(self):
		"""
		removing all the shown gifts from the window
		"""
		for index in range(ROWS * COLUMNS):
			if self.gift_switch[index] == 1:
				self.window.remove(self.gift_list[index])
				self.gift_switch[index] = 0
				self.gift_vy[index] = 0

	def paddle_move(self, event):
		"""
		change the paddle x position when the mouse moves
		"""
		if event.x < self.paddle.width // 2:
			self.paddle.x = 0
			self.fake_ball_x = (self.paddle.width - self.ball_size) // 2
		elif self.window.width - self.paddle.width // 2 < event.x:
			self.paddle.x = self.window.width - self.paddle.width
			self.fake_ball_x = self.window.width - self.paddle.width // 2 - self.ball_size // 2
		else:
			self.paddle.x = event.x - self.paddle.width // 2
			self.fake_ball_x = event.x - self.ball_size // 2

	def start(self, event):
		"""
		set the starting boolean to True
		"""
		self.game_start = True

	def life_check(self):
		"""
		check if the ball's life or the bricks' life hits zero
		if ball's life hits zero, return 1
		if bricks' life hits zero, return 2
		else, return 0
		"""
		if self.lives == 0:
			return 1
		elif sum(self.brick_lives) == 0:
			return 2
		return 0

	def lose_life(self):
		"""
		change settings when the ball fell to the bottom
		"""
		self.lives -= 1
		self.game_start = False
		self.speed_set()
		self.paddle_reset()
		self.ball_amount_reset()
		self.clear_gift()
		self.slow_fraction = 1
		for index in range(self.ball_amount):
			self.ball_lives[index] = 1
		self.ball_show()
		hearts = ""
		for i in range(self.lives):
			hearts += "♥"
		self.life_label.text = hearts
		self.life_label.x = self.window.width - self.life_label.width
		self.life_score = self.score

	def boundary_bump(self):
		"""
		check if the ball has contact with the boundary
		"""
		for index in range(MAX_BALL_AMOUNT):
			if self.ball_lives[index] == 1:
				if self.window.width - self.ball_size < self.ball_list[index].x:
					self.vx_list[index] = -abs(self.vx_list[index])
				elif self.ball_list[index].x < 0:
					self.vx_list[index] = abs(self.vx_list[index])
				if self.ball_list[index].y < 0:
					self.vy_list[index] = abs(self.vy_list[index])
				elif self.window.height - self.ball_size < self.ball_list[index].y:
					self.ball_lives[index] = 0
					self.window.remove(self.ball_list[index])
					if sum(self.ball_lives) == 0:
						self.lose_life()

	def single_brick(self, brick):
		"""
		brick : the brick object that the ball has contact with
		change settings when a ball collides into a single brick
		"""
		self.window.remove(brick)
		index = self.brick_list.index(brick)
		self.brick_lives[index] = 0
		self.score += self.brick_score_list[index]
		self.score_text.text = "Score : " + str(self.score)
		if self.brick_gift[index] >= 1:
			self.gift_switch[index] = 1
			self.gift_vy[index] = self.gift_speed
			self.window.add(self.gift_list[index])

	def ball_bump(self):
		"""
		check if the ball has contact with the bricks or the paddle
		"""
		for index in range(MAX_BALL_AMOUNT):
			if self.ball_lives[index] == 1:
				lx = self.ball_list[index].x
				mx = self.ball_list[index].x + self.ball_size // 2
				rx = self.ball_list[index].x + self.ball_size
				uy = self.ball_list[index].y
				my = self.ball_list[index].y + self.ball_size // 2
				dy = self.ball_list[index].y + self.ball_size
				up_object = self.window.get_object_at(mx, uy-1)
				down_object = self.window.get_object_at(mx, dy+1)
				left_object = self.window.get_object_at(lx-1, my)
				right_object = self.window.get_object_at(rx+1, my)
				if up_object is self.paddle or left_object is self.paddle or right_object is self.paddle or down_object is self.paddle:
					self.vy_list[index] = -abs(self.vy_list[index])
				elif up_object in self.brick_list:
					self.vy_list[index] = abs(self.vy_list[index])
					self.single_brick(up_object)
				elif down_object in self.brick_list:
					self.vy_list[index] = -abs(self.vy_list[index])
					self.single_brick(down_object)
				elif left_object in self.brick_list:
					self.vx_list[index] = abs(self.vx_list[index])
					self.single_brick(left_object)
				elif right_object in self.brick_list:
					self.vx_list[index] = -abs(self.vx_list[index])
					self.single_brick(right_object)

	def object_move(self):
		"""
		move the objects(shown balls, shown gifts)
		"""
		vx, vy, gvy = self.speed_change()
		for index in range(MAX_BALL_AMOUNT):
			if self.ball_lives[index] == 1:
				self.ball_list[index].x += vx[index]
				self.ball_list[index].y += vy[index]
			else:
				self.ball_list[index].x = self.fake_ball_x
				self.ball_list[index].y = self.fake_ball_y
		for num in range(ROWS * COLUMNS):
			self.gift_list[num].y += self.gift_vy[num]

	def gift_bump(self):
		"""
		check if the gifts has contact with the paddle
		"""
		for index in range(ROWS * COLUMNS):
			if self.gift_switch[index] == 1:
				lx = self.gift_list[index].x
				mx = self.gift_list[index].x + self.gift_size // 2
				rx = self.gift_list[index].x + self.gift_size
				uy = self.gift_list[index].y
				my = self.gift_list[index].y + self.gift_size // 2
				dy = self.gift_list[index].y + self.gift_size
				up_object = self.window.get_object_at(mx, uy-1)
				down_object = self.window.get_object_at(mx, dy+1)
				left_object = self.window.get_object_at(lx-1, my)
				right_object = self.window.get_object_at(rx+1, my)
				if up_object is self.paddle or left_object is self.paddle or right_object is self.paddle or down_object is self.paddle:
					self.gift_switch[index] = 0
					self.window.remove(self.gift_list[index])
					self.gift_vy[index] = 0
					if self.brick_gift[index] == 1:
						self.paddle_width += self.window.width//20
						self.paddle_resize()
					elif self.brick_gift[index] == 2:
						self.ball_amount += 1
						self.ball_add()
					elif self.brick_gift[index] == 3:
						self.slow_fraction *= 0.9
					elif self.brick_gift[index] == 4:
						if self.paddle_width >= self.window.width//8:
							self.paddle_width -= self.window.width//10 
						self.paddle_resize()

	def intro(self):
		"""
		the intro page setup
		"""
		self.intro_text.font = "-80"
		self.intro_text.x = (self.window.width - self.intro_text.width) // 2
		self.intro_text.y = self.window.height//2 + self.intro_text.height // 2
		self.window.add(self.intro_text)
		self.intro_click_text.font = "-20"
		self.intro_click_text.x = (self.window.width - self.intro_click_text.width) // 2
		self.intro_click_text.y = (self.intro_text.y + self.window.height)//2
		self.window.add(self.intro_click_text)

	def loading(self):
		"""
		the loading page setup
		"""
		self.loading_text.font = "-70"
		self.loading_text.x = (self.window.width - self.loading_text.width) // 2
		self.loading_text.y = self.window.height // 3
		self.window.add(self.loading_text)
		self.progress_bar.font = "-40"
		self.progress_bar.x = (self.window.width - self.progress_bar.width) // 2
		self.progress_bar.y = self.loading_text.y + self.loading_text.height
		self.window.add(self.progress_bar)
		self.menu_text.x = (self.window.width - self.menu_text.width) // 2
		self.menu_text.y = self.progress_bar.y + int(self.progress_bar.height*1.2)
		self.window.add(self.menu_text)
		for num in range(len(GIFT_COLOR)):
			self.example_gift[num] = GRect(self.gift_size, self.gift_size)
			color_set(self.example_gift[num], GIFT_COLOR[num][0])
			self.example_gift[num].x = self.window.width//2 - self.gift_size*3
			self.example_gift[num].y = self.menu_text.y + int(self.gift_size*1.5*(num+0.7)) - self.gift_size//3
			self.gift_explanation[num] = GLabel(GIFT_COLOR[num][1])
			self.gift_explanation[num].x = self.window.width//2 - self.gift_size*1
			self.gift_explanation[num].y = self.menu_text.y + int(self.gift_size*1.5*(num+0.7)) + self.gift_explanation[num].height
			self.window.add(self.example_gift[num])
			self.window.add(self.gift_explanation[num])
		for tick in range(6):
			self.single_bar(["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"], tick)

	def single_bar(self, sign, tick):
		"""
		sign : the progress bar sign
		tick : the index of the changing bar sign
		changing the progress bar
		"""
		for i in range(8):
			self.progress_bar.text = self.progress_bar.text[:tick]+sign[i]+self.progress_bar.text[tick+1:len(self.progress_bar.text)-1]
			pause(50)

	def win(self):
		"""
		the winning label setting
		"""
		self.ending_text.text = "Congratulations!!!"
		self.ending_text.font = "-45"
		self.ending_text.x = (self.window.width - self.ending_text.width) // 2
		self.ending_text.y = (self.window.height + self.ending_text.height) // 3
		self.window.add(self.ending_text)

	def lose(self):
		"""
		the losing label setting
		"""
		self.ending_text.text = "Game Over"
		self.ending_text.font = "-70"
		self.ending_text.color = "red"
		self.ending_text.x = (self.window.width - self.ending_text.width) // 2
		self.ending_text.y = (self.window.height + self.ending_text.height) // 3
		self.window.add(self.ending_text)

	def final_score(self):
		"""
		the final score page setup
		"""
		self.score_text.text = "Score : " + str(self.score) + " / " + str(sum(self.brick_score_list))
		self.score_text.x = (self.window.width - self.score_text.width) // 2
		self.score_text.y = self.ending_text.y + self.score_text.height * 5
		self.window.add(self.score_text)
		self.retry_click_text.font = "-15"
		self.retry_click_text.x = (self.window.width - self.retry_click_text.width) // 2
		self.retry_click_text.y = (self.window.height + self.score_text.y) // 2
		self.window.add(self.retry_click_text)
		self.game_start = False
		for tick in range(3):
			pause(1000)
			self.retry_click_text.text = self.retry_click_text.text[:19] + str(2-tick) + self.retry_click_text.text[20:]
		pause(1000)


	def high_score(self, all_score):
		"""
		the high score page setup
		"""
		all_score.sort(reverse=True)
		self.highscore_text.font = "-40"
		self.highscore_text.x = self.window.width//2 - self.highscore_text.width//2
		self.highscore_text.y = self.window.height//5
		self.window.add(self.highscore_text)
		nan_text = ""
		for i in range(len(str(sum(self.brick_score_list)))):
			nan_text += "- "
		for num in range(HIGHSCORE_AMOUNT):
			if num < len(all_score):
				spacing = ""
				for s in range(len(str(sum(self.brick_score_list))) - len(str(all_score[num]))):
					spacing += "  "
				self.highscore[num] = GLabel(str(num+1)+".   "+spacing+str(all_score[num]))
			else:
				self.highscore[num] = GLabel(str(num+1)+".   "+nan_text)
			self.highscore[num].font = "-25"
			self.highscore[num].x = self.highscore_eg.x
			self.highscore[num].y = self.highscore_text.y + self.highscore[num].height*2*(num+1)
			self.window.add(self.highscore[num])
