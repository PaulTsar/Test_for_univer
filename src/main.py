from init_sqlite import main as init_database
from ui.auth_ui import login_screen
from ui.menus import admin_menu, teacher_menu, student_menu


def main():
    print("=====================================")
    print("  Система учёта посещаемости студентов  ")
    print("=====================================")

    print("Подготовка базы данных...")
    init_database()

    user = login_screen()

    if user.is_admin:
        admin_menu(user)
    elif user.is_teacher:
        teacher_menu(user)
    elif user.is_student:
        student_menu(user)


if __name__ == "__main__":
    main()