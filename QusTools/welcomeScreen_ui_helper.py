from welcomeScreen_ui import *
from UtcAnalysis.selectImage_ui_helper import *

class WelcomeScreenGUI(Ui_welcomeScreen, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.selectImageGui = SelectImageGUI()
        self.rf2dAnalysisButton.clicked.connect(self.switchToRf2d)

    def switchToRf2d(self):
        if self.selectImageGui.isVisible():
            self.selectImageGui.hide()
            self.show()
        else:
            self.selectImageGui.show()
            self.hide()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = WelcomeScreenGUI()
    ui.show()
    sys.exit(app.exec_())