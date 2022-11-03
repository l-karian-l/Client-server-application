---------------------------------------------------------------------------------------
-- Задания. Разработка функций удаления, обновления, добавления.
---------------------------------------------------------------------------------------
-- Для таблицы «Издательствa»
-- Добавление.
---------------------------------------------------------------------------------------
CREATE PROCEDURE add_publish(add_name_publish varchar(100), add_official_website varchar(100), add_address text, add_what_is_emitting text, add_status text)
LANGUAGE SQL AS $$
	INSERT INTO public.publisher( name_publish, official_website, address, what_is_emitting, status)
	VALUES(add_name_publish, add_official_website, add_address, add_what_is_emitting, add_status);
$$

---------------------------------------------------------------------------------------
-- Удаление
---------------------------------------------------------------------------------------
CREATE PROCEDURE del_publish(del_id_publish varchar(100))
LANGUAGE SQL AS $$
	DELETE FROM public.publisher 
	WHERE id_publish = (SELECT id_publish FROM public.publisher 
		WHERE name_publish = del_id_publish)
$$

---------------------------------------------------------------------------------------
-- Обновление
---------------------------------------------------------------------------------------
CREATE PROCEDURE up_publish(old_name_publish varchar(100), up_official_website varchar(100), 
up_address text, up_what_is_emitting text, up_status text)
LANGUAGE SQL AS $$
	UPDATE public.publisher
	SET official_website = up_official_website, address = up_address, 
	what_is_emitting = up_what_is_emitting, status = up_status
	WHERE name_publish = old_name_publish
$$

---------------------------------------------------------------------------------------
-- Для таблицы «Хранение»
-- Добавление.
---------------------------------------------------------------------------------------
CREATE PROCEDURE add_keeping(add_author_marks varchar(4), add_num_shelf_book integer, 
add_library text)
LANGUAGE SQL AS $$
	INSERT INTO public.keeping(author_marks, num_shelf_book, library)
	VALUES(add_author_marks, add_num_shelf_book, add_library);

	UPDATE public.keeping
	SET total_book = (SELECT SUM(num_book_in_lib)
		FROM public.book_info
		WHERE public.keeping.id_keeping = public.book_info.id_keeping);
$$

---------------------------------------------------------------------------------------
-- Удаление
---------------------------------------------------------------------------------------
CREATE PROCEDURE del_keeping(del_author_marks varchar(4)) LANGUAGE SQL AS $$
	DELETE FROM public.keeping
	WHERE id_keeping = (SELECT id_keeping FROM public.keeping 
		WHERE author_marks = del_author_marks)
$$

---------------------------------------------------------------------------------------
-- Обновление
---------------------------------------------------------------------------------------
CREATE PROCEDURE up_keeping(old_author_marks varchar(4), up_num_shelf_book integer, 
up_library text) LANGUAGE SQL AS $$
	UPDATE public.keeping
	SET num_shelf_book = up_num_shelf_book, library = up_library,
	total_book = (SELECT SUM(num_book_in_lib) FROM public.book_info 
		WHERE public.keeping.id_keeping = public.book_info.id_keeping)
	WHERE author_marks = old_author_marks
$$

---------------------------------------------------------------------------------------
-- Для таблицы «Хранение»
-- Добавление.
---------------------------------------------------------------------------------------
CREATE PROCEDURE add_book(add_name_book varchar(100), add_author varchar(100),
add_genre varchar(100), add_year_publish integer, add_publish varchar(100), 
add_isbn varchar(13), add_keeping varchar(100), add_num_of_pages integer, 
add_num_book_in_lib integer) LANGUAGE SQL AS $$
	INSERT INTO public.book_info(name_book, author, genre, year_publish, publish, isbn, 
	id_keeping, num_of_pages, num_book_in_lib)
	VALUES(add_name_book, add_author, add_genre, add_year_publish, add_publish, add_isbn,
		(SELECT id_keeping FROM public.keeping WHERE author_marks = add_keeping),
		add_num_of_pages, add_num_book_in_lib);

	UPDATE public.keeping
	SET total_book = (SELECT SUM(num_book_in_lib) FROM public.book_info
		WHERE public.keeping.id_keeping = public.book_info.id_keeping);
$$

---------------------------------------------------------------------------------------
-- Удаление
---------------------------------------------------------------------------------------
CREATE PROCEDURE del_book(del_name_book varchar(100), del_isbn varchar(13)) LANGUAGE SQL AS $$
	DELETE FROM public.book_info
	WHERE id_book = (SELECT id_book FROM public.book_info
				WHERE name_book = del_name_book AND isbn = del_isbn);
	
	UPDATE public.keeping
	SET total_book = (SELECT SUM(num_book_in_lib) FROM public.book_info WHERE public.keeping.id_keeping = public.book_info.id_keeping);
$$
---------------------------------------------------------------------------------------
-- Обновление
---------------------------------------------------------------------------------------
CREATE PROCEDURE up_book(old_name_book varchar(100), old_isbn varchar(13),
up_author varchar(100), up_genre varchar(100), up_year_publish integer,
up_publish varchar(100), up_keeping varchar(100), up_num_of_pages integer, 
up_num_book_in_lib integer) LANGUAGE SQL AS $$
	UPDATE public.book_info
	SET author = up_author, genre = up_genre, year_publish = up_year_publish, publish = up_publish, 
		id_keeping = (SELECT id_keeping FROM public.keeping WHERE author_marks = up_keeping),
		num_of_pages = up_num_of_pages, num_book_in_lib = up_num_book_in_lib
	WHERE name_book = old_name_book AND isbn = old_isbn;

	UPDATE public.keeping
	SET total_book = (SELECT SUM(num_book_in_lib) FROM public.book_info
WHERE public.keeping.id_keeping = public.book_info.id_keeping);
$$

