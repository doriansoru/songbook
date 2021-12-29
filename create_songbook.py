#!env python3
# This example has been modified from that one on the README.md file, in order to compile the book into example_folder
import os
from pathlib import Path
from songbook import *
example_folder = 'example'
my_book_name = 'MesseBreve'

# Order by number. To order by title use OrderType.TITLE
book = Songbook(book_name=my_book_name, number_of_song_digits=3, scores_subdir='scores', order=OrderType.NUMBER)
book.build()
print('Ok, build completed.')
compile=input('Do I compile the book with pdflatex? [Y]/n ').lower()
# Compile twice to build the Table of Contents
if compile == '' or  compile == 'y':
	# Move the file into the example folder
	os.rename('.'.join([my_book_name, 'tex']), os.sep.join([example_folder, '.'.join([my_book_name, 'tex'])]))
	os.chdir(example_folder)
	for i in range(2):
		os.system(' '.join(['pdflatex', my_book_name]))
	print(' '.join([os.sep.join([example_folder, '.'.join([my_book_name, 'pdf'])]), 'compiled correctly']))
