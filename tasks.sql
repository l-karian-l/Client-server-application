---------------------------------------------------------------------------------------
-- Задания.
---------------------------------------------------------------------------------------
-- Составной многотабличный запрос с CASE-выражением
--Задание: Посмотреть все книги, их издательство, количество, библиотеку и оценку их количества
---------------------------------------------------------------------------------------
SELECT name_book, num_book_in_lib, publish,(SELECT library FROM public.keeping 
	WHERE public.book_info.id_keeping = public.keeping.id_keeping) AS library,
	(CASE
		WHEN num_book_in_lib = 0 THEN 'Отсутствуют'
		WHEN num_book_in_lib = 1 THEN 'Заканчиваются'
		WHEN num_book_in_lib <= 7 THEN 'Мало'
		WHEN num_book_in_lib <= max(num_book_in_lib) THEN 'Есть в наличии'
	END) AS Evaluate_Count
FROM public.book_info 
GROUP BY name_book, num_book_in_lib, publish, library;

---------------------------------------------------------------------------------------
-- Многотабличный VIEW, с возможностью его обновления;
--Задание: Показать данные читателя и абонемента, который взял более 3х экземпляров одной книги.
---------------------------------------------------------------------------------------
CREATE OR REPLACE VIEW info_reader_and_order AS
SELECT 
	(SELECT distinct r.reader_name FROM public.reader AS r WHERE (o.id_reader_ticket = r.id_reader_ticket)),
	(SELECT r.reader_last_name FROM public.reader AS r WHERE (o.id_reader_ticket = r.id_reader_ticket)),
	(SELECT r.reader_address FROM public.reader AS r WHERE (o.id_reader_ticket = r.id_reader_ticket)),
	o.id_book, o.num_of_copies
FROM public.book_order AS o
WHERE (o.num_of_copies >= 3);

CREATE OR REPLACE FUNCTION num_of_copies_iro() RETURNS trigger AS $$
BEGIN
	IF (NEW.num_of_copies != OLD.num_of_copies) THEN
		UPDATE public.book_order SET num_of_copies = NEW.num_of_copies
		WHERE id_book = new.id_book;

		UPDATE public.book_info SET books_so_far = num_book_in_lib - NEW.num_of_copies
		WHERE id_book = new.id_book;
		RETURN NEW;
	END IF;
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER num_of_copies_iro_trigger
INSTEAD OF UPDATE ON public.info_reader_and_order
FOR EACH ROW EXECUTE PROCEDURE num_of_copies_iro();

---------------------------------------------------------------------------------------
-- Некоррелированный запрос в where.
--Задание: Книги, в которых страниц больше или равно среднему.
---------------------------------------------------------------------------------------
SELECT name_book, num_of_pages FROM book_info
WHERE num_of_pages >= (SELECT AVG(num_of_pages) FROM book_info);

---------------------------------------------------------------------------------------
-- Некоррелированный запрос в select.
--Задание: Показать сколько книг, на данный момент, есть в библиотеке.
---------------------------------------------------------------------------------------
SELECT (
	(SELECT SUM(num_book_in_lib) FROM book_info) - (SELECT COUNT(id_book) FROM public.book_order)
) AS "Num_book_in_library";

---------------------------------------------------------------------------------------
-- Некоррелированный запрос в from.
--Задание: Книги, которые были изданы позже 2016 года.
---------------------------------------------------------------------------------------
SELECT name_book, year_publish
FROM (
	SELECT id_book,name_book, year_publish
	FROM book_info
	WHERE year_publish > 2016
) AS book_info;

---------------------------------------------------------------------------------------
-- Коррелированные подзапросы (минимум 3 запроса); 
--Задание: Те книги (название, автор, ID), которые взяли более 3 человек
---------------------------------------------------------------------------------------
SELECT name_book, author, id_book FROM public.book_info 
WHERE(
	SELECT COUNT(id_book) FROM public.book_order
	WHERE public.book_info.id_book = public.book_order.id_book
)>=3;

---------------------------------------------------------------------------------------
--Задание: Какого издания и сколько книг есть в библиотеке.
---------------------------------------------------------------------------------------
SELECT (
	SELECT name_publish FROM public.publisher 
	WHERE public.publisher.id_publish = public.relation.id_publish) AS name_publish,
	COUNT (id_book) 
FROM public.relation
GROUP BY name_publish;

