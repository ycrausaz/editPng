from tkinter import *
from tkinter import Frame
from tkinter import filedialog
from tkinter import font
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import colorchooser
from tkinter.simpledialog import Dialog
import tkinter as tk
import os
from PIL import ImageTk, Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm
from datetime import datetime
from pathlib import Path
import os.path
from os import path
from configparser import ConfigParser


class configDialog(Dialog):
	def __init__(self, parent, title, initialText, theFontName, theFontSize, theFontColor):
		self.configColor = None
		self.configFont = None
		self.configFontSize = None
		self.my_text = initialText
		self.my_fontName = theFontName
		self.my_fontSize = theFontSize
		self.my_fontColor = theFontColor
		Dialog.__init__(self, parent, title)

	def body(self, frame):
		if self.my_fontName == None or self.my_fontSize == None or self.my_fontColor == None:
			self.my_fontName = "Times"
			self.my_fontSize = "70"
			self.my_fontColor = "Blue"

		self.my_font = font.Font(family=self.my_fontName, size=self.my_fontSize)

		self.my_textField = Label(frame, text=self.my_text, font = self.my_font, width=len(self.my_text), fg=self.my_fontColor)
		self.my_textField.grid(row=0, column=0, columnspan=4)
#		self.my_textField.grid_rowconfigure(0, weight = 1)
#		self.my_textField.grid_columnconfigure(0, weight = 1)

		fontList = font.families()
		self.clickedFont = StringVar()
		self.clickedFont.set(self.my_fontName)
		self.my_configFontDropdown = OptionMenu(frame, self.clickedFont, *fontList, command=self.fontSelectedFromDropdown)
		self.my_configFontDropdown.grid(row=1, column=0)

		fontSizeList = range(10, 100)
		self.clickedFontSize = StringVar()
		self.clickedFontSize.set(self.my_fontSize)
		self.my_configFontSizeDropdown = OptionMenu(frame, self.clickedFontSize, *fontSizeList, command=self.fontSelectedFromDropdown)
		self.my_configFontSizeDropdown.grid(row=1, column=1)

		self.my_btn_fontColor = Button(frame, text="Couleur police", command=self.chooseFontColor)
		self.my_btn_fontColor.grid(row=1, column=2)

		self.ok_button = Button(frame, text="OK", width=5, command=self.ok_pressed)
		self.ok_button.grid(row=2, column=0)
		self.cancel_button = Button(frame, text="Annuler", width=5, command=self.cancel_pressed)
		self.cancel_button.grid(row=2, column=2)

		self.fontSelectedFromDropdown()

	def chooseFontColor(self):
		self.my_fontColor = colorchooser.askcolor()[1]
		self.configColor = self.my_fontColor
#		print("chooseFontColor:")
#		print(self.my_fontColor)
		self.my_textField.config(fg=self.my_fontColor)

	def fontSelectedFromDropdown(self, event=None):
		self.my_font.config(family=self.clickedFont.get())
		self.configFont = self.clickedFont.get()
		self.my_font.config(size=int(self.clickedFontSize.get()))
		self.configFontSize = int(self.clickedFontSize.get())

	def ok_pressed(self):
		self.destroy()

	def cancel_pressed(self):
		self.configFont = None
		self.configFontSize = None
		self.configColor = None
		self.destroy()

	def buttonbox(self):
		pass


