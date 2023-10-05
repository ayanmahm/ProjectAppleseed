from PySide6 import *
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import UserInterfaceEnv, DatabaseManagement, MessageBoxManagement, main, hashlib, time, sys
from ValidationProcess import *


class ServerThread(QObject):
    # updates the value of the progress bar
    update = Signal(int)
    # changes the detail text when a change is made
    newTxt = Signal(str)
    # changes the screen of the UI when there is an exception
    screenUIchange = Signal()
    # sends the signal to move on
    finished = Signal()
    # sends feedback when a failure occurs
    failure = Signal(str)

    def __init__(self, username, password, subject=None):
        self.username = username
        self.password = hashlib.md5(password.encode()).hexdigest()
        if subject is not None:
            self.subject = subject
        super().__init__()

    def existingUser(self):
        # detail text update to say:
        self.newTxt.emit("Processing username")
        # try - error trapping
        try:
            # if the user exists - the check returns true
            if DatabaseManagement.testForExistence(table="users", username=self.username, password=self.password):
                print("true accessed")
                # update progress value
                self.update.emit(99)
                self.newTxt.emit("Processing...")
                print("finished thrd")
                # emit signal to move on
                self.finished.emit()
            # if the check does not work - user does not exist
            else:
                print("else accessed")
                # emit code not found
                self.failure.emit("notfound")
        # if error is that there is no internet connection
        except DatabaseManagement.InternetFail:
            # update detail text to say there is no connection.
            self.newTxt.emit("There was a connection error. You cannot connect right now.\n\nYour documents are "
                             "available in the Documents folder on your computer!")
            # update the UI to error form
            self.screenUIchange.emit()
        # if error is with text handling from form.
        except TypeError:
            self.screenUIchange.emit()
            # explain error with detail text
            self.newTxt.emit("Your entry was blank or a conversion error occured. Please try again")
            # emit failure signal
            self.failure.emit()

    def newUser(self):
        try:
            self.newTxt.emit("Checking your details")
            # Check for the user's directory
            if DatabaseManagement.testForExistence(table="users", item=self.username, column="username"):
                self.newTxt.emit("Redirecting you to your account")
                self.failure.emit("exists")
                return False
            self.update.emit(20)
            # Create user when confirmed their details not on server
            self.newTxt.emit("Uploading you to the server")
            DatabaseManagement.newUser(self.username, self.password, self.subject)
            self.update.emit(60)
            self.newTxt.emit("Creating your workspace")
            # Create files for experience
            # ManageFiles did not work inside PyQT6/PySide6 files strangely.
            DatabaseManagement.ManageFiles(self.username)
            self.update.emit(99)
            self.newTxt.emit("Loading workspace")
            self.finished.emit()
            print("finished thrd")
        except DatabaseManagement.InternetFail:
            self.newTxt.emit("There was a connection error. You cannot connect right now.")
            self.screenUIchange.emit()
        except:
            self.failure.emit()



