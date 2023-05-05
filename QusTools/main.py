import sys
from PySide2.QtWidgets import QApplication
from welcomeScreen_ui_helper import WelcomeScreenGUI

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("Application starting")
    welcomeApp = QApplication(sys.argv)
    print("QApplication initialized")
    welcomeUI = WelcomeScreenGUI()
    print("Welcome Screen initialized")
    print("Loading display...")
    welcomeUI.show()
    print("Display succeeded")
    sys.exit(welcomeApp.exec_())