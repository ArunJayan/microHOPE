############################################################################
## microHOPE IDE ---->Qt Version										  ##
## Author  : Arun Jayan													  ##
## Email ID: arunjayan32@gmail.com										  ##
## Based on Ajith Kumar's work											  ##
## License : GNU GPL version 3							          		  ##
############################################################################

########## Importing Lib's ##########
import sys
from PyQt4 import QtGui as QG	#QtGui as QG
from PyQt4 import QtCore as QC	#QtCore as Qc
####################################

class MH_MainWindow(QG.QMainWindow):
	
	def __init__(self):
		QG.QMainWindow.__init__(self,None)
		
		####------Upper ToolBar -----------####
		new = QG.QAction(QG.QIcon("pixmaps/document-new.png"),"New",self)
		new.Shortcut("Ctrl+N")	
		new.setStatusTip("Creates a 
