CREATE TABLE IF NOT EXISTS "groups" (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES "groups" (group_id)
);

CREATE TABLE IF NOT EXISTS lessons (
    lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    group_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES "groups" (group_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
);

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    status TEXT NOT NULL
        CHECK (status IN ('present', 'absent', 'excused')),
    FOREIGN KEY (lesson_id) REFERENCES lessons (lesson_id),
    FOREIGN KEY (student_id) REFERENCES students (student_id),
    UNIQUE (lesson_id, student_id)
);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'teacher', 'student')),
    student_id INTEGER UNIQUE,
    teacher_id INTEGER UNIQUE,
    FOREIGN KEY (student_id) REFERENCES students (student_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id),
    CHECK (
        (role = 'admin' AND student_id IS NULL AND teacher_id IS NULL)
        OR
        (role = 'student' AND student_id IS NOT NULL AND teacher_id IS NULL)
        OR
        (role = 'teacher' AND teacher_id IS NOT NULL AND student_id IS NULL)
    )
);
