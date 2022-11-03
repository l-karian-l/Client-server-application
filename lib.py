from PyQt5 import QtCore, QtGui, QtWidgets
from psycopg2.extras import DictCursor
from addwindow import AddWindow
from Upwindow import UpWindow
from delwindow import DelWindow
from PyQt5 import uic
import pandas as pd
import Pandas
import connect

class LibWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LibWindow, self).__init__()
        uic.loadUi('Libririan.ui', self)
        
        #Заполнение строчки "Имя и Фамилия пользователя" 
        self.lab_user_name.setText("Библиотекарь")

        #При нажатии на кнопку "Выход"
        self.btn_exit.clicked.connect(self.user_exit)

#"Основное" окно
        #При нажатии на кнопку "Книги"
        self.btn_book.clicked.connect(self.show_book)
    
        #При нажатии на кнопку "Издательства"
        self.btn_publish.clicked.connect(self.show_publish) 

        #При нажатии на кнопку "Хранение" 
        self.btn_keeping.clicked.connect(self.show_keeping)
       
        #При нажатии на кнопку "Заказы"
        self.btn_order.clicked.connect(self.show_order)

        #При нажатии на кнопку "Читатели"
        self.btn_reader.clicked.connect(self.show_reader)  

        #При нажатии на кнопку "Удаленные заказы"
        self.btn_history.clicked.connect(self.show_history)    

        #При нажатии на кнопку "Связь"
        self.btn_relation.clicked.connect(self.show_relation)

        #При нажатии на кнопку "Добавить"
        self.btn_add.clicked.connect(self.open_add_win) 

        #При нажатии на кнопку "Изменить"
        self.btn_update.clicked.connect(self.open_up_win) 

        #При нажатии на кнопку "Удалить"
        self.btn_delete.clicked.connect(self.open_del_win) 

#Окно "Демонстрация навыков"      
        #При нажатии на кнопку "CASE" 
        self.btn_case.clicked.connect(self.show_case)

        #При нажатии на кнопку "Некор. WHERE"
        self.btn_nkor_where.clicked.connect(self.show_nkor_where) 
    
        #При нажатии на кнопку "Некор. SELECT"
        self.btn_nkor_select.clicked.connect(self.show_nkor_select)

        #При нажатии на кнопку "Некор. FROM"
        self.btn_nkor_from.clicked.connect(self.show_nkor_from)

        #При нажатии на кнопку "1 Кор. подзп."
        self.btn_kor_1.clicked.connect(self.show_kor_1)

        #При нажатии на кнопку "2 Кор. подзп."
        self.btn_kor_2.clicked.connect(self.show_kor_2)

        #При нажатии на кнопку "3 Кор. подзп."
        self.btn_kor_3.clicked.connect(self.show_kor_3)
    
        #При нажатии на кнопку "HAVING"
        self.btn_having.clicked.connect(self.show_having)

        #При нажатии на кнопку "ANY"
        self.btn_any.clicked.connect(self.show_any)

        #При нажатии на кнопку "Скал. фун-ия"
        self.btn_skal_func.clicked.connect(self.show_skal_func)

        #При нажатии на кнопку "Вектр. фун-ия"
        self.btn_vect_func.clicked.connect(self.show_vect_func)

        #При нажатии на кнопку "VIEW"
        self.btn_view.clicked.connect(self.show_view)

        #При нажатии на кнопку "Обновить VIEW"
        self.btn_view_up.clicked.connect(self.show_view_up)

        #При нажатии на кнопку "Обновить VIEW"
        self.btn_tranz.clicked.connect(self.show_tranz)

        #При нажатии на кнопку "Добавить" при Демонстрации транзакции
        self.btn_tz_ad.clicked.connect(self.show_tranz_add)

    #Для подключения к БД
    def connect_bd(self, email, pas):
        self.dbu = connect.connect_db(email, pas)
        if self.dbu == False:
            return self.dbu
        else:
            self.cur = self.dbu.cursor(cursor_factory=DictCursor)

        #Заполнение ComboBox "Название книги" для VIEW
        self.cur.execute('SELECT name_book FROM book_info')
        resul1 = self.cur.fetchall()
        combox1 = [row[0] for row in resul1]
        for row in combox1:
            self.cB_book_v.addItem(row)
        
        #Заполнение ComboBox "Читатель" для VIEW
        self.cur.execute('SELECT reader_last_name FROM reader')
        resul2 = self.cur.fetchall()
        combox2 = [row[0] for row in resul2]
        for row in combox2:
            self.cB_read_v.addItem(row)

        #Заполнение ComboBox "Название книги" для Транзакции
        self.cur.execute('SELECT name_book FROM book_info')
        resul3 = self.cur.fetchall()
        combox3 = [row[0] for row in resul3]
        for row in combox3:
            self.cB_book_tz.addItem(row)

    #Для выхода из аккаунта
    def user_exit(self):
        from login import LoginWindow
        self.Login = LoginWindow()
        self.Login.show()
        self.hide()


