import psycopg2

def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц, содержащих сведения о работодателях и вакансиях"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                    employer_id SERIAL PRIMARY KEY,
                    employer_name VARCHAR(255) NOT NULL,
                    employer_website_id INTEGER
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    vacancy_name VARCHAR NOT NULL,
                    salary_average NUMERIC,
                    vacancy_url TEXT
                )
            """)

    conn.commit()
    conn.close()

def save_data_to_database(data: list[dict], database_name: str, params: dict):
    """Функция сохраняет данные из API-ответа в базу данных"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        employer_data = data[0]["employer"]
        cur.execute(
            """
            INSERT INTO employers (employer_name, employer_website_id)
            VALUES (%s, %s)
            RETURNING employer_id
            """,
            (employer_data["name"], employer_data["id"])
        )
        employer_id = cur.fetchone()
        for vacancy in data:
            salary_data = vacancy["salary"]
            if salary_data:
                if salary_data["from"] and salary_data["to"]:
                    salary_avg = round((salary_data["from"] + salary_data["to"]) / 2, 2)
                elif salary_data["from"]:
                    salary_avg = salary_data["from"]
                else:
                    salary_avg = salary_data["to"]
            else:
                salary_avg = None
            cur.execute(
                """
                INSERT INTO vacancies (employer_id, vacancy_name, salary_average, vacancy_url)
                VALUES (%s, %s, %s, %s)
                """,
                (employer_id, vacancy["name"], salary_avg, vacancy["alternate_url"])
            )
    conn.commit()
    conn.close()


