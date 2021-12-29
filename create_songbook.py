#!env python3
import os
from pathlib import Path
from songbook import *
# Order by number. To order by title use OrderType.TITLE
book = Songbook(book_name="MesseBreve", number_of_song_digits=3, scores_subdir='scores', order=OrderType.NUMBER)
book.build()
print("Ok, build completed.")
compile=input("Do I compile the book with pdflatex? [Y]/n ").lower()
# Compile twice to build the Table of Contents
if compile == "" or  compile == "y":
	for i in range(2):
		os.system("pdflatex MesseBreve")
