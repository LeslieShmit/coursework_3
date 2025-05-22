import psycopg2

def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц, содержащих сведения о работодателях и вакансиях"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                    employer_id SERIAL PRIMARY KEY,
                    employer_name VARCHAR(255) NOT NULL,
                    employer_website_id INTEGER,
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    vacancy_name VARCHAR NOT NULL,
                    salary_average REAL,
                    employer_url TEXT
                )
            """)

    conn.commit()
    conn.close()