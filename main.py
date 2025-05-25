from config import config
from src.api_connection import HH
from src.db_manager import DBManager
from src.utils import create_database, save_data_to_database

list_of_companies = [
    "78638",
    "1740",
    "3529",
    "80",
    "11691810",
    "11485264",
    "856498",
    "8651204",
    "5685015",
    "9393023",
]


def main():
    params = config()
    create_database("vacancies_db", params)
    for employer in list_of_companies:
        vacancies = HH().load_vacancies(employer)
        save_data_to_database(vacancies, "vacancies_db", params)
    print("База данных была успешно создана.")
    db_manager = DBManager(
        database_name="vacancies_db",
        user=params["user"],
        password=params["password"],
        host=params["host"],
        port=params["port"],
    )
    while True:
        print("Выберете одно из желаемых действий, и введите его номер без точки")
        print(
            "1. Получить список всех компаний и количество вакансий у каждой компании"
        )
        print(
            """2. Получить список всех вакансий с указанием названия компании,
названия вакансии и зарплаты и ссылки на вакансию"""
        )
        print("3. Получить среднюю зарплату по вакансиям")
        print(
            "4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям"
        )
        print(
            "5. Получить список всех вакансий, в названии которых содержится ключевое слово"
        )
        print("6. Завершение работы")
        chosen_action = input("Введите номер желаемого действия: ")
        if chosen_action == "1":
            data = db_manager.get_companies_and_vacancies_count()
            for el in data:
                print(f"{el[0]}: {el[1]}")
        elif chosen_action == "2":
            data = db_manager.get_all_vacancies()
            for el in data:
                if el[2]:
                    print(
                        f"{el[1]}. Компания: {el[0]}, зарплата: {el[2]}, ссылка: {el[3]}"
                    )
                else:
                    print(
                        f"{el[1]}. Компания: {el[0]}, зарплата не указана, ссылка: {el[3]}"
                    )
        elif chosen_action == "3":
            data = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {data[0][0]}")
        elif chosen_action == "4":
            data = db_manager.get_vacancies_with_higher_salary()
            for el in data:
                print(f"{el[1]}. Компания: {el[0]}, зарплата: {el[2]}, ссылка: {el[3]}")
        elif chosen_action == "5":
            chosen_keyword = input("Введите ключевое слово для поиска: ")
            data = db_manager.get_vacancies_with_keyword(chosen_keyword)
            if data:
                for el in data:
                    if el[2]:
                        print(
                            f"{el[1]}. Компания: {el[0]}, зарплата: {el[2]}, ссылка: {el[3]}"
                        )
                    else:
                        print(
                            f"{el[1]}. Компания: {el[0]}, зарплата не указана, ссылка: {el[3]}"
                        )
            else:
                print(f"Вакансий по ключевому слову {chosen_keyword} не найдено")
        elif chosen_action == "6":
            db_manager.close_conn()
            print("Завершение работы")
            break
        else:
            print("Введены некорректные данные")


if __name__ == "__main__":
    main()
