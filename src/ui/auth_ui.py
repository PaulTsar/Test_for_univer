from __future__ import annotations
from services import auth_service


def login_screen():
    print("\n=== Вход в систему ===")
    print("Для теста используйте логины: admin, teacher1, student1")
    print("Пароль для всех: Demo123!")

    while True:
        login = input("Логин: ").strip()
        password = input("Пароль: ").strip()

        user = auth_service.authenticate(login, password)
        if user:
            print(f"\nДобро пожаловать, {user.login} ({user.role_name})!")
            return user
        else:
            print("Неверный логин или пароль. Попробуйте снова.\n")