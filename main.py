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

	authorInputBox = InputBox(controlX + 200, 60, 260, 30)
	bookInputBox = InputBox(controlX + 200, 100, 260, 30)
	searchBookAuthorButton = Button("Search", controlX + 20, 140, 85, 30, SKYBLUE)
	storyInputBox = InputBox(controlX + 200, 240, 260, 30)		
	searchStoryButton = Button("Search", controlX + 20, 280, 85, 30, SKYBLUE)
	genreDropDown = DropDown(controlX + 200, 380, 260, 30, [ "Sci-Fi", "Detectives", "Adventures"])
	genrePickButton = Button("Search", controlX + 20, 420, 85, 30, SKYBLUE)
	authorStorySearchInputBox = InputBox(controlX + 200, 520, 260, 30)
	authorStorySearchButton = Button("Search", controlX + 20, 560, 85, 30, SKYBLUE)
	
	authorNovelCountInputBox = InputBox(controlX + 200, 660, 260, 30)
	authorNovelCountDropDown = DropDown(controlX + 200, 700, 260, 30, [ "Sci-Fi", "Detectives", "Adventures"])
	authorNovelCountButton = Button("Count", controlX + 20, 740, 70, 30, SKYBLUE)
	authorNovelCountInputCheckBox = CheckBox(controlX + 150, 660, 30, 30)
	authorNovelCountDropDownCheckBox = CheckBox(controlX + 150, 700, 30, 30)

	duplicatesButton = Button("Print", controlX + 300, 840, 60, 30, SKYBLUE)

	resultViewer = ResultViewer()

	currentInputBox = authorInputBox

	while not window_should_close():
		# =====================================
		# Input
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

		if (currentInputBox.drawAsClicked):
			key = get_key_pressed()
			if (key >= 32 and key <= 125):
				if (currentInputBox.charsLeft > 0):
					currentInputBox.inputText += chr(key).lower()
					currentInputBox.charsLeft -= 1
			elif (is_key_pressed(KEY_BACKSPACE)):
				currentInputBox.inputText = currentInputBox.inputText[:-1]
				if (currentInputBox.charsLeft <= 21):
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
		BackgroundBox.draw(controlX, 45, screen_width, 135, GRAY)
		draw_text("Find book by author or name", controlX + 20, 10, 30, DARKGRAY)

		Splitter.draw(controlX, 45)
		draw_text("Author", controlX + 20, 60, 30, DARKGRAY)
		authorInputBox.draw()

		draw_text("Book name", controlX + 20, 100, 30, DARKGRAY)
		bookInputBox.draw()

		searchBookAuthorButton.draw()
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

		Splitter.draw(controlX, 180)
		#=======================================


		#=======================================
		# Search story by name
		BackgroundBox.draw(controlX, 225, screen_width, 99, GRAY)
		draw_text("Find novel by name", controlX + 20, 190, 30, DARKGRAY)				
		Splitter.draw(controlX, 225)
		draw_text("Story name", controlX + 20, 240, 30, DARKGRAY)
		storyInputBox.draw()

		searchStoryButton.draw()
		if (searchStoryButton.isClicked()):
			cur = connection.cursor()
			cur.execute(""" SELECT story_name, book_name, author_name, genre, comment FROM books NATURAL JOIN stories where stories.story_name = ?""", (storyInputBox.inputText, ))
			resultViewer.header = ["Story name", "Book name", "Author name", "Genre", "Comment"]
			resultViewer.results = cur.fetchall()
		Splitter.draw(controlX, 320)
		#=======================================
		
		#=======================================
		# Search author's stories
		BackgroundBox.draw(controlX, 505, screen_width, 95, GRAY)
		draw_text("Search author's novels", controlX + 20, 470, 30, DARKGRAY)
		Splitter.draw(controlX, 505)
		draw_text("Author", controlX + 20, 520, 30, DARKGRAY)
		authorStorySearchInputBox.draw()
		authorStorySearchButton.draw()
		if (authorStorySearchButton.isClicked()):
			cur = connection.cursor()
			cur.execute(""" SELECT story_name, book_name, author_name, genre, price, comment FROM books NATURAL JOIN stories WHERE books.author_name = ?""", (authorStorySearchInputBox.inputText, ))
			resultViewer.header = ["Story name", "Book name", "Author name", "Genre", "Price", "Comment"]
			resultViewer.results = cur.fetchall()

		Splitter.draw(controlX, 600)
		#=======================================

		#=======================================
		# Print books by a genre
		BackgroundBox.draw(controlX, 365, screen_width, 99, GRAY)
		Splitter.draw(controlX, 460)
		draw_text("Print books by a genre", controlX + 20, 330, 30, DARKGRAY)
		Splitter.draw(controlX, 365)
		draw_text("Pick genre", controlX + 20, 380, 30, DARKGRAY)
		genreDropDown.draw()
		genrePickButton.draw()
		if (genrePickButton.isClicked()):
			cur = connection.cursor()
			cur.execute(""" SELECT book_name, author_name, story_name, genre, price, comment FROM stories NATURAL JOIN books WHERE stories.genre = ?""", (genreDropDown.currentVariant,))
			resultViewer.header = ["Book name", "Author name", "Story name", "Genre", "Price", "Comment"]
			resultViewer.results = cur.fetchall()
		#=======================================

		#=======================================
		# Output duplicates
		BackgroundBox.draw(controlX, 820, screen_width, 100, GRAY)
		draw_text("Duplicates Info", controlX + 20, 790, 30, DARKGRAY)
		Splitter.draw(controlX, 820)
		duplicatesButton.draw()	
		draw_text("Print duplicates", controlX + 20, 840, 30, DARKGRAY)
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
		BackgroundBox.draw(controlX, 645, screen_width, 135, GRAY)
		draw_text("Count novels", controlX + 20, 610, 30, DARKGRAY)
		Splitter.draw(controlX, 645)
		Splitter.draw(controlX, 780)
		draw_text("Author", controlX + 20, 660, 30, DARKGRAY)
		authorNovelCountInputBox.draw()
		draw_text("Genre", controlX + 20, 700, 30, DARKGRAY)
		authorNovelCountDropDown.draw()
		authorNovelCountButton.draw()
		authorNovelCountInputCheckBox.draw()
		authorNovelCountDropDownCheckBox.draw()
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