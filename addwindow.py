from PyQt5 import QtCore, QtGui, QtWidgets
from psycopg2.extras import DictCursor
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
import pandas as pd
import Pandas

class AddWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AddWindow, self).__init__()
        uic.loadUi('Addwin.ui', self)

        #Заполнение строчки пользователя 
        self.lab_nln.setText("Библиотекарь")

        #Пользователь нажимает кнопку "Назад"
        self.btn_back.clicked.connect(self.back_push_btn)

        #Заполнение ComboBox "Издательство" в окне "Книги"
        self.cur_add.execute('SELECT name_publish FROM publisher')
        resul1 = self.cur_add.fetchall()
        combox1 = [row[0] for row in resul1]
        for row in combox1:
            self.cB_publish_b.addItem(row)

        #Заполнение ComboBox "Авторский знак" в окне "Книги"
        self.cur_add.execute('SELECT author_marks FROM keeping')
        resul2 = self.cur_add.fetchall()
        combox2 = [row[0] for row in resul2]
        for row in combox2:
            self.cB_mark_b.addItem(row)      

        #Заполнение ComboBox "Название книги" в окне "Заказ книги"
        self.cur_add.execute('SELECT name_book FROM book_info')
        resul3 = self.cur_add.fetchall()
        combox3 = [row[0] for row in resul3]
        for row in combox3:
            self.cB_nameb_o.addItem(row)

        #Заполнение ComboBox "Читатель" в окне "Заказ книги"
        self.cur_add.execute('SELECT reader_last_name FROM reader')
        resul4 = self.cur_add.fetchall()
        combox4 = [row[0] for row in resul4]
        for row in combox4:
            self.cB_read_o.addItem(row)

    #Окно "Издательства"
        #Отображение таблицы "Издательства" до изменений
        rec2 = pd.read_sql('''SELECT id_publish as \"ID-Издательства\", 
                            name_publish  as \"Издательство\",
                            official_website as \"Сайт\", 
                            address as \"Адрес\", 
                            what_is_emitting as \"Что выпускает\",
                            status as \"Статус\"
                         FROM publisher ''', self.dbu_add)
        self.model = Pandas.TableModel(rec2)
        self.tab_publ.setModel(self.model)

        #Пользователь нажимает кнопку "Добавить"
        self.btn_add_p.clicked.connect(self.add_publish)

    #Окно "Хранение"
        #Отображение таблицы "Хранение" до изменений
        rec2 = pd.read_sql('''SELECT id_keeping as \"ID-Хранения\",
                            author_marks as \"Авторский знак\",
                            total_book as \"Количество книг\", 
                            num_shelf_book as \"Стеллажная группа\", 
                            library as \"Какая библиотека\"
                            FROM keeping ''', self.dbu_add)
        self.model = Pandas.TableModel(rec2)
        self.tab_keep.setModel(self.model)

        #Пользователь нажимает кнопку "Добавить"
        self.btn_add_k.clicked.connect(self.add_keeping)
    
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
                            num_book_in_lib as \"В библиотеке\"
                        FROM book_info ''', self.dbu_add)
        self.model = Pandas.TableModel(rec2)
        self.tab_book.setModel(self.model)

        #Пользователь нажимает кнопку "Добавить"
        self.btn_add_b.clicked.connect(self.add_book)

    #Окно "Читатели"
        #Отображение таблицы "Читатели" до изменений
        rec2 = pd.read_sql('''SELECT  id_reader_ticket as \"ID читателя\", 
                            reader_name as \"Имя\",
                            reader_last_name as \"Фамилия\",
                            reader_address as \"Адрес\",
                            reader_phone as \"Телефон\",
                            birth_date as \"День Рождения\",
                            reader_registration_date as \"Дата регистрации\"
                            FROM reader''', self.dbu_add)
        self.model = Pandas.TableModel(rec2)
        self.tab_reader.setModel(self.model)

        #Пользователь нажимает кнопку "Добавить"
        self.btn_add_r.clicked.connect(self.add_reader)

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
                            FROM book_order ''', self.dbu_add)
        self.model = Pandas.TableModel(rec2)
        self.tab_order.setModel(self.model)

        #Пользователь нажимает кнопку "Добавить"
        self.btn_add_o.clicked.connect(self.add_order)

