import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="root",
        password="root",
        database="library_db"
    )


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
            author VARCHAR(50) NOT NULL,
            genre ENUM("Fiction", "Non-Fiction", "Science", "History", "Other") NOT NULL,
            is_available BOOLEAN NOT NULL,
            borrowed_by_member_id INT NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(200) UNIQUE NOT NULL,
            is_active BOOLEAN NOT NULL,
            total_borrows INT NOT NULL
        );
        """
    )
    conn.commit()
    cursor.close()
    conn.close()