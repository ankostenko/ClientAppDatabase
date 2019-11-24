from raylibpy import *

class Button:
	def __init__(self, text, posX, posY, width, height, color):
		self.posY = posY
		self.rect = Rectangle(posX, posY, width, height)
		self.text = text
		self.drawAsClicked = False

	def isClicked(self):
		if (check_collision_point_rec(get_mouse_position(), self.rect)):
			if (is_mouse_button_pressed(MOUSE_LEFT_BUTTON)):
				return True
			
			if (is_mouse_button_down(MOUSE_LEFT_BUTTON)):
				self.drawAsClicked = True
			else:
				self.drawAsClicked = False
		else:
			self.drawAsClicked = False
			return False

	def draw(self, newY):
		self.rect.y = self.posY + newY
		if (self.drawAsClicked):
			draw_rectangle_rec(self.rect, LIGHTGRAY)
		else:
			draw_rectangle_rec(self.rect, GRAY)

		draw_rectangle_lines_ex(self.rect, 2, DARKGRAY)
		draw_text(self.text, self.rect.x + 5, self.rect.y + 5, 20, SKYBLUE)

class CheckBox:
	def __init__(self, posX, posY, width, height, checked):
		self.posY = posY
		self.rect = Rectangle(posX, posY, width, height)
		self.checked = checked

	def isClicked(self):
		if (check_collision_point_rec(get_mouse_position(), self.rect)):
			if (is_mouse_button_pressed(MOUSE_LEFT_BUTTON)):
				self.checked = not self.checked

	def draw(self, newY):
		self.rect.y = self.posY + newY
		self.isClicked()
		draw_rectangle_rec(self.rect, LIGHTGRAY)
		draw_rectangle_lines_ex(self.rect, 2, DARKBLUE)

		if (self.checked):
			new_rect = Rectangle(self.rect.x + 5, self.rect.y + 5, self.rect.width - 10, self.rect.height - 10)
			draw_rectangle_rec(new_rect, DARKBLUE)

class HorizontalScroller:
	def __init__(self):
		self.startScrollPoint = Vector2(0, 0)
		self.scrollPressed = False
		self.leftScrollerEdge = 0

	def draw(self, tableWidth, viewerWidth):
		viewerWidth -= 15
		ratioTableWidthToViewerWidth = tableWidth / viewerWidth
		horizontalScrollWidth = viewerWidth
		if (ratioTableWidthToViewerWidth > 1):
			horizontalScrollWidth = viewerWidth * (2 - ratioTableWidthToViewerWidth)
		else:
			self.leftScrollerEdge = 0
			return
		scrollerRect = Rectangle(self.leftScrollerEdge, 880, horizontalScrollWidth, 20)
		if (check_collision_point_rec(get_mouse_position(), scrollerRect)):
			if (is_mouse_button_pressed(MOUSE_LEFT_BUTTON)):
				self.startScrollPoint = get_mouse_position() - Vector2(self.leftScrollerEdge, 0)
				self.scrollPressed = True
			if (is_mouse_button_down(MOUSE_LEFT_BUTTON)):
				mousePosition = get_mouse_position()
				self.leftScrollerEdge = mousePosition.x - self.startScrollPoint.x

		if (not check_collision_point_rec(get_mouse_position(), Rectangle(scrollerRect.x, scrollerRect.y, viewerWidth, scrollerRect.height)) and not self.scrollPressed):
			return

		draw_rectangle_rec(scrollerRect, DARKBLUE)

		if (self.scrollPressed and is_mouse_button_released(MOUSE_LEFT_BUTTON)):
			self.scrollPressed = False

		if (self.scrollPressed):
			mousePosition = get_mouse_position()
			self.leftScrollerEdge = mousePosition.x - self.startScrollPoint.x 

			if (self.leftScrollerEdge < 0):
				self.leftScrollerEdge = 0
			if (self.leftScrollerEdge + horizontalScrollWidth > viewerWidth):
				self.leftScrollerEdge = viewerWidth - horizontalScrollWidth

