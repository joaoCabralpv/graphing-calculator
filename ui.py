import PySide6
from PySide6 import QtWidgets
import sys
import ParseExprssion

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):


        super().__init__()
        self.setWindowTitle("Calculator")

        self.scrollArea = QtWidgets.QScrollArea()

        self.vbox=QtWidgets.QVBoxLayout()

        self.widget=QtWidgets.QWidget()
        #self.vbox.setSpacing(10)
        self.vbox.addStretch()
        self.widget.setLayout(self.vbox)
        self.current_line_edit=QtWidgets.QLineEdit()
        self.current_connection = self.current_line_edit.returnPressed.connect(self.expression_entered)
        self.vbox.addWidget(self.current_line_edit)

        self.scrollArea.setVerticalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(PySide6.QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widget)

        self.setCentralWidget(self.scrollArea)

    def expression_entered(self):
        text=self.current_line_edit.text()
        if text == "":
            return
        self.current_line_edit.disconnect(self.current_connection)
        label=QtWidgets.QLabel(str(ParseExprssion.solve(text)))
        self.vbox.addWidget(label)
        self.current_line_edit.setDisabled(True)
        self.current_line_edit=QtWidgets.QLineEdit()
        self.current_connection = self.current_line_edit.returnPressed.connect(self.expression_entered)
        self.vbox.addWidget(self.current_line_edit)
        
        print(text)
        


calc=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
calc.exec()