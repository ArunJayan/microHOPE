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
      # keyword
      brush = QBrush( Qt.darkBlue, Qt.SolidPattern )
      keyword.setForeground( brush )
      keyword.setFontWeight( QFont.Bold )
      keywords = QStringList( [ "int","float","double","char"
								,"unsigned","long","uint8_t",
								"uint16_t","uint32_t","uint64_t","if","else","for","switch","while","do",
								"return","void"] )
	
      for word in keywords:
        pattern = QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, keyword )
        self.highlightingRules.append( rule )
      #Preprocessor Directive
      brush = QBrush( Qt.darkGreen, Qt.SolidPattern )
      PREPROCESS_DIR.setForeground( brush )
      PREPROCESS_DIR.setFontWeight( QFont.Bold )
      pattern = QRegExp("#[^\n]*")
      rule = HighlightingRule( pattern, PREPROCESS_DIR )
      self.highlightingRules.append( rule )
      #header <......>
      
      brush = QBrush( Qt.blue, Qt.SolidPattern )
      headerfile.setForeground( brush ) 
      headerfile.setFontWeight( QFont.Bold )
      pattern = QRegExp("<[^\n]*")
      rule = HighlightingRule( pattern , headerfile )
      self.highlightingRules.append( rule )
      
      # ATMEGA32_REG
      ATMEGA32_REG.setForeground( brush )
      keywords = QStringList( [ "DDRC","DDRA","DDRB","DDRD",
								"PORTA","PORTB","PORTC","PORTD"
								"ADCSRA","ADEN","ADMUX","REFS0","ADSC"
								,"ADIF","ADCH","ADCL",
								"UCSRB","TXEN","RXEN","UBRRH","UBRRL","UCSRC","URSEL","UCSZ1","UCSZ0",
								"UCSRA","RXC","UDR","UDRE"] )
      for word in keywords:
        pattern = QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, ATMEGA32_REG )
        self.highlightingRules.append( rule )


      # assignmentOperator
      brush = QBrush( Qt.darkGray, Qt.SolidPattern )
      pattern = QRegExp( "(<){1,2}-" )
      assignmentOperator.setForeground( brush )
      assignmentOperator.setFontWeight( QFont.Bold )
      rule = HighlightingRule( pattern, assignmentOperator )
      self.highlightingRules.append( rule )
      
      # delimiter
      pattern = QRegExp( "[\)\(]+|[\{\}]+|[][]+" )
      delimiter.setForeground( brush )
      delimiter.setFontWeight( QFont.Bold )
      rule = HighlightingRule( pattern, delimiter )
      self.highlightingRules.append( rule )

      # specialConstant
      brush = QBrush( Qt.darkBlue, Qt.SolidPattern )
      specialConstant.setForeground( brush )
      keywords = QStringList( [ "Inf", "NA", "NaN", "NULL" ] )
      for word in keywords:
        pattern = QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, specialConstant )
        self.highlightingRules.append( rule )

      # boolean
      boolean.setForeground( brush )
      keywords = QStringList( [ "TRUE", "FALSE" ] )
      for word in keywords:
        pattern = QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, boolean )
        self.highlightingRules.append( rule )

      # number
      pattern = QRegExp( "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" )
      pattern.setMinimal( True )
      number.setForeground( brush )
      number.setFontWeight( QFont.Bold )
      rule = HighlightingRule( pattern, number )
      self.highlightingRules.append( rule )

      # comment
      brush = QBrush( Qt.red, Qt.SolidPattern )
      pattern = QRegExp( "//[^\n]*" )
      comment.setForeground( brush )
      rule = HighlightingRule( pattern, comment )
      self.highlightingRules.append( rule )

      # string
      brush = QBrush( Qt.magenta, Qt.SolidPattern )
      pattern = QRegExp( "\".*\"" )
      pattern.setMinimal( True )
      string.setForeground( brush )
      rule = HighlightingRule( pattern, string )
      self.highlightingRules.append( rule )
      
      # singleQuotedString
      pattern = QRegExp( "\'.*\'" )
      pattern.setMinimal( True )
      singleQuotedString.setForeground( brush )
      rule = HighlightingRule( pattern, singleQuotedString )
      self.highlightingRules.append( rule )

    def highlightBlock( self, text ):
      for rule in self.highlightingRules:
        expression = QRegExp( rule.pattern )
        index = expression.indexIn( text )
        while index >= 0:
          length = expression.matchedLength()
          self.setFormat( index, length, rule.format )
          index = text.indexOf( expression, index + length )
      self.setCurrentBlockState( 0 )

class HighlightingRule():

