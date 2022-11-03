from PyQt5 import QtCore, QtGui, QtWidgets
from psycopg2.extras import DictCursor
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
import pandas as pd
import Pandas

class UpWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(UpWindow, self).__init__()
        uic.loadUi('Upwin.ui', self)

        #Заполнение строчки пользователя 
        self.lab_nln.setText("Библиотекарь")

        #Пользователь нажимает кнопку "Назад"
        self.btn_back.clicked.connect(self.back_push_btn)

        #Заполнение ComboBox "Авторский знак" в окне "Хранение"
        self.cur_up.execute('SELECT author_marks FROM keeping')
        resul1 = self.cur_up.fetchall()
        combox1 = [row[0] for row in resul1]
        for row in combox1:
            self.cB_mark_k.addItem(row)
        
        #Заполнение ComboBox "Название" в окне "Издательства"
        self.cur_up.execute('SELECT name_publish FROM publisher')
        resul2 = self.cur_up.fetchall()
        combox2 = [row[0] for row in resul2]
        for row in combox2:
            self.cB_name_p.addItem(row)

        #Заполнение ComboBox "Название" в окне "Книги"
        self.cur_up.execute('SELECT name_book FROM book_info')
        resul3 = self.cur_up.fetchall()
        combox3 = [row[0] for row in resul3]
        for row in combox3:
            self.cB_name_b.addItem(row)

        #Заполнение ComboBox "Издательство" в окне "Книги"
        self.cur_up.execute('SELECT name_publish FROM publisher')
        resul4 = self.cur_up.fetchall()
        combox4 = [row[0] for row in resul4]
        for row in combox4:
            self.cB_publish_b.addItem(row)

        #Заполнение ComboBox "Авторский знак" в окне "Книги"
        self.cur_up.execute('SELECT author_marks FROM keeping')
        resul5 = self.cur_up.fetchall()
        combox5 = [row[0] for row in resul5]
        for row in combox5:
            self.cB_mark_b.addItem(row)

        #Заполнение ComboBox "Название книги" в окне "Заказ книги"
        self.cur_up.execute('SELECT name_book FROM book_info')
        resul6 = self.cur_up.fetchall()
        combox6 = [row[0] for row in resul6]
        for row in combox6:
            self.cB_nameb_o.addItem(row)

        #Заполнение ComboBox "Читатель" в окне "Заказ книги"
        self.cur_up.execute('SELECT reader_last_name FROM reader')
        resul7 = self.cur_up.fetchall()
        combox7 = [row[0] for row in resul7]
        for row in combox7:
            self.cB_read_o.addItem(row)

        #Заполнение ComboBox "Фамилия читателя" в окне "Читатели"
        self.cur_up.execute('SELECT reader_last_name FROM reader')
        resul8 = self.cur_up.fetchall()
        combox8 = [row[0] for row in resul8]
        for row in combox8:
            self.cB_lname_r.addItem(row)

    #Окно "Издательства"
        #Отображение таблицы "Издательства" до изменений
        rec2 = pd.read_sql('''SELECT id_publish as \"ID-Издательства\", 
                            name_publish  as \"Издательство\",
                            official_website as \"Сайт\", 
                            address as \"Адрес\", 
                            what_is_emitting as \"Что выпускает\",
                            status as \"Статус\"
                         FROM publisher ''', self.dbu_up)
        self.model = Pandas.TableModel(rec2)
        self.tab_publish.setModel(self.model)

        #Пользователь нажимает кнопку "Изменить"
        self.btn_up_p.clicked.connect(self.up_publish)

    #Окно "Хранение"
        #Отображение таблицы "Хранение" до изменений
        rec2 = pd.read_sql('''SELECT id_keeping as \"ID-Хранения\",
                            author_marks as \"Авторский знак\",
                            total_book as \"Количество книг\", 
                            num_shelf_book as \"Стеллажная группа\", 
                            library as \"Какая библиотека\"
                            FROM keeping ''', self.dbu_up)
        self.model = Pandas.TableModel(rec2)
        self.tab_keep.setModel(self.model)

        #Пользователь нажимает кнопку "Изменить"
        self.btn_up_k.clicked.connect(self.up_keeping)
        
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
                        FROM book_info ''', self.dbu_up)
        self.model = Pandas.TableModel(rec2)
        self.tab_book.setModel(self.model)

        #Пользователь нажимает кнопку "Изменить"
        self.btn_up_b.clicked.connect(self.up_book)

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
                            FROM book_order ''', self.dbu_up)
        self.model = Pandas.TableModel(rec2)
        self.tab_order.setModel(self.model)

        #Пользователь нажимает кнопку "Изменить"
        self.btn_up_o.clicked.connect(self.up_order)

        #Пользователь нажимает кнопку "Продлить"
        self.btn_ext_o.clicked.connect(self.ext_order)

        #Пользователь нажимает кнопку "Вернуть"
        self.btn_bac_o.clicked.connect(self.ret_order)

    #Окно "Читатели"
        #Отображение таблицы "Читатели" до изменений
        rec2 = pd.read_sql('''SELECT  id_reader_ticket as \"ID читателя\", 
                            reader_name as \"Имя\",
                            reader_last_name as \"Фамилия\",
                            reader_address as \"Адрес\",
                            reader_phone as \"Телефон\",
                            birth_date as \"День Рождения\",
                            reader_registration_date as \"Дата регистрации\"
                            FROM reader''', self.dbu_up)
        self.model = Pandas.TableModel(rec2)
        self.tab_reader.setModel(self.model)

        #Пользователь нажимает кнопку "Изменить"
        self.btn_up_r.clicked.connect(self.up_read)


    #Пользователь нажимает кнопку "Назад"
    def back_push_btn(self):
        self.close()

    #Для подключения к БД
    def connect_user_order(self, dbu):
        self.dbu_up = dbu
        self.cur_up = self.dbu_up.cursor(cursor_factory=DictCursor)

