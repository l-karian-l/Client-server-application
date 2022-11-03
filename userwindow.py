from PyQt5 import QtCore, QtGui, QtWidgets
from psycopg2.extras import DictCursor
from user_data import DataWindow
from orderbook import OrderWindow
from PyQt5 import uic
import re
import pandas as pd
import Pandas
import sys
import connect

class UserWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(UserWindow, self).__init__()
        uic.loadUi('Userwindow.ui', self)
        
        #Пользователь нажимает кнопку "Мои данные"
        self.btn_user_data.clicked.connect(self.open_user_data)

        #При нажатии на кнопку "Книги"
        self.btn_book.clicked.connect(self.show_book)

        #При нажатии на кнопку "Издательства"
        self.btn_publish.clicked.connect(self.show_publish)

        #При нажатии на кнопку "Выход"
        self.btn_user_exit.clicked.connect(self.user_exit)

        #При нажатии на кнопку "Взять книгу"
        self.btn_order.clicked.connect(self.open_user_order)

    #Отображение окна "Взять книгу"
    def open_user_order(self):
            OrderWindow.connect_user_order(OrderWindow, self.dbu)
            self.Data = OrderWindow()
            self.Data.show()

    #Отображение окна "Мои данные"
    def open_user_data(self):
            DataWindow.connect_user_data(DataWindow, self.dbu)
            self.Data = DataWindow()
            self.Data.show()

    #Отображение в таблице списка книг
    def show_book(self):
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
                        FROM book_info ''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_book_or_publish.setModel(self.model)

        #Таблица для абонементов
        rec = pd.read_sql('''SELECT id_order as \"ID бронирования\",
                            (select name_book from book_info
                            where book_info.id_book = book_order.id_book) as \"ID книги\", 
                            (select reader_last_name from reader
                            where reader.id_reader_ticket = book_order.id_reader_ticket) as \"ID читателя\", 
                            issure_date as \"Дата выдачи\",
                            return_date as \"Дата возврата\",
                            num_of_copies as \"Количество\",
                            status as \"Статус\"
                            FROM book_order''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_subscr.setModel(self.model)

    #Отображение в таблице списка издательств
    def show_publish(self):
        rec = pd.read_sql('''SELECT id_publish as \"ID-Издательства\", 
                            name_publish  as \"Издательство\",
                            official_website as \"Сайт\", 
                            address as \"Название\", 
                            what_is_emitting as \"Что выпускает\",
                            status as \"Статус\"
                         FROM publisher ''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_book_or_publish.setModel(self.model)

    #Для подключения к БД
    def connect_bd(self, email, pas):
        self.dbu = connect.connect_db(email, pas)
        if self.dbu == False:
            return self.dbu
        else:
            self.cur = self.dbu.cursor(cursor_factory=DictCursor)

    #Таблица для абонементов
        rec = pd.read_sql('''SELECT id_order as \"ID бронирования\",
                            (select name_book from book_info
                            where book_info.id_book = book_order.id_book) as \"ID книги\", 
                            (select reader_last_name from reader
                            where reader.id_reader_ticket = book_order.id_reader_ticket) as \"ID читателя\", 
                            issure_date as \"Дата выдачи\",
                            return_date as \"Дата возврата\",
                            num_of_copies as \"Количество\",
                            status as \"Статус\"
                            FROM book_order''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_subscr.setModel(self.model)

    #Заполнение строчки "Имя и Фамилия пользователя" 
        self.cur.execute( f"SELECT reader_name, reader_last_name FROM reader;")
        rec = re.sub(r"[^\w\s]" , "", str(self.cur.fetchall()))
        self.lab_user_name.setText(rec)

    #Для выхода из аккаунта
    def user_exit(self):
        from login import LoginWindow
        self.Login = LoginWindow()
        self.Login.show()
        self.hide()
