import sqlite3
from sqlite3 import Error

from gui import *

def create_connection(filename):
	connection = None
	try:
		connection = sqlite3.connect(filename)
		print(sqlite3.version)
	except Error as e:
		print(e)

	return connection

def create_table(connection, sql_query):
	try:
		c = connection.cursor()
		c.execute(sql_query)
	except Error as e:
		print(e)

def insert_book(connection, book):
	query = ''' INSERT INTO books(book_id, book_name, author_name, pub_date, pub_plc, price, is_borrowed)
				VALUES(?, ?, ?, ?, ?, ?, ?) '''

	cur = connection.cursor()
	cur.execute(query, book)
	connection.commit()

	return cur.lastrowid


def init_database():
	connection = create_connection("c:/dev/clientappdatabase/library.db")

	with connection:
		create_table(connection, """
				CREATE TABLE IF NOT EXISTS books (
					book_id integer PRIMARY KEY,
					book_name text NOT NULL,
					author_name text NOT NULL,
					pub_date text NOT NULL,
					pub_plc text NOT NULL,
					price integer NOT NULL,
					is_borrowed integer NOT NULL
				)""")

		create_table(connection, """
				CREATE TABLE IF NOT EXISTS stories (
					book_id integer NOT NULL,
					story_name text NOT NULL,
					genre text NOT NULL,
					comment text NOT NULL
				)""")

	return connection

def print_output(ouput):
	for i in ouput:
		print(i)

