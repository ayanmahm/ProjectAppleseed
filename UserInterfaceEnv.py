import hashlib, sys, os, DatabaseManagement, webbrowser, ValidationProcess, SetUpPage, main, MessageBoxManagement, GradeManager
from PySide6 import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

ComboBoxItems = ['English', 'Maths', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Psychology', 'Art and Design']
AttnFormat = '''font-family: Work Sans, Segoe UI, Arial, sans-serif; font-weight: 800;'''
BodyFormat = '''font-family: Work Sans, Segoe UI, Arial, sans-serif;'''
SubheadFormat = 'font-family: Work Sans SemiBold, Segoe UI Semibold, sans-serif;'

# Note that we are using QMainWindow in order to utilise Menus and Toolbars
class ProfileWindow(QMainWindow):

    def spawnCourses(self, item):
        # Object to contain the
        self.item = QWidget(self)
        self.item.setFixedSize(700, 100)
        # Title of the course
        self.itemHead = QLabel(item[0], self.item)
        self.itemHead.setStyleSheet(SubheadFormat + '''font-size: 15px;''')
        self.itemHead.move(10, 10)
        self.itemHead.adjustSize()

        # Description of course
        if item[3] is None:
            self.itemDescription = QLabel("A description wasn't provided for this course", self.item)
        else:
            self.itemDescription = QLabel(item[3], self.item)
        # The next two lines contain the description so that it does not exceed the boundary of the QFrame
        self.itemDescription.setFixedWidth(690)
        self.itemDescription.setWordWrap(True)
        self.itemDescription.move(10, 35)
        self.itemDescription.adjustSize()

        if item[5] is None:
            det = (item[1] + " • " + item[2] + " • An expiry date wasn't provided for this course")
        else:
            det = (item[1] + " • " + item[2] + " • " + item[5].strftime("%x"))
        self.itemDetails = QLabel(det, self.item)
        self.itemDetails.move(10, 75)
        self.itemDetails.setStyleSheet('''font-size: 11px; color: gray; font-style: italic;''')
        self.itemDetails.adjustSize()

        self.sendButton = QPushButton(self.item, flat=True)
        self.sendButton.move(550, 65)
        self.sendButton.setToolTip("Send to a friend")
        self.sendButton.setIcon(QIcon("assets/images/ASSend.png"))
        self.sendButton.setIconSize(QSize(25, 25))
        self.sendButton.clicked.connect(lambda: self.sendTo(item[0], item[4]))

        self.itemButton = QPushButton("View course", self.item)
        self.itemButton.move(600, 70)
        self.itemButton.clicked.connect(lambda: webbrowser.open_new(item[4]))

        return self.item

    def sendTo(self, title, url):
        self.DMWindow = Send2Friend(self.UN, title=title, url=url)
        self.DMWindow.show()

    # Function to manage the window
    def MakeMenu(self):
        # Create a Menu that is attached to the Window header
        self.WindowBar = self.menuBar()
        # Set the menu to the window
        self.setMenuBar(self.WindowBar)
        # Menu for Account
        self.AccMenu = QMenu("Account", self)
        self.WindowBar.addMenu(self.AccMenu)
        self.ac = QAction("View Details", self)
        self.AccMenu.addAction(self.ac)
        self.ac.triggered.connect(self.MoveToAccount)
        self.lgt = QAction("Log out of " + self.UN, self)
        self.AccMenu.addAction(self.lgt)
        self.lgt.triggered.connect(lambda:[self.close(), self.logout()])

    def logout(self):
        if self.lgtprocess is None:
            self.lgtprocess = main.MainScreen()
            self.lgtprocess.show()
        else:
            self.lgtprocess = None

    def MoveToAccount(self):
        if self.AccountWindow is None:
            self.AccountWindow = Account(username=self.UN, password=self.PW, spc=self.specialism)
            self.AccountWindow.show()
        else:
            self.AccountWindow = None

    def MoveToGrades(self):
        if self.GradeWindow is None:
            self.GradeWindow = Grades(self.UN)
            self.GradeWindow.show()
        else:
            self.GradeWindow = None

    def MoveToChoices(self):
        if self.ChoicesWindow is None:
            self.ChoicesWindow = Choices(self.UN)
            self.ChoicesWindow.show()
        else:
            self.ChoicesWindow = None

    def makeGr(self, u, s):
        if self.gradeMkr is None:
            self.gradeMkr = GradeManager.SpecialismProvider(u, s)
            self.gradeMkr.show()
        else:
            self.gradeMkr = None

    def refreshFctn(self):
        if self.refreshInstance is None:
            self.refreshInstance = SetUpPage.ServerConnection(username=self.UN, password=self.PW, token="ref")
            self.refreshInstance.show()
        else:
            self.refreshInstance = None

    def MoveToInbox(self):
        if self.InboxWin is None:
            self.InboxWin = showInbox(self.UN)
            self.InboxWin.show()
        else:
            self.InboxWin = None

    # open
    def OpenFiles(self, filename):
        try:
            os.system(filename)
        except:
            DatabaseManagement.ManageFiles(self.UN)
            os.system(filename)

    def __init__(self, username, password, **kwargs):
        self.UN = username
        self.PW = password
        # window for graph
        self.gradeMkr = None
        # window for refresh
        self.refreshInstance = None
        # window for settings
        self.AccountWindow = None
        # attribute for log out
        self.lgtprocess = None
        # window to add grade
        self.GradeWindow = None
        # window to manage university choices
        self.ChoicesWindow = None
        # specialism variable
        self.specialism = None
        # window to create message
        self.DMWindow = None
        # window to view messages.
        self.InboxWin = None

        # attributes for directory locations
        drx_name = "C:/Users/mahma/Documents/GitHub/appleseed/assets/documents/" + username
        cv_name = drx_name + "/" + username + "CV.docx"
        ps_name = drx_name + "/" + username + "PS.docx"
        super().__init__()
        self.setWindowIcon(QIcon("assets/images/asLogo.png"))

        self.setStyleSheet(BodyFormat)
        self.MakeMenu()
        self.setFixedSize(1000, 530)

        # frame for cv, personal statement and grade inputs
        self.FuturePlanningFrame = QFrame(self)
        self.FuturePlanningFrame.setFrameStyle(QFrame.Box)
        self.FuturePlanningFrame.setLineWidth(1)
        self.FuturePlanningFrame.setFixedSize(200, 255)
        self.FuturePlanningFrame.move(10, 30)
        self.FuturePlanningFrame.setLineWidth(1)

        # personal statement features
        self.PersonalStatement = QLabel("View your personal statement", self.FuturePlanningFrame)
        self.PersonalStatement.move(10, 10)
        self.PSButton = QPushButton("Open", self.FuturePlanningFrame)
        self.PSButton.clicked.connect(lambda: self.OpenFiles(ps_name))
        self.PSButton.move(10, 35)

        # cv features
        self.CV = QLabel("View your CV", self.FuturePlanningFrame)
        self.CV.move(10, 70)
        self.CVButton = QPushButton("Open", self.FuturePlanningFrame)
        self.CVButton.clicked.connect(lambda: self.OpenFiles(cv_name))
        self.CVButton.move(10, 95)

        # university features
        self.uni = QLabel("Manage your university choices", self.FuturePlanningFrame)
        self.uni.move(10, 130)
        self.unibtn = QPushButton("Manage", self.FuturePlanningFrame)
        self.unibtn.clicked.connect(self.MoveToChoices)
        self.unibtn.move(10, 155)

        # grade input features.
        self.grade = QLabel("Update your grades", self.FuturePlanningFrame)
        self.grade.move(10, 190)
        self.grdbtn = QPushButton("Update", self.FuturePlanningFrame)
        self.grdbtn.clicked.connect(self.MoveToGrades)
        self.grdbtn.move(10, 215)

        # graph frame (house graph content)
        self.GraphFrame = QFrame(self)
        self.GraphFrame.setFrameStyle(QFrame.Box)
        self.GraphFrame.setLineWidth(1)
        self.GraphFrame.setFixedSize(200, 220)
        self.GraphFrame.move(10, 300)
        self.GraphFrame.setLineWidth(1)

        # graph title and options
        self.graphTitle = QLabel("Progress Report", self.GraphFrame)
        self.graphTitle.setStyleSheet(SubheadFormat + '''font-size: 15px; ''')
        self.graphTitle.move(10, 10)

        self.graphtext = QLabel("Generate your progress graph", self.GraphFrame)
        self.graphtext.move(10, 40)

        self.choice1 = QComboBox(self.GraphFrame)
        self.choice1.move(10, 70)
        self.choice1.addItems(ComboBoxItems)

        self.graphBTN = QPushButton("Generate", self.GraphFrame)
        self.graphBTN.move(10, 100)
        self.graphBTN.clicked.connect(lambda: self.makeGr(self.UN, self.choice1.currentText()))

        # inbox title and buttons
        self.inboxTitle = QLabel("Messages", self.GraphFrame)
        self.inboxTitle.move(10, 140)
        self.inboxTitle.setStyleSheet(SubheadFormat + '''font-size: 15px; ''')

        self.inboxBTN = QPushButton("Inbox", self.GraphFrame)
        self.inboxBTN.move(10, 170)
        self.inboxBTN.clicked.connect(lambda: self.MoveToInbox())

        # Contents of the second side
        # Display the username to show success
        self.userDisplay = QLabel("Welcome @" + self.UN + "!", self)
        self.userDisplay.move(225, 40)
        self.userDisplay.setStyleSheet(SubheadFormat + '''font-size: 30px;''')
        self.userDisplay.adjustSize()

        # defined header to show the section
        self.header = QLabel("COURSES", self)
        self.header.move(226, 85)
        self.header.setStyleSheet(SubheadFormat + '''font-size: 15px; letter-spacing: 1px;''')
        self.header.adjustSize()

        # refresh button
        self.refresh = QPushButton("Refresh", self)
        self.refresh.setToolTip("Clicking here will open a new session")
        self.refresh.move(850, 50)
        # QApplication and QStyle have transitioned from QtGui to QtWidgets as of PySide5 / PyQt5
        self.refresh.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_BrowserReload))
        self.refresh.clicked.connect(lambda: [self.close(), self.refreshFctn()])


        # create an area to show courses
        self.Area = QFrame(self)
        self.Area.adjustSize()

        # Append the scrollarea onto the QFrame
        self.SArea = QScrollArea(self)
        self.SArea.setWidgetResizable(True)
        # Disable the horizontal scrolling policy
        self.SArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        policy = self.SArea.sizePolicy()
        policy.setVerticalStretch(1)
        policy.setHorizontalStretch(1)
        self.SArea.setWidget(self.Area)
        self.SArea.setFixedSize(750, 400)
        self.SArea.move(225, 120)

        # set a vertical area to stack courses on top of each other
        self.CourseMenu = QVBoxLayout(self.Area)
        self.CourseMenu.setSpacing(3)

        # show that the user has a specialty
        try:
            self.specialism = DatabaseManagement.RetrieveCourse(self.UN)
            # related courses
            if self.specialism is None:
                self.specialism = ""
            self.relCourses = DatabaseManagement.ReturnAllMethod('courses', self.specialism)
            # non-related courses
            self.XtraCourses = DatabaseManagement.ReturnAllOthers('courses', self.specialism)
        except:
            self.close()
            self.error = QErrorMessage(self)
            self.error.showMessage("Something went wrong. Check your internet connection and try again.")

        else:
            if self.specialism is not None:
                self.headerSpecialism = QLabel(self.specialism, self)
                self.headerSpecialism.move(350, 85)
                self.headerSpecialism.setStyleSheet(BodyFormat + '''font-size: 15px;''')
                self.headerSpecialism.adjustSize()
            for items in self.relCourses:
                self.addition = self.spawnCourses(items)
                self.CourseMenu.addWidget(self.addition)
            for items in self.XtraCourses:
                self.addition = self.spawnCourses(items)
                self.CourseMenu.addWidget(self.addition)


