from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from psycopg2.extras import DictCursor
from PyQt5 import uic
import pandas as pd
import Pandas
import re

class OrderWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(OrderWindow, self).__init__()
        uic.loadUi('Orderbook.ui', self)

    #Заполнение строчки "Имя и Фамилия пользователя" 
        self.cur_uorder.execute( f"SELECT reader_name, reader_last_name FROM reader;")
        rec = re.sub(r"[^\w\s]" , "", str(self.cur_uorder.fetchall()))
        self.lab_user_name.setText(rec)

    #Пользователь нажимает кнопку "Назад"
        self.btn_back.clicked.connect(self.back_push_btn)

    #Таблица книги
        rec = pd.read_sql('''SELECT name_book as \"Название\", 
                            author as \"Автор \",
                            genre as \"Жанр \",
                            year_publish as \"Год издания\",
                            publish as \"Издательство\",
                            isbn as \"ISBN\" ,
                            (select author_marks from public.keeping
                            where book_info.id_keeping = public.keeping.id_keeping) as \"Авторский знак\",
                            num_of_pages as \"Кол-во страниц\",
                            books_so_far as \"Доступно\"
                        FROM book_info ''', self.dbu_uorder)
        self.model = Pandas.TableModel(rec)
        self.tab_book.setModel(self.model)

    #Заполнение ComboBox "Название книги" при взятии книги
        self.cur_uorder.execute('SELECT name_book FROM book_info')
        resul1 = self.cur_uorder.fetchall()
        combox1 = [row[0] for row in resul1]
        for row in combox1:
            self.cB_book.addItem(row)

    #Заполнение строки "Читателя" при взятии книги
        self.cur_uorder.execute( f"SELECT reader_last_name FROM reader;")
        rec = re.sub(r"[^\w\s]" , "", str(self.cur_uorder.fetchall()))
        self.le_naz_r.setText(rec)

    #Заполнение ComboBox "Название книги" при продлении книги
        self.cur_uorder.execute('SELECT name_book FROM book_info WHERE num_book_in_lib <> 0')
        resul2 = self.cur_uorder.fetchall()
        combox2 = [row[0] for row in resul2]
        for row in combox2:
            self.cB_book_ext.addItem(row)

    #Заполнение строки "Читателя" при взятии книги
        self.cur_uorder.execute( f"SELECT reader_last_name FROM reader;")
        rec = re.sub(r"[^\w\s]" , "", str(self.cur_uorder.fetchall()))
        self.le_read_ex.setText(rec)

    #Пользователь нажимает кнопку "Книги"
        self.btn_book.clicked.connect(self.book_push_btn)
    
    #Пользователь нажимает кнопку "Абонементы"
        self.btn_order.clicked.connect(self.order_push_btn)

    #Пользователь нажимает кнопку "Взять"
        self.btn_take.clicked.connect(self.take_push_btn)

    #Пользователь нажимает кнопку "Взять"
        self.btn_ext.clicked.connect(self.ext_push_btn)

    #Пользователь нажимает кнопку "Назад"
    def back_push_btn(self):
        self.close()

    #Для подключения к БД
    def connect_user_order(self, dbu):
        self.dbu_uorder = dbu
        self.cur_uorder = self.dbu_uorder.cursor(cursor_factory=DictCursor)

    #Кнопка "Книги"        
    def book_push_btn(self):
        rec = pd.read_sql('''SELECT id_book as \"ID-книги\",
                            name_book as \"Название\", 
                            author as \"Автор \",
                            genre as \"Жанр \",
                            year_publish as \"Год издания\",
                            publish as \"Издательство\",
                            isbn as \"ISBN\" ,
                            (select author_marks from public.keeping
                            where book_info.id_keeping = public.keeping.id_keeping) as \"Авторский знак\",
                            num_of_pages as \"Кол-во страниц\",
                            books_so_far as \"Доступно\"
                        FROM book_info 
                        WHERE  books_so_far != 0''', self.dbu_uorder)
        self.model = Pandas.TableModel(rec)
        self.tab_book.setModel(self.model)

    #Кнопка "Абонементы"        
    def order_push_btn(self):
        rec = pd.read_sql('''SELECT id_order as \"ID бронирования\",
                            id_book as \"ID книги\", 
                            id_reader_ticket as \"ID читателя\", 
                            issure_date as \"Дата выдачи\",
                            return_date as \"Дата возврата\",
                            num_of_copies as \"Количество\",
                            status as \"Статус\"
                            FROM book_order ''', self.dbu_uorder)
        self.model = Pandas.TableModel(rec)
        self.tab_book.setModel(self.model)

    #Кнопка "Взять"        
    def take_push_btn(self):
        nbook = self.te_numb.toPlainText()
        if (self.te_numb.toPlainText() != "" and nbook.isdigit()):
            rec1 = [{"nameb": self.cB_book.currentText(),
                "read": self.le_naz_r.text(),
                "numb": self.te_numb.toPlainText()
                }]
            self.cur_uorder.executemany('CALL add_order(%(nameb)s, %(read)s, %(numb)s)', rec1)
            self.dbu_uorder.commit()

        #Окно, что все выполнилось успешно
            inf = QMessageBox()
            inf.setWindowTitle("Информация")
            inf.setText("Книга забронирована!")
            inf.setIcon(QMessageBox.Icon.Information)
            inf.setStandardButtons(QMessageBox.StandardButton.Ok)
            inf.exec_()

        #Отображение таблицы "Заказ книги" после изменений
            rec2 = pd.read_sql('''SELECT id_order as \"ID бронирования\",
                                (select name_book from book_info
                                where book_info.id_book = book_order.id_book) as \"ID книги\", 
                                (select reader_last_name from reader
                                where reader.id_reader_ticket = book_order.id_reader_ticket) as \"ID читателя\", 
                                issure_date as \"Дата выдачи\",
                                return_date as \"Дата возврата\",
                                num_of_copies as \"Количество\",
                                status as \"Статус\"
                                FROM book_order ''', self.dbu_uorder)
            self.model = Pandas.TableModel(rec2)
            self.tab_book.setModel(self.model)

            self.te_numb.setText("")

        elif (self.te_numb.toPlainText() == ""):
            error2 = QMessageBox()
            error2.setWindowTitle("Ошибка ввода")
            error2.setText("Количество книг не может быть пустым.")
            error2.setIcon(QMessageBox.Icon.Warning)
            error2.setStandardButtons(QMessageBox.StandardButton.Ok)
            error2.exec_()
        else:
            error3 = QMessageBox()
            error3.setWindowTitle("Ошибка ввода")
            error3.setText("Вы ввели не число.")
            error3.setIcon(QMessageBox.Icon.Warning)
            error3.setStandardButtons(QMessageBox.StandardButton.Ok)
            error3.exec_()

    #Кнопка "Продлить"
    def ext_push_btn(self):
        rec1 = [{"nameb": self.cB_book_ext.currentText(),
                "read": self.le_read_ex.text()}]
        self.cur_uorder.executemany('CALL extend_the_book(%(nameb)s, %(read)s)', rec1)
        self.dbu_uorder.commit()

        #Окно, что все выполнилось успешно
        inf = QMessageBox()
        inf.setWindowTitle("Информация")
        inf.setText("Книга продлена.")
        inf.setIcon(QMessageBox.Icon.Information)
        inf.setStandardButtons(QMessageBox.StandardButton.Ok)
        inf.exec_()

        #Отображение таблицы "Заказ книги" после изменений
        rec2 = pd.read_sql('''SELECT id_order as \"ID бронирования\",
                                (select name_book from book_info
                                where book_info.id_book = book_order.id_book) as \"ID книги\", 
                                (select reader_last_name from reader
                                where reader.id_reader_ticket = book_order.id_reader_ticket) as \"ID читателя\", 
                                issure_date as \"Дата выдачи\",
                                return_date as \"Дата возврата\",
                                num_of_copies as \"Количество\",
                                status as \"Статус\"
                                FROM book_order ''', self.dbu_uorder)
        self.model = Pandas.TableModel(rec2)
        self.tab_book.setModel(self.model)

