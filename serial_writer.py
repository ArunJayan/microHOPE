# serial writer 
try :
	import wx
except ImportError:
	raise ImportError ,"The wxPython module is required to run this program"
import serial 
import commands
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
					 
					 self.device = self.detect()
					 self.out = serial.Serial(self.device, 38400, stopbits=1, timeout = 1.0)
					 
					 self.mhpanel = wx.Panel(self)
					 self.mhpanel.SetBackgroundColour("black")
					 self.charalabel = wx.StaticText(self.mhpanel,-1,label=u'Character : ',pos = (1,30),style = wx.TE_MULTILINE)
					 self.charalabel.SetBackgroundColour(wx.BLUE)
					 self.charalabel.SetForegroundColour(wx.RED)
					 				 
					 self.entry = wx.TextCtrl(self.mhpanel,-1,value=u"",pos= (90,25),size = wx.Size(610,30),style =wx.EXPAND)
					 
					 button = wx.Button(self.mhpanel,-1,label="Send!!",pos =(615,120))
					 self.Bind(wx.EVT_BUTTON, self.OnButtonClick, button)
					 
					 self.baudlabel = wx.StaticText(self.mhpanel,-1,label=u' Baudrate :  38400*',pos = (1,80),style = wx.TE_MULTILINE)
					 self.baudlabel.SetBackgroundColour(wx.BLUE)
					 self.baudlabel.SetForegroundColour(wx.RED)
					 
					 self.label_notif = wx.StaticText(self.mhpanel,-1,label=u'',pos = (5,120),style = wx.EXPAND)
					 self.label_notif.SetBackgroundColour("yellow")
					 self.label_notif.SetForegroundColour(wx.RED)
					 
					 

					 self.entry.SetFocus()
					 self.entry.SetSelection(-1,-1)
	def OnButtonClick(self,event):
			self.num = (self.entry.GetValue())
			if self.num == "":
				dlg = wx.MessageDialog(self,"Type a character",'uHOPE :: Status',wx.CANCEL|wx.ICON_WARNING)
				dlg.ShowModal()
				dlg.Destroy()
			else :
				self.send_usart(self.num)
			self.entry.SetFocus()
			self.entry.SetSelection(-1,-1)
	def detect(self):
		command = 'ls /dev/ttyACM*'
		result = commands.getstatusoutput(command)
		if result[0] == 0:
			return result[1]
		else :
			self.Destroy()
	def send_usart(self,data):
		self.out.write(data)
		self.recv = self.out.read()
		#self.label_notif.SetLabel('Data Send through USART ::'+self.recv)
		
				
if __name__ == "__main__":
	ser = MhSerialCharaWrite(False)
	ser.MainLoop()
