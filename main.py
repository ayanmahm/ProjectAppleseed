import sys, os, MessageBoxManagement, ValidationProcess, SetUpPage
# Use the Qt library to visualise
from PySide6 import *
from PySide6 import QtWidgets
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

AttnFormat = '''font-family: Work Sans, Segoe UI, Arial, sans-serif; font-weight: 800;'''
BodyFormat = '''font-family: Work Sans, Segoe UI, Arial, sans-serif;'''
SubheadFormat = 'font-family: Work Sans SemiBold, Segoe UI Semibold, sans-serif;'

class Genesis(QtWidgets.QWidget):

    def spawnMessage(self, c=None):
        self.setWindowTitle("Hello world!")
        self.resize(300, 250)
        self.setStyleSheet(BodyFormat)
        # display a message to the user
        self.title = QLabel("Have we moved?", self)
        self.title.setStyleSheet(AttnFormat + '''font-size: 20px;''')
        self.title.move(20, 20)
        self.content = QLabel("It seems like this is a new computer, or you've moved my files.",
                              self)
        self.content.setWordWrap(True)
        self.content.setGeometry(20, 60, 195, 40)
        self.content = QLabel("Make sure that the assets folder is in the same location as the main.py file or "
                              "you will lose your documentation.", self)
        # set the text to wrap within the window so there is no overflow
        self.content.setWordWrap(True)
        self.content.setStyleSheet(BodyFormat + '''font-weight: 600;''')
        self.content.setGeometry(20, 110, 200, 60)

        self.warn = QLabel("Your documents will save in the Documents folder.", self)
        self.warn.setWordWrap(True)
        self.warn.setStyleSheet(SubheadFormat + '''color: red; font-weight: 600;''')
        self.warn.setGeometry(20, 190, 175, 40)

        self.okbtn = QPushButton("OK", self)
        self.okbtn.move(200, 200)
        self.okbtn.clicked.connect(lambda: self.restoration())
        self.show()

    def actAsNormal(self):
        if self.screen is None:
            self.screen = MainScreen()
            self.screen.show()
        else:
            self.screen = None

    def restoration(self):
        self.close()
        # if the main folder does not exist
        if not os.path.exists(self.appleseed):
            # create folder
            os.mkdir(self.appleseed)
        # if the assets folder does not exist
        if not os.path.exists(self.appleseed_as):
            # create folder
            os.mkdir(self.appleseed_as)
        # if the document folder does not exist
        if not os.path.exists(self.appleseed_dc):
            # create folder
            os.mkdir(self.appleseed_dc)
        QFontDatabase.addApplicationFont("WorkSans-Regular.ttf")
        QFontDatabase.addApplicationFont("WorkSans-Light.ttf")
        QFontDatabase.addApplicationFont("WorkSans-Bold.ttf")
        QFontDatabase.addApplicationFont("WorkSans-Italic.ttf")
        QFontDatabase.addApplicationFont("WorkSans-LightItalic.ttf")
        QFontDatabase.addApplicationFont("WorkSans-BoldItalic.ttf")
        QFontDatabase.addApplicationFont("WorkSans-SemiBold.ttf")
        QFontDatabase.addApplicationFont("WorkSans-SemiBoldItalic.ttf")
        self.actAsNormal()

    def __init__(self):
        # assign the main folder path to an attribute
        self.appleseed = os.path.expanduser('~/Documents/appleseed')
        # assign the assets folder to an attribute
        self.appleseed_as = self.appleseed + "/assets"
        # assign the documents folder to an attribute
        self.appleseed_dc = self.appleseed_as + "/documents"
        self.screen = None

        super().__init__()
        # if either the main folder, the assets folder or the document folder doesn't exist
        if not os.path.exists(self.appleseed) or not os.path.exists(self.appleseed_as) or not os.path.exists(
                self.appleseed_dc):
            self.spawnMessage()
        else:
            self.close()
            self.actAsNormal()


