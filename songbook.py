import glob
import os
import sys
import gettext
import locale
from enum import Enum

class OrderType(Enum):
	TITLE = 0
	NUMBER = 1

DEBUG = True
class Songbook:
	def __init__(self, number_of_song_digits=2, book_name='book', cover_name='cover', scores_subdir='scores', order = 'number'):
		# Initialize some variables
		self._cover_filename = scores_subdir + os.path.sep + cover_name + ".pdf"
		self._title_separator = '-'
		self._space_separator = '_'
		self._number_of_song_digits = number_of_song_digits
		self._pattern = (scores_subdir + os.path.sep + '?' * number_of_song_digits) + self._title_separator + '*' + '.pdf'
		self.book_name = book_name
		self.order = order
		# Set the locale
		locale_language = gettext.translation('base', localedir='locales', languages=[locale.getdefaultlocale()[0].partition('_')[0]])
		locale_language.install()
		_ = locale_language.gettext

	def build(self):
		if DEBUG == True:
			print(_("Leggo i nomi degli spartiti in una lista"))
		scores = glob.glob(self._pattern)
		# Sort the scores 
		if self.order == OrderType.NUMBER:
			scores.sort(key = self.get_score_number)
		else:
			scores.sort(key = self.get_score_title)
		if DEBUG == True:
			print(_("creo") + " " + self.book_name + ".tex")
		# Prepare and populate the latex file
		latex_book_filename = self.book_name + ".tex"
		try:
			latex_book = open(latex_book_filename, "w")
		except:
			print(_("Impossibile aprire il file latex"))
			quit()
		latex_book.write("""\\documentclass[a4paper]{book}
			\\usepackage{pdfpages}
			\\usepackage[utf8]{inputenc}
			\\usepackage[T1]{fontenc}
			\\usepackage[hidelinks]{hyperref}
			\\pagestyle{empty}
			\\renewcommand{\contentsname}{Indice}
			\\pdfminorversion=7
			\\begin{document}
				\\includepdf[pages=-]{\detokenize{""" + self._cover_filename + """}}
				\\tableofcontents\n""")
		if DEBUG == True:				
			print(_("popolo") + " " + self.book_name + ".tex " + _("con i dati degli spartiti"))
		i = 1
		for score in scores:
			number = str(self.get_score_number(score))
			title = self.get_score_title(score)
			latex_book.write("""\\chapter*{""" + number + """ - """ + title + """}
				\\addcontentsline{toc}{chapter}{n. """ + ("\\phantom{" + ("0" * (self._number_of_song_digits - len(number))) + "}" + number) + """ - """ + title  + """}
				{
					\\centering
					\\includepdf[pages=-]{\detokenize{""" + score + """}}
				}""")
		latex_book.write("\\end{document}")
		latex_book.close()
		if DEBUG == True:
			print(_("fine!"))

	def help(self):
		"""
		Prints an help message.
		"""
		print(_("Utilizzo:") + "\n\t" + sys.argv[0] + " [" + _("NOME FILE DEL LIBRO") + "]")

	def get_score_number(self, score):
		"""
		Returns the number of the score:
			only the last digit character of score if the first is 0
			otherwise the first self.score_number_digits characters.
		"""
		# Finds the last zero
		score = os.path.split(score)[1]
		zero_position = 0
		while score[(zero_position):(zero_position + 1)] == "0":
			zero_position += 1
		score = score[zero_position:self._number_of_song_digits]
		return int(score)

	def get_score_title(self, score):
		"""
		Returns the title of the score:
			from (self.score_number_digits + 1) to -4 character
			replacing _ with space.
		"""
		score = os.path.split(score)[1]
		return score[(self._number_of_song_digits + 1):-4].replace(self._space_separator, " ")
