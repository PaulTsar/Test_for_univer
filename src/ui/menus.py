from __future__ import annotations
from models.user import User
from repositories import group_repository, lesson_repository, student_repository, attendance_repository
from services import attendance_service


def admin_menu(user: User):
    while True:
        print(f"\n=== Меню Администратора ({user.login}) ===")
        print("1. Показать всех студентов")
        print("2. Показать все группы")
        print("3. Добавить группу")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            students = student_repository.get_all()
            print("\nСписок студентов:")
            for s in students:
                print(f"ID: {s.student_id} | {s.full_name} | Группа: {s.group_name}")
        elif choice == "2":
            groups = group_repository.get_all()
            print("\nСписок групп:")
            for g in groups:
                print(f"ID: {g.group_id} | {g.name}")
        elif choice == "3":
            name = input("Введите название новой группы: ").strip()
            if name:
                group_repository.create(name)
                print("Группа успешно добавлена!")
            else:
                print("Название не может быть пустым.")
        elif choice == "0":
            break
        else:
            print("Неверный ввод.")


def teacher_menu(user: User):
    while True:
        print(f"\n=== Меню Преподавателя ({user.login}) ===")
        print("1. Мои занятия")
        print("2. Отметить посещаемость на занятии")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            lessons = lesson_repository.get_all()
            my_lessons = [l for l in lessons if l.teacher_id == user.teacher_id]
            print("\nВаши занятия:")
            for l in my_lessons:
                print(f"ID: {l.lesson_id} | Дата: {l.date} | Группа: {l.group_name}")
        elif choice == "2":
            try:
                lesson_id = int(input("Введите ID занятия: ").strip())
                student_id = int(input("Введите ID студента: ").strip())
                print("Статусы: 1 - Присутствовал (present), 2 - Отсутствовал (absent), 3 - Уважительная (excused)")
                status_choice = input("Выберите статус (1/2/3): ").strip()

                status_map = {"1": "present", "2": "absent", "3": "excused"}
                status = status_map.get(status_choice)

                if not status:
                    print("Неверный статус.")
                    continue

                attendance_service.mark_attendance(user, lesson_id, student_id, status)
                print("Посещаемость успешно отмечена!")
            except ValueError:
                print("ID должны быть числами.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            break
        else:
            print("Неверный ввод.")


def student_menu(user: User):
    while True:
        print(f"\n=== Меню Студента ({user.login}) ===")
        print("1. Моя посещаемость")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            if not user.student_id:
                print("Ошибка: у вашей учетной записи нет привязки к студенту.")
                continue

            attendances = attendance_service.get_student_attendance(user.student_id)
            print("\nВаша посещаемость:")
            if not attendances:
                print("Записей пока нет.")
            for att in attendances:
                date_str = att.lesson_date if att.lesson_date else "Дата не указана"
                print(f"{date_str} | Статус: {att.status_name}")
        elif choice == "0":
            break
        else:
            print("Неверный ввод.")