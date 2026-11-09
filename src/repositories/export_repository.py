from database_sqlite import get_connection


def get_students_for_export():
    connection = get_connection()

    try:
        cursor = connection.execute('''
            SELECT
                s.student_id,
                s.full_name,
                g.group_id,
                g.name
            FROM students AS s
            LEFT JOIN "groups" AS g
                ON s.group_id = g.group_id
            ORDER BY s.student_id
        ''')

        rows = cursor.fetchall()
        return rows

    finally:
        connection.close()