class ServerConnection(QtWidgets.QWidget):

    def ExistingOperations(self):
        # Allow for operations to occur in the background by using multithreading.
        self.OpThread = QThread()
        self.Commands = ServerThread(self.username, self.password)
        # Connect to the class which contains the thread.
        self.Commands.moveToThread(self.OpThread)
        # Signals and slots to handle the output
        # Automatically start to execute code when the thread is first called.
        self.OpThread.started.connect(self.Commands.existingUser)
        # The thread should terminate as soon as the commands are complete
        self.Commands.finished.connect(self.MoveToProcess)
        self.Commands.finished.connect(self.OpThread.quit)
        # Delete the thread and the class of commands once done.
        self.Commands.finished.connect(self.Commands.deleteLater)
        self.OpThread.finished.connect(self.Commands.deleteLater)
        # Where to report any updates to progress
        self.Commands.update.connect(self.updateStatusBar)
        self.Commands.newTxt.connect(self.updateUnderTextService)
        self.Commands.screenUIchange.connect(self.updateBarDesign)
        self.Commands.failure.connect(self.feedback)
        # Execute thread
        self.OpThread.start()

    def NewUserOperations(self):
        # Allow for operations to occur in the background by using multithreading.
        self.OpThread = QThread()
        self.Commands = ServerThread(self.username, self.password, self.subject)
        # Connect to the class which contains the thread.
        self.Commands.moveToThread(self.OpThread)
        # Signals and slots to handle the output
        # Automatically start to execute code when the thread is first called.
        self.OpThread.started.connect(self.Commands.newUser)
        # The thread should terminate as soon as the commands are complete
        self.Commands.finished.connect(self.MoveToProcess)
        self.Commands.finished.connect(self.OpThread.quit)
        # Delete the thread and the class of commands once done.
        self.Commands.finished.connect(self.Commands.deleteLater)
        self.OpThread.finished.connect(self.Commands.deleteLater)
        # Where to report any updates to progress
        self.Commands.update.connect(self.updateStatusBar)
        self.Commands.newTxt.connect(self.updateUnderTextService)
        self.Commands.screenUIchange.connect(self.updateBarDesign)
        self.Commands.failure.connect(self.feedback)
        # Execute thread
        self.OpThread.start()

    def MoveToProcess(self):
        self.close()
        self.ldr = LoaderScreen(username=self.username, password=self.password)

    def refreshFctn(self):
        self.close()
        if self.refreshInstance is None:
            self.refreshInstance = ServerConnection(username=self.username, password=self.password,
                                                              token="ref")
            self.refreshInstance.show()
        else:
            self.refreshInstance = None

    # slot which gives feedback and generates the relevant screen
    def feedback(self, signal=None):
        print("feedback accessed")
        self.err = QErrorMessage(self)
        if signal == "notfound":
            if self.window is None:
                self.close()
                self.window = main.SignUpScreen()
                self.window.show()
                self.err.showMessage("A user with those details wasn't found. Check your details are correct and try "
                                     "again.")
            else:
                self.window = None
        elif signal == "exists":
            if self.window is None:
                self.close()
                self.window = main.MainScreen()
                self.window.show()
                self.err.showMessage("This account already exists. Please log in instead.")
            else:
                self.window = None
        else:
            self.close()
            if self.window is None:
                self.window = main.MainScreen()
                self.window.show()
                self.err.showMessage("Something here went wrong :/\nTry again later.")
            else:
                self.window = None

    # Slot to update the Progress Bar when something is done
    @Slot(int)
    def updateStatusBar(self, amount):
        self.progress.setValue(amount)

    # Slot to update the information when something is done
    @Slot(str)
    def updateUnderTextService(self, text):
        self.detailedText.setText(text)
        self.detailedText.adjustSize()

    # This method is used to update the UI to report an error
    def updateBarDesign(self):
        self.setWindowTitle("Something went wrong!")
        self._logo.setText("oops!")
        self.setWindowIcon(QIcon("assets/images/ASError.png"))
        self._SubText.setText("Looks like something went wrong!")
        self._logo.adjustSize()
        self._SubText.adjustSize()
        self.progress.setValue(99)
        self.progress.setGeometry(-1, 110, 700, 20)
        self.progress.setGraphicsEffect(None)
        self.refresh.setVisible(True)
        self.home.setVisible(True)


    # interface
    def __init__(self,  username, password, subject=None, token=None, *args, **kwargs):
        # call to the parent class
        super().__init__(*args, **kwargs)
        # set the window title
        self.setWindowTitle("Loading")
        self.setWindowIcon(QIcon("assets/images/ASLoader.png"))
        # variables
        self.username = username
        self.password = password
        self.token = token
        self.refreshInstance = None
        if subject is not None:
            self.subject = subject

        self.window = None
        self.setFixedSize(600, 200)

        self._logo = QLabel("welcome", self)
        self._logo.move(35, 25)
        self._logo.setStyleSheet('''
                font-family: Work Sans, Arial, sans-serif;
                font-weight:800;
                font-size: 40px;''')

        # if the function is being called for existing users:
        if self.token == "exist":
            self._SubText = QLabel("Obtaining your dashboard", self)
        elif self.token == "gen":
            self._SubText = QLabel("Setting you up for first time use...", self)
        elif self.token == "ref":
            self._SubText = QLabel("Refreshing your dashboard", self)
        else:
            self._SubText = QLabel("Loading", self)
        self._SubText.move(35, 75)

        # progress bar
        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setGeometry(35, 110, 500, 20)

        # Shadow on progress bar
        self.BarShadow = QGraphicsDropShadowEffect(self.progress)
        self.BarShadow.setOffset(0)
        self.BarShadow.setBlurRadius(25)
        self.progress.setGraphicsEffect(self.BarShadow)

        # Text which appears underneath the loading bar
        self.detailedText = QLabel(self)
        self.detailedText.move(35, 140)
        self.SuccessProcedure = None

        # Refresh button for error screen
        self.refresh = QPushButton("Refresh", self)
        self.refresh.setToolTip("Clicking here will open a new session")
        self.refresh.setStyleSheet('''font-family: Work Sans, Segoe UI, Arial, sans-serif; padding: 5px;''')
        self.refresh.move(350, 35)
        # QApplication and QStyle have transitioned from QtGui to QtWidgets as of PySide5 / PyQt5
        self.refresh.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_BrowserReload))
        self.refresh.clicked.connect(lambda: [self.close(), self.refreshFctn()])
        self.refresh.setVisible(False)

        # Home button for error screen
        self.home = QPushButton("Main Screen", self)
        self.home.setToolTip("Clicking here will open a new session")
        self.home.setStyleSheet('''font-family: Work Sans, Segoe UI, Arial, sans-serif; padding: 5px;''')
        self.home.move(450, 35)
        # QApplication and QStyle have transitioned from QtGui to QtWidgets as of PySide5 / PyQt5
        self.home.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_VistaShield))
        self.home.clicked.connect(lambda: [self.close(), self.feedback()])
        self.home.setVisible(False)

        if self.token == "exist" or self.token == "ref":
            self.ExistingOperations()
        elif self.token == "gen":
            self.NewUserOperations()


