INSERT INTO "groups" (group_id, name)
VALUES (1, '26-ИВТ-4-1'), (2, '26-ИВТ-4-2')
ON CONFLICT (group_id) DO NOTHING;

INSERT INTO teachers (teacher_id, full_name)
VALUES
    (1, 'Морозов Андрей Петрович'),
    (2, 'Орлова Ирина Викторовна')
ON CONFLICT (teacher_id) DO NOTHING;

INSERT INTO students (student_id, full_name, group_id)
VALUES
    (1, 'Иванов Павел Сергеевич', 1),
    (2, 'Петрова Анна Андреевна', 1),
    (3, 'Сидоров Максим Олегович', 2),
    (4, 'Соколова Мария Игоревна', 2)
ON CONFLICT (student_id) DO NOTHING;

INSERT INTO lessons (lesson_id, date, group_id, teacher_id)
VALUES
    (1, '2026-10-21', 1, 1),
    (2, '2026-10-22', 1, 2),
    (3, '2026-10-21', 2, 2),
    (4, '2026-10-22', 2, 1)
ON CONFLICT (lesson_id) DO NOTHING;

INSERT INTO attendance (attendance_id, lesson_id, student_id, status)
VALUES
    (1, 1, 1, 'present'),
    (2, 1, 2, 'absent'),
    (3, 2, 1, 'excused'),
    (4, 2, 2, 'present'),
    (5, 3, 3, 'present'),
    (6, 3, 4, 'excused'),
    (7, 4, 3, 'absent'),
    (8, 4, 4, 'present')
ON CONFLICT (attendance_id) DO NOTHING;
