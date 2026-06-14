from db_connection import get_connection


class BookDB:
    def create_book(data):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
        """
        INSERT INTO books (title, author, genre, is_avalible) 
        VALUES (%s, %s, %s, TRUE)
        """,
        (data["title"], data["author"], data["genre"])
        )
        conn.commit()

        cursor.close()
        conn.close()

    
    def get_all_books():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows
    

    def get_book_by_id(id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books WHERE id = %s",(id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()
        return row
    

    def update_book(id, data):
        conn = get_connection()
        cursor = conn.cursor()

        set_clause = ", ".join(f"{key} = %s" for key in data.keys())

        cursor.execute(
            f"UPDATE books SET {set_clause} WHERE id = %s",
            list(data.keys()) + [id]
        )
        conn.commit()

        cursor.close()
        conn.close()
    

    def update_book(id, val, member_id):
        conn = get_connection()
        cursor = conn.cursor()

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

        cursor.execute("SELECT COUNT(*) FROM books")
        count = cursor.fetchone()

        cursor.close()
        conn.close()
        return count
    

    def count_available_books():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = TRUE")
        count = cursor.fetchone()

        cursor.close()
        conn.close()
        return count
    

    def count_borrowed_books():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = FALSE")
        count = cursor.fetchone()

        cursor.close()
        conn.close()
        return count
    

    def count_borrowed_books():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = FALSE")
        count = cursor.fetchone()

        cursor.close()
        conn.close()
        return count
    

    def count_borrowed_books(genre):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM books WHERE genre = %s", (genre,))
        count = cursor.fetchone()

        cursor.close()
        conn.close()
        return count
    

    def count_active_borrows_by_member(member_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM books WHERE borrowed_by_member_id = %s", (member_id,))
        count = cursor.fetchone()

        cursor.close()
        conn.close()
        return count