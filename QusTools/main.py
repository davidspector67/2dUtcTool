import sys
from PyQt5.QtWidgets import QApplication
from welcomeScreen import WelcomeGUI

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    welcomeApp = QApplication(sys.argv)
    welcomeUI = WelcomeGUI()
    welcomeUI.show()
    sys.exit(welcomeApp.exec_())