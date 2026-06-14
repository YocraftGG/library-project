from db_connection import get_connection
from logs.setup_logger import logger


class MemberDB:
    def create_member(data):
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("creates a new member in database: %s", data)
        cursor.execute(
        """
        INSERT INTO members (name, email, is_active, total_borrows) 
        VALUES (%s, %s, TRUE, 0)
        """,
        (data["name"], data["email"])
        )
        conn.commit()

        cursor.close()
        conn.close()


    def get_all_members():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        logger.debug("gets all members from database")
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows
    

    def get_member_by_id(id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        logger.debug("gets member %s from database", id)
        cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.cursor()
        return row
    

    def update_member(id, data):
        conn = get_connection()
        cursor = conn.cursor()

        set_clouse = ", ".join(f"{key}= %s" for key in data.keys())

        logger.debug("update member %s in database: %s", id, data)
        cursor.execute(f"UPDATE members SET {set_clouse} WHERE id = %s", list(data.vales()) + [id])
        conn.commit()

        cursor.close()
        conn.close()


    def deactivate_member(id):
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("deactivates member %s in database", id)
        cursor.execute("UPDATE members SET is_active = FALSE WHERE id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()


    def activate_member(id):
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("activates member %s in database", id)
        cursor.execute("UPDATE members SET is_active = TRUE WHERE id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()


    def increment_borrows(id):
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("incrementes total borrows of member %s in database", id)
        cursor.execute("UPDATE members SET total_borrows = total_borrows + 1 WHERE id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()


    def count_active_members():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM members WHERE is_active = TRUE")
        count = cursor.fetchone()

        cursor.close()
        conn.close()
        return count
    

    def count_active_members():
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("gets count of active member %s in database", id)
        cursor.execute("SELECT * FROM members WHERE is_active = TRUE")
        count = cursor.fetchone()

        cursor.close()
        conn.close()
        return count
    

    def get_top_member():
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("gets the member with the most total borrows in database")
        cursor.execute("SELECT * FROM members ORDER BY total_borrows DESC LIMIT 1")
        top = cursor.fetchone()

        cursor.close()
        conn.close()
        return top