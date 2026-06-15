from database.db_connection import get_connection
from logs.setup_logger import logger


class MemberDB:
    def create_member(data):
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("Creates a new member in database: %s", data)
        cursor.execute(
        """
        INSERT INTO members (name, email, is_active, total_borrows) 
        VALUES (%s, %s, TRUE, 0)
        """,
        (data["name"], data["email"])
        )
        conn.commit()

        new_id = cursor.lastrowid

        cursor.close()
        conn.close()
        return new_id


    def get_all_members():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        logger.debug("Gets all members from database")
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows
    

    def get_member_by_id(id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        logger.debug("Gets member %s from database", id)
        cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return row
    

    def update_member(id, data):
        conn = get_connection()
        cursor = conn.cursor()

        set_clouse = ", ".join(f"{key}= %s" for key in data.keys())

        logger.debug("Update member %s in database: %s", id, data)
        cursor.execute(f"UPDATE members SET {set_clouse} WHERE id = %s", list(data.values()) + [id])
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

        logger.debug("Activates member %s in database", id)
        cursor.execute("UPDATE members SET is_active = TRUE WHERE id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()


    def increment_borrows(id):
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("Incrementes total borrows of member %s in database", id)
        cursor.execute("UPDATE members SET total_borrows = total_borrows + 1 WHERE id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()
    

    def count_active_members():
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("Gets count of active member %s in database", id)
        cursor.execute("SELECT COUNT(*) FROM members WHERE is_active = TRUE")
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return count
    

    def get_top_member():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        logger.debug("Gets the member with the most total borrows in database")
        cursor.execute("SELECT * FROM members ORDER BY total_borrows DESC LIMIT 1")
        top = cursor.fetchone()

        cursor.close()
        conn.close()
        return top
    

    def is_active(id):
        conn = get_connection()
        cursor = conn.cursor()

        logger.debug("Gets member %s activity", id)
        cursor.execute("SELECT is_active FROM members WHERE id = %s", (id,))
        is_active = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return is_active