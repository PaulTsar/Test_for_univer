from init_sqlite import main as init_database
from check_sqlite import main as show_database

def main():
    print("Hello, World!")
    print("Система учёта посещаемости студентов")
    print("Учебный проект")
    print("Программа успешно запущена.")

    init_database()
    show_database()


if __name__ == "__main__":
    main()