---------------------------------------------------------------------------------------
--Задание: Авторские знаки и сколько книг есть в библиотеке, с определенным знаком.
---------------------------------------------------------------------------------------
SELECT author_marks, (
	SELECT count(name_book) FROM public.book_info
	WHERE public.keeping.id_keeping = public.book_info.id_keeping) AS count_book 
FROM public.keeping
GROUP BY author_marks, count_book;

---------------------------------------------------------------------------------------
-- Многотабличный запрос, содержащий группировку записей, агрегативные функции и параметр, используемый в разделе HAVING;
--Задание: Самая популярная книга среди пользователей библиотеки.
---------------------------------------------------------------------------------------
SELECT b.name_book, b.author 
FROM public.book_info AS b 
JOIN public.book_order AS o ON (b.id_book = o.id_book)
GROUP BY b.name_book, b.author
HAVING count(*) >= 1 
ORDER BY count(*) DESC LIMIT 1;

---------------------------------------------------------------------------------------
-- Запрос, содержащий предикат ANY(SOME);
--Задание: Книги (ID, название), у которых жанр – «медицина»
---------------------------------------------------------------------------------------
SELECT id_book, name_book, genre FROM book_info
WHERE genre = ANY(SELECT genre FROM book_info WHERE genre LIKE '%медицина%');

---------------------------------------------------------------------------------------
-- Создать индексы для увеличения скорости выполнения запросов;
---------------------------------------------------------------------------------------
CREATE INDEX publish_index
ON public.publisher
USING btree(address, what_is_emitting);

CREATE INDEX book_inf_index
ON public.book_info
using brin(name_book) WITH(autosummarize = True);

CREATE INDEX reader_index
ON public.reader(reader_name, reader_last_name, reader_address, reader_phone);

---------------------------------------------------------------------------------------
-- В таблице 4 предусмотреть поле, которое заполняется автоматически по срабатыванию триггера 
--	при добавлении, обновлении и удалении данных
--Задание: Статус книги (Действительно, Просрочено, Продлить, Возвращено)
---------------------------------------------------------------------------------------
CREATE TABLE history_status_order(id serial PRIMARY KEY, history_status text);

