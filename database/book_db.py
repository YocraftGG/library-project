from database.db_connection import get_connection

from logs.setup_logger import logger


class BookDB:
    def create_book(data):
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("Creates a new book in database: %s", data)
        cursor.execute(
        """
        INSERT INTO books (title, author, genre, is_available) 
        VALUES (%s, %s, %s, TRUE)
        """,
        (data["title"], data["author"], data["genre"])
        )
        conn.commit()

        new_id = cursor.lastrowid

        cursor.close()
        conn.close()
        return new_id

    
    def get_all_books():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        logger.debug("Gets all books from database")
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows
    

    def get_book_by_id(id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        logger.debug("Gets book %s from database", id)
        cursor.execute("SELECT * FROM books WHERE id = %s",(id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()
        return row
    

    def update_book(id, data):
        conn = get_connection()
        cursor = conn.cursor()

        set_clause = ", ".join(f"{key} = %s" for key in data.keys())

        logger.debug("Update book %s in database: %s", id, data)
        cursor.execute(
            f"UPDATE books SET {set_clause} WHERE id = %s",
            list(data.values()) + [id]
        )
        conn.commit()

        cursor.close()
        conn.close()
    

    def set_available(id, val, member_id):
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("Makes book %s %s in database", id, val)
        cursor.execute(
            """
            UPDATE books 
            SET is_available = %s, borrowed_by_member_id = %s
            WHERE id = %s
            """,
            (val, member_id, id)
        )
        conn.commit()

        cursor.close()
        conn.close()


    def count_total_books():
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("Gets count of total books in database")
        cursor.execute("SELECT COUNT(*) FROM books")
        count = cursor.fetchone()

        cursor.close()
        conn.close()
        return count
    

    def count_available_books():
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("Gets count of available books in database")
        cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = TRUE")
        count = cursor.fetchone()

        cursor.close()
        conn.close()
        return count
    

    def count_borrowed_books():
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("Gets count of borrowed books in database")
        cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = FALSE")
        count = cursor.fetchone()

        cursor.close()
        conn.close()
        return count
    

    def count_by_genre(genre):
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("Gets count of %s books in database", genre)
        cursor.execute("SELECT COUNT(*) FROM books WHERE genre = %s", (genre,))
        count = cursor.fetchone()

        cursor.close()
        conn.close()
        return count
    

    def count_active_borrows_by_member(member_id):
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("Gets count of borrowed books by member %s in database", member_id)
        cursor.execute("SELECT COUNT(*) FROM books WHERE borrowed_by_member_id = %s", (member_id,))
        count = cursor.fetchone()
        print("aaaaaa", count)

        cursor.close()
        conn.close()
        return count[0]
    

    def is_available(id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT is_available FROM books WHERE id = %s", (id,))
        is_available = cursor.fetchone()

        cursor.close()
        conn.close()
        return is_available[0]