class coordDialog(Dialog):
	def __init__(self, parent, title, old_x, old_y):
		self.old_x = old_x
		self.old_y = old_y
		self.setCoord_x = None
		self.setCoord_y = None
		Dialog.__init__(self, parent, title)

	def body(self, frame):
		self.my_old_label_x = Label(frame, text="Ancien horizontal = ", justify=RIGHT)
		self.my_old_label_x.grid(row=0, column=0, sticky=E)

		my_text=self.old_x
		self.my_old_entry_x = Label(frame, text=my_text, justify=LEFT)
		self.my_old_entry_x.grid(row=0, column=1, sticky=W)

		self.my_old_label_y = Label(frame, text="Ancien vertical = ", justify=RIGHT)
		self.my_old_label_y.grid(row=0, column=2, sticky=E)

		my_text=self.old_y
		self.my_old_entry_y = Label(frame, text=my_text, justify=LEFT)
		self.my_old_entry_y.grid(row=0, column=3, sticky=W)

		self.my_label_x = Label(frame, text="Nouveau horizontal = ", justify=RIGHT)
		self.my_label_x.grid(row=1, column=0, sticky=E)

		self.my_entry_x = Entry(frame, width=5)
		self.my_entry_x.insert(END, self.old_x)
		self.my_entry_x.grid(row=1, column=1, sticky=W)

		self.my_label_y = Label(frame, text="Nouveau vertical = ", justify=RIGHT)
		self.my_label_y.grid(row=1, column=2, sticky=E)

		self.my_entry_y = Entry(frame, width=5)
		self.my_entry_y.insert(END, self.old_y)
		self.my_entry_y.grid(row=1, column=3, sticky=W)

		self.my_entry_x.selection_range(0, END)

		self.my_entry_x.bind('<KP_Enter>', self.ok_pressed)
		self.my_entry_y.bind('<KP_Enter>', self.ok_pressed)
		self.my_entry_x.bind('<Return>', self.ok_pressed)
		self.my_entry_y.bind('<Return>', self.ok_pressed)

		self.ok_button = Button(frame, text="OK", width=5, command=self.ok_pressed)
		self.ok_button.grid(row=2, column=0, columnspan=2)
		self.cancel_button = Button(frame, text="Annuler", width=5, command=self.cancel_pressed)
		self.cancel_button.grid(row=2, column=2, columnspan=2)

		return self.my_entry_x

	# Trick for the method to be accepted as event from the button command AND the .bind
	def ok_pressed(self, event=None):
		self.setCoord_x = self.my_entry_x.get()
		self.setCoord_y = self.my_entry_y.get()
		self.destroy()

	def cancel_pressed(self, event=None):
		self.setCoord_x = None
		self.setCoord_y = None
		self.destroy()

	def buttonbox(self):
		pass


class dbmg(Frame):

	def setCoord(self, event):
		theCoords = coordDialog(root, "Positionnement", self.my_input_text_x, self.my_input_text_y)
		if theCoords.setCoord_x == None and theCoords.setCoord_y == None:
			pass
		else:
			self.my_input_text_x = theCoords.setCoord_x
			self.my_input_text_y = theCoords.setCoord_y
			self.injectText()

	def imageConfig(self):
		my_config = configDialog(root, "Configuration", self.my_input_text.get(), self.my_fontName, self.my_fontSize, self.my_fontColor)
		if my_config.configFont == None and my_config.configFontSize == None and my_config.configColor == None:
			print("Nothing selected")
		else:
			# self.my_btn_setText.configure(state = tk.NORMAL)
			self.my_btn_position.configure(state = tk.NORMAL)
			# https://stackoverflow.com/questions/54838013/oserror-cannot-open-resource
			self.my_fontName = fm.findfont(fm.FontProperties(family=my_config.configFont))
			self.my_fontSize = my_config.configFontSize
			self.my_font = ImageFont.truetype(font=self.my_fontName, size=self.my_fontSize)
			self.my_fontName = my_config.configFont
			self.my_fontColor = my_config.my_fontColor
			self.injectText()

	def chooseCoord(self, event):
		if self.my_btn_position['state'] == tk.NORMAL:
			self.my_input_text_x = event.x
			self.my_input_text_y = event.y
			self.injectText()

	def readText(self, event):
		if len(self.my_input_text.get()) > 0:
			self.my_btn_config.configure(state=tk.NORMAL)
		else:
			self.my_btn_config.configure(state=tk.DISABLED)
	
	def getCursor(self, event):
		x, y = event.x, event.y
		if self.my_btn_position['state'] == tk.NORMAL:
			if x >= 0 and x <= self.my_label.winfo_width() and y >= 0 and y <= self.my_label.winfo_height():
				txt = 'Old position ('
				txt += '%4s' % self.my_input_text_x
				txt += ', '
				txt += '%4s' % self.my_input_text_y
				txt += ')\n'
				txt += 'New position ('
				txt += '%4s' % x
				txt += ', '
				txt += '%4s' % y
				txt += ')'
				self.my_btn_position.config(text=txt, width=20, justify=LEFT)

	def chooseImage(self):