class Account(QtWidgets.QWidget):

    # move to the detail changer
    def moveDetailEditor(self, username, change, property):
        if self.Winchange is None:
            self.Winchange = changeScreen(username=username, old=change, property=property)
            self.Winchange.show()
        else:
            self.Winchange = None

    # move to delete screen
    def move2Del(self, username):
        self.close()
        if self.delChange is None:
            self.delChange = DeleteAccount(username)
            self.delChange.show()
        else:
            self.delChange = None

    def __init__(self, username, password, **kwargs):
        # obtain username and password from previous window
        self.un = username
        self.pw = password
        # for testing
        self.rnMode = kwargs.get('runtime', None)
        if self.rnMode == "debug":
            self.pwCheck = password
        # for testing
        self.speciality = kwargs.get('spc', None)
        # window for delete window
        self.delChange = None
        # window for password
        self.Winchange = None
        super().__init__()
        # window metadata
        self.setWindowTitle(username + "'s account")
        self.setWindowIcon(QIcon("assets/images/ASSettings.png"))
        self.setFixedSize(400, 325)

        # window header
        self.WinTitle = QLabel("Your account", self)
        self.WinTitle.move(11, 12)
        self.WinTitle.setStyleSheet(SubheadFormat + '''letter-spacing:-0.5px; font-size: 25px''')

        # frame skeleton
        self.DetailSection = QFrame(self)
        self.DetailSection.setGeometry(10, 60, 380, 250)
        self.DetailSection.setFrameStyle(QFrame.StyledPanel)
        self.DetailSection.setStyleSheet('''
                QFrame {
                    border-radius: 5px;
                    border: 1px solid #BBCBBC;
                    }
                    ''')
        # Shadow on FRAME
        self.DSFrame = QGraphicsDropShadowEffect(self.DetailSection)
        self.DSFrame.setOffset(0)
        self.DSFrame.setBlurRadius(10)
        self.DetailSection.setGraphicsEffect(self.DSFrame)

        # content for frame, frame dimensions mimic self.DetailSection 's geometry
        # two frames are stacked on top of each other due to abnormal properties when using self.DetailSection
        self.DSContent = QFrame(self)
        self.DSContent.setGeometry(self.DetailSection.frameGeometry())
        self.DSHeader = QLabel("Your details", self.DSContent)
        self.DSHeader.move(20, 20)
        self.DSHeader.setStyleSheet(SubheadFormat + '''font-size: 15px; letter-spacing: 0.5px;''')

        # formatting options for the screen
        headerstyle = BodyFormat +'''weight: 650;'''
        delstyle = AttnFormat + '''font-weight: 800; color: red; font-size: 13px;'''
        warningstyle= BodyFormat + '''font-size: 11px; color: gray; font-style: italic;'''

        # username
        self.DSUNheader = QLabel("Username", self.DSContent)
        self.DSUNheader.move(20, 60)
        self.DSUNheader.setStyleSheet(headerstyle)
        self.DSUNContent = QLabel(self.un, self.DSContent)
        self.DSUNContent.move(100, 60)
        # warning
        self.DSUNwarning = QLabel("your username cannot be changed.", self.DSContent)
        self.DSUNwarning.move(100, 77)
        self.DSUNwarning.setStyleSheet(warningstyle)

        # password
        self.DSPWheader = QLabel("Password", self.DSContent)
        self.DSPWheader.move(20, 115)
        self.DSPWheader.setStyleSheet(headerstyle)

        # detail text for password
        self.DSPWContent = QLabel("You can't see your password from here.", self.DSContent)
        self.DSPWContent.setGeometry(100,75,100,100)
        self.DSPWContent.setWordWrap(True)
        self.DSPWContent.setStyleSheet(warningstyle)

        # button to change password
        self.DSPWButton = QPushButton(" Change password ", self.DSContent)
        self.DSPWButton.clicked.connect(lambda: self.moveDetailEditor(username=self.un, change=self.pw, property="password"))
        self.DSPWButton.move(210, 113)

        # password
        self.DSSPheader = QLabel("Speciality", self.DSContent)
        self.DSSPheader.move(20, 160)
        self.DSSPheader.setStyleSheet(headerstyle)
        # remove clause in coursework
        if self.speciality is not None:
            self.DSSPContent = QLabel(self.speciality, self.DSContent)
        else:
            self.DSSPContent = QLabel(DatabaseManagement.RetrieveCourse(self.un), self.DSContent)
        self.DSSPContent.move(100, 160)
        self.DSSPButton = QPushButton(" Change speciality ", self.DSContent)
        self.DSSPButton.clicked.connect(lambda: self.moveDetailEditor(username=self.un, change=self.pw,
                                                                      property="board"))
        self.DSSPButton.move(210, 156)
        self.DSSPwarning = QLabel("You need to restart the program to see changes", self.DSContent)
        self.DSSPwarning.move(100, 180)
        self.DSSPwarning.setStyleSheet(warningstyle)

        # delete account header
        self.Delheader = QLabel("Delete my account", self.DSContent)
        self.Delheader.move(20, 210)
        self.Delheader.setStyleSheet(delstyle)

        # delete account button
        self.DelBtn = QPushButton("Delete account", self.DSContent)
        self.DelBtn.setIcon(QIcon("assets/images/ASError.png"))
        self.DelBtn.clicked.connect(lambda: self.move2Del(self.un))
        self.DelBtn.move(210, 210)


