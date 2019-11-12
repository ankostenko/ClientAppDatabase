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
	query = ''' INSERT INTO books(id, book_name, author_name, pub_date, pub_plc) 
				VALUES(?, ?, ?, ?, ?) '''

	cur = connection.cursor()
	cur.execute(query, book)
	connection.commit()

	return cur.lastrowid


def init_database():
	connection = create_connection("c:/dev/database/library.db")

	with connection:
		create_table(connection, """
				CREATE TABLE IF NOT EXISTS books (
					id integer PRIMARY KEY,
					book_name text NOT NULL,
					author_name text NOT NULL,
					pub_date text NOT NULL,
					pub_plc text NOT NULL,

					FOREIGN KEY (id)
						REFERENCES book_name_to_id(id)
				)""")

		create_table(connection, """ 
				CREATE TABLE IF NOT EXISTS sci_fi (
					id integer PRIMARY KEY
				)""")

		create_table(connection, """ 
				CREATE TABLE IF NOT EXISTS detectives (
					id integer PRIMARY KEY
				)""")

		create_table(connection, """ 
				CREATE TABLE IF NOT EXISTS adventures (
					id integer PRIMARY KEY
				)""")

		create_table(connection, """
				CREATE TABLE IF NOT EXISTS stories (
					id integer NOT NULL,
					story_name text NOT NULL
				)""")

		create_table(connection, """ 
				CREATE TABLE IF NOT EXISTS book_name_to_id(
					book_name text NOT NULL,
					id integer PRIMARY KEY
				)""")

		create_table(connection, """ 
				CREATE TABLE IF NOT EXISTS author_name_to_id(
					author_name text NOT NULL,
					id integer NOT NULL
				)""")

		create_table(connection, """ 
				CREATE TABLE IF NOT EXISTS story_name_to_id(
					story_name text NOT NULL,
					id integer NOT NULL
				)""")


		create_table(connection, """
				CREATE TABLE IF NOT EXISTS book_to_genre(
					id integer NOT NULL,
					genre text NOT NULL
				)""")

	return connection