#"Основное" окно
    #Показ таблицы "info_table" при нажатии на кнопку "Книги" 
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
                            num_book_in_lib as \"Всего в библиотеке\",
                            books_so_far as \"На данный момент\"
                        FROM book_info ''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_base.setModel(self.model)

    #Показ таблицы "publisher" при нажатии на кнопку "Издательства" 
    def show_publish(self):
        rec = pd.read_sql('''SELECT id_publish as \"ID-Издательства\", 
                            name_publish  as \"Издательство\",
                            official_website as \"Сайт\", 
                            address as \"Адрес\", 
                            what_is_emitting as \"Что выпускает\",
                            status as \"Статус\"
                         FROM publisher ''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_base.setModel(self.model)

    #Показ таблицы "Хранение" при нажатии на кнопку "Хранение" 
    def show_keeping(self):
        rec = pd.read_sql('''SELECT id_keeping as \"ID-Хранения\",
                            author_marks as \"Авторский знак\",
                            total_book as \"Количество книг\", 
                            num_shelf_book as \"Стеллажная группа\", 
                            library as \"Какая библиотека\"
                            FROM keeping ''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_base.setModel(self.model)

    #Показ таблицы "book_order" при нажатии на кнопку "Заказы" 
    def show_order(self):
        rec = pd.read_sql('''SELECT id_order as \"ID бронирования\",
                            id_book as \"ID книги\", 
                            id_reader_ticket as \"ID читателя\", 
                            issure_date as \"Дата выдачи\",
                            return_date as \"Дата возврата\",
                            num_of_copies as \"Количество\",
                            status as \"Статус\"
                            FROM book_order ''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_base.setModel(self.model)

    #Показ таблицы "reader" в "Основном" окне при нажатии на кнопку "Читатели" 
    def show_reader(self):
        rec = pd.read_sql('''SELECT  id_reader_ticket as \"ID читателя\", 
                            reader_name as \"Имя\",
                            reader_last_name as \"Фамилия\",
                            reader_address as \"Адрес\",
                            reader_phone as \"Телефон\",
                            birth_date as \"День Рождения\",
                            reader_registration_date as \"Дата регистрации\"
                            FROM reader''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_base.setModel(self.model)

    #Показ таблицы "history_status_order" при нажатии на кнопку "Удаленные записи" 
    def show_history(self):
        rec = pd.read_sql('''SELECT id as \"ID\", 
                                    history_status as \"Статус\"
                            FROM history_status_order''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_base.setModel(self.model)

    #Показ таблицы "relation" при нажатии на кнопку "Связь..." 
    def show_relation(self):
        rec = pd.read_sql('''SELECT id_relation as \"ID-связи\", 
                                    (SELECT name_publish FROM publisher WHERE publisher.id_publish = relation.id_publish) as \"Издательство\", 
                                    (SELECT name_book FROM book_info WHERE book_info.id_book = relation.id_book) as \"Книга\"
                            FROM relation''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_base.setModel(self.model)
    
    #Отображение окна "Добавить"
    def open_add_win(self):
        AddWindow.connect_user_add(AddWindow, self.dbu)
        self.Add = AddWindow()
        self.Add.show()

    #Отображение окна "Изменить"
    def open_up_win(self):
        UpWindow.connect_user_order(UpWindow, self.dbu)
        self.Add = UpWindow()
        self.Add.show()

    #Отображение окна "Удалить"
    def open_del_win(self):
        DelWindow.connect_user_order(DelWindow, self.dbu)
        self.Add = DelWindow()
        self.Add.show()
       

#Окно "Демонстрация навыков" 
    #Показ выполения CASE
    def show_case(self):
        self.lab_text.setText("Посмотреть все книги, их издательство, количество, библиотеку и оценку их количества.")
        rec = pd.read_sql('''SELECT name_book as \"Название\", 
                                num_book_in_lib as \"Книг в библиотеке\",
                                publish as \"Издательтсво\",
                                (SELECT library 
                                    FROM public.keeping 
                                    WHERE public.book_info.id_keeping = public.keeping.id_keeping) as \"Библиотека\",
                                (CASE
                                    WHEN num_book_in_lib = 0 THEN 'Отсутствуют'
	                                WHEN num_book_in_lib = 1 THEN 'Заканчиваются'
	                                WHEN num_book_in_lib <= 7 THEN 'Мало'
	                                WHEN num_book_in_lib <= max(num_book_in_lib) THEN 'Есть в наличии'
	                            END) as \"Оценка количества\"
                            FROM public.book_info 
                            GROUP BY name_book, num_book_in_lib, publish, \"Библиотека\" ''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model)

    #Показ выполения некоррелированного запроса в where.
    def show_nkor_where(self):
        self.lab_text.setText("Книги, в которых страниц больше или равно среднему.")
        rec = pd.read_sql('''SELECT name_book as \"Название\", 
                                num_of_pages as \"Количество страниц\"
                            FROM book_info
                            WHERE num_of_pages >= (SELECT AVG(num_of_pages) FROM book_info)''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model)

    #Показ выполения некоррелированного запроса в select.
    def show_nkor_select(self):
        self.lab_text.setText("Сколько книг, на данный момент, есть в библиотеке.")
        rec = pd.read_sql('''SELECT (
	                            (SELECT SUM(num_book_in_lib) FROM book_info) - 
	                            (SELECT COUNT(id_book) FROM public.book_order)
                            ) AS \"Количество книг в библиотеке\"''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model)

    #Показ выполения некоррелированного запроса в from.
    def show_nkor_from(self):
        self.lab_text.setText("Книги, которые были изданы позже 2016 года.")
        rec = pd.read_sql('''SELECT name_book as \"Название\", 
                                    year_publish as \"Год издания\"
                            FROM (
	                            SELECT id_book,name_book,year_publish
	                            FROM book_info
	                            WHERE year_publish > 2016
                            ) AS book_info''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model)        

    #Показ выполения 1 коррелированного запроса.
    def show_kor_1(self):
        self.lab_text.setText("Те книги (название, автор, ID), которые взяли более 3 человек.")
        rec = pd.read_sql('''SELECT name_book as \"Название\", 
                                    author as \"Автор \", 
                                    id_book as \"ID книги\"
                            FROM public.book_info 
                            WHERE(
	                            SELECT COUNT(id_book) 
	                            FROM public.book_order
		                        WHERE public.book_info.id_book = public.book_order.id_book
                            )>=3;''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model)  

    #Показ выполения 2 коррелированного запроса.
    def show_kor_2(self):
        self.lab_text.setText("Какого издания и сколько книг есть в библиотеке.")
        rec = pd.read_sql('''SELECT (SELECT name_publish 
                                        FROM publisher
                                        WHERE publisher.id_publish = relation.id_publish) as \"Издательство\",
                                    COUNT(id_book) as \"Количество книг\" 
                            FROM relation
                            GROUP BY \"Издательство\" ''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model)  

    #Показ выполения 3 коррелированного запроса.
    def show_kor_3(self):
        self.lab_text.setText("Авторские знаки и сколько книг есть в библиотеке, с определенным знаком")
        rec = pd.read_sql('''SELECT author_marks as \"Авторский знак\", 
                                (   SELECT count(name_book)
                                    FROM public.book_info
                                    WHERE public.keeping.id_keeping = public.book_info.id_keeping
                                ) as \"Количество книг \"  
                            FROM public.keeping
                            GROUP BY author_marks, \"Количество книг \" ''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model) 

    #Показ выполения HAVING
    def show_having(self):
        self.lab_text.setText("Самая популярная книга среди пользователей библиотеки.")
        rec = pd.read_sql('''SELECT b.name_book as \"Название\", 
                                    b.author as \"Автор\"
                            FROM public.book_info AS b 
                            JOIN public.book_order AS o ON (b.id_book = o.id_book)
                            GROUP BY b.name_book, b.author
                            HAVING count(*) >= 1 
                            ORDER BY count(*) DESC LIMIT 1''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model)  

    #Показ выполения ANY
    def show_any(self):
        self.lab_text.setText("Книги (ID, название), у которых жанр – «медицина»")
        rec = pd.read_sql('''SELECT id_book as \"ID книги\", 
                                    name_book as \"Название\", 
                                    genre as \"Жанр\"
                            FROM book_info
                            WHERE genre = ANY(
                                SELECT genre 
                                FROM book_info 
                                WHERE genre LIKE '%медицина%')''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model)  

    #Показ выполения скалярной функции
    def show_skal_func(self):
        self.lab_text.setText("Как работает скалярная функция. Информация о книге (автор, название), и к какой стеллажной группе она принадлежит")
        rec = pd.read_sql('''SELECT author as \"Автор\", 
                                    name_book as \"Название\",
                                    where_book('Кот Боб') as \"Стеллажная группа\"
                            FROM public.book_info   
                            WHERE name_book = 'Кот Боб' ''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model)  

    #Показ выполения векторной функции
    def show_vect_func(self):
        self.lab_text.setText("Как работает векторная функция. Все читатели, кто просрочил сдачу книги на сегодняшний день.")
        rec = pd.read_sql('''SELECT notices_book_overdue()''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model)  

    #Показ выполения VIEW
    def show_view(self):
        self.lab_text.setText("Данные о книге и о читателе, который взял более 3х экземпляров одной книги.")
        rec = pd.read_sql('''SELECT reader_name as \"Имя читателя\", 
                                    reader_last_name as \"Фамилия читателя\",
                                    reader_address as \"Адрес читателя\",
                                    (select name_book from book_info where book_info.id_book = info_reader_and_order.id_book) as \"Книга\",
                                    num_of_copies as \"Кол-во книг\"
                from info_reader_and_order''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model) 

    #Выполнение изменения VIEW
    def show_view_up(self):
        self.lab_text.setText("Обновленные данные о книге и о читателе, который взял более 3х экземпляров одной книги.")
        rec1 = [{"book": self.cB_book_v.currentText(),
                "read": self.cB_read_v.currentText(),
                "numb": self.te_numb_v.toPlainText()
                }]
        self.cur.executemany('''UPDATE public.info_reader_and_order 
                                    SET num_of_copies = %(numb)s
                                    WHERE id_book = (select id_book from book_info where book_info.name_book = %(book)s) 
                                    AND reader_last_name = %(read)s''', rec1)
        self.dbu.commit()

        rec = pd.read_sql('''SELECT reader_name as \"Имя читателя\", 
                                    reader_last_name as \"Фамилия читателя\",
                                    reader_address as \"Адрес читателя\",
                                    (select name_book from book_info where book_info.id_book = info_reader_and_order.id_book) as \"Книга\",
                                    num_of_copies as \"Кол-во книг\"
                from info_reader_and_order''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model) 

    #Показ выполения транзакции
    def show_tranz(self):
        self.lab_text.setText("Если все экземпляры данной книги были взяты читателями - добавть в табл.. Если нет, то откатить.")
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
                            num_book_in_lib as \"Всего в библиотеке\",
                            books_so_far as \"На данный момент\"
                        FROM book_info ''', self.dbu)
        self.model = Pandas.TableModel(rec)
        self.tab_skils.setModel(self.model)

    #Выполнение изменения транзакции
    def show_tranz_add(self):
        self.lab_text.setText("Добавление данных в дополнительную таблицу, если все экземпляры данной книги были взяты читателями.")
        if (self.te_isbn_tz.toPlainText() != ""):
            self.dbu.rollback()
            self.dbu.autocommit = True
            self.cur.execute('CALL no_book_in_the_library(%s, %s)', (self.cB_book_tz.currentText(),self.te_isbn_tz.toPlainText()))

            rec = pd.read_sql('''SELECT id_no_book as \"ID\", 
                                    information as \"Информация\",
                                    data_no_book as \"Дата\"
                from no_book''', self.dbu)
            self.model = Pandas.TableModel(rec)
            self.tab_tz.setModel(self.model) 
