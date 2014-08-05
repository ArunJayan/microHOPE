#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  MicroHOPE IDE program, a wxpython text widget with File I/O, Compile and Upload , undo and redo , deivice selection 
#  Author  : Arun Jayan
#  email id: arunjayan32@gmail.com , arun.jayan.j@ieee.org
#  Licence : GPL version 3
#  version : microHOPE 4.0.1
"""
##############################################################################################
Features implemented :
	1. We can Compile a AVR C program using this IDE. It will generate a .hex file of corresponding
	   C Program.(to compilation we are using avr-gcc)
	2. It is Mainly designed for MicroHOPE(Micro-controllers for Hobby Projects and Education) .
	3. This IDE will detect 2 Board or versions of microhope hardware ( board using ft232 ic and  another board(latest) using Mcp220 usb interfacing is)
	4. It can uplod programmes to microHOPE using avrdude 
	3. Undo/Redo is implemented . 
	4. A Status bar is there to view the line and column number
	5. A Toolbar is there to easy access
	6. We can also uplod Program through USBASP addon module to mcu.
	7. We can Set microhope Bootloader through USBASP.
	8. We can RESET our microhope from IDE using Soft RST option
	9. Microhope 3.0.1 also support Assembly 
 ##############################################################################################																							##
"""
import wx
import os
import commands
import time
import serial