#Для подключения к БД
    def connect_user_add(self, dbu):
        self.dbu_add = dbu
        self.cur_add = self.dbu_add.cursor(cursor_factory=DictCursor)

#Пользователь нажимает кнопку "Назад"
    def back_push_btn(self):
        self.close()

#Окно "Издательства"
    def add_publish(self):
        if (self.te_p_name.toPlainText() != ""):
            rec1 = [{"name" : self.te_p_name.toPlainText(),
                    "site": self.te_p_site.toPlainText(),
                    "adr": self.te_addres_p.toPlainText(),
                    "wpub": self.te_wpub_p.toPlainText(),
                    "stat": self.cB_stat_p.currentText()
                    }]
            self.cur_add.executemany('CALL add_publish (%(name)s, %(site)s, %(adr)s, %(wpub)s, %(stat)s)', rec1)
            self.dbu_add.commit()

    #Окно, что все выполнилось успешно
            inf = QMessageBox()
            inf.setWindowTitle("Информация")
            inf.setText("Данные успешно добавлены.")
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
                                FROM publisher ''', self.dbu_add)
            self.model = Pandas.TableModel(rec2)
            self.tab_publ.setModel(self.model)

            self.te_p_name.setText("")
            self.te_p_site.setText("")
            self.te_addres_p.setText("")
            self.te_wpub_p.setText("")
        else:
    #Окно ошибки
            error2 = QMessageBox()
            error2.setWindowTitle("Ошибка ввода")
            error2.setText("Название издания не может быть пустым.")
            error2.setIcon(QMessageBox.Icon.Warning)
            error2.setStandardButtons(QMessageBox.StandardButton.Ok)
            error2.exec_()

#Окно "Хранение"
    def add_keeping(self):
        if (self.te_mark_k.toPlainText() != ""):
            rec1 = [{"mark" : self.te_mark_k.toPlainText(),
                    "sgr": self.te_sgr_k.toPlainText(),
                    "lib": self.lab_lib_k.text()
                    }]
            self.cur_add.executemany('CALL add_keeping(%(mark)s, %(sgr)s, %(lib)s)', rec1)
            self.dbu_add.commit()

    #Окно, что все выполнилось успешно
            inf = QMessageBox()
            inf.setWindowTitle("Информация")
            inf.setText("Данные успешно добавлены.")
            inf.setIcon(QMessageBox.Icon.Information)
            inf.setStandardButtons(QMessageBox.StandardButton.Ok)
            inf.exec_()

    #Отображение таблицы "Хранение" после изменений
            rec2 = pd.read_sql('''SELECT id_keeping as \"ID-Хранения\",
                            author_marks as \"Авторский знак\",
                            total_book as \"Количество книг\", 
                            num_shelf_book as \"Стеллажная группа\", 
                            library as \"Какая библиотека\"
                            FROM keeping ''', self.dbu_add)
            self.model = Pandas.TableModel(rec2)
            self.tab_keep.setModel(self.model)

            self.te_p_name.setText("")
            self.te_p_site.setText("")
            self.te_addres_p.setText("")
            self.te_wpub_p.setText("")
        else:
    #Окно ошибки
            error2 = QMessageBox()
            error2.setWindowTitle("Ошибка ввода")
            error2.setText("Название издания не может быть пустым.")
            error2.setIcon(QMessageBox.Icon.Warning)
            error2.setStandardButtons(QMessageBox.StandardButton.Ok)
            error2.exec_()

#Окно "Книги"
    def add_book(self):
        if (self.te_name_b.toPlainText() != ""):
            rec1 = [{"name" : self.te_name_b.toPlainText(),
                    "auth": self.te_author_b.toPlainText(),
                    "genr": self.te_genre_b.toPlainText(),
                    "year": self.te_yaer_b.toPlainText(),
                    "publ": self.cB_publish_b.currentText(),
                    "isbn": self.te_isbn_b.toPlainText(),
                    "mark": self.cB_mark_b.currentText(),
                    "numpg": self.te_numpg_b.toPlainText(),
                    "numb": self.te_numb_b.toPlainText()
                    }]
            self.cur_add.executemany('CALL add_book(%(name)s, %(auth)s, %(genr)s, %(year)s, %(publ)s, %(isbn)s, %(mark)s, %(numpg)s, %(numb)s)', rec1)
            self.dbu_add.commit()

    #Окно, что все выполнилось успешно
            inf = QMessageBox()
            inf.setWindowTitle("Информация")
            inf.setText("Данные успешно добавлены.")
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
                        FROM book_info ''', self.dbu_add)
            self.model = Pandas.TableModel(rec2)
            self.tab_book.setModel(self.model)

            self.te_name_b.setText(""),
            self.te_author_b.setText(""),
            self.te_genre_b.setText(""),
            self.te_yaer_b.setText(""),
            self.te_isbn_b.setText(""),
            self.te_numpg_b.setText(""),
            self.te_numb_b.setText("")
        else:
    #Окно ошибки
            error2 = QMessageBox()
            error2.setWindowTitle("Ошибка ввода")
            error2.setText("Название издания не может быть пустым.")
            error2.setIcon(QMessageBox.Icon.Warning)
            error2.setStandardButtons(QMessageBox.StandardButton.Ok)
            error2.exec_()
        