class UpdaterCore(QObject):
    finished = Signal(str)

    def __init__(self, username, new, property):
        self.username = username
        self.new = new
        self.prop = property
        super().__init__()

    def changeProperty(self):
        # when the changed element is the password
        if self.prop == "password":
            try:
                # encrypt the password first
                NEWpassword = hashlib.md5(self.new.encode()).hexdigest()
                # upload the password
                DatabaseManagement.UpdateDetails("password", NEWpassword, self.username)
                self.finished.emit("success")
            except:
                self.finished.emit("failure")
        # otherwise
        else:
            try:
                # upload new item to server
                DatabaseManagement.UpdateDetails(self.prop, self.new, self.username)
                self.finished.emit("success")
            except:
                self.finished.emit("failure")


class ChoiceDownloadClass(QObject):
    finished = Signal(tuple)
    def __init__(self, user):
        self.un = user
        super().__init__()

    def runtime(self):
        tup = DatabaseManagement.CustomSQLInteraction(f'''SELECT * FROM courses WHERE username = '{self.un}';''')
        self.finished.emit(tup)


class loaderWINDOW(QObject):
    load = Signal()
    v_fail = Signal()
    emitSig = Signal(str)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username', None)
        self.pw = kwargs.get('password', None)
        if self.pw is not None:
            self.password = hashlib.md5(self.pw.encode()).hexdigest()
        super().__init__()

    def loader(self):
        print("loading window")
        self.emitSig.emit("Your feed has loaded. If you still see this screen, an error has occured.")
        self.load.emit()