#		my_path = Path(__file__).parents[3]
		self.my_filename = filedialog.askopenfilename(initialdir=self.my_path, title="Choix du fichier", filetypes=(("PNG file", "*.png"), ("JPG file", "*.jpg")))
		if len(self.my_filename) > 0:
			if path.exists(self.my_filename):
				self.my_image = Image.open(self.my_filename)
				my_imageTk = ImageTk.PhotoImage(self.my_image)
				self.my_label.configure(image=my_imageTk)
				self.my_label.image = my_imageTk
				self.my_input_label.configure(state=tk.NORMAL)
				self.my_input_text.configure(state=tk.NORMAL)
	
	def injectText(self):
		self.my_image = Image.open(self.my_filename)
		my_imageDraw = ImageDraw.Draw(self.my_image)
		my_imageDraw.text((int(self.my_input_text_x), int(self.my_input_text_y)), self.my_input_text.get(), font=self.my_font, fill=self.my_fontColor)
		my_imageTk = ImageTk.PhotoImage(self.my_image)
		self.my_label.configure(image = my_imageTk)
		self.my_label.image = my_imageTk
		self.my_btn_save.configure(state = tk.NORMAL)
	
	def saveImage(self):
		self.my_saved_filename = os.path.basename(self.my_filename)
		self.my_saved_filename = os.path.splitext(self.my_saved_filename)[0]
		self.my_saved_filename = "result_" + self.my_saved_filename
		self.my_saved_filename += "_"
		self.my_saved_filename += self.my_input_text.get()
		self.my_saved_filename += "_" + datetime.now().strftime("%Y%m%d%H%M%S")
		self.my_saved_filename += ".png"