---------------------------------------------------------------------------------------
-- Для таблицы «Связь издательства с книгой»
-- Добавление.
---------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION add_relation() RETURNS TRIGGER AS $$
DECLARE
BEGIN
	IF TG_OP='INSERT' THEN
		INSERT INTO public.relation(id_publish, id_book)
		VALUES((SELECT id_publish FROM public.publisher WHERE name_publish = NEW.publish), 
			NEW.id_book);
		RETURN NEW; 
	END IF; 
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER add_relation_trigger
BEFORE INSERT ON public.book_info
FOR EACH ROW EXECUTE PROCEDURE add_relation();

---------------------------------------------------------------------------------------
-- Удаление
---------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION del_relation() RETURNS TRIGGER AS $$
DECLARE
BEGIN
	IF TG_OP='DELETE' THEN
		DELETE FROM public.relation
		WHERE id_relation = (SELECT id_relation FROM public.relation WHERE id_book = OLD.id_book);
		RETURN OLD; 
	END IF; 
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER del_relation_trigger
BEFORE DELETE ON public.book_info
FOR EACH ROW EXECUTE PROCEDURE del_relation();

---------------------------------------------------------------------------------------
-- Обновление
---------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION up_relation() RETURNS TRIGGER AS $$
DECLARE
BEGIN
	IF TG_OP='UPDATE' THEN
		IF(OLD.id_book = NEW.id_book) AND (OLD.publish != NEW.publish) THEN
			UPDATE public.relation
			SET id_publish = (SELECT id_publish FROM public.publisher WHERE name_publish = NEW.publish)
			WHERE id_book = NEW.id_book;
			RETURN NEW; 
		END IF; 
	END IF;
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER up_relation_trigger
BEFORE UPDATE ON public.book_info
FOR EACH ROW EXECUTE PROCEDURE up_relation();

---------------------------------------------------------------------------------------
-- Для таблицы «Абонемент читателя»
-- Добавление.
---------------------------------------------------------------------------------------
CREATE PROCEDURE add_reader(add_reader_name varchar(30), add_reader_last_name 
varchar(30), add_reader_address text, add_reader_phone varchar(30), add_birth_date date)
LANGUAGE SQL AS $$
	INSERT INTO public.reader(reader_name, reader_last_name, reader_address, reader_phone, 
		birth_date, reader_registration_date)
	VALUES(add_reader_name, add_reader_last_name, add_reader_address, add_reader_phone, 
		add_birth_date, current_date);
$$

---------------------------------------------------------------------------------------
-- Удаление
---------------------------------------------------------------------------------------
CREATE PROCEDURE del_reader(del_reader varchar(100)) LANGUAGE SQL AS $$
	DELETE FROM public.reader
	WHERE id_reader_ticket = (SELECT id_reader_ticket FROM public.reader 
		WHERE reader_last_name = del_reader)
$$

---------------------------------------------------------------------------------------
-- Для таблицы «Взять книгу»
-- Добавление.
---------------------------------------------------------------------------------------
CREATE PROCEDURE add_order(add_book varchar(100), add_reader varchar(100), 
add_num_of_copies integer) LANGUAGE SQL AS $$
	INSERT INTO public.book_order(id_book, id_reader_ticket, issure_date, return_date, 
		num_of_copies)
	VALUES(( SELECT id_book FROM public.book_info WHERE name_book = add_book),
		(SELECT id_reader_ticket FROM public.reader WHERE reader_last_name = add_reader),
		(current_date), (current_date + 14), add_num_of_copies);
$$

---------------------------------------------------------------------------------------
-- Удаление
---------------------------------------------------------------------------------------
CREATE PROCEDURE up_order(old_name_book varchar(100), old_reader varchar(100), 
up_num_of_copies integer) LANGUAGE SQL AS $$
	UPDATE public.book_order SET num_of_copies = up_num_of_copies
	WHERE id_book = (SELECT id_book FROM public.book_info WHERE name_book = old_name_book)
		AND id_reader_ticket = (SELECT id_reader_ticket FROM public.reader 
		WHERE reader_last_name = old_reader)
$$

---------------------------------------------------------------------------------------
-- Продление книги
---------------------------------------------------------------------------------------
CREATE PROCEDURE extend_the_book(old_name_book varchar(100), old_reader varchar(100))
LANGUAGE SQL AS $$
	UPDATE public.book_order SET return_date = (return_date + 7)
	WHERE id_book = (SELECT id_book FROM public.book_info WHERE name_book = old_name_book)
		AND id_reader_ticket = (SELECT id_reader_ticket FROM public.reader 
			WHERE reader_last_name = old_reader)
$$

---------------------------------------------------------------------------------------
-- Возврат книги
---------------------------------------------------------------------------------------
CREATE PROCEDURE return_the_book(old_name_book varchar(100), old_reader varchar(100))
LANGUAGE SQL AS $$
	UPDATE public.book_order SET return_date = NULL
	WHERE id_book = (SELECT id_book FROM public.book_info WHERE name_book = old_name_book)
		AND id_reader_ticket = (SELECT id_reader_ticket FROM public.reader 
			WHERE reader_last_name = old_reader)
$$
