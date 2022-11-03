from PyQt5 import QtCore, QtGui, QtWidgets
from psycopg2.extras import DictCursor
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
import pandas as pd
import Pandas

class DelWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(DelWindow, self).__init__()
        uic.loadUi('Delwin.ui', self)

        #Заполнение строчки пользователя 
        self.lab_nln.setText("Библиотекарь")

        #Пользователь нажимает кнопку "Назад"
        self.btn_back.clicked.connect(self.back_push_btn)

        #Заполнение ComboBox "Авторский знак" в окне "Хранение"
        self.cur_del.execute('SELECT author_marks FROM keeping')
        resul1 = self.cur_del.fetchall()
        combox1 = [row[0] for row in resul1]
        for row in combox1:
            self.cB_mark_k.addItem(row)

        #Заполнение ComboBox "Название" в окне "Издательства"
        self.cur_del.execute('SELECT name_publish FROM publisher')
        resul2 = self.cur_del.fetchall()
        combox2 = [row[0] for row in resul2]
        for row in combox2:
            self.cB_name_p.addItem(row)

        #Заполнение ComboBox "Название" в окне "Книги"
        self.cur_del.execute('SELECT name_book FROM book_info')
        resul3 = self.cur_del.fetchall()
        combox3 = [row[0] for row in resul3]
        for row in combox3:
            self.cB_name_b.addItem(row)

        #Заполнение ComboBox "Название книги" в окне "Заказ книги"
        self.cur_del.execute('SELECT name_book FROM book_info')
        resul4 = self.cur_del.fetchall()
        combox4 = [row[0] for row in resul4]
        for row in combox4:
            self.cB_nameb_o.addItem(row)

        #Заполнение ComboBox "Читатель" в окне "Заказ книги"
        self.cur_del.execute('SELECT reader_last_name FROM reader')
        resul5 = self.cur_del.fetchall()
        combox5 = [row[0] for row in resul5]
        for row in combox5:
            self.cB_read_o.addItem(row)

        #Заполнение ComboBox "Фамилия читателя" в окне "Читатели"
        self.cur_del.execute('SELECT reader_last_name FROM reader')
        resul6 = self.cur_del.fetchall()
        combox6 = [row[0] for row in resul6]
        for row in combox6:
            self.cB_lname_r.addItem(row)

    #Окно "Издательства"
        #Отображение таблицы "Издательства" до изменений
        rec2 = pd.read_sql('''SELECT id_publish as \"ID-Издательства\", 
                            name_publish  as \"Издательство\",
                            official_website as \"Сайт\", 
                            address as \"Адрес\", 
                            what_is_emitting as \"Что выпускает\",
                            status as \"Статус\"
                         FROM publisher ''', self.dbu_del)
        self.model = Pandas.TableModel(rec2)
        self.tab_publish.setModel(self.model)

        #Пользователь нажимает кнопку "Добавить"
        self.btn_del_p.clicked.connect(self.del_publish)

    #Окно "Хранение"
        #Отображение таблицы "Хранение" до изменений
        rec2 = pd.read_sql('''SELECT id_keeping as \"ID-Хранения\",
                            author_marks as \"Авторский знак\",
                            total_book as \"Количество книг\", 
                            num_shelf_book as \"Стеллажная группа\", 
                            library as \"Какая библиотека\"
                            FROM keeping ''', self.dbu_del)
        self.model = Pandas.TableModel(rec2)
        self.tab_keep.setModel(self.model)

        #Пользователь нажимает кнопку "Добавить"
        self.btn_del_k.clicked.connect(self.del_keeping)

    #Окно "Книги"
        #Отображение таблицы "Книги" до изменений
        rec2 = pd.read_sql('''SELECT id_book as \"ID-книги\",
                            name_book as \"Название\", 
                            author as \"Автор \",
                            genre as \"Жанр \",
                            year_publish as \"Год издания\",
                            publish as \"Издательство\",
                            isbn as \"ISBN\" ,
                            (select author_marks from public.keeping
                            where book_info.id_keeping = public.keeping.id_keeping) as \"Авторский знак\",
                            num_of_pages as \"Кол-во страниц\",
                            num_book_in_lib as \"В библиотеке\",
                            books_so_far as \"На данный момент\"
                        FROM book_info ''', self.dbu_del)
        self.model = Pandas.TableModel(rec2)
        self.tab_book.setModel(self.model)

        #Пользователь нажимает кнопку "Удалить"
        self.btn_del_b.clicked.connect(self.del_book)

    #Окно "Заказ книги"
        #Отображение таблицы "Заказ книги" до изменений
        rec2 = pd.read_sql('''SELECT id_order as \"ID бронирования\",
                            (select name_book from book_info
                            where book_info.id_book = book_order.id_book) as \"ID книги\", 
                            (select reader_last_name from reader
                            where reader.id_reader_ticket = book_order.id_reader_ticket) as \"ID читателя\", 
                            issure_date as \"Дата выдачи\",
                            return_date as \"Дата возврата\",
                            num_of_copies as \"Количество\",
                            status as \"Статус\"
                            FROM book_order ''', self.dbu_del)
        self.model = Pandas.TableModel(rec2)
        self.tab_order.setModel(self.model)

        #Пользователь нажимает кнопку "Удалить"
        self.btn_del_o.clicked.connect(self.del_order)

    #Окно "Читатели"
        #Отображение таблицы "Читатели" до изменений
        rec2 = pd.read_sql('''SELECT  id_reader_ticket as \"ID читателя\", 
                            reader_name as \"Имя\",
                            reader_last_name as \"Фамилия\",
                            reader_address as \"Адрес\",
                            reader_phone as \"Телефон\",
                            birth_date as \"День Рождения\",
                            reader_registration_date as \"Дата регистрации\"
                            FROM reader''', self.dbu_del)
        self.model = Pandas.TableModel(rec2)
        self.tab_read.setModel(self.model)

        #Пользователь нажимает кнопку "Добавить"
        self.btn_del_r.clicked.connect(self.del_reader)
        
    #Пользователь нажимает кнопку "Назад"
    def back_push_btn(self):
        self.close()

    #Для подключения к БД
    def connect_user_order(self, dbu):
        self.dbu_del = dbu
        self.cur_del = self.dbu_del.cursor(cursor_factory=DictCursor)