class microhope(wx.Frame):
	def __init__(self,parent,id,title,size):
		wx.Frame.__init__(self,parent,id,title,size = wx.Size(800,600))
		
		self.modify = False
		self.Last_file = ''
		self.Last_dir = ''
		self.undo = []
		self.redo = []
		self.dname = ''
		self.fname = ''
		self.mhdevice = 'Not connected'
		self.mcu = 'atmega32'
		self.isnew = True
		# Text widget
		self.SetTitle("uHOPE :: File --> "+"Not selected"+"\t\tDevice -->"+"Not connected")
		self.text = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
		self.text.Bind(wx.EVT_TEXT, self.istext_changed, id=1)
		self.text.Bind(wx.EVT_KEY_DOWN, self.key_down)
		self.Bind(wx.EVT_CLOSE, self.Quit)
		self.backup = self.text.GetValue()
		self.statusbar = self.CreateStatusBar() 
		# menu-bar
		menubar = wx.MenuBar()
		# file-menu
		file_menu = wx.Menu()
		file_menu.Append(10,"&New\tCtrl+N","Create a new Document")
		file_menu.AppendSeparator()
		file_menu.Append(11,"&Open\tCtrl+O","Open a file")
		examples = wx.Menu()
		examples.Append(0,"None",kind = wx.ITEM_RADIO)
		examples.Append(400,"blink.c",'Blinks a LED on PB0',kind = wx.ITEM_RADIO)
		examples.Append(401,"adc.c",'Reads ADC channel 0 and diplays the result on the LCD',kind = wx.ITEM_RADIO)
		examples.Append(405,'adc-loop.c','Reads ADC channel 0 and diplays the result on the LCD in loop',kind = wx.ITEM_RADIO)
		examples.Append(406,"adc-v2.c",'ADC -version 2',kind = wx.ITEM_RADIO)
		examples.Append(407,"adc-v3.c",'ADC -version 3',kind = wx.ITEM_RADIO)
		examples.Append(402,"copy.c",'Copies a PORTA and display it on PORTB',kind = wx.ITEM_RADIO)
		examples.Append(403,"copy2.c",'Copy 2',kind = wx.ITEM_RADIO)
		examples.Append(404,'copy3.c','Copy 3',kind = wx.ITEM_RADIO)
		examples.Append(409,"echo.c","echo.c" , kind = wx.ITEM_RADIO)
		examples.Append(410,"echo-v2.c","echo-v2.c", kind = wx.ITEM_RADIO)
		examples.Append(413,"pwm-tc0.c","PWM-tc0 version 1",kind = wx.ITEM_RADIO)
		examples.Append(411,"h-bridge.c","H-Bridge Controlling motor",kind = wx.ITEM_RADIO)
		examples.Append(414,"pwm-tc0-v2.c","PWM tc0 version 2",kind = wx.ITEM_RADIO)
		examples.Append(415,"cro.c","To make microHOPE as small CRO",kind = wx.ITEM_RADIO)
		examples.Append(416,"cro2.c","To make microHOPE as small CRO (version 2)" , kind = wx.ITEM_RADIO)
		examples.Append(408,'hello.c','Print message in LCD',kind = wx.ITEM_RADIO)
		examples.Append(412,"hello-blink.c","Blinking messages in LCD",kind = wx.ITEM_RADIO)
		file_menu.AppendMenu(444,"Examples",examples)
		file_menu.Append(12,"&Save\tCtrl+S","Save the current file")
		file_menu.Append(13,"&SaveAs\tShift+Ctrl+S","Save the current file with a different name")
		file_menu.AppendSeparator()
		file_menu.Append(999,"&Init()\tCtrl+I","Initialize microhope working directory")
		file_menu.Append(14,"&Exit\tCtrl+Q","Quit the programme")
		self.Bind(wx.EVT_MENU,self.open_echoc,id = 409)
		self.Bind(wx.EVT_MENU,self.open_hbridgec , id = 411)
		self.Bind(wx.EVT_MENU,self.open_pwmtc0v1 , id = 413)
		self.Bind(wx.EVT_MENU,self.open_pwmtc0v2 , id = 414)
		self.Bind(wx.EVT_MENU,self.open_cro,id = 415)
		self.Bind(wx.EVT_MENU,self.open_cro2 , id = 416)
		self.Bind(wx.EVT_MENU,self.open_echo2c,id = 410)
		self.Bind(wx.EVT_MENU,self.open_adcv2,id = 406)
		self.Bind(wx.EVT_MENU,self.open_copyc,id = 402)
		self.Bind(wx.EVT_MENU,self.open_copy2c,id = 403)
		self.Bind(wx.EVT_MENU,self.open_copy3c,id = 404)
		self.Bind(wx.EVT_MENU,self.open_adcv3,id = 407)
		self.Bind(wx.EVT_MENU,self.init,id = 999)
		self.Bind(wx.EVT_MENU,self.open_blinkc,id = 400)
		self.Bind(wx.EVT_MENU,self.open_helloc,id = 408)
		self.Bind(wx.EVT_MENU,self.open_helloblink , id = 412)
		self.Bind(wx.EVT_MENU,self.open_adc,id = 401)
		self.Bind(wx.EVT_MENU,self.open_adcloop,id = 405)
		self.Bind(wx.EVT_MENU,self.Newfile,id=10)
		self.Bind(wx.EVT_MENU,self.open_file,id=11)
		self.Bind(wx.EVT_MENU,self.save_file,id=12)
		self.Bind(wx.EVT_MENU,self.save_as,id=13)
		self.Bind(wx.EVT_MENU,self.Quit,id=14)
		# edit-menu
		editmenu = wx.Menu()
		editmenu.Append(15,"&Undo\tCtrl+Z","")
		editmenu.Append(16,"&Redo\tCtrl+Y","")
		editmenu.AppendSeparator()
		editmenu.Append(17,"&Cut\tCtrl+X","Cut the selection")
		editmenu.Append(18,"&Copy\tCtrl+C","Copy the selection")
		editmenu.Append(19,"&Paste\tCtrl+P","Paste the clipboard")
		editmenu.Append(20,"&Delete\tDelete","Deleted the selected text")
		editmenu.AppendSeparator()
		editmenu.Append(21,"&Select All\tCtrl+A","select the entire document")
		self.Bind(wx.EVT_MENU,self.Undo,id=15)
		self.Bind(wx.EVT_MENU,self.Redo,id=16)
		self.Bind(wx.EVT_MENU,self.Cut,id=17)
		self.Bind(wx.EVT_MENU,self.Copy,id=18)
		self.Bind(wx.EVT_MENU,self.Paste,id=19)
		self.Bind(wx.EVT_MENU,self.Delete,id=20)
		self.Bind(wx.EVT_MENU,self.Select_All,id=21)
		#view-menu #
		viewmenu = wx.Menu()
		self.statusbaritem = wx.MenuItem(viewmenu, 22,"&Statusbar","Show or hide the statusbar in the current window")
		self.statusbaritem.SetCheckable(True)
		viewmenu.AppendItem(self.statusbaritem)
		self.statusbaritem.Check()
		wx.EVT_MENU(self, 22, self.toggle_statusbar)
		chng_bg_font_color = wx.Menu()
		chng_bg_font_color.Append(23,"Black on white(default)",kind = wx.ITEM_RADIO)
		chng_bg_font_color.Append(24,"White on Black",kind = wx.ITEM_RADIO)
		viewmenu.AppendMenu(25,"Theme",chng_bg_font_color)
		font_size = wx.Menu()
		font_size.Append(26,"Default",kind = wx.ITEM_RADIO)
		font_size.Append(27,"10",kind = wx.ITEM_RADIO)
		font_size.Append(28,"11",kind = wx.ITEM_RADIO)
		font_size.Append(29,"12",kind = wx.ITEM_RADIO) 
		font_size.Append(30,"13",kind = wx.ITEM_RADIO)
		font_size.Append(31,"14",kind = wx.ITEM_RADIO)
		font_size.Append(32,"15",kind = wx.ITEM_RADIO)
		font_size.Append(33,"16",kind = wx.ITEM_RADIO)
		font_size.Append(34,"17",kind = wx.ITEM_RADIO)
		font_size.Append(35,"18",kind = wx.ITEM_RADIO)
		font_size.Append(36,"19",kind = wx.ITEM_RADIO)
		font_size.Append(37,"20",kind = wx.ITEM_RADIO)
		font_size.Append(38,"Large",kind = wx.ITEM_RADIO)
		viewmenu.AppendMenu(39,"Font Size",font_size)
		self.Bind(wx.EVT_MENU,self.font_Large, id =38)
		self.Bind(wx.EVT_MENU,self.fontsize10, id = 27)
		self.Bind(wx.EVT_MENU,self.fontsize11, id = 28)
		self.Bind(wx.EVT_MENU,self.fontsize12, id = 29)
		self.Bind(wx.EVT_MENU,self.fontsize13, id = 30)
		self.Bind(wx.EVT_MENU,self.fontsize14, id = 31)
		self.Bind(wx.EVT_MENU,self.fontsize15, id = 32)
		self.Bind(wx.EVT_MENU,self.font_size_default, id = 39)
		self.Bind(wx.EVT_MENU,self.fontsize16, id = 33)
		self.Bind(wx.EVT_MENU,self.fontsize17, id = 34)
		self.Bind(wx.EVT_MENU,self.fontsize18, id = 35)
		self.Bind(wx.EVT_MENU,self.fontsize19, id = 36)
		self.Bind(wx.EVT_MENU,self.fontsize20, id = 37)
		self.Bind(wx.EVT_MENU,self.black_white,id = 23)
		self.Bind(wx.EVT_MENU,self.white_black,id = 24)
		#-_----------------------------------_#
		#device
		devise = wx.Menu()
		devise.Append(90,'Detect Board\tCtrl+B','Detect the hardware')
		devise.AppendSeparator()
		devise.Append(52,'Set Bootloader','For setting the mcu by uploading the bootloader')
		devise.Append(50,'Soft RST','Software RESET')
		self.Bind(wx.EVT_MENU,self.detect, id = 90)
		self.Bind(wx.EVT_MENU,self.softRST,id = 50)
		self.Bind(wx.EVT_MENU,self.set_mhbootloader , id = 52)
		#--------------------------------------#
		#Build menu
		build = wx.Menu()
		build.Append(43,'Compile\tCtrl+K','To Compile the program')
		build.Append(51,'Assemble\tCtrl+J','To Assemble the program')
		build.AppendSeparator()
		build.Append(44,'Uplod\tCtrl+L','To upload the program to mcu')
		build.Append(53,'Upload via USBASP','Upload program via USBASP')
		self.Bind(wx.EVT_MENU,self.mhcompile,id = 43)
		self.Bind(wx.EVT_MENU,self.mhupload,id = 44)
		self.Bind(wx.EVT_MENU,self.mhAssemble , id = 51)
		self.Bind(wx.EVT_MENU,self.usbasp_uplod , id = 53)
		#---------------------------------#
		about = wx.Menu()
		about.Append(45,"&Help\tShift+Ctrl+H","")
		about.Append(46,"&About\tShift+Ctrl+Z","")
		about.Append(47,"&Author\tShift+Ctrl+A","")
		self.Bind(wx.EVT_MENU,self.mhhelp,id =45)
		self.Bind(wx.EVT_MENU,self.About,id = 46)
		self.Bind(wx.EVT_MENU,self.Author,id= 47)
		#-----------------------------------------#
	#toolbar
		toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.NO_BORDER)
		toolbar.SetBackgroundColour("#f2f1f0")
		toolbar.AddSimpleTool(140, wx.Image('/usr/share/pixmaps/document-new.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Create a new document', '')
		toolbar.AddSimpleTool(141, wx.Image('/usr/share/pixmaps/document-open.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Open a file', '')
		toolbar.AddSimpleTool(142,wx.Image('/usr/share/pixmaps/document-save.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Save the current file', '')
		toolbar.AddSeparator()
		toolbar.AddSimpleTool(150, wx.Image('/usr/share/pixmaps/edit-undo.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Undo the last action', '')
		toolbar.AddSimpleTool(151, wx.Image('/usr/share/pixmaps/edit-redo.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Redo the last undone action', '')
		toolbar.AddSeparator()
		toolbar.AddSimpleTool(143, wx.Image('/usr/share/pixmaps/edit-cut.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Cut the selection', '')
		toolbar.AddSimpleTool(144, wx.Image('/usr/share/pixmaps/edit-copy.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Copy the selection', '')
		toolbar.AddSimpleTool(145, wx.Image('/usr/share/pixmaps/edit-paste.png',  wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Paste the clipboard', '')
		toolbar.AddSeparator()
		toolbar.AddSimpleTool(146,wx.Image('/usr/share/pixmaps/gnome-run.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'To compile the current programe','')
		toolbar.AddSimpleTool(147,wx.Image('/usr/share/pixmaps/gtk-sort-descending.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'To upload the pgm to mh','')
		toolbar.AddSimpleTool(200,wx.Image('/usr/share/pixmaps/hardware.png' ,wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'To detect microhope hardware','')
		toolbar.AddSeparator()
		toolbar.AddSimpleTool(148,wx.Image('/usr/share/pixmaps/help-about.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap(),'Help for microHOPE','')
		self.Bind(wx.EVT_TOOL, self.Newfile, id=140)
		self.Bind(wx.EVT_TOOL, self.open_file, id=141)
		self.Bind(wx.EVT_TOOL, self.save_file, id=142)
		self.Bind(wx.EVT_TOOL, self.Cut, id=143)
		self.Bind(wx.EVT_TOOL, self.Copy, id=144)
		self.Bind(wx.EVT_TOOL, self.Paste, id=145)
		self.Bind(wx.EVT_TOOL, self.mhcompile, id=146)
		self.Bind(wx.EVT_TOOL, self.mhupload , id=147)
		self.Bind(wx.EVT_TOOL,self.mhhelp, id =148)
		self.Bind(wx.EVT_TOOL,self.Undo, id = 150)
		self.Bind(wx.EVT_TOOL,self.Redo, id =151)
		self.Bind(wx.EVT_TOOL,self.detect , id = 200)
		#-----------------------------------#
		menubar.Append(file_menu,"File")
		menubar.Append(editmenu,"Edit")
		menubar.Append(viewmenu,"View")
		menubar.Append(devise,"Device")
		menubar.Append(build,"Build")
		menubar.Append(about,"About")
		self.SetToolBar(toolbar)
		self.SetMenuBar(menubar)
		self.Show()
	def istext_changed(self,event):
		self.modify = True
		if self.fname == '':
			self.SetTitle("uHOPE :: File -->New File.c *"+"\t\tDevice -->"+self.mhdevice)
		else :
			self.SetTitle("uHOPE :: File -->"+self.dname+"/"+self.fname+"*"+"\t\tDevice -->"+self.mhdevice)
		event.Skip()
	def key_down(self,event):
		kycode = event.GetKeyCode()
		self.undo.append(self.text.GetValue())
		if len(self.undo) >= 30: self.undo = self.undo[1:]
		c,l = self.text.PositionToXY(self.text.GetInsertionPoint())
		stat = "line =%s\t\tcolumn=%s" % (l+1,c+1)
		self.StatusBar.SetStatusText(stat, number=0)
		event.Skip()
	def save_as(self,event):
		self.dirname = ''
		dlg = wx.FileDialog(self,"Choose a file",self.dirname,"","*.*",wx.SAVE)
		
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			file_ = open(os.path.join(self.dirname,self.filename),'w')
			file_.write(self.text.GetValue().encode('utf8'))
			file_.close()
		dlg.Destroy()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.dname = self.dirname
		self.fname = self.filename
		self.isnew = False
		self.modify = False
	def save_file(self,event):
		if self.isnew == False :
			#self.show(self.dname)
			#self.show(self.filename)
			file_ = open(os.path.join(self.dname,self.fname),'w')
			file_.write(self.text.GetValue().encode("utf8"))
			self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
			self.modify = False
		elif self.isnew == True:
			 self.save_as(event)
	def open_file(self,event):
		self.filename = ''
		self.dirname = 'microhope/'
		dlg = wx.FileDialog(self,"Choose a file",self.dirname,"","*.*",wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			
			self.dirname = dlg.GetDirectory()
			file_ = open(os.path.join(self.dirname,self.filename),'r')
			self.text.SetValue(file_.read())
			file_.close()
			self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		dlg.Destroy()
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def Quit(self,event):
		if self.modify == True:
			dlg = wx.MessageDialog(self,"Save before exiting ?",'',wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL |  wx.ICON_QUESTION)
			chk = dlg.ShowModal()
			if chk == wx.ID_YES:
				self.save_file(event)
				self.Destroy()
			elif chk == wx.ID_CANCEL:
				dlg.Destroy()
			else:
				self.Destroy()
		elif self.modify == False:
			dlg = wx.MessageDialog(self,"Are you sure ?",'',wx.YES_NO | wx.YES_DEFAULT |  wx.ICON_QUESTION)
			chk = dlg.ShowModal()
			if chk == wx.ID_YES:
				self.Destroy()
			else:
				dlg.Destroy()
		else:
			self.Destroy()
	def Undo(self,event):
		place = self.text.GetInsertionPoint()
		self.redo.append(self.text.GetValue())
		self.text.SetValue(self.undo[len(self.undo)-1])
		self.text.SetInsertionPoint(place)
		self.undo = self.undo[:-1]
		if len(self.redo) >= 30 : self.redo = self.redo[1:]
	def Redo(self,event):
		place = self.text.GetInsertionPoint()
		self.text.SetValue(self.redo[len(self.redo)-1])
		self.text.SetInsertionPoint(place)
		self.redo = self.redo[:-1]
	def Newfile(self,event):
		if self.modify == True:
			dlg = wx.MessageDialog(self,"Save before opening New File ?",'',wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL |  wx.ICON_QUESTION)
			chk = dlg.ShowModal()
			if chk == wx.ID_YES:
				self.save_file(event)
				dlg.Destroy()
				self.filename,self.dirname = 'New file',''
				self.text.Clear()
				self.SetTitle("uHOPE :: File --> "+self.filename+".c\t\tDevice -->"+self.mhdevice)
				self.dname = self.dirname
				self.fname = self.filename
			
			elif chk == wx.ID_CANCEL:
				dlg.Destroy()
			else:
				self.filename,self.dirname = 'New file',''
				self.text.Clear()
				self.SetTitle("uHOPE :: File --> "+self.filename+".c\t\tDevice -->"+self.mhdevice)
				self.fname = self.filename
				self.dname = self.dirname
		else :
			self.filename,self.dirname = 'New file',''
			self.text.Clear()
			self.SetTitle("uHOPE :: File --> "+self.filename+".c\t\tDevice -->"+self.mhdevice)
			self.fname = self.filename
			self.dname = self.dirname
		self.isnew = True
	def toggle_statusbar(self,event):
		if self.statusbar.IsShown():
			self.statusbar.Hide()
			self.statusbaritem.Check(False)
		else:
			self.statusbar.Show()
			self.statusbaritem.Check()
	def Cut(self,event):
		self.text.Cut()
	def Copy(self,event):
		self.text.Copy()
	def Paste(self,event):
		self.text.Paste()
	def Delete(self,event):
		frm , to = self.text.GetSelection()
		self.text.Remove(frm,to)
	def Select_All(self,event):
		self.text.SelectAll()
	def fontsize10(self,event):
		self.text.SetFont(wx.Font(10,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def fontsize11(self,event):
		self.text.SetFont(wx.Font(11,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def fontsize12(self,event):
		self.text.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def fontsize13(self,event):
		self.text.SetFont(wx.Font(13,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def fontsize14(self,event):
		self.text.SetFont(wx.Font(14,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def fontsize15(self,event):
		self.text.SetFont(wx,Font(15,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def fontsize16(self,event):
		self.text.SetFont(wx.Font(16,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def fontsize17(self,event):
		self.text.SetFont(wx.Font(17,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def fontsize18(self,event):
		self.text.SetFont(wx.Font(18,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def fontsize19(self,event):
		self.text.SetFont(wx.Font(19,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def fontsize20(self,event):
		self.text.SetFont(wx.Font(20,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def font_Large(self,event):
		self.text.SetFont(wx.Font(25,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def font_size_default(self,event):
		self.text.SetFont(wx.Font(13,wx.MODERN,wx.NORMAL,wx.NORMAL,False,u'Liberation Serif'))
	def black_white(self,event):
		self.text.SetBackgroundColour("white")
		self.text.SetForegroundColour(wx.BLACK)
	def white_black(self,event):
		self.text.SetBackgroundColour("#220a3e")
		self.text.SetForegroundColour(wx.WHITE)
	def show(self,msg):
		dlg = wx.MessageDialog(self,msg,'uHOPE :: Status',wx.OK|wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()	
	def show_err(self,msg):
		dlg = wx.MessageDialog(self,msg,'uHOPE :: Status',wx.CANCEL|wx.ICON_ERROR)
		dlg.ShowModal()
		dlg.Destroy()
	def warning(self,msg):
		dlg = wx.MessageDialog(self,msg,'uHOPE :: Status',wx.CANCEL|wx.ICON_WARNING)
		dlg.ShowModal()
		dlg.Destroy()
	def mhcompile(self,event):
		if self.fname == '':
			self.warning('Filename not selected .')
			return 
		self.save_file(event)
		self.fd = self.dname+"/"+self.fname
		self.fname_witout_extn = self.dname+"/"+os.path.splitext(self.fname)[0]
		command = 'avr-gcc -Wall -O2 -mmcu=atmega32 -o %s  %s' %(self.fname_witout_extn,self.fd)
		
		self.result = commands.getstatusoutput(command)
		
		if self.result[0] != 0:
			self.show_err('Compilation Error :\n'+self.result[1])
			self.SetTitle("uHOPE :: File --> "+self.dname+"/"+self.fname+"\t\tDevice -->"+self.mhdevice)
			return
		
		
		command = 'avr-objcopy -j .text -j .data -O ihex %s %s.hex' %(self.fname_witout_extn,self.fname_witout_extn) 
		
		self.result = commands.getstatusoutput(command)
		self.show('Compilation Done')
		self.SetTitle("uHOPE :: File --> "+self.dname+"/"+self.fname+"\t\tDevice -->"+self.mhdevice)
	def mhupload(self,event):
		if self.mhdevice == '':
			self.warning('Device not selected\nPlease select a device')
			self.devce = []
			self.command = "ls /dev/ttyUSB*"
			self.result = commands.getstatusoutput(self.command)
			if self.result[0] == 0:
				self.devce += self.result[1].split('\n')
			if self.devce == []:
				return
			else :
				self.mhdevice = self.command.split(" ")[1]

			self.command = 		"ls /dev/ttyACM*"
			self.result = commands.getstatusoutput(self.command)
			if self.result[0] == 0:
				self.devce += self.result[1].split('\n')
			if self.devce == []:
				return
			else :
				self.mhdevice = self.command.split(" ")[1]
				
		self.fname_witout_extn = os.path.splitext(self.fname)[0]
		self.fname_witout_extn = self.dname +"/"+self.fname_witout_extn
		
		command= 'avrdude -b 19200 -P %s -pm32 -c stk500v1 -U flash:w:%s.hex'%(self.mhdevice, self.fname_witout_extn)
		result = commands.getstatusoutput(command)
		if result[0] != 0:
			self.warning('Upload Error:\n'+result[1]+'\nTry pressing microHOPE Reset button just before Uploading')
			self.SetTitle("uHOPE :: File --> "+self.dname+"/"+self.fname+"\t\tDevice -->"+self.mhdevice)
			return
		else:
			self.show('Upload Completed\n'+result[1])
			self.SetTitle("uHOPE :: File --> "+self.dname+"/"+self.fname+"\t\tDevice -->"+self.mhdevice)
	def mhhelp(self,event):
		dlg = wx.MessageDialog(self,"Steps:\n1.Write a program on editor / Open a programe C or Assembler files\n2.Compile it by cliking on compile\n3.You can view the objdump file(*.lst) by opening it in the editoring\n4.Connect microHOPE and wait a minute\n5.Click on Device->Detect Board to detect your board\n6.If microHOPE is not found , repeat or reconnect microHOPE\n7.Upload the hex file to microHOPE (Build->Upload)\n8.If upload fails check microHOPE and upload again\n\nNote: Make sure that microhope folder from /etc/skel/ is copied to your home folder .\nIt contains example programes , mh-libs etc.","microHOPE-Help",wx.OK|wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
	def Author(self,event):
		dlg = wx.MessageDialog(self,"Author :Arun Jayan\narun.jayan.j@ieee.org\nGNU USERS NETWORK","Author of IDE",wx.OK|wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
	def mh_status(self,f,d):
		if f == '':
			f = 'Not selected'
		if d == '':
			d = 'Not selected'
		msg = 'uHOPE :: File -> %s & Device -> %s'%(f,d)
		self.show(msg)
	def About(self,event):
		abt = wx.MessageDialog(self,"microHOPE is a developement Board using Atmega32\nCreated by :Dr.Ajith Kumar B P\n\t\t\t\t IUAC,New Delhi","About uHOPE",wx.OK|wx.ICON_INFORMATION)
		abt.ShowModal()
		abt.Destroy()
	def pulseRTS(self,dev):
		ser = serial.Serial(dev , 38400, stopbits = 1,timeout = 1.0)
		ser.setRTS(0)
		ser.setRTS(1)
		ser.setRTS(0)
		ser.close()
	def softRST(self,event):
			if self.mhdevice == "/dev/ttyACM0":
				self.pulseRTS('/dev/ttyACM0')
			elif self.mhdevice == "/dev/ttyUSB0":
				self.pulseRTS('/dev/ttyUSB0')	
	def mhAssemble(self,event):
		if self.fname == '':
			self.show('Filename not selected .')
			return 
		self.save_file(event)
		self.fd = self.dname+"/"+self.fname
		self.fname_witout_extn = self.dname+"/"+os.path.splitext(self.fname)[0]
		command = 'avr-gcc -Wall -O2 -mmcu=atmega32 -o %s %s' %(self.fname_witout_extn,self.fd)
		
		self.result = commands.getstatusoutput(command)
		
		if self.result[0] != 0:
			self.show('Assembler Error :\n'+self.result[1])
			self.SetTitle("uHOPE :: File --> "+self.dname+"/"+self.fname+"\t\tDevice -->"+self.mhdevice)
			return
		
		
		command = 'avr-objcopy -j .text -j .data -O ihex %s %s.hex' %(self.fname_witout_extn,self.fname_witout_extn) 
		
		self.result = commands.getstatusoutput(command)
		command = 'avr-objdump -S %s > %s.lst'%(self.fname_witout_extn,self.fname_witout_extn)
		self.result = commands.getstatusoutput(command)
		self.show('Assembing Done')
		self.SetTitle("uHOPE :: File --> "+self.dname+"/"+self.fname+"\t\tDevice -->"+self.mhdevice)
	def set_mhbootloader(self,event):
		self.SetTitle("Setting up MicroHOPE bootloader via USBASP.....")
		self.show("Setting up MicroHOPE bootloader via USBASP.... \nIt will take few seconds")
		self.command = 'avrdude -B10 -c usbasp -patmega32 -U flash:w:/etc/skel/microhope/ISP/ATmegaBOOT_168_atmega32.hex'
		self.result = commands.getstatusoutput(self.command)
		if self.result[0] != 0 :
			self.show('Error: Check Connections....')
			
			return 
		self.command = 'avrdude -B10 -c usbasp -patmega32 -U lfuse:w:0xff:m -U hfuse:w:0xda:m'
		self.result = commands.getstatusoutput(self.command)
		if self.result[0] != 0:
			self.show('Error: Setting up fuses')
			
			return 
		self.show('Upload Completed')
		self.SetTitle("uHOPE :: File --> "+self.dname+"/"+self.fname+"\t\tDevice -->"+self.mhdevice)
	def usbasp_uplod(self,event):
		self.show("Uploading through USBASP ....")
		self.fname_witout_extn = self.dname+"/"+os.path.splitext(self.fname)[0]
		self.command ="avrdude -c usbasp -patmega32 -U flash:w:%s.hex"%(self.fname_witout_extn)
		self.result = commands.getstatusoutput(self.command)
		if self.result[0] != 0:
			self.show("Check connections of USBASP")
			
			return
		else:
			self.show("Uploading via USBASP completed.....")
		self.SetTitle("uHOPE :: File --> "+self.dname+"/"+self.fname+"\t\tDevice -->"+self.mhdevice)

	def detect(self,event):
		command = "ls /dev/ttyUSB*"
		result = commands.getstatusoutput(command)
		devc = []
		if result[0] == 0:
			devc = result[1].split('\n')
		command = "ls /dev/ttyACM*"	
		result = commands.getstatusoutput(command)
		
		if result[0] == 0:
			devc = result[1].split('\n')
		if devc == []:
			self.show('microHOPE hardware not found?')
			if self.fname =='':
				self.SetTitle("uHOPE :: File --> New File"+"\t\tDevice --> Not Connected")
			else :
				self.SetTitle("uHOPE :: File --> "+self.dname+"/"+self.fname+"\t\tDevice --> Not Connected")
			return 
		else:
			self.mhdevice = devc[0]
			if self.fname =='':
				self.SetTitle("uHOPE :: File --> New File"+"\t\tDevice -->"+self.mhdevice)
			else :
				self.SetTitle("uHOPE :: File --> "+self.dname+"/"+self.fname+"\t\tDevice -->"+self.mhdevice)
			self.show("Device is found at "+ devc[0])
	def open_blinkc(self,event):
		self.filename = 'blink.c'
		self.dirname = 'microhope'
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_helloc(self,event):
		self.filename = 'hello.c'
		self.dirname = 'microhope'
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_adc(self,event):
		self.filename = 'adc.c'
		self.dirname = 'microhope'
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_echoc(self,event):
		self.filename = 'echo.c'
		self.dirname = 'microhope'
		file_ = open(os.path.join(self.dirname , self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_echo2c(self,event):
		self.filename = 'echo-v2.c'
		self.dirname  = 'microhope'
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_adcloop(self,event):
		self.filename = 'adc-loop.c'
		self.dirname = 'microhope'
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_adcv2(self,event):
		self.filename = 'adc-v2.c'
		self.dirname = 'microhope'
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_adcv3(self,event):
		self.filename = "adc-v3.c"
		self.dirname = "microhope"
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_copyc(self,event):
		self.filename = "copy.c"
		self.dirname = "microhope"
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_copy2c(self,event):
		self.filename = "copy2.c"
		self.dirname = "microhope"
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_copy3c(self,event):
		self.filename = "copy3.c"
		self.dirname = "microhope"
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_hbridgec(self,event):
		self.filename = "h-bridge.c"
		self.dirname = 'microhope'
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_helloblink(self,event):
		self.filename = "hello-blink.c"
		self.dirname = 'microhope'
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False	
	def open_pwmtc0v1(self,event):
		self.filename = "pwm-tc0.c"
		self.dirname = 'microhope'
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False	
	def open_pwmtc0v2(self,event):
		self.filename = "pwm-tc0-v2.c"
		self.dirname = 'microhope'
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_cro(self,event):
		self.filename = "cro.c"
		self.dirname = 'microhope'
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
	def open_cro2(self,event):
		self.filename = "cro2.c"
		self.dirname = 'microhope'
		file_ = open(os.path.join(self.dirname,self.filename),'r')
		self.text.SetValue(file_.read())
		file_.close()
		self.SetTitle("uHOPE :: File --> "+self.dirname+"/"+self.filename+"\t\tDevice -->"+self.mhdevice)
		self.fname = self.filename
		self.dname = self.dirname
		self.isnew = False
		self.modify = False
## to create micrphope working directory 
	def init(self,event):
		dlg = wx.MessageDialog(None,"Create microHope environment\nDo you want to create your own microHope environment?\n\nIf you reply \"Yes\", a subdirectory named microHope will be created in your home directory, and a set of files will be copied into it.\n\nIf any previous installation existed, its contents will be overwriten.",'uHOPE init()',wx.YES_NO | wx.YES_DEFAULT |  wx.ICON_QUESTION)
		chk = dlg.ShowModal()
		if chk == wx.ID_YES:
			dlg.Destroy()
			os.system("mkdir -p ~/microhope && cp -Rd /etc/skel/microhope/* ~/microhope/")
			self.show("creating microhope environment")
		elif chk == wx.ID_CANCEL:
			dlg.Destroy()
		else:
			dlg.Destroy()
			
def main():
	app = wx.App()
	microhope(None,-1,'uHOPE','size')
	app.MainLoop()
	
if __name__ == '__main__':
	main()
