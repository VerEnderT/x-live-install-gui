
##!/usr/bin/python3

import sys
import os
import argparse
import urllib.request
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QProcess


# Pfad zum gewünschten Arbeitsverzeichnis # Das Arbeitsverzeichnis festlegen
arbeitsverzeichnis = os.path.expanduser('/usr/share/x-live/install-gui')

os.chdir(arbeitsverzeichnis)

class InstallerApp(QtWidgets.QWidget):
    def __init__(self, flatpak_id=None, deb_name=None, pic_url=None, title_name="App", desc=""):
        super().__init__()
        
        self.flatpak_id = flatpak_id
        self.deb_name = deb_name
        self.pic_url = pic_url
        self.title_name = title_name
        self.desc = " "
        self.blinker = False
        if desc: 
            self.desc = desc.replace("\\n","\n")
        
        self.initUI()

    def initUI(self):
        # Set up the window
        self.setWindowTitle(str(self.title_name) + " installieren" )
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        self.setGeometry(100, 100, 700, 500)
        self.setFixedSize(700,500)
        # Background image
        if self.pic_url:
            # Download the image to a temporary location
            local_image_path = "/tmp/x-live/xinstall/screenshot.png"
            os.makedirs(os.path.dirname(local_image_path), exist_ok=True)
            try:
                urllib.request.urlretrieve(self.pic_url, local_image_path)
                # Display the image
                background_label = QtWidgets.QLabel(self)
                background_pixmap = QtGui.QPixmap(local_image_path)
                background_label.setPixmap(background_pixmap)
                background_label.setScaledContents(True)
                background_label.setGeometry(0, 0, 700, 500)
            except Exception as e:
                print(f"Bild konnte nicht geladen werden: {e}")

        # Foreground Widget
        foreground_widget = QtWidgets.QWidget(self)
        foreground_widget.setStyleSheet("background-color: rgba(20, 20, 20, 190);color: white;")
        foreground_widget.setGeometry(50, 50, 600, 400)
        
        # Layout for foreground content
        layout = QtWidgets.QVBoxLayout(foreground_widget)
        
        # title label
        label = QtWidgets.QLabel(f"Dies ist ein inoffizieler Installer für\n {self.title_name}")
        label.setStyleSheet("color: white; font-size: 24px;")
        label.setMaximumHeight(60)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        
        # description label
        desc_label = QtWidgets.QLabel(f"{self.desc}")
        desc_label.setStyleSheet("color: white; font-size: 18px;")
        desc_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(desc_label)
        
        # status label
        self.status = ""
        self.label_status = QtWidgets.QLabel(f"Status:\n {self.status}")
        self.label_status.setStyleSheet("color: white; font-size: 14px;padding: 5px")
        self.label_status.setMaximumHeight(40)
        layout.addWidget(self.label_status)
        self.label_status.hide()
        
        
        
        about_button = QtWidgets.QPushButton(f"über")
        #about_button.clicked.connect(self.install_flatpak)
        about_button.setStyleSheet("background-color: rgba(0, 60, 0, 150);color: white;")
        #layout.addWidget(self.flatpak_button)
        
        # Flatpak Button
        if self.flatpak_id:
            self.flatpak_button = QtWidgets.QPushButton(f"Installieren als Flatpak: {self.flatpak_id}")
            self.flatpak_button.clicked.connect(self.install_flatpak)
            self.flatpak_button.setStyleSheet("background-color: rgba(0, 60, 0, 150);color: white;")
            layout.addWidget(self.flatpak_button)
        
        # Debian Package Button
        if self.deb_name:
            self.deb_button = QtWidgets.QPushButton(f"Installieren als Systempaket: {self.deb_name}")
            self.deb_button.setStyleSheet("background-color: rgba(0, 60, 0, 150);color: white;")
            self.deb_button.clicked.connect(self.install_deb)
            layout.addWidget(self.deb_button)
            
        # slider gif label
        self.slider_label = QtWidgets.QLabel()
        self.movie = QtGui.QMovie("slide.gif")
        self.slider_label.setMovie(self.movie)
        self.movie.setScaledSize(QtCore.QSize(580,20))
        self.movie.start()
        self.slider_label.setFixedHeight(30)
        self.slider_label.hide()
        layout.addWidget(self.slider_label)
        
    def install_deb(self):
        print(f"Installing Debian package: {self.deb_name}")
        self.deb_button.hide()
        if self.flatpak_id:
            self.flatpak_button.hide()
        self.label_status.show()
        self.start_install_deb()
        
        
    def install_flatpak(self):
        print(f"Installing Flatpak package: {self.flatpak_id}")
        self.flatpak_button.hide()
        if self.deb_name:
            self.deb_button.hide()
        self.label_status.show()
        self.start_install_flatpak()
        
    def start_install_flatpak(self):
        self.install_type="flat"
        self.label_status.setText(f"Status:\nStarte Installation...")
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyRead.connect(self.read_output)
        self.process.finished.connect(self.process_finished)
        self.process.start('flatpak', ['install', self.flatpak_id , '-y'])
        
    def start_install_deb(self):
        self.install_type="deb"
        self.label_status.setText(f"Status:\nStarte Installation...")
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyRead.connect(self.read_output)
        self.process.finished.connect(self.process_finished)
        command = f'apt update && apt install -y {self.deb_name}'
        self.process.start('pkexec', ['sh', '-c', command])

    def read_output(self):
        if self.install_type=="deb":self.slider_label.show()
        if self.process:
            output = self.process.readAll().data().decode()
            output = output.replace('\r\n', '\n').replace('\r', '\n').replace("\n","")
            if output != "":
                #self.label_status.setText(f"Status:\n{output}")
                self.status=output
        if self.blinker:
            self.blinker=False
            self.label_status.setText(f"Status: .\n{self.status}")
        else:
            self.blinker=True
            self.label_status.setText(f"Status: \n{self.status}")

    def process_finished(self, exit_code, exit_status):
        self.slider_label.hide()
        if exit_status == QProcess.NormalExit and exit_code == 0:
            self.label_status.setText(f"Status:\nInstallation erfolgreich beendet!")
            QtWidgets.QMessageBox.information(self, "Erfolg", "Installation erfolgreich beendet!")
        else:
            self.label_status.setText(f"Status:\nInstallation fehlgeschlagen.")
            QtWidgets.QMessageBox.critical(self, "Fehler", "Installation Fehlgeschlagen.")

def main():
    parser = argparse.ArgumentParser(description="Installer App")
    parser.add_argument("-flatpak", type=str, help="Flatpak ID des zu installierenden Programms")
    parser.add_argument("-deb", type=str, help="Name des Debian Pakets")
    parser.add_argument("-pic", type=str, help="Pfad zum Hintergrundbild")
    parser.add_argument("-name", type=str, help="Titel des zu installierenden Programms")
    parser.add_argument("-desc", type=str, help="beschreibung des zu installierenden Programms")

    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    installer_app = InstallerApp(flatpak_id=args.flatpak, deb_name=args.deb, pic_url=args.pic, title_name=args.name, desc=args.desc)
    installer_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
