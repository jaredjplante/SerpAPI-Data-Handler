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


def test_check_excel_table():
    # test to see if excel data matches table
    # assumes data was already written to table
    conn, cursor = databaseutils.open_db("JobData.sqlite")
    data = excelutils.get_excel_data("Sprint3Data.xlsx")
    cursor.execute("SELECT company_name, posted_at, job_title FROM listings_excel WHERE job_id = '2907e6de3fa805a1'")
    record = cursor.fetchone()
    assert data[0]['company_name'] == record[0]
    assert data[0]['posting_age'] == record[1]
    assert data[0]['job_title'] == record[2]
    cursor.execute("SELECT company_name, posted_at, job_title FROM listings_excel WHERE job_id = '1c693745ac26dbba'")
    record = cursor.fetchone()
    assert data[1]['company_name'] == record[0]
    assert data[1]['posting_age'] == record[1]
    assert data[1]['job_title'] == record[2]
    cursor.execute("SELECT company_name, posted_at, job_title FROM listings_excel WHERE job_id = 'ed15838c7b0e695f'")
    record = cursor.fetchone()
    assert data[2]['company_name'] == record[0]
    assert data[2]['posting_age'] == record[1]
    assert data[2]['job_title'] == record[2]

    databaseutils.close_db(conn)


def test_check_old_tables():
    conn, cursor = databaseutils.open_db("JobData.sqlite")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='listings'")
    table_bool = cursor.fetchone()
    assert table_bool
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='qualifications'")
    table_bool = cursor.fetchone()
    assert table_bool

    databaseutils.close_db(conn)
