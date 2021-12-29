# songbook
A python class to create a book with songs scores by merging multiple pdf in one pdf through a LaTex file.

# Requirements

- Python3
- A LaTeX distribution

# How to use

- Create a directory (for instance: `scores`)
- Decide how many digits for your score filenames (depending on the number of the scores): for instance 3
- Put your pdfs into your `scores` directory and rename them with the following format: `number-Title_underscore_Separated.pdf` (for instance: `004-O_salutaris.pdf`)
- Put a `cover.pdf`, containing the cover page, into your scores directory
- Decide if you want to order the final scores by title or by number
- Create and run a script, like in the following example (see `create_songbook.py`):
```
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

```
- Open your final file, in this case `MesseBreve.pdf`
