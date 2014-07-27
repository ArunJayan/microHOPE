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
				 size = wx.DefaultSize , style = wx.DEFAULT_FRAME_STYLE ):
					 super(MhFrame,self).__init__(parent,id,title,pos,size,style)
					 
					 self.mhpanel = wx.Panel(self)
					 self.mhpanel.SetBackgroundColour("black")
					 					 
					 self.entry = wx.TextCtrl(self.mhpanel,-1,value="",pos= (5,9),size = wx.Size(295,30),style =wx.EXPAND)
					 self.Bind(wx.EVT_TEXT_ENTER, self.OnPressEnter, self.entry)
					 
					 button = wx.Button(self.mhpanel,-1,label="Send!",pos =(300,9))
					 self.Bind(wx.EVT_BUTTON, self.OnButtonClick, button)
					 
					 self.label = wx.StaticText(self.mhpanel,-1,label=u'',pos = (5,50),style = wx.EXPAND)
					 self.label.SetBackgroundColour(wx.BLUE)
					 self.label.SetForegroundColour(wx.WHITE)
					 
					 self.entry.SetFocus()
					 self.entry.SetSelection(-1,-1)
	def OnButtonClick(self,event):
			self.label.SetLabel( self.entry.GetValue() + " (You sended)" )
			self.entry.SetFocus()
			self.entry.SetSelection(-1,-1)

	def OnPressEnter(self,event):
			self.label.SetLabel( self.entry.GetValue() + " (You pressed ENTER)" )
			self.entry.SetFocus()
			self.entry.SetSelection(-1,-1)
if __name__ == "__main__":
	ser = MhSerialCharaWrite(False)
	ser.MainLoop()