#Окно "Издательства"
    def up_publish(self):
            rec1 = [{"name" : self.cB_name_p.currentText(),
                    "site": self.te_site_p.toPlainText(),
                    "adr": self.te_addres_p.toPlainText(),
                    "wpub": self.te_wpub_p.toPlainText(),
                    "stat": self.cB_stat_p.currentText()
                    }]
            self.cur_up.executemany('CALL up_publish(%(name)s, %(site)s, %(adr)s, %(wpub)s, %(stat)s)', rec1)
            self.dbu_up.commit()

    #Окно, что все выполнилось успешно
            inf = QMessageBox()
            inf.setWindowTitle("Информация")
            inf.setText("Данные успешно обновлены.")
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
                                FROM publisher ''', self.dbu_up)
            self.model = Pandas.TableModel(rec2)
            self.tab_publish.setModel(self.model)

            self.te_site_p.setText("")
            self.te_addres_p.setText("")
            self.te_wpub_p.setText("")

#Окно "Хранение"
    def up_keeping(self):
        rec1 = [{"mark" : self.cB_mark_k.currentText(),
                    "sgr": self.te_sgr_k.toPlainText(),
                    "lib": self.te_libk_k.toPlainText()
                }]
        self.cur_up.executemany('CALL up_keeping(%(mark)s, %(sgr)s, %(lib)s)', rec1)
        self.dbu_up.commit()

    #Окно, что все выполнилось успешно
        inf = QMessageBox()
        inf.setWindowTitle("Информация")
        inf.setText("Данные успешно обновлены.")
        inf.setIcon(QMessageBox.Icon.Information)
        inf.setStandardButtons(QMessageBox.StandardButton.Ok)
        inf.exec_()

    #Отображение таблицы "Хранение" после изменений
        rec2 = pd.read_sql('''SELECT id_keeping as \"ID-Хранения\",
                            author_marks as \"Авторский знак\",
                            total_book as \"Количество книг\", 
                            num_shelf_book as \"Стеллажная группа\", 
                            library as \"Какая библиотека\"
                            FROM keeping ''', self.dbu_up)
        self.model = Pandas.TableModel(rec2)
        self.tab_keep.setModel(self.model)

        self.te_sgr_k.setText("")
        self.te_libk_k.setText("")

#Окно "Книги"
    def up_book(self):
        if (self.te_isbn_b.toPlainText() != ""):
            rec1 = [{"name": self.cB_name_b.currentText(),
                    "isbn": self.te_isbn_b.toPlainText(),
                    "auth": self.te_author_b.toPlainText(),
                    "genr": self.te_genre_b.toPlainText(),
                    "year": self.te_yaer_b.toPlainText(),
                    "publ": self.cB_publish_b.currentText(),
                    "mark": self.cB_mark_b.currentText(),
                    "numpg": self.te_numpg_b.toPlainText(),
                    "numb": self.te_numb_b.toPlainText()
                    }]
            print(rec1)
            self.cur_up.executemany('CALL up_book(%(name)s,  %(isbn)s, %(auth)s, %(genr)s, %(year)s, %(publ)s, %(mark)s, %(numpg)s, %(numb)s)', rec1)
            self.dbu_up.commit()

    #Окно, что все выполнилось успешно
            inf = QMessageBox()
            inf.setWindowTitle("Информация")
            inf.setText("Данные успешно обновлены.")
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
                        FROM book_info ''', self.dbu_up)
            self.model = Pandas.TableModel(rec2)
            self.tab_book.setModel(self.model)

            self.te_isbn_b.setText("")
            self.te_author_b.setText(""),
            self.te_genre_b.setText(""),
            self.te_yaer_b.setText(""),
            self.te_numpg_b.setText(""),
            self.te_numb_b.setText("")
        else:
    #Окно ошибки
            error2 = QMessageBox()
            error2.setWindowTitle("Ошибка ввода")
            error2.setText("Код ISBN не может быть пустым.")
            error2.setIcon(QMessageBox.Icon.Warning)
            error2.setStandardButtons(QMessageBox.StandardButton.Ok)
            error2.exec_()

