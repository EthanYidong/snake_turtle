import turtle as tt
import math
import random
import operator

class GridSystem:
	def __init__(self, size, dims, x, y):
		self.size = size
		self.dims = dims
		self.x = x - size * (dims + 1) / 2
		self.y = y - size * (dims - 1) / 2

		t = tt.Turtle()
		t.hideturtle()
		t.pencolor("red")
		t.up()
		t.goto(self.x, self.y)
		t.down()
		for _ in range(4):
			t.fd(size * dims)
			t.left(90)
	
	def to_real_coords(self, x, y):
		return (self.x + x * self.size, self.y + y * self.size)
	
	def wrap(self, x, y):
		if x < 0:
			x = self.dims + x
		if y < 0: 
			y = self.dims + y
		if x >= self.dims:
			x = x - self.dims
		if y >= self.dims:
			y = y - self.dims
		return (x, y)
	
	def rand(self):
		return (random.randint(0, self.dims - 1), random.randint(0, self.dims - 1))

class Box:
	def __init__(self, grid, size, x, y):
		self.grid = grid
		self.real_x, self.real_y = grid.to_real_coords(x, y)
		self.x = x
		self.y = y
		self.size = size
	
	def __eq__(self, o):
		return self.x == o.x and self.y == o.y
	
	def next_box(self, x, y):
		x, y = self.grid.wrap(self.x + x, self.y + y)
		return Box(self.grid, self.size, x, y)
	
	def render(self, t):
		t.up()
		t.goto(self.real_x, self.real_y)
		t.down()
		t.begin_fill()

		for _ in range(4):
			t.fd(self.size)
			t.left(90)
		t.end_fill()
	
	@staticmethod
	def rand(grid, size):
		r_x, r_y = grid.rand()
		return Box(grid, size, r_x, r_y)

class Snake:
	heading_map = {
		"left": [-1, 0],
		"right": [1, 0],
		"up": [0, 1],
		"down": [0, -1],
	}

	def __init__(self, x, y, heading, size, dims, length, speed):
		self.t = tt.Turtle()
		self.heading = heading
		self.used_heading = heading
		self.size = size
		self.length = length
		self.speed = speed
		self.grid = GridSystem(size, dims, x, y)
		self.boxes = [Box(self.grid, size, math.floor(dims / 2), math.floor(dims / 2))]
		self.food = Box.rand(self.grid, size)

		self.t.hideturtle()

		scr = tt.Screen()
		scr.ontimer(lambda: self.update(), 10)
		scr.onkeypress(lambda: self.set_heading("up"), "Up")
		scr.onkeypress(lambda: self.set_heading("down"), "Down")
		scr.onkeypress(lambda: self.set_heading("left"), "Left")
		scr.onkeypress(lambda: self.set_heading("right"), "Right")

	def set_heading(self, heading):
		if list(map(operator.add, self.heading_map[self.used_heading], self.heading_map[heading])) != [0, 0]:
			self.heading = heading

	def render(self):
		t = self.t
		t.clear()
		t.fillcolor("black")
		for i, box in reversed(list(enumerate(self.boxes))):
			if i == 0:
				t.fillcolor("blue")
			box.render(t)
		t.fillcolor("yellow")
		self.food.render(t)

	def update(self):
		x, y = self.heading_map[self.heading]
		self.used_heading = self.heading

		self.boxes.insert(0, self.boxes[0].next_box(x, y))

		head = self.boxes[0]

		if head in self.boxes[1:]:
			t = self.t
			t.up()
			t.home()
			t.down()
			t.pencolor("green")
			t.write("You lose! You scored: %s" % self.length, align="center", font=("Arial", "32", "normal"))
			tt.Screen().update()
			return
		if head == self.food:
			self.food = Box.rand(self.grid, self.size)
			self.length += 1

		if len(self.boxes) > self.length:
			self.boxes.pop()

		tt.Screen().ontimer(lambda: self.update(), self.speed)
		self.render()
		tt.update()

def main():
	scr = tt.Screen()
	scr.setup(500, 500)

	tt.tracer(0)

	snake = Snake(0, 0, "left", 10, 48, 6, 100)

	snake.render()

	scr.listen()
	tt.done()

if __name__ == "__main__":
	main()