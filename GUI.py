from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QCheckBox,
    QSpinBox,
    QProgressBar,
)
import sys


class Home(QMainWindow):
    def __init__(self) -> None:
        """
        init the main window for the gui

        """
        super(Home, self).__init__()
        uic.loadUi("./GUI.ui", self)

        self.parent_directory = self.findChild(QPushButton, "Parent_Directory")
        self.CloudComPy_directory = self.findChild(QPushButton, "CloudComPy310_path")
        self.script_path = self.findChild(QPushButton, "Filter_script_path")
        self.output_path = self.findChild(QPushButton, "Output_Directory")
        self.clear_button = self.findChild(QPushButton, "clear_button")
        self.start = self.findChild(QPushButton, "start")
        self.checkBox = self.findChild(QCheckBox, "checkBox")
        self.frames = self.findChild(QSpinBox, "frames")
        self.top_bar_label = self.findChild(QLabel, "top_bar_label")
        self.top_bar_label.setVisible(False)
        self.bottom_bar_label = self.findChild(QLabel, "bottom_bar_label")
        self.bottom_bar_label.setVisible(False)
        self.top_bar = self.findChild(QProgressBar, "top_bar")
        self.top_bar.setVisible(False)
        self.bottom_bar = self.findChild(QProgressBar, "bottom_bar")
        self.bottom_bar.setVisible(False)
        self.parent_directory.clicked.connect(self.directory_path)
        self.CloudComPy_directory.clicked.connect(self.directory_path)
        self.script_path.clicked.connect(self.file_path)
        self.output_path.clicked.connect(self.directory_path)
        self.clear_button.clicked.connect(self.clear)
        self.start.clicked.connect(self.run)
        self.parent_label = self.findChild(QLabel, "parent_label")
        self.CloudComPy_label = self.findChild(QLabel, "CloudComPy_label")
        self.filter_label = self.findChild(QLabel, "filter_label")
        self.out_label = self.findChild(QLabel, "out_label")

        self.show()

    def directory_path(self):
        button = self.sender()
        button_name = button.text()

        if button_name == "Parent Directory":
            path = QFileDialog.getExistingDirectory(
                self,
                "Open file",
                "D:\\CMS\\Bachelor\\Softwares\\VeloView\\records\\Test parent style",
            )
            if path == "":
                self.errorMessage("Error", "Please select a directory")
                self.parent_label.setText("")
                return
            self.parent_label.setText(path)
        elif button_name == "CloudComPy310":
            path = QFileDialog.getExistingDirectory(
                self,
                "Open file",
                "D:\\CMS\\Bachelor\\Softwares\\CloudComparePYBinaries\\CloudComPy310",
            )
            if path == "":
                self.errorMessage("Error", "Please select a directory")
                self.CloudComPy_label.setText("")
                return
            self.CloudComPy_label.setText(path)
        elif button_name == "Output Directory":
            path = QFileDialog.getExistingDirectory(
                self,
                "Open file",
                "D:\\CMS\\Bachelor\\Egyptian KITTI Dataset\\Try parent style",
            )
            if path == "":
                self.errorMessage("Error", "Please select a directory")
                self.out_label.setText("")
                return
            self.out_label.setText(path)

    def file_path(self):
        button = self.sender()
        button_name = button.text()
        path = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "D:\\CMS\\Bachelor\\Softwares\\CloudComparePYBinaries\\CloudComPy310\\filter.py",
            "Python files (*.py)",
        )
        if path[0] == "":
            self.errorMessage("Error", "Please select a python file")
            self.filter_label.setText("")
            return
        self.filter_label.setText(path[0])

    def errorMessage(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def infoMessage(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def clear(self):
        self.parent_label.setText("")
        self.CloudComPy_label.setText("")
        self.filter_label.setText("")
        self.out_label.setText("")
        self.checkBox.setChecked(False)
        self.frames.setValue(0)

    def run(self):
        if (
            self.parent_label.text() == ""
            or self.CloudComPy_label.text() == ""
            or self.filter_label.text() == ""
            or self.out_label.text() == ""
        ):
            self.errorMessage("Error", "Please fill all the fields")
            return
        print(self.checkBox.isChecked())


def main():
    app = QApplication(sys.argv)
    window = Home()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