#Окно "Издательства"
    def del_publish(self):
            rec1 = [{"name": self.cB_name_p.currentText()}]
            self.cur_del.executemany('CALL del_publish (%(name)s)', rec1)
            self.dbu_del.commit()

    #Окно, что все выполнилось успешно
            inf = QMessageBox()
            inf.setWindowTitle("Информация")
            inf.setText("Данные успешно удалены.")
            inf.setIcon(QMessageBox.Icon.Information)
            inf.setStandardButtons(QMessageBox.StandardButton.Ok)
            inf.exec_()

    #Отображение таблицы "Издательства" после изменений
            rec2 = pd.read_sql('''SELECT id_publish as \"ID-Издательства\", 
                                    name_publish  as \"Издательство\",
                                    official_website as \"Сайт\", 
                                    address as \"Адрес\", 
                                    what_is_emitting as \"Что выпускает\",
                                    status as \"Статус\"
                                FROM publisher ''', self.dbu_del)
            self.model = Pandas.TableModel(rec2)
            self.tab_publish.setModel(self.model)

#Окно "Хранение"
    def del_keeping(self):
        rec1 = [{"mark": self.cB_mark_k.currentText()}]
        self.cur_del.executemany('CALL del_keeping(%(mark)s)', rec1)
        self.dbu_del.commit()

    #Окно, что все выполнилось успешно
        inf = QMessageBox()
        inf.setWindowTitle("Информация")
        inf.setText("Данные успешно удалены.")
        inf.setIcon(QMessageBox.Icon.Information)
        inf.setStandardButtons(QMessageBox.StandardButton.Ok)
        inf.exec_()

    #Отображение таблицы "Хранение" после изменений
        rec2 = pd.read_sql('''SELECT id_keeping as \"ID-Хранения\",
                            author_marks as \"Авторский знак\",
                            total_book as \"Количество книг\", 
                            num_shelf_book as \"Стеллажная группа\", 
                            library as \"Какая библиотека\"
                            FROM keeping ''', self.dbu_del)
        self.model = Pandas.TableModel(rec2)
        self.tab_keep.setModel(self.model)

