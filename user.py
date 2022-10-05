from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QTextEdit, QLabel, QPushButton, QListWidget
from PyQt5.Qt import QGridLayout, QHBoxLayout, QMessageBox, Qt
import os
import shutil

class UserWindow(QWidget):
    USER = 0
    SHARED = 1

    def __init__(self):
        super(UserWindow, self).__init__()

        self.setWindowTitle('МБКС ЛР1 | Лазарев Михайлин | Пользователь')

        # +++++++++++++++++++++++++++ Folders +++++++++++++++++++++++++++

        self.gbFolders = QGroupBox('Пути')
        self.layoutFolders = QGridLayout()
        self.leUserFPath = QLineEdit('User')
        self.leSharedFPath = QLineEdit('Shared')

        self.layoutFolders.addWidget(QLabel('Пользовательская папка: '), 0, 0)
        self.layoutFolders.addWidget(self.leUserFPath, 0, 1)
        self.layoutFolders.addWidget(QLabel('Общая папка: '), 1, 0)
        self.layoutFolders.addWidget(self.leSharedFPath, 1, 1)

        self.gbFolders.setLayout(self.layoutFolders)

        # ++++++++++++++=++++++++++++++++++++++++++++++++++++++++++++++++

        # **************************** EDITOR ***************************

        self.gbEditor = QGroupBox('Редактор')
        self.layoutEditor = QGridLayout()
        self.leFileName = QLineEdit()
        self.teEditor = QTextEdit()
        self.layoutEditorSub = QHBoxLayout()
        self.btnSaveFile = QPushButton('Сохранить')
        self.btnSaveFile.clicked.connect(self.btnSaveFileClicked)

        self.layoutEditorSub.setStretch(0, 1)
        self.layoutEditorSub.addWidget(self.btnSaveFile, 1)

        self.layoutEditor.addWidget(QLabel('Имя файла: '), 0, 0)
        self.layoutEditor.addWidget(self.leFileName, 0, 1)
        self.layoutEditor.addWidget(self.teEditor, 1, 0, 1, 2)
        self.layoutEditor.addLayout(self.layoutEditorSub, 2, 0, 1, 2)

        self.gbEditor.setLayout(self.layoutEditor)

        # ***************************************************************

        # @@@@@@@@@@@@@@@@@@@@@@@@@@ TRANSFERER @@@@@@@@@@@@@@@@@@@@@@@@@

        self.gbTransferer = QGroupBox('Перемещение файлов')
        self.layoutTransferer = QGridLayout()

        self.lwUserFolder = QListWidget()
        self.lwSharedFolder = QListWidget()
        self.btnMoveShared = QPushButton('>>')
        self.btnMoveShared.clicked.connect(self.btnMoveSharedClicked)

        self.layoutTransferer.addWidget(QLabel('Пользовательская папка:'), 0, 0)
        self.layoutTransferer.addWidget(self.lwUserFolder, 1, 0, 2, 1)
        self.layoutTransferer.addWidget(QLabel('Общая папка:'), 0, 2)
        self.layoutTransferer.addWidget(self.lwSharedFolder, 1, 2, 2, 1)
        self.layoutTransferer.addWidget(self.btnMoveShared, 1, 1)

        self.gbTransferer.setLayout(self.layoutTransferer)

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.leUserFPath.textChanged.connect(self.updateUserFilesList)
        self.leSharedFPath.textChanged.connect(self.updateSharedFilesList)

        self.updateUserFilesList()
        self.updateSharedFilesList()

        self.layoutMain = QGridLayout()
        self.layoutMain.addWidget(self.gbFolders, 0, 0)
        self.layoutMain.addWidget(self.gbEditor, 1, 0)
        self.layoutMain.addWidget(self.gbTransferer, 2, 0)

        self.setLayout(self.layoutMain)

    def updateUserFilesList(self):
        self.lwUserFolder.clear()

        try:
            listFiles = [file for file in os.listdir(self.leUserFPath.text())
                         if os.path.isfile(os.path.join(self.leUserFPath.text(), file))]

            for file in listFiles:
                self.lwUserFolder.addItem(file)
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

    def copyFile(self, sourcePath, targetPath):
        pass

    def btnSaveFileClicked(self):
        fileName = self.leFileName.text()

        if len(fileName) <= 3:
            QMessageBox.warning(None, 'Некорректное название файла', 'Название файла должно содержать более 3 '
                                                                     'симоволов', QMessageBox.Ok)
            return

        with open(os.path.join(self.leUserFPath.text(), fileName), 'w') as fs:
            fs.write(self.teEditor.toPlainText())

        self.updateUserFilesList()

    def btnMoveSharedClicked(self):
        try:
            if self.lwUserFolder.currentRow() >= 0:
                shutil.copyfile(os.path.join(self.leUserFPath.text(), self.lwUserFolder.currentItem().text()),
                                os.path.join(self.leSharedFPath.text(), self.lwUserFolder.currentItem().text()))

            self.updateSharedFilesList()
        except:
            QMessageBox.warning(None, 'Ошибка', 'Ошибка копирования файла', QMessageBox.Ok)

    def keyPressEvent(self, event):
        try:
            if event.key() == Qt.Key_Delete:
                if self.focusWidget() == self.lwUserFolder:
                    os.remove(os.path.join(self.leUserFPath.text(), self.lwUserFolder.currentItem().text()))
                    self.updateUserFilesList()

                elif self.focusWidget() == self.lwSharedFolder:
                    os.remove(os.path.join(self.leSharedFPath.text(), self.lwSharedFolder.currentItem().text()))
                    self.updateSharedFilesList()
        except:
            QMessageBox.warning(None, 'Ошибка', 'Ошибка удаления файла', QMessageBox.Ok)
