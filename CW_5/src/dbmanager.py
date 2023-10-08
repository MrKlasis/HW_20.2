import psycopg2

class DBManager:
    def __init__(self, host, port, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

    def save_to_database(self, vacancies):
        cur = self.conn.cursor()
        #сохранение данных в ДБ
        for vacancy in vacancies['items']:
            vacancy_id = vacancy['id']
            vacancy_name = vacancy['name']
            vacancy_salary_min = vacancy['salary']['from'] if vacancy['salary'] and 'from' in vacancy[
                'salary'] else None
            vacancy_salary_max = vacancy['salary']['to'] if vacancy['salary'] and 'to' in vacancy['salary'] else None
            vacancy_url = vacancy['url']
            vacancy_company_id = vacancy['employer']['id'] if vacancy['employer'] and 'id' in vacancy[
                'employer'] else None

            # Проверка, существует ли запись с таким id в таблице "vacancies"
            cur.execute("""
                SELECT id FROM vacancies WHERE id = %s
            """, (vacancy_id,))
            existing_vacancy = cur.fetchone()

            if existing_vacancy:
                print(f"Запись с id={vacancy_id} уже существует в таблице 'vacancies'. Пропускаем вставку.")
                continue

            # Вставка данных в таблицу "companies"
            cur.execute("""
                INSERT INTO companies (id, name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (vacancy_company_id, vacancy['employer']['name']))

            # Вставка данных в таблицу "vacancies"
            cur.execute("""
                INSERT INTO vacancies (id, name, salary_min, salary_max, url, company_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (vacancy_id, vacancy_name, vacancy_salary_min, vacancy_salary_max, vacancy_url, vacancy_company_id))

        self.conn.commit()
        cur.close()

    def get_companies_and_vacancies_count(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT companies.name, COUNT(vacancies.id)
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.company_id
            GROUP BY companies.name;
        """)
        return cur.fetchall()

    def get_all_vacancies(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id;
        """)
        return cur.fetchall()

    def get_avg_salary(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT AVG(salary_min + salary_max) / 2
            FROM vacancies;
        """)
        return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        cur = self.conn.cursor()
        cur.execute("""
            SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
            WHERE (vacancies.salary_min + vacancies.salary_max) / 2 > %s;
        """, (avg_salary,))
        return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
            WHERE vacancies.name ILIKE %s;
        """, ('%' + keyword + '%',))
        return cur.fetchall()

