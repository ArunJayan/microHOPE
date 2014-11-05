#test version 

#This is the Qt Version of MicroHope IDE
#Here we are using PyQt4 library
#Author : Arun Jayan
#Email ID : arunjayan32@gmail.com

__author__ = 'Arun Jayan'
__email__ = "arunjayan32@gmail.com"


from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class MyHighlighter( QSyntaxHighlighter ):

    def __init__( self, parent, theme ):
      QSyntaxHighlighter.__init__( self, parent )
      self.parent = parent
      keyword = QTextCharFormat()
      ATMEGA32_REG = QTextCharFormat()
      PREPROCESS_DIR = QTextCharFormat()
      headerfile = QTextCharFormat()
      assignmentOperator = QTextCharFormat()
      delimiter = QTextCharFormat()
      specialConstant = QTextCharFormat()
      boolean = QTextCharFormat()
      number = QTextCharFormat()
      comment = QTextCharFormat()
      string = QTextCharFormat()
      singleQuotedString = QTextCharFormat()

      self.highlightingRules = []