#Окно "Заказ книги"
    def add_order(self):
        if (self.te_numb_o.toPlainText() != ""):
            rec1 = [{"nameb": self.cB_nameb_o.currentText(),
                    "read": self.cB_read_o.currentText(),
                    "numb": self.te_numb_o.toPlainText()
                    }]
            print(rec1)
            self.cur_add.executemany('CALL add_order(%(nameb)s, %(read)s, %(numb)s)', rec1)
            self.dbu_add.commit()

    #Окно, что все выполнилось успешно
            inf = QMessageBox()
            inf.setWindowTitle("Информация")
            inf.setText("Данные успешно добавлены.")
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
                            FROM book_order ''', self.dbu_add)
            self.model = Pandas.TableModel(rec2)
            self.tab_order.setModel(self.model)

            self.te_numb_o.setText("")
        else:
    #Окно ошибки
            error2 = QMessageBox()
            error2.setWindowTitle("Ошибка ввода")
            error2.setText("Количество книг не может быть пустым.")
            error2.setIcon(QMessageBox.Icon.Warning)
            error2.setStandardButtons(QMessageBox.StandardButton.Ok)
            error2.exec_()

#Окно "Читатели"
    def add_reader(self):
        if (self.te_name_r.toPlainText() != ""):
            rec1 = [{"name": self.te_name_r.toPlainText(),
                    "lname": self.te_lname_r.toPlainText(),
                    "addr": self.te_addre_r.toPlainText(),
                    "phon": self.te_phone_r.toPlainText(),
                    "bth": self.te_bth_r.toPlainText()
                    }]
            self.cur_add.executemany('CALL add_reader(%(name)s, %(lname)s, %(addr)s, %(phon)s, %(bth)s)', rec1)
            self.dbu_add.commit()

    #Окно, что все выполнилось успешно
            inf = QMessageBox()
            inf.setWindowTitle("Информация")
            inf.setText("Данные успешно добавлены.")
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
                            FROM reader''', self.dbu_add)
            self.model = Pandas.TableModel(rec2)
            self.tab_reader.setModel(self.model)

            self.te_name_r.setText("")
            self.te_lname_r.setText("")
            self.te_addre_r.setText("")
            self.te_phone_r.setText("")
            self.te_bth_r.setText("")
        else:
    #Окно ошибки
            error2 = QMessageBox()
            error2.setWindowTitle("Ошибка ввода")
            error2.setText("Название издания не может быть пустым.")
            error2.setIcon(QMessageBox.Icon.Warning)
            error2.setStandardButtons(QMessageBox.StandardButton.Ok)
            error2.exec_()
