# serial writer 
try :
	import wx
except ImportError:
	raise ImportError ,"The wxPython module is required to run this program"
import serial 

class MhSerialCharaWrite(wx.App):
	def OnInit(self):
		self.mframe = MhFrame(None,title = "Serial Chara Writer ")
		self.SetTopWindow(self.mframe)
		self.mframe.Show()
		
		return True

class MhFrame(wx.Frame):
	def __init__(self,parent,id = wx.ID_ANY, title = "" , pos = wx.DefaultPosition , 
				 size = wx.Size(700,150) , style = wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
		wx.CAPTION|wx.CLIP_CHILDREN):
					 super(MhFrame,self).__init__(parent,id,title,pos,size,style)
					 
					 self.mhpanel = wx.Panel(self)
					 self.mhpanel.SetBackgroundColour("black")
					 self.label = wx.StaticText(self.mhpanel,-1,label=u'Character : ',pos = (1,30),style = wx.TE_MULTILINE)
					 				 
					 self.entry = wx.TextCtrl(self.mhpanel,-1,value="",pos= (90,25),size = wx.Size(610,30),style =wx.EXPAND)
					 self.Bind(wx.EVT_TEXT_ENTER, self.OnPressEnter, self.entry)
					 
					 button = wx.Button(self.mhpanel,-1,label="Send!!",pos =(615,120))
					 self.Bind(wx.EVT_BUTTON, self.OnButtonClick, button)
					 
					 self.label = wx.StaticText(self.mhpanel,-1,label=u'Baudrate : ',pos = (1,80),style = wx.TE_MULTILINE)
					 
					 self.baud = wx.TextCtrl(self.mhpanel , value = "", pos = (90,75),size = wx.Size(610,30) ,style = wx.EXPAND)
					 self.Bind(wx.EVT_TEXT_ENTER,self.OnPressEnter,self.baud)
					 
					 self.label = wx.StaticText(self.mhpanel,-1,label=u'',pos = (5,120),style = wx.EXPAND)
					 self.label.SetBackgroundColour(wx.BLUE)
					 self.label.SetForegroundColour(wx.WHITE)
					 
					 

					 self.entry.SetFocus()
					 self.entry.SetSelection(-1,-1)
	def OnButtonClick(self,event):
			self.label.SetLabel( self.entry.GetValue() + " (You send)" )
			self.entry.SetFocus()
			self.entry.SetSelection(-1,-1)

	def OnPressEnter(self,event):
			self.label.SetLabel( self.entry.GetValue() + " (You Send)" )
			self.entry.SetFocus()
			self.entry.SetSelection(-1,-1)
if __name__ == "__main__":
	ser = MhSerialCharaWrite(False)
	ser.MainLoop()
