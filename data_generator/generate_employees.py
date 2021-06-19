import random
import datetime

from faker import Faker
from dateutil.relativedelta import relativedelta

faker = Faker('pt_BR')
employee_count = 50
output_file = "generated_employees.sql"
today = datetime.datetime.now()
plus_month = relativedelta(months=1)
minus_day = relativedelta(days=1)

if __name__ == '__main__':
    employees = []
    payrolls = []
    payroll_items = []
    payroll_id = 1

    ROLES = {
        1: {
            "salary": 4000
        },
        2: {
            "salary": 2000
        },
        3: {
            "salary": 1600
        },
        4: {
            "salary": 1700
        },
        5: {
            "salary": 1700
        }
    }

    print(f"Generating {str(employee_count)} employees...")

    for employee_id in range(1, employee_count):
        role = random.choice(list(range(1, 6)))
        salary = ROLES[role]["salary"]
        employee = {
            "name": faker.name(),
            "cpf": faker.cpf(),
            "rg": faker.rg(),
            "birth_date": faker.date_between(start_date='-30y', end_date='-18y').strftime("%Y-%m-%d"),
            "role_id": role,
            "hire_date": faker.date_between(start_date='-2y', end_date='today').strftime("%Y-%m-%d"),
            "resignation_date": None,
            "salary": salary,
        }
        employees.append({
            "employee_id": employee_id,
            "line": f"INSERT INTO employee VALUES(DEFAULT, '{employee['name']}', '{employee['cpf']}', '{employee['rg']}',"
            f"'{employee['birth_date']}', {employee['role_id']}, '{employee['hire_date']}', "
            f"NULL, {employee['salary']});"
        })
        split_date = employee['hire_date'].split('-')
        next_salary = datetime.datetime(int(split_date[0]), int(split_date[1]), 5) + plus_month

        while next_salary < today:
            while next_salary.weekday() > 4:
                next_salary = next_salary - minus_day

            payrolls.append(
                {
                    "employee_id": employee_id,
                    "payroll_id": payroll_id,
                    "line": f"INSERT INTO payroll VALUES(DEFAULT, {employee_id}, {salary}, true, "
                            f"'{next_salary.strftime('%Y-%m-%d')}');"
                }
            )

            payroll_items.append(
                {
                    "payroll_id": payroll_id,
                    "line": f"INSERT INTO payroll_item VALUES(DEFAULT, {payroll_id}, 'Salário', 'salary', {salary});"
                }
            )

            payroll_id += 1
            next_salary = next_salary.replace(day=5)
            next_salary = next_salary + plus_month

    print(f"Writting SQL Statements to {output_file}...")
    with open(output_file, "w", encoding='UTF-8') as of:
        for final in employees:
            of.write(final["line"] + "\n")

            for payroll in payrolls:
                if payroll['employee_id'] != final['employee_id']:
                    continue
                of.write(payroll["line"] + "\n")

                for payroll_item in payroll_items:
                    if payroll_item['payroll_id'] != payroll['payroll_id']:
                        continue
                    of.write(payroll_item["line"] + "\n")
            of.write("-- END EMPLOYEE" + "\n")

    print("Done!")