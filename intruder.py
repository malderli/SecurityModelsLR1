from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QTextEdit, QLabel, QPushButton, QListWidget
from PyQt5.Qt import QGridLayout, QHBoxLayout, QMessageBox, QTimer
import os
import shutil


class IntruderWindow(QWidget):
    def __init__(self):
        super(IntruderWindow, self).__init__()

        self.interceptionTimer = QTimer()
        self.interceptionTimer.timeout.connect(self.intercept)

        self.setWindowTitle('МБКС ЛР1 | Лазарев Михайлин | Злоумышленник')

        # +++++++++++++++++++++++++++ Folders +++++++++++++++++++++++++++

        self.gbFolders = QGroupBox('Пути')
        self.layoutFolders = QGridLayout()
        self.leIntruderFPath = QLineEdit('Intruder')
        self.leSharedFPath = QLineEdit('Shared')

        self.layoutFolders.addWidget(QLabel('Папка нарушителя: '), 0, 0)
        self.layoutFolders.addWidget(self.leIntruderFPath, 0, 1)
        self.layoutFolders.addWidget(QLabel('Общая папка: '), 1, 0)
        self.layoutFolders.addWidget(self.leSharedFPath, 1, 1)

        self.gbFolders.setLayout(self.layoutFolders)

        # ++++++++++++++=++++++++++++++++++++++++++++++++++++++++++++++++

        # **************************** Viewer ***************************

        self.gbViewer = QGroupBox('Просмотр перехваченных файлов')
        self.layoutViewer = QGridLayout()
        self.leFileName = QLineEdit()
        self.teViewer = QTextEdit()
        self.btnOpenFile = QPushButton('Открыть')
        self.btnOpenFile.clicked.connect(self.btnOpenClicked)

        self.teViewer.setReadOnly(True)

        self.layoutViewer.addWidget(QLabel('Имя файла: '), 0, 0)
        self.layoutViewer.addWidget(self.leFileName, 0, 1)
        self.layoutViewer.addWidget(self.btnOpenFile, 0, 2)
        self.layoutViewer.addWidget(self.teViewer, 1, 0, 1, 3)

        self.gbViewer.setLayout(self.layoutViewer)

        # ***************************************************************

        # @@@@@@@@@@@@@@@@@@@@@@@@@ Interceptor @@@@@@@@@@@@@@@@@@@@@@@@@

        self.gbInterceptor = QGroupBox('Перехват файлов')
        self.layoutInterceptor = QGridLayout()

        self.lwIntruderFolder = QListWidget()
        self.lwSharedFolder = QListWidget()
        self.btnStartInterception = QPushButton('Начать перехват')
        self.btnStartInterception.setCheckable(True)
        self.btnStartInterception.clicked.connect(self.btnStartInterceptionClicked)

        self.layoutInterceptor.addWidget(QLabel('Общая папка:'), 0, 0)
        self.layoutInterceptor.addWidget(self.lwSharedFolder, 1, 0)
        self.layoutInterceptor.addWidget(QLabel('Перехваченные файлы:'), 0, 1)
        self.layoutInterceptor.addWidget(self.lwIntruderFolder, 1, 1)
        self.layoutInterceptor.addWidget(self.btnStartInterception, 2, 0, 1, 2)

        self.gbInterceptor.setLayout(self.layoutInterceptor)

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.updateIntruderFilesList()

        self.layoutMain = QGridLayout()
        self.layoutMain.addWidget(self.gbFolders, 0, 0)
        self.layoutMain.addWidget(self.gbInterceptor, 1, 0)
        self.layoutMain.addWidget(self.gbViewer, 2, 0)

        self.setLayout(self.layoutMain)

    def intercept(self):
        self.lwSharedFolder.clear()
        self.lwIntruderFolder.clear()

        try:
            listSharedFiles = [file for file in os.listdir(self.leSharedFPath.text())
                               if os.path.isfile(os.path.join(self.leSharedFPath.text(), file))]

            listInterceptedFiles = [file for file in os.listdir(self.leIntruderFPath.text())
                                    if os.path.isfile(os.path.join(self.leIntruderFPath.text(), file))]

            for file in listSharedFiles:
                self.lwSharedFolder.addItem(file)

            for file in listInterceptedFiles:
                self.lwIntruderFolder.addItem(file)

            for file in listSharedFiles:
                if not file in listInterceptedFiles:
                    shutil.copyfile(os.path.join(self.leSharedFPath.text(), file),
                                    os.path.join(self.leIntruderFPath.text(), file))
        except:
            QMessageBox.warning(None, 'Ошибка', 'Ошибка перехвата', QMessageBox.Ok)
            self.interceptionTimer.stop()
            self.lwSharedFolder.clear()
            self.lwIntruderFolder.clear()
            self.btnStartInterception.setChecked(False)
            self.btnStartInterception.setText('Начать перехват')
            self.leIntruderFPath.setEnabled(True)
            self.leSharedFPath.setEnabled(True)

    def btnStartInterceptionClicked(self):
        if self.btnStartInterception.isChecked():
            self.btnStartInterception.setText('Прекратить перехват')
            self.interceptionTimer.start(50)
            self.leIntruderFPath.setEnabled(False)
            self.leSharedFPath.setEnabled(False)
        else:
            self.btnStartInterception.setText('Начать перехват')
            self.interceptionTimer.stop()
            self.lwSharedFolder.clear()
            self.leIntruderFPath.setEnabled(True)
            self.leSharedFPath.setEnabled(True)

    def btnOpenClicked(self):
        try:
            with open(os.path.join(self.leIntruderFPath.text(), self.leFileName.text())) as fs:
                text = fs.read()

            self.teViewer.setText(text)
        except:
            QMessageBox.warning(None, 'Ошибка', 'Ошибка открытия файла', QMessageBox.Ok)

    def updateIntruderFilesList(self):
        self.lwIntruderFolder.clear()

        try:
            listFiles = [file for file in os.listdir(self.leIntruderFPath.text())
                         if os.path.isfile(os.path.join(self.leIntruderFPath.text(), file))]

            for file in listFiles:
                self.lwIntruderFolder.addItem(file)
        except:
            pass

    def updateSharedFilesList(self):
        self.lwSharedFolder.clear()

        try:
            listFiles = [file for file in os.listdir(self.leSharedFPath.text())
                         if os.path.isfile(os.path.join(self.leSharedFPath.text(), file))]

            for file in listFiles:
                self.lwSharedFolder.addItem(file)
        except:
            pass
