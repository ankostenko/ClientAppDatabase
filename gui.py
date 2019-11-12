from raylibpy import *

class Button:
	def __init__(self, text, posX, posY, width, height, color):
		self.button = Rectangle(posX, posY, width, height)
		self.text = text
		self.drawAsClicked = False

	def isClicked(self):
		if (check_collision_point_rec(get_mouse_position(), self.button)):
			if (is_mouse_button_pressed(MOUSE_LEFT_BUTTON)):
				return True
			
			if (is_mouse_button_down(MOUSE_LEFT_BUTTON)):
				self.drawAsClicked = True
			else:
				self.drawAsClicked = False
		else:
			self.drawAsClicked = False
			return False

	def draw(self):
		if (self.drawAsClicked):
			draw_rectangle_rec(self.button, LIGHTGRAY)
		else:
			draw_rectangle_rec(self.button, GRAY)

		draw_rectangle_lines_ex(self.button, 2, DARKGRAY)
		draw_text(self.text, self.button.x + 5, self.button.y + 5, 20, SKYBLUE)

class CheckBox:
	def __init__(self, posX, posY, width, height):
		self.rect = Rectangle(posX, posY, width, height)
		self.checked = True

	def isClicked(self):
		if (check_collision_point_rec(get_mouse_position(), self.rect)):
			if (is_mouse_button_pressed(MOUSE_LEFT_BUTTON)):
				self.checked = not self.checked

	def draw(self):
		self.isClicked()
		draw_rectangle_rec(self.rect, LIGHTGRAY)
		draw_rectangle_lines_ex(self.rect, 2, DARKBLUE)

		if (self.checked):
			new_rect = Rectangle(self.rect.x + 5, self.rect.y + 5, self.rect.width - 10, self.rect.height - 10)
			draw_rectangle_rec(new_rect, DARKBLUE)

class DropDown:
	def __init__(self, posX, posY, width, height, variants = []):
		self.rect = Rectangle(posX, posY, width, height)
		self.currentVariant = variants[0]
		self.variants = variants
		self.drawAsClicked = False

	def isClicked(self):
		if (check_collision_point_rec(get_mouse_position(), self.rect)):
			if (is_mouse_button_pressed(MOUSE_LEFT_BUTTON)):
				self.drawAsClicked = not self.drawAsClicked
				return True
		else:
			return False

	def draw(self):
		self.isClicked()
		draw_rectangle_rec(self.rect, RAYWHITE)
		draw_text(self.currentVariant, self.rect.x + 35, self.rect.y + 5, 20, SKYBLUE)
		draw_rectangle_rec(Rectangle(self.rect.x, self.rect.y, 20, self.rect.height), DARKBLUE)
		draw_rectangle_lines_ex(self.rect, 2, DARKPURPLE)

		if (self.drawAsClicked):
			index = 0
			for vari in self.variants:
				currentRect = Rectangle(self.rect.x, self.rect.y + (index + 1) * 30, self.rect.width, 35)
				if (check_collision_point_rec(get_mouse_position(), currentRect)):
					if (is_mouse_button_pressed(MOUSE_LEFT_BUTTON)):
						self.currentVariant = self.variants[index]
						self.drawAsClicked = False
						pass
				if self.currentVariant == vari:
					draw_rectangle_rec(currentRect, DARKPURPLE)
				else:
					draw_rectangle_rec(currentRect, RAYWHITE)
				
				draw_text(vari, self.rect.x + 5, self.rect.y + 5 + (index + 1) * 30, 20, SKYBLUE)
				index += 1
		

class InputBox:
	def __init__(self, posX, posY, width, height):
		self.button = Rectangle(posX, posY, width, height)
		self.drawAsClicked = False
		self.inputText = ""
		self.charsLeft = 21

	def isClicked(self):
		if (check_collision_point_rec(get_mouse_position(), self.button)):
			if (is_mouse_button_pressed(MOUSE_LEFT_BUTTON)):
				return True
		else:
			return False

	def draw(self):
		draw_rectangle_rec(self.button, RAYWHITE)
		if (self.drawAsClicked):
			draw_rectangle_lines_ex(self.button, 2, RED)
		else:
			draw_rectangle_lines_ex(self.button, 2, DARKPURPLE)

		draw_text(self.inputText, self.button.x + 5, self.button.y + 5, 20, SKYBLUE)

class Splitter:
	def draw(posX, posY):
		draw_rectangle(posX, posY, 2 * posX, 3, DARKGRAY)

class BackgroundBox:
	def draw(posX, posY, width, height, color):
		draw_rectangle_rec(Rectangle(posX, posY, width, height), color)