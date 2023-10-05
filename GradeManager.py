from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import DatabaseManagement, sys, os
import pyqtgraph as pg

# test list of grades
listGrades = (100, 96, 58, 87, 48)

# screen to show grades (inherits pyqtgraph convenience class LayoutWidget)
class SpecialismProvider(pg.LayoutWidget):

    def __init__(self, user, sub):
        self.user = user
        self.sub = sub
        super().__init__()
        # retrieve grades from database
        gradeTuple = DatabaseManagement.retrieveGrades(user, sub)
        if len(gradeTuple) == 0:
            self.showErr()
        # a list for the values of the grades.
        self.xval = []
        for items in gradeTuple:
            self.xval.append(items[3])
        self.setFixedSize(600, 600)

        # window properties
        self.setWindowTitle(f"{self.user}'s grade history for {self.sub}")
        self.setStyleSheet('''background-color: black;''')

        # create a plot widget using pyqtgraph
        self.graph = pg.PlotWidget()
        self.graph.showGrid(x=True, y=True)
        # axis titles: left is for y-axis and bottom is for x-axis
        self.graph.setLabel("left", "Score")
        self.graph.setLabel("bottom", f"Data Entries for {sub}")
        # plot the values from the above list onto the graph, use crosses as the plot symbol
        self.graph.plot(self.xval, symbol="x")
        # window heading
        self.label4Graph = QLabel("Analysis Mode.")
        self.label4Graph.setStyleSheet('''font: Work Sans SemiBold, Segoe UI Semibold, Arial Black, sans-serif; color: 
        white; font-size: 20px; letter-spacing:-0.5px;''')
        # add the heading onto the widget at (0,0) on the grid layout
        self.addWidget(self.label4Graph, 0, 0)
        # add the graph below the header.
        self.addWidget(self.graph, 1, 0)
        # label containing instructions on interfacing with the graph
        self.label4Settings = QLabel("Left click + drag: move graph. Right click + drag: adjust scale\nRight click on axis: adjust axis scale. Mouse wheel / 2 finger swipe: axis zoom.", self)
        self.label4Settings.setStyleSheet('''color:gray;''')
        self.label4Settings.setGeometry(170, 7, 430, 20)
        self.label4Settings.adjustSize()

    def showErr(self):
        # generate an error message
        self.fail = QErrorMessage(self)
        self.fail.setStyleSheet('''background-color: white;''')
        self.fail.showMessage("You haven't uploaded a grade for this subject yet. Please add a grade if you want to see progress for this subject.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.exit(app.exec())
