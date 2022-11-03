from PyQt5 import QtCore, QtGui, QtWidgets
from psycopg2.extras import DictCursor
from PyQt5 import uic
import re

class DataWindow(QtWidgets.QMainWindow):
        def __init__(self):
                super(DataWindow, self).__init__()
                uic.loadUi('Udata.ui', self)

        #Заполнение строчки "Имя и Фамилия пользователя" 
                self.cur_udata.execute( f"SELECT reader_name, reader_last_name FROM reader;")
                rec = re.sub(r"[^\w\s]" , "", str(self.cur_udata.fetchall()))
                self.label_user_name.setText(rec)

        #Пользователь нажимает кнопку "Назад"
                self.btn_back.clicked.connect(self.back_push_btn)

        #Заполнение строчки "Имя пользователя" 
                self.cur_udata.execute( f"SELECT reader_name FROM reader;")
                rec = re.sub(r"[^\w\s]" , "", str(self.cur_udata.fetchall()))
                self.label__udata_name.setText(rec)

        #Заполнение строчки "Фамилия пользователя"
                self.cur_udata.execute( f"SELECT reader_last_name FROM reader;")
                rec = re.sub(r"[^\w\s]" , "", str(self.cur_udata.fetchall()))
                self.label__udata_lname.setText(rec)

        #Заполнение строчки "Адрес пользователя"
                self.cur_udata.execute( f"SELECT reader_address FROM reader;")
                rec = re.sub(r"[^\w\s]" , "", str(self.cur_udata.fetchall()))
                self.label__udata_address.setText(rec)

        #Заполнение строчки "Телефон пользователя"
                self.cur_udata.execute( f"SELECT reader_phone FROM reader;")
                rec = re.sub(r"[^\w\s]" , "", str(self.cur_udata.fetchall()))
                self.label__udata_phone.setText(rec)

        #Заполнение строчки "День Рождение пользователя" 
                self.cur_udata.execute( f"SELECT birth_date FROM reader;")
                rec = re.sub(r"\D","-", (re.sub(r"\D(?=\d{3})|\D{3}", "", str(self.cur_udata.fetchall()))))
                self.label__udata_bth.setText(str(rec))

        #Заполнение строчки "Дата Регистрации пользователя" 
                self.cur_udata.execute( f"SELECT reader_registration_date FROM reader;")
                rec = re.sub(r"\D","-", (re.sub(r"\D(?=\d{3})|\D{3}", "", str(self.cur_udata.fetchall()))))
                self.label__udata_registr.setText(str(rec)) 

        #Пользователь нажимает кнопку "Назад"
        def back_push_btn(self):
                self.close()
        
        #Для подключения к БД
        def connect_user_data(self, dbu):
                self.dbu_udata = dbu
                self.cur_udata = self.dbu_udata.cursor(cursor_factory=DictCursor)