class VerticalScroller:
	def __init__(self):
		self.topScollerEdge = 0
		self.scrollPressed = False
		self.startScrollPoint = Vector2(0, 0)

	def draw(self, startX, startY, tableHeight, viewerHeight, viewerWidth):
		ratioTableWidthToViewerWidth = tableHeight / viewerHeight
		verticalScrollHeight = viewerHeight
		if (ratioTableWidthToViewerWidth > 1):
			verticalScrollHeight = viewerHeight * (2 - ratioTableWidthToViewerWidth)
		else:
			return

		scollerWidthPix = 15
		scrollerRect = Rectangle(viewerWidth - scollerWidthPix, self.topScollerEdge, scollerWidthPix, verticalScrollHeight)
		if (check_collision_point_rec(get_mouse_position(), scrollerRect)):
			if (is_mouse_button_pressed(MOUSE_LEFT_BUTTON)):
				self.startScrollPoint = get_mouse_position() - Vector2(0, self.topScollerEdge)
				self.scrollPressed = True
			if (is_mouse_button_down(MOUSE_LEFT_BUTTON)):
				mousePosition = get_mouse_position()
				self.topScollerEdge = mousePosition.y - self.startScrollPoint.y
		
		mousePosition = get_mouse_position()
		wheelMovement = 0
		if (mousePosition.x > startX and mousePosition.y > startY and mousePosition.x < viewerWidth and mousePosition.y < viewerHeight):
			wheelMovement = -get_mouse_wheel_move() * 15 
			self.topScollerEdge += wheelMovement

		if (wheelMovement == 0 and not check_collision_point_rec(get_mouse_position(), Rectangle(scrollerRect.x, scrollerRect.y, scrollerRect.width, viewerHeight)) and not self.scrollPressed):
			return

		draw_rectangle_rec(scrollerRect, DARKBLUE)

		if (self.scrollPressed and is_mouse_button_released(MOUSE_LEFT_BUTTON)):
			self.scrollPressed = False

		if (self.scrollPressed):
			mousePosition = get_mouse_position()
			self.topScollerEdge = mousePosition.y - self.startScrollPoint.y

		if (self.topScollerEdge < 0):
			self.topScollerEdge = 0
		if (self.topScollerEdge + verticalScrollHeight > viewerHeight):
			self.topScollerEdge = viewerHeight - verticalScrollHeight

class ResultViewer:
	def __init__(self):
		self.results = []
		self.oldResults = []
		self.header = ""
		self.tableWidth = 0
		self.tableHeight = 0
		self.horizontalScroller = HorizontalScroller()
		self.verticalScroller = VerticalScroller()

	def draw(self, width, height):
		prevColHeight = -self.verticalScroller.topScollerEdge
		draw_rectangle(0, prevColHeight, width, 50, GRAY)

		if (not self.results):
			draw_text("Nothing to display here...", 225, 400, 50, DARKBLUE)
			return
		
		ColorEven = LIGHTGRAY
		ColorOdd = RAYWHITE
		# Swap color to end with the gray color
		if (len(self.results) % 2 == 0):
			ColorEven, ColorOdd = ColorOdd, ColorEven
		# First draw row's background
		for index in range(len(self.results)):
			if (index % 2 == 0):
				draw_rectangle(0, 50 * (index + 1) + prevColHeight, width, 50, ColorEven)
			else:
				draw_rectangle(0, 50 * (index + 1) + prevColHeight, width, 50, ColorOdd)


		# Horizontal scroller
		magicAligningConstant = 20
		self.horizontalScroller.draw(self.tableWidth, width + magicAligningConstant)

		prevColWidth = -self.horizontalScroller.leftScrollerEdge

		self.tableWidth = 0
		for column in range(0, len(self.header)):
			# Determine max length in a column
			leftPadding = 10
			topPadding = 10
			columnHeight = 50
			self.tableHeight = 0
			columnWidth = measure_text(self.header[column], 30) + magicAligningConstant
			for result in self.results:
				length = measure_text(str(result[column]), 30) + magicAligningConstant
				if (columnWidth < length):
					columnWidth = length
				
				self.tableHeight += columnHeight


			draw_text(str(self.header[column]), leftPadding + prevColWidth, topPadding + prevColHeight, 30, DARKBLUE)  
			for index, result in enumerate(self.results, start = 1):
				draw_text(str(result[column]), leftPadding + prevColWidth, topPadding + columnHeight * index + prevColHeight, 30, DARKBLUE)
			if (column != len(self.header) - 1):
				draw_rectangle(prevColWidth + columnWidth, 0, 2, columnHeight * (len(self.results) + 1) + prevColHeight, DARKGRAY)
			prevColWidth += columnWidth
			self.tableWidth += columnWidth
			
		# Vertical scroller
		self.verticalScroller.draw(0, 0, self.tableHeight, height, width)

		Splitter.draw(0, 10)

	def set(self, new_results):
		self.verticalScroller.topScollerEdge = 0


