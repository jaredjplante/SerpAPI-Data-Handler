import sqlite3

import openpyxl
import databaseutils


def get_excel_data(filename):
    total_data = []
    excel_sheet = openpyxl.load_workbook(filename)
    sheet = excel_sheet.active
    for row in sheet.rows:
        company_name = row[0].value
        posting_age = row[1].value
        job_id = row[2].value
        location = f'{row[3].value}, {row[4].value}'
        max_salary = row[6].value
        min_salary = row[7].value
        salary_time = row[8].value
        job_title = row[9].value
        row_dict = {
            'company_name': company_name,
            'posting_age': posting_age,
            'job_id': job_id,
            'location': location,
            'max_salary': max_salary,
            'min_salary': min_salary,
            'salary_time': salary_time,
            'job_title': job_title
        }
        total_data.append(row_dict)
    # remove headers
    total_data.pop(0)
    return total_data


def write_excel_data(data: list[dict], cursor: sqlite3.Cursor):
    for row_dict in data:
        databaseutils.write_to_excel_table(row_dict['job_id'], row_dict['job_title'], row_dict['company_name'],
                                           row_dict['location'], row_dict['min_salary'], row_dict['max_salary'],
                                           row_dict['salary_time'], row_dict['posting_age'], cursor)
