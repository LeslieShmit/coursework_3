import psycopg2

class DBManager:
    """Класс для взаимодействия с базой данных"""
    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """Метод получает список всех компаний и количество вакансий у каждой компании"""
        conn = psycopg2.connect(dbname=self.database_name, params=self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT employer_name, COUNT(vacancy_id) AS vacancy_count 
                FROM employers
                LEFT JOIN vacancies USING(employer_id)
                GROUP BY employer_name
                """
            )
            data = cur.fetchall()
        conn.close()
        return data


    def get_all_vacancies(self):
        """Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        conn = psycopg2.connect(dbname=self.database_name, params=self.params)
        with conn.cursor() as cur:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT employer_name, vacancy_name, salary_average, vacancy_url
                    FROM vacancies
                    LEFT JOIN employers
                    USING(employer_id)
                    """
                )
                data = cur.fetchall()
            conn.close()
            return data

    def get_avg_salary(self):
        """Метод получает среднюю зарплату по вакансиям"""
        conn = psycopg2.connect(dbname=self.database_name, params=self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT ROUND(AVG(salary_average)) FROM vacancies
                """
            )
            data = cur.fetchall()
        conn.close()
        return data

    def get_vacancies_with_higher_salary(self):
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        conn = psycopg2.connect(dbname=self.database_name, params=self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT employer_name, vacancy_name, salary_average, vacancy_url
                FROM vacancies
                LEFT JOIN employers
                USING(employer_id)
                WHERE salary_average > (SELECT AVG(salary_average) FROM vacancies)
                """
            )
            data = cur.fetchall()
        conn.close()
        return data

    def get_vacancies_with_keyword(self, keyword):
        """Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        conn = psycopg2.connect(dbname=self.database_name, params=self.params)
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT employer_name, vacancy_name, salary_average, vacancy_url
                FROM vacancies
                LEFT JOIN employers
                USING(employer_id)
                WHERE vacancy_name ILIKE '%{keyword}s%'
                """
            )
            data = cur.fetchall()
        conn.close()
        return data