def main():
	connection = init_database()

	screen_width = 1600
	screen_height = 900
	init_window(screen_width, screen_height, "Home Library")
	set_target_fps(60)

	controlX = screen_width / 2 + 300
	controlY = 0


	authorInputBox = InputBox(controlX + 200, controlY + 60, 260, 30, 21)
	bookInputBox = InputBox(controlX + 200, controlY + 100, 260, 30, 21)
	searchBookAuthorButton = Button("Search", controlX + 20, controlY + 140, 85, 30, SKYBLUE)
	storyInputBox = InputBox(controlX + 200, controlY + 240, 260, 30, 21)		
	searchStoryButton = Button("Search", controlX + 20, controlY + 280, 85, 30, SKYBLUE)
	genreDropDown = DropDown(controlX + 200, controlY + 380, 260, 30, [ "Sci-Fi", "Detectives", "Adventures"])
	genrePickButton = Button("Search", controlX + 20, controlY + 420, 85, 30, SKYBLUE)
	authorStorySearchInputBox = InputBox(controlX + 200, controlY + 520, 260, 30, 21)
	authorStorySearchButton = Button("Search", controlX + 20, controlY + 560, 85, 30, SKYBLUE)
	
	authorNovelCountInputBox = InputBox(controlX + 200, controlY + 660, 260, 30, 21)
	authorNovelCountDropDown = DropDown(controlX + 200, controlY + 700, 260, 30, [ "Sci-Fi", "Detectives", "Adventures"])
	authorNovelCountButton = Button("Count", controlX + 20, controlY + 740, 70, 30, SKYBLUE)
	authorNovelCountInputCheckBox = CheckBox(controlX + 150, controlY + 660, 30, 30)
	authorNovelCountDropDownCheckBox = CheckBox(controlX + 150, controlY + 700, 30, 30)

	duplicatesButton = Button("Print", controlX + 300, controlY + 840, 60, 30, SKYBLUE)

	searchNovelByCommentInputBox = InputBox(controlX + 200, controlY + 960, 260, 30, 100)
	searchNovelByCommentButton = Button("Search", controlX + 20, controlY + 1000, 85, 30, SKYBLUE)

	addCommentNovelInputBox = InputBox(controlX + 200, controlY + 1110, 260, 30, 21)
	addCommentCommentInputBox = InputBox(controlX + 200, controlY + 1150, 260, 30, 100)
	addCommentButton = Button("Update", controlX + 20, controlY + 1190, 85, 30, SKYBLUE)
	
	currentInputBox = authorInputBox

	resultViewer = ResultViewer()
	
	while not window_should_close():
		# =====================================
		# Input
		mousePosition = get_mouse_position()
		if (mousePosition.x > controlX):
			controlY += get_mouse_wheel_move() * 15

		if (controlY > 0):
			controlY = 0
		if (controlY < -350):
			controlY = -350

		if (authorInputBox.isClicked()):
			currentInputBox.drawAsClicked = False
			currentInputBox = authorInputBox
			currentInputBox.drawAsClicked = True

		if (bookInputBox.isClicked()):
			currentInputBox.drawAsClicked = False
			currentInputBox = bookInputBox
			currentInputBox.drawAsClicked = True

		if (storyInputBox.isClicked()):
			currentInputBox.drawAsClicked = False
			currentInputBox = storyInputBox
			currentInputBox.drawAsClicked = True

		if (authorStorySearchInputBox.isClicked()):
			currentInputBox.drawAsClicked = False
			currentInputBox = authorStorySearchInputBox
			currentInputBox.drawAsClicked = True

		if (authorNovelCountInputBox.isClicked()):
			currentInputBox.drawAsClicked = False
			currentInputBox = authorNovelCountInputBox
			currentInputBox.drawAsClicked = True

		if (searchNovelByCommentInputBox.isClicked()):
			currentInputBox.drawAsClicked = False
			currentInputBox = searchNovelByCommentInputBox
			currentInputBox.drawAsClicked = True

		if (addCommentNovelInputBox.isClicked()):
			currentInputBox.drawAsClicked = False
			currentInputBox = addCommentNovelInputBox
			currentInputBox.drawAsClicked = True

		if (addCommentCommentInputBox.isClicked()):
			currentInputBox.drawAsClicked = False
			currentInputBox = addCommentCommentInputBox
			currentInputBox.drawAsClicked = True

		if (currentInputBox and currentInputBox.drawAsClicked):
			key = get_key_pressed()
			if (key >= 32 and key <= 125):
				if (currentInputBox.charsLeft > 0):
					currentInputBox.inputText += chr(key).lower()
					currentInputBox.charsLeft -= 1
			elif (is_key_pressed(KEY_BACKSPACE)):
				currentInputBox.inputText = currentInputBox.inputText[:-1]
				if (currentInputBox.charsLeft <= currentInputBox.maxCharacters):
					currentInputBox.charsLeft += 1
		# =====================================

		begin_drawing()

		clear_background(RAYWHITE)

		#=======================================
		# Result viewer
		resultViewer.draw(controlX - 1, screen_height)
		#=======================================
		

		# Control panel
		draw_rectangle(controlX, 0, screen_width / 2, screen_height, LIGHTGRAY)
		draw_line(controlX, 0, controlX, screen_height, DARKGRAY)

		# ======================================
		# Book search by author or name controls
		BackgroundBox.draw(controlX, controlY + 45, screen_width, 135, GRAY)
		draw_text("Find book by author or name", controlX + 20, controlY + 10, 30, DARKGRAY)

		Splitter.draw(controlX, controlY + 45)
		draw_text("Author", controlX + 20, controlY + 60, 30, DARKGRAY)
		authorInputBox.draw(controlY)

		draw_text("Book name", controlX + 20, controlY + 100, 30, DARKGRAY)
		bookInputBox.draw(controlY)

		searchBookAuthorButton.draw(controlY)
		if(searchBookAuthorButton.isClicked()):
			cur = connection.cursor()
			if (authorInputBox.inputText and bookInputBox.inputText):
				print(bookInputBox.inputText)
				cur.execute(""" SELECT book_name, author_name, pub_date, pub_plc, price
								FROM books WHERE (books.book_name = ? AND books.author_name = ?) """, (bookInputBox.inputText, authorInputBox.inputText))
				resultViewer.header = ["Book name", "Author name", "Publication Date", "Publication Place", "Price"]
				resultViewer.results = cur.fetchall()
			elif (authorInputBox.inputText):
				cur.execute(""" SELECT book_name, author_name, pub_date, pub_plc, price
								FROM books WHERE books.author_name = ? """, (authorInputBox.inputText, ))
				resultViewer.header = ["Book name", "Author name", "Publication Date", "Publication Place", "Price"]
				resultViewer.results = cur.fetchall()
			elif (bookInputBox.inputText):
				cur.execute(""" SELECT book_name, author_name, pub_date, pub_plc, price
								FROM books WHERE books.book_name = ? """, (bookInputBox.inputText, ))
				resultViewer.header = ["Book name", "Author name", "Publication Date", "Publication Place", "Price"]
				resultViewer.results = cur.fetchall()

		Splitter.draw(controlX, controlY + 180)
		#=======================================


		#=======================================
		# Search story by name
		BackgroundBox.draw(controlX, controlY + 225, screen_width, 99, GRAY)
		draw_text("Find novel by name", controlX + 20, controlY + 190, 30, DARKGRAY)				
		Splitter.draw(controlX, controlY + 225)
		draw_text("Story name", controlX + 20, controlY + 240, 30, DARKGRAY)
		storyInputBox.draw(controlY)

		searchStoryButton.draw(controlY)
		if (searchStoryButton.isClicked()):
			cur = connection.cursor()
			cur.execute(""" SELECT story_name, book_name, author_name, genre, comment FROM books NATURAL JOIN stories where stories.story_name = ?""", (storyInputBox.inputText, ))
			resultViewer.header = ["Story name", "Book name", "Author name", "Genre", "Comment"]
			resultViewer.results = cur.fetchall()
		Splitter.draw(controlX, controlY + 320)
		#=======================================
		
		#=======================================
		# Search author's stories
		BackgroundBox.draw(controlX, controlY + 505, screen_width, 95, GRAY)
		draw_text("Search author's novels", controlX + 20, controlY + 470, 30, DARKGRAY)
		Splitter.draw(controlX, controlY + 505)
		draw_text("Author", controlX + 20, controlY + 520, 30, DARKGRAY)
		authorStorySearchInputBox.draw(controlY)
		authorStorySearchButton.draw(controlY)
		if (authorStorySearchButton.isClicked()):
			cur = connection.cursor()
			cur.execute(""" SELECT story_name, book_name, author_name, genre, price, comment FROM books NATURAL JOIN stories WHERE books.author_name = ?""", (authorStorySearchInputBox.inputText, ))
			resultViewer.header = ["Story name", "Book name", "Author name", "Genre", "Price", "Comment"]
			resultViewer.results = cur.fetchall()

		Splitter.draw(controlX, controlY + 600)
		#=======================================

		#=======================================
		# Print books by a genre
		BackgroundBox.draw(controlX, controlY + 365, screen_width, 99, GRAY)
		Splitter.draw(controlX, controlY + 460)
		draw_text("Print books by a genre", controlX + 20, controlY + 330, 30, DARKGRAY)
		Splitter.draw(controlX, controlY + 365)
		draw_text("Pick genre", controlX + 20, controlY + 380, 30, DARKGRAY)
		genreDropDown.draw(controlY)
		genrePickButton.draw(controlY)
		if (genrePickButton.isClicked()):
			cur = connection.cursor()
			cur.execute(""" SELECT book_name, author_name, story_name, genre, price, comment FROM stories NATURAL JOIN books WHERE stories.genre = ?""", (genreDropDown.currentVariant,))
			resultViewer.header = ["Book name", "Author name", "Story name", "Genre", "Price", "Comment"]
			resultViewer.results = cur.fetchall()
		#=======================================

		#=======================================
		# Output duplicates
		BackgroundBox.draw(controlX, controlY + 820, screen_width, 70, GRAY)
		draw_text("Duplicates Info", controlX + 20, controlY + 790, 30, DARKGRAY)
		Splitter.draw(controlX, controlY + 820)
		duplicatesButton.draw(controlY)	
		draw_text("Print duplicates", controlX + 20, controlY + 840, 30, DARKGRAY)
		if (duplicatesButton.isClicked()):
			cur = connection.cursor()
			cur.execute(""" SELECT book_name, author_name, pub_date, pub_plc, story_name, genre, price, comment FROM books
							NATURAL JOIN
							(SELECT * FROM stories NATURAL JOIN (SELECT story_name FROM stories GROUP BY story_name HAVING COUNT(story_name) > 1))""")
			resultViewer.header = ["Book name", "Author name", "Publication Date", "Publication Place", "Story name", "Genre", "Price", "Comment"]
			resultViewer.results = cur.fetchall()
		#=======================================

		#=======================================
		# Count stories by author or genre
		BackgroundBox.draw(controlX, controlY + 645, screen_width, 135, GRAY)
		draw_text("Count novels", controlX + 20, controlY + 610, 30, DARKGRAY)
		Splitter.draw(controlX, controlY + 645)
		Splitter.draw(controlX, controlY + 780)
		draw_text("Author", controlX + 20, controlY + 660, 30, DARKGRAY)
		authorNovelCountInputBox.draw(controlY)
		draw_text("Genre", controlX + 20, controlY + 700, 30, DARKGRAY)
		authorNovelCountDropDown.draw(controlY)
		authorNovelCountButton.draw(controlY)
		authorNovelCountInputCheckBox.draw(controlY)
		authorNovelCountDropDownCheckBox.draw(controlY)
		if (authorNovelCountButton.isClicked()):
			cur = connection.cursor()
			if (authorNovelCountDropDownCheckBox.checked and authorNovelCountInputCheckBox.checked):
				cur.execute(""" SELECT COUNT(distinct story_name) FROM books NATURAL JOIN stories WHERE books.author_name = ? and stories.genre = ?""", 
					(authorNovelCountInputBox.inputText, authorNovelCountDropDown.currentVariant))
				resultViewer.header = [f"Number of {authorNovelCountDropDown.currentVariant} novels by {authorNovelCountInputBox.inputText} "]
			elif (authorNovelCountDropDownCheckBox.checked):
				cur.execute(""" SELECT COUNT(distinct story_name) FROM books NATURAL JOIN stories WHERE stories.genre = ? """, (authorNovelCountDropDown.currentVariant,))
				resultViewer.header = [f"Number of {authorNovelCountDropDown.currentVariant} novels"]
			elif (authorNovelCountInputCheckBox.checked):
				cur.execute(""" SELECT COUNT(distinct story_name) FROM books NATURAL JOIN stories WHERE books.author_name = ?""", (authorNovelCountInputBox.inputText, ))
				resultViewer.header = [f"Number of novels by {authorNovelCountInputBox.inputText}"]

			resultViewer.results = cur.fetchall()
		#=======================================

		#=======================================
		# Search novels by comment
		BackgroundBox.draw(controlX, controlY + 940, screen_width, 110, GRAY)
		Splitter.draw(controlX, controlY + 890)
		draw_text("Search a novel by a comment", controlX + 20, controlY + 900, 30, DARKGRAY)
		Splitter.draw(controlX, controlY + 940)
		draw_text("Comment", controlX + 20, controlY + 960, 30, DARKGRAY)
		searchNovelByCommentInputBox.draw(controlY)
		searchNovelByCommentButton.draw(controlY)
		if (searchNovelByCommentButton.isClicked()):
			cur = connection.cursor()
			cur.execute(""" SELECT book_name, story_name, author_name, genre, price, comment FROM books NATURAL JOIN stories WHERE stories.comment = ? """, (searchNovelByCommentInputBox.inputText,))
			resultViewer.header = ["Book name", "Story name", "Author name", "Genre", "Price", "Comment"]
			resultViewer.results = cur.fetchall()
		Splitter.draw(controlX, controlY + 1050)
		#=======================================
		
		#=======================================
		# Add or update comment
		BackgroundBox.draw(controlX, controlY + 1090, screen_width, 145, GRAY)
		draw_text("Update or add comment", controlX + 20, controlY + 1060, 30, DARKGRAY)
		Splitter.draw(controlX, controlY + 1090)

		draw_text("Novel", controlX + 20, controlY + 1110, 30, DARKGRAY)
		addCommentNovelInputBox.draw(controlY)
		draw_text("Comment", controlX + 20, controlY + 1150, 30, DARKGRAY)
		addCommentCommentInputBox.draw(controlY)
		addCommentButton.draw(controlY)

		if (addCommentButton.isClicked()):
			cur = connection.cursor()
			cur.execute(""" UPDATE stories SET comment = ? WHERE stories.story_name = ?""", (addCommentCommentInputBox.inputText, addCommentNovelInputBox.inputText))
			cur.execute(""" SELECT story_name, comment FROM stories WHERE stories.story_name = ?""", (addCommentNovelInputBox.inputText, ))
			connection.commit()
			resultViewer.header = ["Story name", "Comment"]
			resultViewer.results = cur.fetchall()
		#=======================================

		end_drawing()

	close_window()

	dump_data = False

	if dump_data:
		book1 = (0, "book #1", "author #1", "12-03-1999", "place #1", 1200, 0)
		book2 = (1, "book #3", "author #2", "12-03-1994", "place #2",  800, 0)
		book3 = (2, "book #2", "author #1", "12-03-2009", "place #3", 1300, 0)
		insert_book(connection, book1)
		insert_book(connection, book2)
		insert_book(connection, book3)

	if dump_data:
		cur = connection.cursor()
		cur.execute(""" INSERT INTO stories(book_id, story_name, genre, comment) VALUES(0, "story #1", "Sci-Fi"		, "comment #1") """)
		cur.execute(""" INSERT INTO stories(book_id, story_name, genre, comment) VALUES(0, "story #2", "Adventures"	, 			"") """)
		cur.execute(""" INSERT INTO stories(book_id, story_name, genre, comment) VALUES(1, "story #3", "Sci-Fi"		, "comment #2") """)
		cur.execute(""" INSERT INTO stories(book_id, story_name, genre, comment) VALUES(1, "story #4", "Detectives"	, "comment #3") """)
		cur.execute(""" INSERT INTO stories(book_id, story_name, genre, comment) VALUES(1, "story #5", "Detectives"	, "comment #4") """)
		cur.execute(""" INSERT INTO stories(book_id, story_name, genre, comment) VALUES(1, "story #6", "Sci-Fi"		, "comment #5") """)
		cur.execute(""" INSERT INTO stories(book_id, story_name, genre, comment) VALUES(2, "story #7", "Adventures"	, 			"") """)
		cur.execute(""" INSERT INTO stories(book_id, story_name, genre, comment) VALUES(0, "story #7", "Adventures"	, "comment #7") """)
		connection.commit()

main()