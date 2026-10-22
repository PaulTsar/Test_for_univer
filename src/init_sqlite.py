import hashlib
import secrets

from database_sqlite import DB_PATH, PROJECT_DIR, get_connection


def make_password_hash(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 600000)
    return f'pbkdf2_sha256$600000${salt.hex()}${digest.hex()}'


def main():
    schema = (PROJECT_DIR / 'schema_sqlite.sql').read_text(encoding='utf-8')
    seed = (PROJECT_DIR / 'seed_sqlite.sql').read_text(encoding='utf-8')

    # user_id, login, role, student_id, teacher_id.
    users = [
        (1, 'admin', 'admin', None, None),
        (2, 'teacher1', 'teacher', None, 1),
        (3, 'teacher2', 'teacher', None, 2),
        (4, 'student1', 'student', 1, None),
        (5, 'student2', 'student', 2, None),
        (6, 'student3', 'student', 3, None),
        (7, 'student4', 'student', 4, None),
    ]

    connection = get_connection()
    try:
        connection.executescript('BEGIN;\n' + schema + '\n' + seed)

        for user_id, login, role, student_id, teacher_id in users:
            exists = connection.execute(
                'SELECT 1 FROM users WHERE user_id = ?', (user_id,)
            ).fetchone()
            if exists:
                continue

            connection.execute('''
                INSERT INTO users
                    (user_id, login, password_hash, role, student_id, teacher_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id, login, make_password_hash('Demo123!'),
                role, student_id, teacher_id,
            ))

        connection.commit()
        print('Таблицы и тестовые данные готовы.')
        print('Файл базы:', DB_PATH)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == '__main__':
    main()
