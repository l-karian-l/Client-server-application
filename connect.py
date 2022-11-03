from psycopg2 import OperationalError
import psycopg2
    
def connect_db(email, pas):
        try:
            db = psycopg2.connect(
                host = "localhost",
                user = email, 
                password = pas,
                database = "library",
                port = "5432"
            )

            print("Connection to PostreSQL DB successful")
            return db
        except OperationalError as e:
            print(f"The error '{e}' occurred")
            return False


        
