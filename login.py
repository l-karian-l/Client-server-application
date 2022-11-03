
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from userwindow import UserWindow
from lib import LibWindow
from PyQt5 import uic
import re
import sys

class LoginWindow(QtWidgets.QDialog):
        def __init__(self):
                super(LoginWindow, self).__init__()
                uic.loadUi('login_CD.ui', self)
                self.btn_enter.clicked.connect(self.login_push_btn)

        def open_user_window(self, email, pas):
                self.User = UserWindow()
                self.con_db = self.User.connect_bd(email, pas)
                if self.con_db == False:
                        return self.con_db
                else:
                        self.User.show()

        def open_lib_window(self, email, pas):
                self.Librar = LibWindow()
                self.con_db = self.Librar.connect_bd(email, pas)
                if self.con_db == False:
                        return self.con_db
                else:
                        self.Librar.show()        

        def login_push_btn(self):
                email = self.le_login.text()
                pas = self.le_password.text()

                if email != "":
                        if pas != "":
                                email1 = re.sub("[0-9]","",email)

                                if (email == "admin") and (pas == "00000"):
                                #Окно библиотекаря
                                        self.open_lib_window(email, pas)
                                        if self.con_db == False:
                                                error1 = QMessageBox()
                                                error1.setWindowTitle("Ошибка входа")
                                                error1.setText("Данного аккаунта не существует!")
                                                error1.setIcon(QMessageBox.Icon.Warning)
                                                error1.setStandardButtons(QMessageBox.StandardButton.Ok)
                                                error1.setInformativeText("Попробуйте ввести данные повторно.")
                                                error1.buttonClicked.connect(self.popup)
                                                error1.exec_()
                                        else:
                                                self.hide()  
                                
                                elif (email1 in "reader"):
                                #Окно пользователя
                                        self.open_user_window(email, pas)
                                        if self.con_db == False:
                                                error1 = QMessageBox()
                                                error1.setWindowTitle("Ошибка входа")
                                                error1.setText("Данного аккаунта не существует!")
                                                error1.setIcon(QMessageBox.Icon.Warning)
                                                error1.setStandardButtons(QMessageBox.StandardButton.Ok)
                                                error1.setInformativeText("Попробуйте ввести данные повторно.")
                                                error1.buttonClicked.connect(self.popup)
                                                error1.exec_()
                                        else:
                                                self.hide()
                                                
                                else:
                                        error1 = QMessageBox()
                                        error1.setWindowTitle("Ошибка входа")
                                        error1.setText("Данного аккаунта не существует!")
                                        error1.setIcon(QMessageBox.Icon.Warning)
                                        error1.setStandardButtons(QMessageBox.StandardButton.Ok)
                                        error1.setInformativeText("Попробуйте ввести данные повторно.")
                                        error1.buttonClicked.connect(self.popup)
                                        error1.exec_()
                        else:
                                error2 = QMessageBox()
                                error2.setWindowTitle("Ошибка ввода")
                                error2.setText("Пароль не может быть пустым.")
                                error2.setIcon(QMessageBox.Icon.Warning)
                                error2.setStandardButtons(QMessageBox.StandardButton.Ok)
                                error2.buttonClicked.connect(self.popup)
                                error2.exec_()
                else:
                        error3 = QMessageBox()
                        error3.setWindowTitle("Ошибка ввода")
                        error3.setText("Логин не может быть пустым.")
                        error3.setIcon(QMessageBox.Icon.Warning)
                        error3.setStandardButtons(QMessageBox.StandardButton.Ok)
                        error3.buttonClicked.connect(self.popup)
                        error3.exec_()
                        
        def popup(self, btn):
                if btn.text() == "OK":
                        self.le_password.setText("")

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        Login = LoginWindow()
        Login.show()
        sys.exit(app.exec_())