class LoaderScreen(QtWidgets.QWidget):

    def ManifestWndw(self):
        # Allow for operations to occur in the background by using multithreading.
        self.thread = QThread()
        self.cmds = loaderWINDOW()
        # Connect to the class which contains the thread.
        self.cmds.moveToThread(self.thread)
        # Signals and slots to handle the output
        # Automatically start to execute code when the thread is first called.
        self.thread.started.connect(self.cmds.loader)
        self.cmds.emitSig.connect(self.updatescaryText)
        # The thread should terminate as soon as the commands are complete
        self.cmds.load.connect(self.MoveToProcess)
        self.cmds.load.connect(self.thread.quit)
        # Delete the thread and the class of commands once done.
        self.cmds.load.connect(self.cmds.deleteLater)
        self.thread.finished.connect(self.cmds.deleteLater)
        # Execute thread
        self.thread.start()

    def LoaderThread(self):
        # Allow for operations to occur in the background by using multithreading.
        self.thread = QThread()
        self.cmds = UpdaterCore(username=self.username, property=self.property, new=self.nu)
        # Connect to the class which contains the thread.
        self.cmds.moveToThread(self.thread)
        # Signals and slots to handle the output
        # Automatically start to execute code when the thread is first called.
        self.thread.started.connect(self.cmds.changeProperty)
        # The thread should terminate as soon as the commands are complete
        self.cmds.finished.connect(self.feedback)
        self.cmds.finished.connect(self.thread.quit)
        # Delete the thread and the class of commands once done.
        self.cmds.finished.connect(self.cmds.deleteLater)
        self.thread.finished.connect(self.cmds.deleteLater)
        # Execute thread
        self.thread.start()

    # slot which gives feedback and generates the relevant screen
    def feedback(self, signal=None):
        print("feedback accessed")
        self.err = QErrorMessage(self)
        if signal == "success":
            self.close()
            self.err.showMessage("Your details were updated successfully")
        else:
            self.close()
            self.err.showMessage("Something here went wrong :/\nTry again later.")

    def MoveToProcess(self):
        print("reached")
        if self.SuccessProcedure is None:
            self.SuccessProcedure = UserInterfaceEnv.ProfileWindow(username=self.username, password=self.password)
            self.close()
            self.SuccessProcedure.show()
        else:
            self.SuccessProcedure = None

    @Slot(str)
    def updatescaryText(self, I):
        self.undertext.setText(I)
        self.undertext.adjustSize()

    # interface
    def __init__(self, **kwargs):
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.property = kwargs.get('property', None)
        self.nu = kwargs.get('new', None)
        self.chStat = kwargs.get('choices', None)
        self.SuccessProcedure = None
        super().__init__()
        self.setWindowTitle("Loading")
        self.setWindowIcon(QIcon("assets/images/asLogo.png"))
        self.window = None
        self.setFixedSize(400, 150)

        # text on screen
        self._logo = QLabel("Loading", self)
        self._logo.setGeometry(0, 25, 400, 50)
        self._logo.setStyleSheet(main.SubheadFormat + '''font-weight: 700; font-size: 30px;''')
        self._logo.setAlignment(Qt.AlignCenter)

        self.undertext = QLabel("Loading user details", self)
        self.undertext.setStyleSheet(main.BodyFormat + '''font-size: 13px;''')
        self.undertext.setGeometry(0, 75, 400, 50)
        self.undertext.setAlignment(Qt.AlignCenter)

        # Text which appears underneath the loading bar
        self.detailedText = QLabel(self)
        self.detailedText.move(35, 140)
        self.show()

        if self.property is not None:
            if self.property == "salp":
                self.show()
            else:
                self.LoaderThread()
        else:
            self.ManifestWndw()