# class for main screen
class MainScreen(QtWidgets.QWidget):

    def MoveToSignUp(self):
        if self.SignUp is None:
            self.SignUp = SignUpScreen()
            self.SignUp.show()
        else:
            self.SignUp = None

    # Function to move from login to set up upon successful validation
    def MoveToProcess(self, u, p, t):
        self.close()
        if self.SuccessProcedure is None:
            self.SuccessProcedure = SetUpPage.ServerConnection(u, p, token=t)
            self.SuccessProcedure.show()
        else:
            self.SuccessProcedure = None

    def Validation(self, item):
        message = QErrorMessage(self)
        message.setWindowTitle("Something happened")
        message.setWindowIcon(QIcon("assets/images/ASError.png"))
        if len(item[0]) == 0:
            message.showMessage('''You need to enter a username.''')
            return False
        elif len(item[1]) == 0:
            message.showMessage('''You need to enter a password.''')
            return False
        for items in item:
            print(items)
            if items == item[0]:
                errorItem = "username"
            elif items == item[1]:
                errorItem = "password"
            else:
                errorItem = "entry"
            if ValidationProcess.ValidateInput(items) == 1:
                message.showMessage(f'''Please change your {errorItem}. The forbidden characters are: \n''' + ' '.join(
                    ValidationProcess.forbidden_items))
                return False
            elif ValidationProcess.ValidateInput(items) == 2:
                message.showMessage(f'''Please make your {errorItem} longer. It should be at least 6 characters long.''')
                return False
        self.close()
        self.MoveToProcess(item[0], item[1], "exist")
        return True

    # initiate the window
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setWindowIcon(QIcon("assets/images/ASCorner.png"))
        self.setFixedSize(400, 300)
        # "Welcome" text
        self._Title = QLabel(self)
        # Qt uses CSS to style windows.
        self._Title.setStyleSheet(AttnFormat + """ font-size: 25px; """)
        self._Title.setText("Welcome")
        self._Title.move(100, 10)
        self._Title.show()

        # "Username" indicator
        self._UNlabel = QLabel("Username", self)
        self._UNlabel.setAccessibleName("Username")
        self._UNlabel.move(100, 60)
        self._UNlabel.show()

        # "Password" indicator
        self._PWLabel = QLabel("Password", self)

        self._PWLabel.setAccessibleName("Password")
        self._PWLabel.move(100, 100)
        self._PWLabel.show()

        # "Username" field
        self.UNEntry = QLineEdit(self)
        self.UNEntry.setAccessibleName("Username entry column")
        self.UNEntry.move(175, 58)
        self.UNEntry.show()

        # "Password" filed
        self.PWEntry = QLineEdit(self)
        self.PWEntry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PWEntry.setAccessibleName("Password entry column")
        self.PWEntry.move(175, 98)
        self.PWEntry.show()

        self.SuccessProcedure = None
        # Button to confirm the login
        self._Ok = QPushButton("Confirm", self)
        self._Ok.clicked.connect(lambda: [self.Validation([self.UNEntry.text(), self.PWEntry.text()])])
        self._Ok.setFixedWidth(65)
        self._Ok.move(175, 140)
        # Add accessible properties for users of assistive technologies
        self._Ok.setAccessibleName("Confirm")
        self._Ok.setAccessibleDescription("Clicking here will submit what you typed to the server.")
        self._Ok.show()

        # Button to cancel
        self._Cancel = QPushButton("Cancel", self)
        self._Cancel.setFixedWidth(65)
        self._Cancel.move(245, 140)
        self._Cancel.clicked.connect(lambda: self.close())
        self._Cancel.setToolTip("Clicking here will close the application")
        # Add accessible properties for users of assistive technologies
        self._Cancel.setAccessibleName("Cancel")
        self._Cancel.show()

        # Text above sign up button
        self._Title = QLabel("Haven't set up an account yet?", self)
        # Qt uses CSS to style windows.
        self._Title.setStyleSheet(SubheadFormat + """font-size: 15px;""")
        self._Title.move(100, 200)
        self._Title.show()

        self.SignUp = None
        # Sign up button
        self._NewUser = QPushButton("Click to sign up", self)
        self._NewUser.clicked.connect(lambda: [self.MoveToSignUp(), self.close()])
        self._NewUser.move(100, 230)
        self._NewUser.setFixedSize(150, 30)
        # Add accessible properties for users of assistive technologies
        self._NewUser.setAccessibleName("Sign Up")
        self._NewUser.setAccessibleDescription("Click here to make a new account.")
        self._NewUser.show()