#		self.my_path = Path(__file__).parents[3]
		self.file_saved = filedialog.asksaveasfile(filetypes=(("PNG Images", "*.png"), ("JPG Images", "*.jpg")), initialdir=self.my_path, initialfile=self.my_saved_filename)
		if self.file_saved is not None:
			self.my_saved_filename = self.file_saved.name
			self.my_image.save(self.my_saved_filename)
			self.my_path = os.path.dirname(self.my_saved_filename)
			messagebox.showinfo("showinfo", "Le fichier '" + os.path.basename(self.my_saved_filename) + "' a été créé avec succès dans le répertoire '" + os.path.dirname(self.my_saved_filename) + "'.")

	def exitProg(self):
		self.dbmg_config.set('Font', 'fontname', str(self.my_fontName))
		self.dbmg_config.set('Font', 'fontsize', str(self.my_fontSize))
		self.dbmg_config.set('Font', 'fontcolor', str(self.my_fontColor))
		self.dbmg_config.set('Coord', 'x', str(self.my_input_text_x))
		self.dbmg_config.set('Coord', 'y', str(self.my_input_text_y))
		self.dbmg_config.set('Path', 'lastusedpath', str(self.my_path))
		self.dbmg_config.set('Text', 'lasttext', self.my_input_text.get())
		self.saveCfg(self.dbmg_config_path, self.dbmg_config)
		root.destroy()

	def buildGUI(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent

		# self.my_fontName = None
		# self.my_fontSize = None
		# self.my_fontColor = None

		self.my_label = Label(root)
		self.my_label.grid(row=0, column=0, columnspan=7)

		self.my_image = Image.open("background-small.png")
		self.my_image = ImageTk.PhotoImage(self.my_image)
		self.my_label.configure(image=self.my_image)
		self.my_label.image = self.my_image

		self.my_filename = ""

		self.my_btn_open = Button(parent, text="Choisir image", height=2, command=self.chooseImage)
		self.my_btn_open.grid(row=1, column=0)

		self.my_input_label = Label(parent, text="Texte à injecter : ")
		self.my_input_label.grid(row=1, column=1)
		self.my_input_label.configure(state=tk.DISABLED)

		txt = StringVar(root, value=self.initialText)
		self.my_input_text = Entry(parent, width=50, textvariable=txt)
		self.my_input_text.grid(row=1, column=2)
		self.my_input_text.configure(state=tk.DISABLED)

		self.my_btn_config = Button(parent, text="Configuration", height=2, command=self.imageConfig)
		self.my_btn_config.grid(row=1, column=3)
		self.my_btn_config.configure(state=tk.DISABLED)

		self.my_btn_position = Button(parent, width=20, justify=CENTER, height=2)
		self.my_btn_position.grid(row=1, column=4)
		self.my_btn_position.configure(state = tk.DISABLED)

		self.my_btn_save = Button(parent, text="Sauvegarder", height=2, command=self.saveImage)
		self.my_btn_save.grid(row=1, column=5)
		self.my_btn_save.configure(state = tk.DISABLED)

		self.my_btn_exit = Button(parent, text="Exit", height=2, command=self.exitProg)
		self.my_btn_exit.grid(row=1, column=6)

		self.my_label.bind('<Motion>', self.getCursor)
		self.my_label.bind('<Button>', self.chooseCoord)
		self.my_input_text.bind('<Key>', self.readText)
		self.my_btn_position.bind('<Button>', self.setCoord)

	def as_dict(config):
		the_dict = {}

		for section in config.sections():
			the_dict[section] = {}
			for key, val in config.items(section):
				the_dict[section][key] = val

		return the_dict

	def loadCfg(self, path, cfg):
		if not os.path.isfile(path) or os.path.getsize(path) < 1:
			saveCfg(path, cfg)
		cfg.read(path, encoding='utf-8')  # "read" doesn't return a value.

	def saveCfg(self, path, cfg):
		with open(path, mode='w', encoding="utf-8") as cfgfile:
			cfg.write(cfgfile)

	def __init__(self, parent):
		self.dbmg_config = ConfigParser()
		self.dbmg_config_path = os.path.join(str(Path.home()), '.dbmg_config.cfg')
		if not os.path.exists(self.dbmg_config_path):
			self.dbmg_config.add_section('Font')
			self.dbmg_config.set('Font', 'fontname', 'Verdana')
			self.dbmg_config.set('Font', 'fontsize', '55')
			self.dbmg_config.set('Font', 'fontcolor', 'red')
			self.dbmg_config.add_section('Coord')
			self.dbmg_config.set('Coord', 'x', '300')
			self.dbmg_config.set('Coord', 'y', '300')
			self.dbmg_config.add_section('Path')
			self.dbmg_config.set('Path', 'lastusedpath', str(Path.home()))
			self.dbmg_config.add_section('Text')
			self.dbmg_config.set('Text', 'lasttext', 'Default text...')
			self.saveCfg(self.dbmg_config_path, self.dbmg_config)

		self.loadCfg(self.dbmg_config_path, self.dbmg_config)
		self.my_fontName = self.dbmg_config.get('Font', 'fontname')
		self.my_fontSize = self.dbmg_config.get('Font', 'fontsize')
		self.my_fontColor = self.dbmg_config.get('Font', 'fontcolor')
		self.my_input_text_x = self.dbmg_config.get('Coord', 'x')
		self.my_input_text_y = self.dbmg_config.get('Coord', 'y')
		self.my_path = self.dbmg_config.get('Path', 'lastusedpath')
		self.initialText = self.dbmg_config.get('Text', 'lasttext')
		self.buildGUI(parent)


if __name__ == "__main__":
	root = Tk()
	root.title('deb.massage - Promo customization')
#	img = tk.Image("photo", file="icon.png")
#	root.tk.call('wm', 'iconphoto', root._w, img)
	my_dbmg = dbmg(root)
	root.mainloop()
