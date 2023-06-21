import sys
from PySide2.QtWidgets import QApplication
from UtcAnalysis.selectImage_ui_helper import *

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    welcomeApp = QApplication(sys.argv)
    welcomeUI = SelectImageGUI()
    welcomeUI.show()
    sys.exit(welcomeApp.exec_())