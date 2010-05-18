# -*- coding: utf-8 -*-
"""
  Generate Metadata file with retrieving metadata from Daum
      XBMC .nfo
      Windows Media Center .xml
  by edge @ xbmc-korea.com
"""
import unicodedata
import Tkinter
from Tkconstants import *

__version__ = "0.2.0"

class KorMeta(Tkinter.Frame):
	def __init__(self, root):
		# GUI
		Tkinter.Frame.__init__(self, root)

		# button functions
		from lib.movie_cmd import MovieCommand
		self.movieCmd = MovieCommand(root)
		from lib.series_cmd import SeriesCommand
		self.seriesCmd = SeriesCommand(root)
		from lib.music_cmd import MusicCommand
		self.musicCmd = MusicCommand(root)

		# line 1: selection
		f1 = Tkinter.Frame(self)

		#   select mode
		self.opVar = Tkinter.StringVar()
		f1a = Tkinter.Frame(f1, relief=GROOVE, borderwidth=1)
		r1 = Tkinter.Radiobutton(f1a, text="Movie", variable=self.opVar, value="movie", command=self.set_mode_movie)
		r2 = Tkinter.Radiobutton(f1a, text="TV Series", variable=self.opVar, value="series", command=self.set_mode_series)
		r3 = Tkinter.Radiobutton(f1a, text="Music", variable=self.opVar, value="music", command=self.set_mode_music)
		r1.pack(anchor=W)
		r2.pack(anchor=W)
		r3.pack(anchor=W)
		f1a.pack(side=LEFT,padx=15)
		r1.select()

		#   select output mode
		self.out_xml = Tkinter.IntVar()
		self.out_nfo = Tkinter.IntVar()
		f1b = Tkinter.Frame(f1, relief=GROOVE, borderwidth=1)
		c1 = Tkinter.Checkbutton(f1b, text="XBMC nfo", variable=self.out_nfo)
		c2 = Tkinter.Checkbutton(f1b, text="WMC xml", variable=self.out_xml, command=self.set_imgout)
		c1.pack(anchor=W)
		c2.pack(anchor=W)
		f1b.pack(side=LEFT,padx=15)
		c1.select()
		c2.deselect()

		#   select output mode
		self.out_poster = Tkinter.IntVar()
		self.out_backdrop = Tkinter.IntVar()
		f1c = Tkinter.Frame(f1, relief=GROOVE, borderwidth=1)
		self.cb_o1 = Tkinter.Checkbutton(f1c, text="Poster", variable=self.out_poster, state=DISABLED)
		self.cb_o2 = Tkinter.Checkbutton(f1c, text="Backdrop", variable=self.out_backdrop, state=DISABLED)
		self.cb_o1.pack(anchor=W)
		self.cb_o2.pack(anchor=W)
		f1c.pack(side=LEFT,padx=15)
		self.cb_o1.deselect()
		self.cb_o2.deselect()

		f1.pack(padx=5,fill=X)

		# line 2: directory
		f2 = Tkinter.Frame(self)
		self.pathVar = Tkinter.StringVar()
		Tkinter.Label(f2, text="Series").pack(side=LEFT,padx=5)
		Tkinter.Entry(f2, textvariable=self.pathVar, width=40).pack(side=LEFT,fill=X,expand=True)
		f2.pack(padx=5,pady=2,fill=X)

		# line 3: buttons
		f3 = Tkinter.Frame(self)
		self.btn1 = Tkinter.Button(f3, text='Browse', command=self.movieCmd.getdir)
		self.btn2 = Tkinter.Button(f3, text='Import', command=self.movieCmd.getmeta)
		self.btn3 = Tkinter.Button(f3, text='Generate', command=self.movieCmd.genfile)
		self.btn1.pack(side=LEFT,padx=20)
		self.btn2.pack(side=LEFT,padx=20)
		self.btn3.pack(side=LEFT,padx=20)
		Tkinter.Button(f3, text='Quit', command=self.quit).pack(side=RIGHT,padx=30)
		f3.pack(padx=5,pady=4,fill=X)

		# line 4: message box
		f4 = Tkinter.Frame(self)
		self.tb = Tkinter.Text(f4, height=20, width=50)
		s = Tkinter.Scrollbar(f4)
		self.tb.pack(side=LEFT,fill=BOTH,expand=True)
		s.pack(side=RIGHT,fill=Y)
		self.tb.config(yscrollcommand=s.set)
		s.config(command=self.tb.yview)
		f4.pack(padx=5,pady=4,fill=BOTH)

		self.tb.tag_config("i", foreground="blue")
		self.tb.tag_config("e", foreground="red")

		self.movieCmd.hookTextBox(self.tb)
		self.movieCmd.hookPath(self.pathVar)
		self.movieCmd.hookSel(self.out_nfo, self.out_xml, self.out_poster, self.out_backdrop)

		self.seriesCmd.hookTextBox(self.tb)
		self.seriesCmd.hookPath(self.pathVar)
		self.seriesCmd.hookSel(self.out_nfo, self.out_xml, self.out_poster, self.out_backdrop)

		self.musicCmd.hookTextBox(self.tb)
		self.musicCmd.hookPath(self.pathVar)
		self.musicCmd.hookSel(self.out_nfo, self.out_xml, self.out_poster, self.out_backdrop)

	def set_mode_movie(self):
		self.btn1.configure(command=self.movieCmd.getdir)
		self.btn2.configure(command=self.movieCmd.getmeta)
		self.btn3.configure(command=self.movieCmd.genfile)

	def set_mode_series(self):
		self.btn1.configure(command=self.seriesCmd.getdir)
		self.btn2.configure(command=self.seriesCmd.getmeta)
		self.btn3.configure(command=self.seriesCmd.genfile)

	def set_mode_music(self):
		self.btn1.configure(command=self.musicCmd.getdir)
		self.btn2.configure(command=self.musicCmd.getmeta)
		self.btn3.configure(command=self.musicCmd.genfile)

	def set_imgout(self):
		if self.out_xml.get():
			self.cb_o1.configure(state=NORMAL)
			self.cb_o2.configure(state=NORMAL)
		else:
			self.cb_o1.configure(state=DISABLED)
			self.cb_o2.configure(state=DISABLED)

if __name__ == "__main__":
	root = Tkinter.Tk()
	KorMeta(root).pack(fill=BOTH)
	root.mainloop()
# vim: ts=4 sw=4
