import databaseutils
import datautils
import excelutils


def test_web_data():
    job_data = datautils.get_data()
    num_jobs = 0
    for query in job_data:
        for key, value in query.items():
            if key == 'jobs_results':
                num_jobs += len(value)
    assert num_jobs >= 50


def test_database():
    conn, cursor = databaseutils.open_db("test.sqlite")
    databaseutils.setup_db(cursor)
    databaseutils.write_to_tables("Test Title",
                                  "Test Company",
                                  "Test Location",
                                  "50000 days ago",
                                  "This is a test description!",
                                  "5 dollars",
                                  "Yes",
                                  "Must have 10 years of experience",
                                  cursor)
    cursor.execute("SELECT company, location, age, salary FROM listings WHERE title = 'Test Title'")
    record = cursor.fetchone()
    assert record[0] == "Test Company"
    assert record[1] == "Test Location"
    assert record[2] == "50000 days ago"
    assert record[3] == "5 dollars"
    databaseutils.close_db(conn)


def test_excel_columns():
    data = excelutils.get_excel_data("Sprint3Data.xlsx")
    for row in data:
        columns = [row['job_id'], row['job_title'], row['company_name'],
                   row['location'], row['min_salary'], row['max_salary'],
                   row['salary_time'], row['posting_age']]
        assert len(columns) == 8


def test_excel_rows():
    data = excelutils.get_excel_data("Sprint3Data.xlsx")
    assert len(data) >= 300