CREATE OR REPLACE FUNCTION in_up_del_order_status_and_num_book() RETURNS TRIGGER AS $$
DECLARE
BEGIN
	IF CURRENT_DATE NOT BETWEEN OLD.issure_date AND NEW.return_date THEN
		NEW.status = 'Просрочено';
		RETURN NEW; 

	ELSIF TG_OP='INSERT' THEN
		NEW.status = 'Доступен до '|| NEW.return_date;
		RETURN NEW;

	ELSIF TG_OP='UPDATE' THEN
		IF (OLD.return_date = NEW.return_date) AND (OLD.return_date IS NOT NULL) THEN
			NEW.status = 'Доступен до '|| OLD.return_date;
			RETURN NEW;

		ELSIF (NEW.return_date IS NULL) OR (OLD.return_date IS NULL) THEN
			NEW.status = 'Возвращена';
			RETURN NEW;

		ELSIF OLD.return_date != NEW.return_date THEN
			NEW.status = 'Продлен до '||NEW.return_date;
			RETURN NEW;
		END IF;

	ELSIF TG_OP='DELETE' THEN
		INSERT INTO history_status_order(history_status) 
		VALUES ('Были удалены: ID-абонемента ='||OLD.id_order||', ID-книги ='||OLD.id_book||', 
		ID-читателя ='||OLD.id_reader_ticket);
		RETURN OLD;
	END IF; 
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER in_up_del_order_status_and_num_book_trigger
BEFORE INSERT OR UPDATE OR DELETE ON public.book_order
FOR EACH ROW EXECUTE PROCEDURE in_up_del_order_status_and_num_book();

---------------------------------------------------------------------------------------
-- Реализовать отдельную хранимую процедуру или функцию, состоящую из нескольких отдельных 
--	операций в виде единой транзакции, которая при определенных условиях может быть 
--	зафиксирована или откатана;

--Задание: Добавить в дополнительную таблицу информацию о книгах, 
--если все экземпляры данной книги были взяты читателями. А если нет, то откатить
---------------------------------------------------------------------------------------
CREATE TABLE no_book(id_no_book serial PRIMARY KEY, information text, data_no_book date);

CREATE OR REPLACE PROCEDURE no_book_in_the_library(no_name_book varchar(100), no_isbn varchar(13)) AS $$
DECLARE
	n_bo text;
BEGIN
	SELECT ('Острая нехватка: ID-книги = '||id_book||', Название = '||name_book||', Автор = '||author||', ISBN = '||isbn) into n_bo
	FROM public.book_info
	WHERE name_book = no_name_book AND isbn = no_isbn;
	
	IF ((SELECT books_so_far FROM public.book_info WHERE name_book = no_name_book AND isbn = no_isbn) == 0) THEN
		INSERT INTO public.no_book(information, data_no_book)
		VALUES (n_bo, current_date);
		COMMIT;
	ELSE
		ROLLBACK;
	END IF;
END;
$$ LANGUAGE plpgsql;

---------------------------------------------------------------------------------------
-- Реализовать курсор на обновление отдельных данных
--Задание: Курсор на обновление таблицы «Абонемент читателя».
---------------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE up_cursor_reader(old_reader_last_name varchar(100), 
up_reader_name varchar(100), up_reader_address text, up_reader_phone varchar(100),
up_birth_date date) AS $$
DECLARE
	cur CURSOR FOR SELECT * FROM public.reader;
	c_id_reader_ticket integer; c_reader_name varchar(100); c_reader_last_name varchar(100); 
	c_reader_address text; c_reader_phone varchar(100); c_birth_date date; c_reader_registration_date date;
BEGIN
	OPEN cur;
	LOOP
		FETCH cur INTO c_id_reader_ticket, c_reader_name,  c_reader_last_name, c_reader_address, 
		c_reader_phone, c_birth_date, c_reader_registration_date;
		IF NOT FOUND THEN EXIT; END IF;

		IF(c_reader_last_name = old_reader_last_name) THEN
			UPDATE public.reader SET reader_name = up_reader_name, 
			reader_address = up_reader_address, reader_phone = up_reader_phone, 
			birth_date = up_birth_date 
			WHERE CURRENT OF cur;
		END IF;
	END LOOP;
	CLOSE cur;
END;
$$ LANGUAGE plpgsql;

---------------------------------------------------------------------------------------
-- Реализовать собственную скалярную и векторную функции. 
--Задание: Скалярная функция - Информация о месте хранения.
---------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION where_book(book varchar(100)) RETURNS integer AS $$
DECLARE
	w_book integer;
BEGIN
	w_book = (SELECT num_shelf_book FROM public.keeping as kp 
			  join public.book_info as b on (b.name_book = book and b.id_keeping = kp.id_keeping) 
	);
	RETURN w_book;
END;
$$ LANGUAGE plpgsql;

---------------------------------------------------------------------------------------
--Задание: Векторная функция - Вывести данные пользователя (фамилию, имя, номер телефона)
--	и информацию о книге (название, автор), если читатель просрочил сдачу книги на сегодняшний день
---------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION notices_book_overdue() 
RETURNS TABLE (name_r varchar(50),last_name_r varchar(50),phone_r varchar(30), address_r text,
		name_book_r varchar(50),author_r varchar(50)) AS $$
BEGIN
	RETURN QUERY(
		SELECT R.reader_name AS name_r, R.reader_last_name AS last_name_r, R.reader_phone AS phone_r, 
		R.reader_address AS address_r, B.name_book AS name_book_r,B.author AS author_r
		FROM public.book_info B, public.reader R
		RIGHT JOIN public.book_order USING (id_reader_ticket)
		WHERE (public.book_order.status = 'Просрочено')
		AND (public.book_order.id_book = B.id_book)
	);
END;
$$ LANGUAGE plpgsql;

---------------------------------------------------------------------------------------
--  Дополнительно
--Задание: Уменьшить количество книг, если экземпляр книги был забронирован пользователем. 
--Если отменили бронь, то откатить.
---------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION up_num_of_book_tab_order() RETURNS trigger AS $$
BEGIN
	IF TG_OP='INSERT' THEN
		UPDATE public.book_info SET books_so_far = num_book_in_lib - NEW.num_of_copies
		WHERE (public.book_info.id_book = NEW.id_book) AND NEW.status != 'Возвращена';
		RETURN NEW;

	ELSIF TG_OP='UPDATE' THEN
		UPDATE public.book_info SET books_so_far = num_book_in_lib + OLD.num_of_copies
		WHERE public.book_info.id_book = OLD.id_book AND NEW.status = 'Возвращена';
		RETURN NEW;	
	END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER up_num_of_book_in_the_lib_trigger_order
AFTER INSERT OR UPDATE ON public.book_order
FOR EACH ROW EXECUTE PROCEDURE up_num_of_book_tab_order();
