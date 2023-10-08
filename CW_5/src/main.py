import requests
from settings import host, port, database, user, password
from dbmanager import DBManager

# Функция для получения данных о вакансиях с API hh.ru
def get_vacancies():
    url = "https://api.hh.ru/vacancies"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Инициализируем объект DBManager
db_manager = DBManager(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

# Создание таблицы vacancies, если она не существует
create_table_query = """
    CREATE TABLE IF NOT EXISTS companies (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255)
    );
"""
cur = db_manager.conn.cursor()
cur.execute(create_table_query)
db_manager.conn.commit()

create_table_query = """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        salary_min INTEGER,
        salary_max INTEGER,
        url VARCHAR(255),
        company_id INTEGER,
        CONSTRAINT company FOREIGN KEY(company_id) REFERENCES companies(id) ON DELETE SET NULL
    );
"""
cur.execute(create_table_query)
db_manager.conn.commit()

# Получаем данные о вакансиях
vacancies_data = get_vacancies()

if vacancies_data:
    # Сохраняем данные в базу данных
    db_manager.save_to_database(vacancies_data)
    print("Данные успешно сохранены в базу данных.")

    # Проверяем методы класса DBManager
    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
    print("Компании и количество вакансий:")
    for row in companies_and_vacancies_count:
        print(row)

    all_vacancies = db_manager.get_all_vacancies()
    print("Все вакансии:")
    for row in all_vacancies:
        print(row)

    avg_salary = db_manager.get_avg_salary()
    print("Средняя зарплата:", avg_salary)

    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
    print("Вакансии с зарплатой выше средней:")
    for row in vacancies_with_higher_salary:
        print(row)

    keyword = "python"
    vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
    print("Вакансии с ключевым словом", keyword)
    for row in vacancies_with_keyword:
        print(row)
else:
    print("Не удалось получить данные о вакансиях.")