class changeScreen(QtWidgets.QWidget):

    # function to check all values before sending to the server
    def prep(self, f1, f2, f3, p, u):
        # print which property is being checked
        print(p)
        # if the two new entries are not the same
        if f2 != f3:
            # show error message
            self.err = QErrorMessage(self)
            self.err.showMessage("You failed to repeat your info")
        else:
            # if the property is the password
            if p == "password":
                if ValidationProcess.ValidateInput(f1) == 0:
                    # if the encrypted entry of the old password is not the same as the password as on the database
                    if hashlib.md5(f1.encode()).hexdigest() != DatabaseManagement.GetUserDetails(u)[3]:
                        # show error message
                        self.err = QErrorMessage(self)
                        self.err.showMessage("You entered your old password wrong.")
                    else:
                        # otherwise, continue operation as normal, open loader screen
                        if self.loader is None:
                            self.loader = SetUpPage.LoaderScreen(username=u, property=p, new=f2)
                            self.loader.show()
                        else:
                            self.loader = None
                else:
                    # show error message
                    self.err = QErrorMessage(self)
                    self.err.showMessage("Your input did not meet the standards for a password.")
            # if the property value is the course
            elif p == "board":
                # if the plain text entry is the same as the database value
                if f1 != DatabaseManagement.GetUserDetails(u)[5]:
                    # show error message
                    self.err = QErrorMessage(self)
                    self.err.showMessage("You entered your old course wrong.")
                else:
                    # otherwise continue as normal
                    if self.loader is None:
                        self.loader = SetUpPage.LoaderScreen(username=u, property=p, new=f2)
                        self.loader.show()
                    else:
                        self.loader = None

    def __init__(self, **kwargs):
        # inherited properties - username and property to change
        self.property = kwargs.get('property', None)
        self.user = kwargs.get('username', None)
        self.loader = None
        super().__init__()

        # window properties
        self.setFixedSize(400, 270)
        self.setStyleSheet(BodyFormat)
        self.setWindowIcon(QIcon("assets/images/ASSettings.png"))

        # frame to store content
        self.DetailSection = QFrame(self)
        self.DetailSection.setGeometry(10, 10, 380, 250)
        self.DetailSection.setFrameStyle(QFrame.StyledPanel)
        self.DetailSection.setStyleSheet('''
                QFrame {
                    border-radius: 5px;
                    border: 1px solid #BBCBBC;
                    }
                    ''')
        # Shadow on FRAME
        self.DSFrame = QGraphicsDropShadowEffect(self.DetailSection)
        self.DSFrame.setOffset(0)
        self.DSFrame.setBlurRadius(10)
        self.DetailSection.setGraphicsEffect(self.DSFrame)

        # content for frame, dimensions mimic self.DetailSection
        self.DSContent = QFrame(self)
        self.DSContent.setGeometry(self.DetailSection.frameGeometry())
        self.DSHeader = QLabel("Changing details:   " + str(self.property), self.DSContent)
        self.DSHeader.move(20, 20)
        self.DSHeader.setStyleSheet(SubheadFormat + '''font-size: 15px;''')

        # username
        headerstyle =  '''font-weight: 650;'''
        warningstyle = '''font-size: 11px; color: gray; font-style: italic;'''
        self.Oldheader = QLabel("Old", self.DSContent)
        self.Oldheader.move(20, 60)
        self.Oldheader.setStyleSheet(headerstyle)

        self.Oldwarning = QLabel("Enter your current here", self.DSContent)
        self.Oldwarning.move(100, 85)
        self.Oldwarning.setStyleSheet(warningstyle)

        # password
        self.Newheader = QLabel("New", self.DSContent)
        self.Newheader.move(20, 115)
        self.Newheader.setStyleSheet(headerstyle)
        self.NewWarning = QLabel("Enter your new here", self.DSContent)
        self.NewWarning.move(100, 140)
        self.NewWarning.setStyleSheet(warningstyle)

        # password
        self.RepeatHeader = QLabel("Repeat new", self.DSContent)
        self.RepeatHeader.move(20, 170)
        self.RepeatHeader.setStyleSheet(headerstyle)

        self.Repeatwarning = QLabel("Repeat the new entry", self.DSContent)
        self.Repeatwarning.move(100, 195)
        self.Repeatwarning.setStyleSheet(warningstyle)

        self.changeBtn = QPushButton(" Change ", self.DSContent)
        self.changeBtn.move(275, 200)

        if self.property == "board":
            # use combo boxes if changing speciality
            # old entry
            self.Oldentry = QComboBox(self)
            self.Oldentry.addItems(ComboBoxItems)
            self.Oldentry.move(110, 70)

            # "Subject" field
            self.NewEntry = QComboBox(self)
            self.NewEntry.addItems(ComboBoxItems)
            self.NewEntry.move(110, 125)

            # "Subject" field
            self.RepeatEntry = QComboBox(self)
            self.RepeatEntry.addItems(ComboBoxItems)
            self.RepeatEntry.move(110, 180)
            # on click, call prep function to validate entries
            self.changeBtn.clicked.connect(lambda: [self.close(), self.prep(f1=self.Oldentry.currentText(), f2=self.NewEntry.currentText(),f3=self.RepeatEntry.currentText(), p=self.property, u=self.user)])
        else:
            # for non 'board' elements, use line edit instead
            self.Oldentry = QLineEdit(self.DSContent)
            self.Oldentry.move(100, 60)
            self.NewEntry = QLineEdit(self.DSContent)
            self.NewEntry.move(100, 115)
            self.RepeatEntry = QLineEdit(self.DSContent)
            self.RepeatEntry.move(100, 170)
            # on click, call prep function to validate entries
            self.changeBtn.clicked.connect(lambda: [self.close(), self.prep(f1=self.Oldentry.text(), f2=self.NewEntry.text(), f3=self.RepeatEntry.text(), p=self.property, u=self.user)])

        # tooltips + accessible text
        self.Oldentry.setToolTip("Enter your current here")
        self.NewEntry.setToolTip("Enter your new here")
        self.RepeatEntry.setToolTip("Repeat the new entry")

        self.show()