#Окно "Заказ книги"
    def up_order(self):
        if (self.te_numb_o.toPlainText() != ""):
            rec1 = [{"nameb": self.cB_nameb_o.currentText(),
                "read": self.cB_read_o.currentText(),
                "numb": self.te_numb_o.toPlainText()
                }]
            self.cur_up.executemany('CALL up_order(%(nameb)s, %(read)s, %(numb)s)', rec1)
            self.dbu_up.commit()

        #Окно, что все выполнилось успешно
            inf = QMessageBox()
            inf.setWindowTitle("Информация")
            inf.setText("Данные успешно обновлены.")
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
                                FROM book_order ''', self.dbu_up)
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

    def ret_order(self):
        rec1 = [{"nameb": self.cB_nameb_o.currentText(),
                "read": self.cB_read_o.currentText()}]
        self.cur_up.executemany('CALL return_the_book(%(nameb)s, %(read)s)', rec1)
        self.dbu_up.commit()

        #Окно, что все выполнилось успешно
        inf = QMessageBox()
        inf.setWindowTitle("Информация")
        inf.setText("Книга возвращена.")
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
                                FROM book_order ''', self.dbu_up)
        self.model = Pandas.TableModel(rec2)
        self.tab_order.setModel(self.model)

    def ext_order(self):
        rec1 = [{"nameb": self.cB_nameb_o.currentText(),
                "read": self.cB_read_o.currentText()}]
        self.cur_up.executemany('CALL extend_the_book(%(nameb)s, %(read)s)', rec1)
        self.dbu_up.commit()

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
                                FROM book_order ''', self.dbu_up)
        self.model = Pandas.TableModel(rec2)
        self.tab_order.setModel(self.model)

#Окно "Читатели"
    def up_read(self):
        rec1 = [{"lname": self.cB_lname_r.currentText(),
                "name": self.te_name_r.toPlainText(),
                "addr": self.te_addres_r.toPlainText(),
                "phon": self.te_phone_r.toPlainText(),
                "bth": self.te_bth_r.toPlainText()
                }]
        self.cur_up.executemany('CALL up_cursor_reader(%(lname)s, %(name)s, %(addr)s, %(phon)s, %(bth)s)', rec1)
        self.dbu_up.commit()

    #Окно, что все выполнилось успешно
        inf = QMessageBox()
        inf.setWindowTitle("Информация")
        inf.setText("Данные успешно обновлены.")
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
                            FROM reader''', self.dbu_up)
        self.model = Pandas.TableModel(rec2)
        self.tab_reader.setModel(self.model)   
