---------------------------------------------------------------------------------------
-- Создание таблиц
---------------------------------------------------------------------------------------

--Хранение:
CREATE TABLE public.keeping(
	id_keeping serial PRIMARY KEY,
	author_marks varchar(4),
	total_book integer DEFAULT 0,
	num_shelf_book integer DEFAULT 0,
	library text NOT NULL
);

UPDATE public.keeping
SET total_book = (SELECT SUM(num_book_in_lib)
			FROM public.book_info
			WHERE public.keeping.id_keeping = public.book_info.id_keeping);

--Издательства:
CREATE TABLE public.publisher(
	id_publish serial PRIMARY KEY,
	name_publish varchar(100) DEFAULT 'Неизвестно',
	official_website varchar(100) DEFAULT 'Неизвестно',
	address text DEFAULT 'Неизвестно',
	what_is_emitting text DEFAULT 'Неизвестно',
	status text DEFAULT 'Работает'
);

--Информация о книге:
CREATE TABLE public.book_info(
	id_book serial PRIMARY KEY,
	name_book varchar(100) NOT NULL,
	author varchar(100) NOT NULL,
	genre varchar(100) NOT NULL,
	year_publish serial NOT NULL,
	publish varchar(100) NOT NULL,
	isbn varchar(13) NOT NULL, 
	id_keeping serial NOT NULL,
	FOREIGN KEY (id_keeping) REFERENCES public.keeping (id_keeping),
	num_of_pages serial NOT NULL,
	num_book_in_lib integer NOT NULL,
books_so_far integer NOT NULL
);

--Связь издательства с книгой:
CREATE TABLE public.relation(
	id_relation serial PRIMARY KEY,
	id_publish serial NOT NULL,
	FOREIGN KEY (id_publish) REFERENCES public.publisher (id_publish),
	id_book serial NOT NULL,
	FOREIGN KEY (id_book) REFERENCES public.book_info (id_book) );
Абонемент читателя:
CREATE TABLE public.reader(
	id_reader_ticket serial PRIMARY KEY,
	reader_name varchar(30) NOT NULL,
	reader_last_name varchar(30) NOT NULL,
	reader_address text NOT NULL,
	reader_phone varchar(30) UNIQUE NOT NULL,
	birth_date date NOT NULL,
	reader_registration_date date NOT NULL
);

--Заказ книги из отдела каталогизации:
CREATE TABLE public.book_order (
	id_order serial PRIMARY KEY,
	id_book serial,
	FOREIGN KEY (id_book) REFERENCES public.book_info(id_book),
	id_reader_ticket serial,
	FOREIGN KEY (id_reader_ticket) REFERENCES public.reader(id_reader_ticket),
	issure_Date date NOT NULL,
	return_date date,
	num_of_copies serial NOT NULL,
	status text
);
