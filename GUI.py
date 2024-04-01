from PyQt5 import uic
from datetime import datetime
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QCheckBox,
    QSpinBox,
)
import sys


class Home(QMainWindow):
    def __init__(self) -> None:
        """
        init the main window for the gui

        """
        super(Home, self).__init__()
        # Load the UI file
        uic.loadUi("./Utilities/GUI.ui", self)

        self.parent_directory = self.findChild(QPushButton, "Parent_Directory")
        self.CloudComPy_directory = self.findChild(QPushButton, "CloudComPy310_path")
        self.script_path = self.findChild(QPushButton, "Filter_script_path")
        self.output_path = self.findChild(QPushButton, "Output_Directory")
        self.clear_button = self.findChild(QPushButton, "clear_button")
        self.start = self.findChild(QPushButton, "start")
        self.record = self.findChild(QPushButton, "record_button")
        self.view = self.findChild(QPushButton, "view_button")
        self.checkBox = self.findChild(QCheckBox, "checkBox")
        self.live_data = self.findChild(QCheckBox, "live")
        self.frames = self.findChild(QSpinBox, "frames")
        self.fps_label = self.findChild(QLabel, "fps_label")
        self.parent_directory.clicked.connect(self.directory_path)
        self.CloudComPy_directory.clicked.connect(self.directory_path)
        self.script_path.clicked.connect(self.file_path)
        self.output_path.clicked.connect(self.directory_path)
        self.clear_button.clicked.connect(self.clear)
        self.start.clicked.connect(self.run)
        self.record.clicked.connect(self.capture)
        self.view.clicked.connect(self.visualize)
        self.parent_label = self.findChild(QLabel, "parent_label")
        self.CloudComPy_label = self.findChild(QLabel, "CloudComPy_label")
        self.filter_label = self.findChild(QLabel, "filter_label")
        self.out_label = self.findChild(QLabel, "out_label")

        self.show()

    def directory_path(self):
        """
        Opens a file dialog to select a directory based on the button clicked.

        If no directory is selected, it displays an error message and clears the corresponding label.

        Returns:
            None
        """
        button = self.sender()
        button_name = button.text()

        if button_name == "Parent Directory":
            path = QFileDialog.getExistingDirectory(
                self,
                "Select the parent directory that contains the subdirectories of the CSV files",
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
                "Select the directory that contains the CloudComparePY310 binaries",
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
                "Select the directory where the output txt files will be saved",
                "D:\\CMS\\Bachelor\\Egyptian KITTI Dataset\\Try parent style",
            )
            if path == "":
                self.errorMessage("Error", "Please select a directory")
                self.out_label.setText("")
                return
            self.out_label.setText(path)

    def file_path(self):
        """
        Opens a file dialog to select a Python file and sets the selected file path to the filter_label.

        Returns:
            None
        """
        button = self.sender()
        button_name = button.text()
        path = QFileDialog.getOpenFileName(
            self,
            "Select the filter script",
            "D:\\CMS\\Bachelor\\Softwares\\CloudComparePYBinaries\\CloudComPy310\\filter.py",
            "Python files (*.py)",
        )
        if path[0] == "":
            self.errorMessage("Error", "Please select a python file")
            self.filter_label.setText("")
            return
        self.filter_label.setText(path[0])

    def errorMessage(self, title, text):
        """
        Display an error message dialog box.

        Parameters:
        - title (str): The title of the error message box.
        - text (str): The text to be displayed in the error message box.

        Returns:
        None
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def infoMessage(self, title, text):
        """
        Display an information message box.

        Args:
            title (str): The title of the message box.
            text (str): The text to be displayed in the message box.

        Returns:
            None
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def clear(self):
        """
        Clears the labels and checkboxes in the GUI.

        This method sets the text of several labels to an empty string,
        unchecks a checkbox, and sets the value of a frames variable to 1.

        Parameters:
        None

        Returns:
        None
        """
        self.parent_label.setText("")
        self.CloudComPy_label.setText("")
        self.filter_label.setText("")
        self.out_label.setText("")
        self.checkBox.setChecked(False)
        self.frames.setValue(1)

    def hide_all(self):
        """
        Hides all the widgets in the GUI.

        This method hides all the widgets in the GUI except for the start button.

        Parameters:
        None

        Returns:
        None
        """
        self.parent_directory.hide()
        self.CloudComPy_directory.hide()
        self.script_path.hide()
        self.output_path.hide()
        self.clear_button.hide()
        self.start.hide()
        self.record.hide()
        self.view.hide()
        self.checkBox.hide()
        self.live_data.hide()
        self.frames.hide()
        self.fps_label.hide()
        self.parent_label.hide()
        self.CloudComPy_label.hide()
        self.filter_label.hide()
        self.out_label.hide()

    def capture(self):
        """
        Captures the live data from the Velodyne sensor.

        This method captures the live data from the Velodyne sensor and saves it to a .pcap file.

        Parameters:
        None

        Returns:
        None
        """
        path = QFileDialog.getExistingDirectory(
            self,
            "Select the directory to save the .pcap file",
            "D:\\CMS\\Bachelor\\Softwares\\VeloView\\records\\Test parent style",
        )
        if path == "":
            self.errorMessage("Error", "Please select a directory")
            return
        try:
            os.remove(".env")
        except:
            pass
        with open(".env", "w") as file:
            file.write(f'SAVE_FOLDER="{path}"\n')
            file.write(
                f'SUB_DIRECTORY="{datetime.now().strftime("%Y-%m-%d %H-%M-%S.%f")}"'
            )

        from stream import pcap_encoder

        pcap_encoder()

    def visualize(self):
        """
        Visualizes the live data from the Velodyne sensor.

        This method visualizes the live data from the Velodyne sensor .

        Parameters:
        None

        Returns:
        None
        """
        path = QFileDialog.getExistingDirectory(
            self,
            "Select the data directory to visualize",
            "D:\\CMS\\Bachelor\\Softwares\\VeloView\\records\\Test parent style",
        )
        if path == "":
            self.errorMessage("Error", "Please select a directory")
            return

        os.system(f'lidar_visualizer "{path}"')

    def run(self):
        """
        Runs the data preprocessing pipeline.

        This method checks if all the required fields are filled in the GUI. If any field is empty, it displays an error message and returns.
        Otherwise, it creates a .env file and writes the necessary configuration parameters to it. And runs the data preprocessing pipeline.
        Finally, it removes the .env file.

        Note: The import statements should NOT be moved to the top of the file.
              If the import statement is moved to the top, the global variables will be set before the .env file is created.

        Returns:
            None
        """
        if (
            self.parent_label.text() == ""
            or self.CloudComPy_label.text() == ""
            or self.filter_label.text() == ""
            or self.out_label.text() == ""
        ):
            self.errorMessage("Error", "Please fill all the fields")
            return
        try:
            os.remove(".env")
        except:
            pass
        with open(".env", "w") as file:
            parent_directory = self.parent_label.text().replace("/", "\\\\")
            output_directory = self.out_label.text().replace("/", "\\\\")
            filter_script = self.filter_label.text().replace("/", "\\\\")
            cloudcompy_path = self.CloudComPy_label.text().replace("/", "\\\\")
            if cloudcompy_path.split(":")[0] == "D":
                cloudcompy_path = "/d " + cloudcompy_path
            file.write(f'Parent_Directory="{parent_directory}"\n')
            file.write(f'CloudComPy310_path="{cloudcompy_path}"\n')
            file.write(f'Filter_script_path="{filter_script}"\n')
            file.write(f'Output_Directory="{output_directory}"\n')
            file.write(f"Filter={self.checkBox.isChecked()}\n")
            file.write(f"FPS={self.frames.value()}")

        # DO NOT MOVE THIS IMPORT TO THE TOP OF THE FILE OR ELSE YOU WILL DIE . YOU HAVE BEEN WARNED

        from veloview import veloview_preprocessing
        from live import live_preprocessing

        # DO NOT MOVE THIS IMPORT TO THE TOP OF THE FILE OR ELSE YOU WILL DIE . YOU HAVE BEEN WARNED
        if self.live_data.isChecked():
            live_preprocessing(self)
        else:
            veloview_preprocessing(self)
        try:
            os.remove(".env")
        except:
            pass


def main():
    app = QApplication(sys.argv)
    window = Home()
    # window.hide_all()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