class Choices(QtWidgets.QWidget):
    def saveChoices(self, usern, c1, c2, c3, c4, c5, **kwargs):
        if self.prcsBox is None:
            self.prcsBox = MessageBoxManagement.Generate(MessageBoxManagement.UploadDB, "Your new choices are uploading...")
            self.prcsBox.show()
        else:
            self.prcsBox = None
        try:
            if kwargs.get('new', False):
                DatabaseManagement.addtoChoice(user=usern, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5)
            else:
                DatabaseManagement.UpdateChoices(detail="choice1", user=usern, item=c1)
                DatabaseManagement.UpdateChoices(detail="choice2", user=usern, item=c2)
                DatabaseManagement.UpdateChoices(detail="choice3", user=usern, item=c3)
                DatabaseManagement.UpdateChoices(detail="choice4", user=usern, item=c4)
                DatabaseManagement.UpdateChoices(detail="choice5", user=usern, item=c5)
            # show success
            if self.successBox is None:
                self.successBox = MessageBoxManagement.Generate(MessageBoxManagement.SuccessDB)
                self.successBox.show()
            else:
                self.successBox = None
        except ValueError:
            self.err = QErrorMessage(self)
            self.err.showMessage("Your entry was invalid")
        except Exception as e:
            print(e)
            self.err = QErrorMessage(self)
            self.err.showMessage("Something went wrong. Try again!")

    def __init__(self, username):
        self.un = username
        self.prcsBox = None
        self.successBox = None
        self.retGrade = DatabaseManagement.returnChoices(username)
        if self.retGrade is not None:
            self.gradeList = [self.retGrade[2], self.retGrade[3], self.retGrade[4], self.retGrade[5], self.retGrade[6]]
        super().__init__()
        self.setStyleSheet(BodyFormat)
        self.setWindowIcon(QIcon("assets/images/ASSettings.png"))
        self.h1 = QLabel("Choice 1", self)
        self.h1.move(10, 80)
        self.h2 = QLabel("Choice 2", self)
        self.h2.move(10, 110)
        self.h3 = QLabel("Choice 3", self)
        self.h3.move(10, 140)
        self.h4 = QLabel("Choice 4", self)
        self.h4.move(10, 170)
        self.h5 = QLabel("Choice 5", self)
        self.h5.move(10, 200)

        if self.retGrade is not None:
            self.choice1 = QLineEdit(self.gradeList[0], self)
            self.choice2 = QLineEdit(self.gradeList[1], self)
            self.choice3 = QLineEdit(self.gradeList[2], self)
            self.choice4 = QLineEdit(self.gradeList[3], self)
            self.choice5 = QLineEdit(self.gradeList[4], self)
        else:
            self.choice1 = QLineEdit(self)
            self.choice2 = QLineEdit(self)
            self.choice3 = QLineEdit(self)
            self.choice4 = QLineEdit(self)
            self.choice5 = QLineEdit(self)

        self.choice1.move(100, 80)
        self.choice2.move(100, 110)
        self.choice3.move(100, 140)
        self.choice4.move(100, 170)
        self.choice5.move(100, 200)

        self.savebtn = QPushButton("Save choices", self)
        if self.retGrade is None:
            self.savebtn.clicked.connect(lambda: self.saveChoices(usern=self.un, c1=self.choice1.text(), c2=self.choice2.text(),c3=self.choice3.text(), c4=self.choice4.text(), c5=self.choice5.text(), new=True))
        else:
            self.savebtn.clicked.connect(lambda: self.saveChoices(usern=self.un, c1=self.choice1.text(), c2=self.choice2.text(), c3=self.choice3.text(), c4=self.choice4.text(), c5=self.choice5.text()))
        self.savebtn.move(100, 250)

        self.setFixedSize(300, 300)
        self.setWindowTitle(self.un + "'s choices")

        self.WinTitle = QLabel(self.un + "'s choices", self)
        self.WinTitle.setWordWrap(True)
        self.WinTitle.move(11, 12)
        self.WinTitle.setStyleSheet(SubheadFormat + '''letter-spacing:-0.5px; font-size: 22px''')
        self.show()