#Окно "Книги"
    def del_book(self):
        if (self.te_isbn_b.toPlainText() != ""):
            rec1 = [{"name": self.cB_name_b.currentText(),
                    "isbn": self.te_isbn_b.toPlainText()}]
            self.cur_del.executemany('CALL del_book(%(name)s, %(isbn)s)', rec1)
            self.dbu_del.commit()

    #Окно, что все выполнилось успешно
            inf = QMessageBox()
            inf.setWindowTitle("Информация")
            inf.setText("Данные успешно удалены.")
            inf.setIcon(QMessageBox.Icon.Information)
            inf.setStandardButtons(QMessageBox.StandardButton.Ok)
            inf.exec_()

    #Отображение таблицы "Книги" после изменений
            rec2 = pd.read_sql('''SELECT id_book as \"ID-книги\",
                            name_book as \"Название\", 
                            author as \"Автор \",
                            genre as \"Жанр \",
                            year_publish as \"Год издания\",
                            publish as \"Издательство\",
                            isbn as \"ISBN\" ,
                            (select author_marks from public.keeping
                            where book_info.id_keeping = public.keeping.id_keeping) as \"Авторский знак\",
                            num_of_pages as \"Кол-во страниц\",
                            num_book_in_lib as \"В библиотеке\"
                        FROM book_info ''', self.dbu_del)
            self.model = Pandas.TableModel(rec2)
            self.tab_book.setModel(self.model)

            self.te_isbn_b.setText("")
        else:
    #Окно ошибки
            error2 = QMessageBox()
            error2.setWindowTitle("Ошибка ввода")
            error2.setText("Код ISBN не может быть пустым.")
            error2.setIcon(QMessageBox.Icon.Warning)
            error2.setStandardButtons(QMessageBox.StandardButton.Ok)
            error2.exec_()

#Окно "Заказ книги"
    def del_order(self):
        rec1 = [{"nameb": self.cB_nameb_o.currentText(),
                "read": self.cB_read_o.currentText()}]
        self.cur_del.executemany('CALL del_order(%(nameb)s, %(read)s)', rec1)
        self.dbu_del.commit()

    #Окно, что все выполнилось успешно
        inf = QMessageBox()
        inf.setWindowTitle("Информация")
        inf.setText("Данные успешно удалены.")
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
                            FROM book_order ''', self.dbu_del)
        self.model = Pandas.TableModel(rec2)
        self.tab_order.setModel(self.model)

#Окно "Читатели"
    def del_reader(self):
        rec1 = [{"lname": self.cB_lname_r.currentText()}]
        self.cur_del.executemany('CALL del_reader(%(lname)s)', rec1)
        self.dbu_del.commit()

    #Окно, что все выполнилось успешно
        inf = QMessageBox()
        inf.setWindowTitle("Информация")
        inf.setText("Данные успешно удалены.")
        inf.setIcon(QMessageBox.Icon.Information)
        inf.setStandardButtons(QMessageBox.StandardButton.Ok)
        inf.exec_()

    #Отображение таблицы "Читатели" после изменений
        rec2 = pd.read_sql('''SELECT  id_reader_ticket as \"ID читателя\", 
                            reader_name as \"Имя\",
                            reader_last_name as \"Фамилия\",
                            reader_address as \"Адрес\",
                            reader_phone as \"Телефон\",
                            birth_date as \"День Рождения\",
                            reader_registration_date as \"Дата регистрации\"
                            FROM reader''', self.dbu_del)
        self.model = Pandas.TableModel(rec2)
        self.tab_read.setModel(self.model)   

    

    