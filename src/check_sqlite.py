from database_sqlite import DB_PATH, get_connection


def main():
    # Проверка не создаёт случайно новую пустую БД при пропущенном первом шаге.
    if not DB_PATH.exists():
        print('Сначала запустите init_sqlite.py.')
        return

    connection = get_connection()
    try:
        print('Проверка внешних ключей включена:',
              connection.execute('PRAGMA foreign_keys').fetchone()[0])

        print('\nКоличество записей:')
        for table in ('groups', 'teachers', 'students', 'lessons', 'attendance', 'users'):
            # Список имён таблиц задан в коде, а не введён пользователем.
            count = connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            print(f'{table}: {count}')

        print('\nУчётные записи (логин, роль, студент, преподаватель):')
        for row in connection.execute('''
            SELECT login, role, student_id, teacher_id
            FROM users ORDER BY user_id
        '''):
            print(row)

        print('\nПосещаемость группы 1 за октябрь 2026:')
        rows = connection.execute('''
            SELECT l.date, g.name, s.full_name, t.full_name, a.status
            FROM attendance AS a
            JOIN students AS s ON s.student_id = a.student_id
            JOIN lessons AS l ON l.lesson_id = a.lesson_id
            JOIN "groups" AS g ON g.group_id = l.group_id
            JOIN teachers AS t ON t.teacher_id = l.teacher_id
            WHERE l.group_id = ? AND l.date BETWEEN ? AND ?
            ORDER BY l.date, l.lesson_id, s.student_id
        ''', (1, '2026-10-01', '2026-10-31')).fetchall()
        for row in rows:
            print(row)

        print('\nНарушения внешних ключей:',
              connection.execute('PRAGMA foreign_key_check').fetchall())
    finally:
        connection.close()


if __name__ == '__main__':
    main()