def main():
	connection = init_database()

	screen_width = 1200
	screen_height = 900
	init_window(screen_width, screen_height, "Home Library")
	set_target_fps(60)

	controlX = screen_width / 2 + 100

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
	duplicatesButton = Button("Print", controlX + 300, 840, 60, 30, SKYBLUE)

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
			print("[QUERY] Author or name search")
			cur = connection.cursor()
			if (authorInputBox.inputText and bookInputBox.inputText):
				print(authorInputBox.inputText)
				print(bookInputBox.inputText)
				cur.execute(""" SELECT * 
								FROM books 
								WHERE (books.book_name = ? AND books.author_name = ?)""", 
								(bookInputBox.inputText, authorInputBox.inputText))
				print(cur.fetchall())
			elif (authorInputBox.inputText):
				print(authorInputBox.inputText)
				cur.execute(""" SELECT * FROM books
								WHERE books.author_name = ?
								""", (authorInputBox.inputText, ))
				print(cur.fetchall())
			elif (bookInputBox.inputText):
				print(bookInputBox.inputText)
				cur.execute(""" SELECT * FROM books
								WHERE books.book_name = ?
								""", (bookInputBox.inputText, ))
				print(cur.fetchall())
		

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
			cur.execute(""" SELECT * FROM books WHERE books.id = (SELECT id FROM stories WHERE (story_name = ? AND books.id = id))""", (storyInputBox.inputText, ))
			print(cur.fetchall())
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
			print("Search stories - ", authorStorySearchInputBox.inputText)
			cur = connection.cursor()
			cur.execute("""
				SELECT author_name, story_name, book_name, genre FROM
				(SELECT * FROM stories NATURAL JOIN books WHERE books.author_name = ?)
				NATURAL JOIN
				(SELECT * from stories NATURAL JOIN book_to_genre)
				""", (authorStorySearchInputBox.inputText, ))
			print(cur.fetchall())

		Splitter.draw(controlX, 600)
		#=======================================

		#=======================================
		# Print a genre
		BackgroundBox.draw(controlX, 365, screen_width, 99, GRAY)
		Splitter.draw(controlX, 460)
		draw_text("Print books by genre", controlX + 20, 330, 30, DARKGRAY)
		Splitter.draw(controlX, 365)
		draw_text("Pick genre", controlX + 20, 380, 30, DARKGRAY)
		genreDropDown.draw()
		genrePickButton.draw()
		if (genrePickButton.isClicked()):
			print("Books by genre - ")
			cur = connection.cursor()
			cur.execute(""" SELECT book_name, author_name, pub_date, pub_plc, genre
							FROM books INNER JOIN book_to_genre as bg ON books.id = bg.id AND bg.genre = ? """, (genreDropDown.currentVariant,))
			print(cur.fetchall())

		#=======================================

		#=======================================
		# Output duplicates
		BackgroundBox.draw(controlX, 820, screen_width, 100, GRAY)
		draw_text("Duplicates Info", controlX + 20, 790, 30, DARKGRAY)
		Splitter.draw(controlX, 820)
		duplicatesButton.draw()	
		draw_text("Print duplicates", controlX + 20, 840, 30, DARKGRAY)
		if (duplicatesButton.isClicked()):
			print("Print duplicates")
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
		if (authorNovelCountButton.isClicked()):
			print("Count novels - ", authorNovelCountDropDown.currentVariant, authorNovelCountInputBox.inputText)
		#=======================================

		end_drawing()

	close_window()

	dump_data = False

	if dump_data:
		cur = connection.cursor()
		cur.execute(""" INSERT INTO book_name_to_id(book_name, id) VALUES('Name #1', 0) """)
		cur.execute(""" INSERT INTO book_name_to_id(book_name, id) VALUES('Name #3', 1) """)
		cur.execute(""" INSERT INTO book_name_to_id(book_name, id) VALUES('Name #2', 2) """)

		connection.commit()

	if dump_data:
		book1 = (0, "book #1", "author #1", "12-03-1999", "place #1")
		book2 = (1, "book #3", "author #2", "12-03-1994", "place #2")
		book3 = (2, "book #2", "author #1", "12-03-2009", "place #3")
		insert_book(connection, book1)
		insert_book(connection, book2)
		insert_book(connection, book3)

	if dump_data:
		cur = connection.cursor()
		# it should be "id -> book_id"
		cur.execute(""" INSERT INTO stories(id, story_name) VALUES(0, "story #1") """)
		cur.execute(""" INSERT INTO stories(id, story_name) VALUES(0, "story #2") """)
		cur.execute(""" INSERT INTO stories(id, story_name) VALUES(1, "story #3") """)
		cur.execute(""" INSERT INTO stories(id, story_name) VALUES(1, "story #4") """)
		cur.execute(""" INSERT INTO stories(id, story_name) VALUES(1, "story #5") """)
		cur.execute(""" INSERT INTO stories(id, story_name) VALUES(1, "story #6") """)
		cur.execute(""" INSERT INTO stories(id, story_name) VALUES(2, "story #7") """)
		connection.commit()

	if dump_data:
		cur = connection.cursor()
		cur.execute(""" INSERT INTO book_to_genre(id, genre) VALUES(2, "Sci-Fi") """)
		cur.execute(""" INSERT INTO book_to_genre(id, genre) VALUES(0, "Sci-Fi") """)
		cur.execute(""" INSERT INTO book_to_genre(id, genre) VALUES(1, "Adventures") """)
		connection.commit()

	if dump_data:
		cur = connection.cursor()
		cur.execute(""" INSERT INTO author_name_to_id(id, author_name) VALUES(0, "author #1") """)
		cur.execute(""" INSERT INTO author_name_to_id(id, author_name) VALUES(2, "author #1") """)
		cur.execute(""" INSERT INTO author_name_to_id(id, author_name) VALUES(1, "author #2") """)
		connection.commit()

main()