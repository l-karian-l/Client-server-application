import login
import userwindow
import sys
from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QMainWindow()
    ui = login.Ui_Login()
    ui.setupUi(Login)
    Login.show()
    return sys.exit(app.exec_())

def main2(email, pas):
    
    app1 = QtWidgets.QApplication(sys.argv)
    UserWindow = QtWidgets.QMainWindow()
    ui = userwindow.Ui_UserWindow()
    ui.setupUi_user(UserWindow)
    UserWindow.show()
    userwindow.connect_bd(email, pas)
    sys.exit(app1.exec_())

main2()