class time2die(QtWidgets.QWidget):
    def __init__(self):
        super(time2die, self).__init__()
        self.setFixedSize(400, 50)
        self.setWindowIcon(QIcon("assets/images/ASErasecrop.png"))
        self.setWindowTitle("Goodbye")
        self.title = QLabel("You're all set!", self)
        self.title.setStyleSheet(main.AttnFormat + '''font-size: 24px;''')
        self.title.move(10, 10)

        self.button = QPushButton("Goodbye", self)
        self.button.move(250, 15)
        # calling sys.exit will terminate Python completely
        self.button.clicked.connect(lambda: sys.exit())
        self.button.setStyleSheet(main.BodyFormat)
        self.show()

class DeleteThread(QObject):
    load = Signal()
    emitSig = Signal(str)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username', None)
        super().__init__()

    def deleteAccount(self):
        print("Delete reached")
        # delete grades
        self.emitSig.emit(f"Deleting @{self.username}'s grades")
        DatabaseManagement.EradicateGradeHistory(self.username)
        # delete inbox messages
        self.emitSig.emit(f"Deleting @{self.username}'s messages")
        DatabaseManagement.EradicateInboxHistory(self.username)
        # delete user account
        self.emitSig.emit(f"Deleting @{self.username}'s account")
        DatabaseManagement.EradicateUserHistory(self.username)
        self.emitSig.emit("The program will now terminate. Thank you for using Appleseed.")
        self.load.emit()


class deleteClass(QtWidgets.QWidget):

    def DeleteProcess(self):
        # Allow for operations to occur in the background by using multithreading.
        self.thread = QThread()
        self.cmds = DeleteThread(username=self.username)
        # Connect to the class which contains the thread.
        self.cmds.moveToThread(self.thread)
        # Signals and slots to handle the output
        # Automatically start to execute code when the thread is first called.
        self.thread.started.connect(self.cmds.deleteAccount)
        self.cmds.emitSig.connect(self.updatescaryText)
        # The thread should terminate as soon as the commands are complete
        self.cmds.load.connect(self.byebye)
        self.cmds.load.connect(self.thread.quit)
        # Delete the thread and the class of commands once done.
        self.cmds.load.connect(self.cmds.deleteLater)
        self.thread.finished.connect(self.cmds.deleteLater)
        # Execute thread
        self.thread.start()

    @Slot(str)
    def updatescaryText(self, I):
        self.updateText.setText(I)
        self.updateText.setGeometry(0, 75, 400, 50)
        self.updateText.setAlignment(Qt.AlignCenter)

    # transfer to final window
    def byebye(self):
        self.close()
        if self.SuccessProcedure is None:
            self.SuccessProcedure = time2die()
            self.SuccessProcedure.show()
        else:
            self.SuccessProcedure = None

    # interface
    def __init__(self, **kwargs):
        print("reached")
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        # if an administrator uses the delete service, this should be given as true. It assigns False by default.
        self.admin = kwargs.get('admin', False)
        self.SuccessProcedure = None
        super().__init__()
        self.setWindowTitle("Loading")

        self.window = None
        self.setFixedSize(400, 150)
        self.setWindowIcon(QIcon("assets/images/ASErasecrop.png"))

        if self.admin is True:
            self._logo = QLabel("Admin mode accessed.", self)
        else:
            # text on screen
            self._logo = QLabel("We're letting you go", self)
        self._logo.setGeometry(0, 25, 400, 50)
        self._logo.setStyleSheet(main.SubheadFormat + '''font-weight: 700; font-size: 30px;''')
        self._logo.setAlignment(Qt.AlignCenter)

        self.updateText = QLabel("Preparing to delete user data.", self)
        self.updateText.setStyleSheet(main.BodyFormat + '''font-size: 13px;''')
        self.updateText.setGeometry(0, 75, 400, 50)
        self.updateText.setAlignment(Qt.AlignCenter)

        self.DeleteProcess()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.exit(app.exec())
