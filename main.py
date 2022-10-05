import sys
from PyQt5.Qt import QApplication

from user import UserWindow
from intruder import IntruderWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    userwindow = UserWindow()
    intruderwindow = IntruderWindow()

    userwindow.show()
    intruderwindow.show()

    sys.exit(app.exec_())