class Grades(QtWidgets.QWidget):
    # method to upload data point
    def saveDataPoint(self, pcnt, sbj):
        try:
            int(pcnt)
            if 0 <= int(pcnt) <= 100:
                DatabaseManagement.addGrade(self.un, sbj, pcnt)
                # show success
                if self.successBox is None:
                    self.successBox = MessageBoxManagement.Generate(MessageBoxManagement.SuccessDB)
                    self.successBox.show()
                else:
                    self.successBox = None
            else:
                self.err = QErrorMessage(self)
                self.err.showMessage("Your entry was invalid")
        except ValueError:
            self.err = QErrorMessage(self)
            self.err.showMessage("Your entry was invalid")
        except Exception as e:
            print(e)
            self.err = QErrorMessage(self)
            self.err.showMessage("Something went wrong. Try again!")

    def __init__(self, username, **kwargs):
        self.un = username
        super().__init__()
        self.setWindowIcon(QIcon("assets/images/ASSettings.png"))
        self.setStyleSheet(BodyFormat)
        self.successBox = None

        # labels for box
        self.h1 = QLabel("Subject", self)
        self.h1.move(10, 80)
        self.h2 = QLabel("Grade (%)", self)
        self.h2.move(10, 120)

        self.choice1 = QComboBox(self)
        self.choice1.addItems(ComboBoxItems)
        self.choice2 = QLineEdit(self)

        # positioning for editable elements
        self.choice1.move(100, 80)
        self.choice2.move(100, 120)

        # button to submit
        self.savebtn = QPushButton("Save grade", self)
        self.savebtn.clicked.connect(lambda: self.saveDataPoint(self.choice2.text(), self.choice1.currentText()))
        self.savebtn.move(100, 160)

        # wind n \ n 6ow metadata
        self.setFixedSize(300, 225)
        self.setWindowTitle(self.un + "'s grades")

        # window main title
        self.WinTitle = QLabel("New data point", self)
        self.WinTitle.setWordWrap(True)
        self.WinTitle.move(11, 12)
        self.WinTitle.setStyleSheet(SubheadFormat + '''letter-spacing:-0.5px; font-size: 22px''')
        self.show()


