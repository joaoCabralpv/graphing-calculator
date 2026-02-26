import PySide6
from PySide6 import QtWidgets
import sys 

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.vbox=QtWidgets.QVBoxLayout()
        self.widget=QtWidgets.QWidget()
        self.widget.setLayout(self.vbox)
        self.current_line_edit=QtWidgets.QLineEdit()
        self.current_connection = self.current_line_edit.returnPressed.connect(self.expression_entered)
        self.vbox.addWidget(self.current_line_edit)
        self.setCentralWidget(self.widget)

    def expression_entered(self):
        text=self.current_line_edit.text()
        self.current_line_edit.disconnect(self.current_connection)
        label=QtWidgets.QLabel(text)
        self.vbox.addWidget(label)
        self.current_line_edit=QtWidgets.QLineEdit()
        self.current_connection = self.current_line_edit.returnPressed.connect(self.expression_entered)
        self.vbox.addWidget(self.current_line_edit)
        
        print(text)
        


calc=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
calc.exec()