class SignUpScreen(QtWidgets.QWidget):

    # function to allow the user to return to the main screen upon pressing cancel.
    def ReturnToLogin(self):
        if self.LoginScreen is None:
            self.LoginScreen = MainScreen()
            self.LoginScreen.show()
        else:
            self.LoginScreen = None

    # function to allow the forbidden character warning box to appear
    def MoveToWarning(self):
        if self.warning is None:
            self.warning = MessageBoxManagement.Generate(MessageBoxManagement.ForbiddenChars)
            self.warning.show()
        else:
            self.warning = None

    def MoveToProcess(self, u, p, s, t):
        if self.SuccessProcedure is None:
            self.SuccessProcedure = SetUpPage.ServerConnection(u, p, s, t)
            self.SuccessProcedure.show()
        else:
            self.SuccessProcedure = None

    def Validation(self, item):
        message = QErrorMessage(self)
        message.setWindowTitle("Something happened")
        message.setWindowIcon(QIcon("assets/images/ASError.png"))
        if len(item[0]) == 0:
            message.showMessage('''You need to enter a username.''')
            return False
        elif len(item[1]) == 0:
            message.showMessage('''You need to enter a password.''')
            return False
        for items in item:
            print(items)
            if items == item[0]:
                errorItem = "username"
            elif items == item[1]:
                errorItem = "password"
            else:
                errorItem = "entry"
            if ValidationProcess.ValidateInput(items) == 1:
                message.showMessage(f'''Please change your {errorItem}. The forbidden characters are: \n''' + ' '.join(
                    ValidationProcess.forbidden_items))
                return False
            elif ValidationProcess.ValidateInput(items) == 2:
                message.showMessage(f'''Please make your {errorItem} longer. It should be at least 6 characters long.''')
                return False
        self.close()
        self.MoveToProcess(item[0], item[1], self.ComboBoxOption.currentText(), "gen")
        return True

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sign up")
        self.setStyleSheet(BodyFormat)
        self.setFixedSize(350, 300)
        # "Welcome" text
        self._Title = QLabel("Sign up", self)
        # Qt uses CSS to style windows.
        self._Title.setStyleSheet(SubheadFormat + """ font-size: 30px;""")
        self._Title.move(75, 10)

        # "Username" indicator
        self._UNlabel = QLabel("Choose your new username", self)
        self._UNlabel.setAccessibleName("Choose your new username")
        self._UNlabel.move(75, 60)

        # "Password" indicator
        self._PWLabel = QLabel("Choose your password", self)
        self._PWLabel.setAccessibleName("Choose your new password")
        self._PWLabel.move(75, 120)

        # "Password" indicator
        self._SubjLabel = QLabel("Choose your preferred subject", self)
        self._SubjLabel.setAccessibleName("Choose your subject")
        self._SubjLabel.move(75, 200)

        self.warning = None
        # "Password" warning
        self._PWarning = QPushButton("Be careful! Some characters are " + "\u0332".join("prohibited") + ".", self,
                                     flat=True)
        self._PWarning.setStyleSheet("""
            QPushButton {
                color: red;
                font-size:11px;
                }""")
        self._PWarning.setAccessibleName("View characters you can't use in your username or password")
        self._PWarning.setToolTip("Look at the forbidden characters")
        self._PWarning.move(72, 175)
        self._PWarning.clicked.connect(lambda: self.MoveToWarning())

        # "Username" field
        self.UNEntry = QLineEdit(self)
        self.UNEntry.setAccessibleName("Choose your username")
        self.UNEntry.move(75, 90)

        # "Password" field
        self.PWEntry = QLineEdit(self)
        self.PWEntry.setAccessibleName("Choose your password")
        self.PWEntry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PWEntry.move(75, 150)

        # "Subject" field
        self.ComboBoxOption = QComboBox(self)
        self.ComboBoxOption.setAccessibleName("Choose your subject")
        self.ComboBoxOption.addItems(['English', 'Maths', 'Physics', 'Chemistry', 'Biology', 'Computer Science',
                                      'Psychology', 'Art and Design'])
        self.ComboBoxOption.move(75, 220)

        self.SuccessProcedure = None
        # Button to confirm the sign up
        self._Ok = QPushButton("Sign up", self)
        self._Ok.clicked.connect(lambda: self.Validation([self.UNEntry.text(), self.PWEntry.text()]))
        self._Ok.setIcon(QIcon("assets/images/ASSend.png"))
        self._Ok.setIconSize(QSize(20,20))
        self._Ok.setToolTip("Click here to register")
        self._Ok.move(75, 259)

        self.LoginScreen = None
        # Button to return to login
        self._Cancel = QPushButton("Return", self)
        self._Cancel.setFixedWidth(65)
        self._Cancel.move(175, 262)
        self._Cancel.clicked.connect(lambda: [self.close(), self.ReturnToLogin()])
        self._Cancel.setToolTip("Return to Login")

        self.show()


# driver code to run
if __name__ == "__main__":
    # creates an instance of Qt
    app = QtWidgets.QApplication(sys.argv)
    # Allocate the class to form and run
    form = Genesis()
    sys.exit(app.exec())