class sendClass(QObject):
    update = Signal(str)
    finished = Signal(int)

    def __init__(self, user, rec, title, url):
        self.un = user
        self.recipient = rec
        self.sendTitle = title
        self.sendURL = url
        super().__init__()

    def upload(self):
        try:
            self.update.emit("Checking if that user exists.")
            if DatabaseManagement.testForExistence(self.recipient, "users", "username"):
                self.update.emit(f"Sending the course to {self.recipient}")
                DatabaseManagement.addInbox(self.un, self.recipient, self.sendTitle, self.sendURL)
                self.finished.emit(0)
                self.update.emit(f"{self.recipient} got your message!")
                return True
            else:
                self.finished.emit(1)
                self.update.emit("")
                return False
        except DatabaseManagement.InternetFail:
            self.finished.emit(404)
            self.update.emit("")
            return False
        except:
            self.finished.emit(999)
            self.update.emit("")
            return False


class Send2Friend(QtWidgets.QWidget):
    def showSuccess(self):
        if self.successBox is None:
            self.successBox = MessageBoxManagement.Generate(MessageBoxManagement.SuccessDB)
            self.successBox.show()
        else:
            self.successBox = None

    def showError(self, msg):
        self.error = QErrorMessage(self)
        self.error.setWindowTitle("Something went wrong")
        self.error.setWindowIcon(QIcon("assets/images/ASError.png"))
        self.error.showMessage(msg)
        self.error.show()

    def sendItem(self, recipient):
        # Allow for operations to occur in the background by using multithreading.
        self.OpThread = QThread()
        self.Commands = sendClass(self.un, recipient, self.sendTitle, self.sendURL)
        # Connect to the class which contains the thread.
        self.Commands.moveToThread(self.OpThread)
        # Signals and slots to handle the output
        # Automatically start to execute code when the thread is first called.
        self.OpThread.started.connect(self.Commands.upload)
        # The thread should terminate as soon as the commands are complete
        self.Commands.finished.connect(self.thread2error)
        self.Commands.finished.connect(self.OpThread.quit)
        # Delete the thread and the class of commands once done.
        self.Commands.finished.connect(self.Commands.deleteLater)
        self.OpThread.finished.connect(self.Commands.deleteLater)
        # report updates
        self.Commands.update.connect(self.updatescaries)
        # Execute thread
        self.OpThread.start()

    @Slot(str)
    def updatescaries(self, code):
        self.undertext.setText(code)
        self.undertext.adjustSize()

    @Slot(int)
    def thread2error(self, code):
        if code == 0:
            self.showSuccess()
        elif code == 1:
            self.showError("That user doesn't exist. Try again!")
        elif code == 404:
            self.showError("Your connection is lost. Reconnect and try again.")
        else:
            self.showError("Something went wrong. Try again.")

    def __init__(self, username, **kwargs):
        self.un = username
        self.sendTitle = kwargs.get("title", None)
        self.sendURL = kwargs.get("url", None)
        super().__init__()
        # set styles
        self.setStyleSheet(BodyFormat)
        # set icons
        self.setWindowIcon(QIcon("assets/images/ASSettings.png"))
        # create variable name for new window
        self.successBox = None
        self.RefTitle = QLabel(self.sendTitle, self)
        self.RefTitle.setWordWrap(True)
        self.RefTitle.setGeometry(10, 45, 280, 35)
        if len(self.sendURL) >= 40:
            self.URLDisplay = self.sendURL[0:40] + "..."
        else:
            self.URLDisplay = self.sendURL
        self.URLlabel = QLabel(self.URLDisplay, self)
        self.URLlabel.setStyleSheet('''color: blue;''')
        self.URLlabel.move(10, 90)
        # label
        self.h1 = QLabel("Username:", self)
        self.h1.move(10, 120)
        # username line edit option
        self.choice1 = QLineEdit(self)
        self.choice1.move(100, 120)
        # button to submit
        self.savebtn = QPushButton("Send", self)
        self.savebtn.setStyleSheet("font-size:15px;")
        self.savebtn.setIcon(QIcon("assets/images/ASSend.png"))
        self.savebtn.setIconSize(QSize(25, 25))
        self.savebtn.clicked.connect(lambda: self.sendItem(self.choice1.text()))
        self.savebtn.move(99, 150)

        self.setFixedSize(300, 225)
        self.setWindowTitle("Sharing is caring")

        self.WinTitle = QLabel("Send to a friend", self)
        self.WinTitle.setWordWrap(True)
        self.WinTitle.move(11, 12)
        self.WinTitle.setStyleSheet(SubheadFormat + '''letter-spacing:-0.5px; font-size: 22px''')

        self.undertext = QLabel(self)
        self.undertext.move(10, 185)

        self.show()


