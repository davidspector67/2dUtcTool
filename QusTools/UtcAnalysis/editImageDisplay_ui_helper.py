from UtcAnalysis.editImageDisplay_ui import *

class EditImageDisplayGUI(Ui_editBmode, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.contrastValDisplay.setTextVisible(False)
        self.brightnessValDisplay.setTextVisible(False)
        self.sharpnessValDisplay.setTextVisible(False)
    