class BookLenter:
	def __init__(self, connection):
		self.books = []
		self.header = ["Present", "Book name", "Author name"]
		self.connection = connection

	def draw(self, width):
		#draw_rectangle(0, 0, width, 1500, RAYWHITE)

		if (not self.books):
			return

		columnHeight = 50

		draw_rectangle(0, 0, width, columnHeight, GRAY)

		for index in range(0, len(self.books)):
			draw_rectangle(0, (index + 1) * columnHeight, width, columnHeight, LIGHTGRAY)

		magicAligningConstant = 20
		leftPadding = 10
		topPadding = 10

		for column in range(0, len(self.header)):
			columnWidth = measure_text(str(self.header[column]), 30) + magicAligningConstant
			draw_text(str(self.header[column]), leftPadding + columnWidth * column, topPadding, 30, DARKBLUE)
			
			for book in self.books:
				length = measure_text(str(book[column - 1]), 30) + magicAligningConstant
				if (length > columnWidth):
					columnWidth = length

			for index, book in enumerate(self.books, start = 1):
				if (column == 0):
					checkBox = CheckBox(columnWidth / 2 - 2 * leftPadding, topPadding + columnHeight * index, 30, 30, (not bool(book[0])))
					checkBox.draw(0)
					# if a book still in the library but we're lending it
					# print(f"Index: {index} Book: {book} Checked: {checkBox.checked}")
					if (checkBox.checked == False and book[0] == 0):
						cur = self.connection.cursor()
						cur.execute(""" UPDATE books SET is_lent = 1 WHERE books.book_id = ? """, (index - 1, ))
						lst = list(book)
						lst[0] = 1
						self.books[index - 1] = tuple(lst)
						self.connection.commit()
					# if we want to return book to the library
					if (checkBox.checked == True and book[0] == 1):
						cur = self.connection.cursor()
						cur.execute(""" UPDATE books SET is_lent = 0 WHERE books.book_id = ? """, (index - 1, ))
						lst = list(book)
						lst[0] = 0
						self.books[index - 1] = tuple(lst)
						self.connection.commit()

				
				if (column != 0):
					draw_text(str(book[column]), leftPadding + columnWidth * column, topPadding + columnHeight * index, 30, DARKBLUE)

class DropDown:
	def __init__(self, posX, posY, width, height, variants = []):
		self.posY = posY
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

	def draw(self, newY):
		self.rect.y = self.posY + newY
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
	def __init__(self, posX, posY, width, height, maxChars):
		self.posY = posY
		self.rect = Rectangle(posX, posY, width, height)
		self.drawAsClicked = False
		self.inputText = ""
		self.charsLeft = maxChars
		self.maxCharacters = maxChars

	def isClicked(self):
		if (check_collision_point_rec(get_mouse_position(), self.rect)):
			if (is_mouse_button_pressed(MOUSE_LEFT_BUTTON)):
				return True
		else:
			return False

	def draw(self, newY):
		self.rect.y = self.posY + newY
		draw_rectangle_rec(self.rect, RAYWHITE)
		if (self.drawAsClicked):
			draw_rectangle_lines_ex(self.rect, 2, RED)
			# draw cursor pointer
			cursorRect = Rectangle(self.rect.x + 5 + measure_text(self.inputText, 20), self.rect.y + self.rect.height - 5, 15, 3)
			draw_rectangle_rec(cursorRect, DARKPURPLE)
		else:
			draw_rectangle_lines_ex(self.rect, 2, DARKPURPLE)

		draw_text(self.inputText, self.rect.x + 5, self.rect.y + 5, 20, SKYBLUE)

class Splitter:
	def draw(posX, posY):
		draw_rectangle(posX, posY, 2 * posX, 3, DARKGRAY)

class BackgroundBox:
	def draw(posX, posY, width, height, color):
		draw_rectangle_rec(Rectangle(posX, posY, width, height), color)