class downloadMessages(QObject):
    popup = Signal(tuple)
    finished = Signal()

    def __init__(self, user):
        self.username = user
        super().__init__()

    def execute(self):
        results = DatabaseManagement.retrieveMessages(self.username)
        print(results)
        for result in results:
            print(result)
            self.popup.emit(result)
        self.finished.emit()


class showInbox(QMainWindow):
    def retrieval(self):
        # Allow for operations to occur in the background by using multithreading.
        self.OpThread = QThread()
        self.Commands = downloadMessages(self.un)
        # Connect to the class which contains the thread.
        self.Commands.moveToThread(self.OpThread)
        # Signals and slots to handle the output
        # Automatically start to execute code when the thread is first called.
        self.OpThread.started.connect(self.Commands.execute)
        # The thread should terminate as soon as the commands are complete
        self.Commands.popup.connect(self.feedAppend)
        self.Commands.finished.connect(self.OpThread.quit)
        # Delete the thread and the class of commands once done.
        self.Commands.finished.connect(self.Commands.deleteLater)
        self.OpThread.finished.connect(self.Commands.deleteLater)
        # Execute thread
        self.OpThread.start()

    def spawnMessages(self, item):
        self.setStyleSheet(BodyFormat)
        # Object to contain the
        self.item = QWidget(self)
        self.item.setFixedSize(500, 50)

        # Title of the course
        self.itemHead = QLabel(item[1], self.item)
        self.itemHead.setGeometry(0, 0, 30, 15)
        self.itemHead.adjustSize()
        self.itemHead.setWordWrap(True)

        self.itemDetails = QLabel(item[3], self.item)
        self.itemDetails.setWordWrap(True)
        self.itemDetails.setGeometry(100, 0, 150, 15)
        self.itemDetails.adjustSize()

        self.itemButton = QPushButton("View course", self.item)
        self.itemButton.move(400, 0)
        self.itemButton.clicked.connect(lambda: webbrowser.open_new(item[4]))

        return self.item

    def feedAppend(self, item):
        new = self.spawnMessages(item)
        self.CourseMenu.addWidget(new)

    def __init__(self, username):
        self.un = username
        super().__init__()
        self.setWindowTitle("Your inbox")
        self.setWindowIcon(QIcon("assets/images/ASSend.png"))
        self.setFixedSize(550, 250)

        self.title = QLabel("Your inbox", self)
        self.title.move(20, 10)
        self.title.setStyleSheet(SubheadFormat + '''font-size:20px;''')
        self.title.adjustSize()

        # create an area to show courses
        self.Area = QFrame(self)
        self.Area.adjustSize()

        # Append the scrollarea onto the QFrame
        self.SArea = QScrollArea(self)
        self.SArea.setWidgetResizable(True)

        # Disable the horizontal scrolling policy
        self.SArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        policy = self.SArea.sizePolicy()
        policy.setVerticalStretch(1)
        policy.setHorizontalStretch(1)
        self.SArea.setWidget(self.Area)
        self.SArea.setFixedSize(520, 175)
        self.SArea.move(15, 50)

        # Shadow on courses section
        self.SAreaShadow = QGraphicsDropShadowEffect(self.SArea)
        self.SAreaShadow.setOffset(0)
        self.SAreaShadow.setBlurRadius(25)
        self.SArea.setGraphicsEffect(self.SAreaShadow)

        # set a vertical area to stack courses on top of each other
        self.CourseMenu = QVBoxLayout(self.Area)
        self.CourseMenu.setSpacing(1)

        self.retrieval()
        self.show()


