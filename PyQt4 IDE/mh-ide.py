from microhope_lib import mh_latest_ui 
from PyQt4 import QtGui,QtCore
import sys

app_obj = QtGui.QApplication(sys.argv)
mhobj = mh_latest_ui.Mh_ui()
mhobj.show()
sys.exit(app_obj.exec_())
