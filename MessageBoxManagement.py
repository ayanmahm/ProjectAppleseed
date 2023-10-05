# MessageBoxManagement.py is a file used by the software to simplify the generation of message boxes
# imports
from PySide6 import *
from PySide6 import QtWidgets
from PySide6.QtWidgets import *

# List in following order:
# [0] Icon used, [1] Message title, [2] Message content, [3] Standard buttons, [4] Default button

# Validation error codes
ForbiddenPresent = [QMessageBox.Critical, "Forbidden character present.", "You attempted to insert a forbidden "
                                                                          "character.",
                    QMessageBox.Retry, QMessageBox.Retry]
ForbiddenChars = [QMessageBox.Information, "Information", '''*()$&£=" are forbidden characters.''', QMessageBox.Ok]
Success = [QMessageBox.Information, "Information", "The entry was validated.", QMessageBox.Ok | QMessageBox.Retry,
           QMessageBox.Ok]
LengthProblem = [[QMessageBox.Critical, "Validation Error", "Your input is too short", QMessageBox.Retry]]
Username404 = [[QMessageBox.Critical, "Validation Error", "Your username wasn't found", QMessageBox.Retry]]
SuccessDB = [QMessageBox.Information, "Success", "Your information was uploaded to the server!", QMessageBox.Ok]
UploadDB = [QMessageBox.Information, "Processing", "Uploading your information", QMessageBox.Ok]

# function to generate window from given code.
# allows for a detail if needed
def Generate(code, detail=None):
    # basic windows with no function other than to inform - user must click to exit
    if len(code) == 4:
        window = QMessageBox(code[0], code[1], code[2], code[3])
        if detail is not None:
            window.setDetailedText(detail)
            return window
        else:
            return window
    # basic window with single, default button - user can press enter or click to exit
    if len(code) == 5:
        window = QMessageBox(code[0], code[1], code[2], code[3])
        window.setDefaultButton(code[4])
        if detail is not None:
            window.setDetailedText(detail)
            return window
        else:
            return window


if __name__ == "__main__":
    # creates an instance of Qt
    app = QtWidgets.QApplication(sys.argv)
    sys.exit(app.exec())