class DeleteAccount(QtWidgets.QWidget):

    def transition(self):
        # encrypt entry
        self.password = hashlib.md5(self.entry.text().encode()).hexdigest()
        # if password matches the entry
        if DatabaseManagement.testForExistence(table="users", username=self.username, password=self.password):
            if self.transScreen is None:
                # move to delete class
                self.transScreen = SetUpPage.deleteClass(username=self.username, password=self.password)
                self.transScreen.show()
            else:
                self.transScreen = None
        else:
            # show error that account has not been deleted due to error in password entry
            self.m = QErrorMessage(self)
            self.m.showMessage("You entered your password wrong. Your account has not been deleted.")

    def __init__(self, user):
        self.username = user
        # attribute to house deletion process
        self.transScreen = None
        # attribute to return to account menu
        self.AccountWindow = None
        super().__init__()
        # window meta
        self.setFixedSize(500, 200)
        self.setWindowIcon(QIcon("assets/images/ASErase.png"))
        self.setWindowTitle("Delete account")

        # on screen title
        self.title = QLabel("Deleting your account", self)
        self.title.setStyleSheet(AttnFormat + '''font-size: 25px;''')
        self.title.move(20, 20)

        # warning text
        self.message = QLabel("This is irreversible! Pressing submit will delete your account from the server!", self)
        self.message.setStyleSheet(BodyFormat)
        self.message.setWordWrap(True)
        self.message.setGeometry(20, 55, 450, 40)

        # message alerting consequence of deleting account
        self.message = QLabel("All account information, course information, sent messages and grades relating to "
                              f"@{self.username} will be deleted and can not be recovered."
                              f" Your documents will remain in the Documents folder.", self)
        self.message.setStyleSheet(SubheadFormat + '''font-size: 12px;''')
        self.message.setWordWrap(True)
        self.message.setGeometry(20, 90, 450, 50)

        # entry label
        self.entryLabel = QLabel("Password", self)
        self.entryLabel.setStyleSheet(SubheadFormat + '''font-size: 15px;''')
        self.entryLabel.move(20, 150)

        # line edit for password entry
        self.entry = QLineEdit(self)
        # display bullets instead of plain text
        self.entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.entry.move(120, 150)

        # delete button
        self.delete = QPushButton("Delete", self)
        self.delete.setStyleSheet(AttnFormat + '''font-size: 16px; color: red;''')
        self.delete.setIcon(QIcon("assets/images/ASError.png"))
        self.delete.move(300, 147)
        self.delete.clicked.connect(lambda: [self.close(), self.transition()])

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.exit(app.exec())
