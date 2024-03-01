import databaseutils
import datautils
import excelutils
import guihandler

import sys
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from PySide6.QtWidgets import QApplication, QListWidget, QListWidgetItem, QWidget, QTextEdit, QLineEdit, QPushButton


def test_web_data():
    job_data = datautils.get_data()
    num_jobs = 0
    for query in job_data:
        for key, value in query.items():
            if key == 'jobs_results':
                num_jobs += len(value)
    assert num_jobs >= 50


def test_write_database():
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
    databaseutils.write_to_excel_table("500",
                                       "Test Title Excel",
                                       "Test Company Excel",
                                       "Test Location Excel",
                                       "Min Salary Excel",
                                       "Max Salary Excel",
                                       "Salary Time Excel",
                                       "5 minutes ago",
                                       cursor)
    cursor.execute("SELECT company, location, age, salary FROM listings WHERE title = 'Test Title'")
    record = cursor.fetchone()
    assert record[0] == "Test Company"
    assert record[1] == "Test Location"
    assert record[2] == "50000 days ago"
    assert record[3] == "5 dollars"
    cursor.execute("SELECT company_name, location, posted_at, min_salary, max_salary FROM listings_excel WHERE "
                   "job_title"
                   "= 'Test Title Excel'")
    record = cursor.fetchone()
    assert record[0] == "Test Company Excel"
    assert record[1] == "Test Location Excel"
    assert record[2] == "5 minutes ago"
    assert record[3] == "Min Salary Excel"
    assert record[4] == "Max Salary Excel"
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


def create_gui():
    QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.Software)
    data = [["Software Engineer, Full Stack", "Capital One", "us, New York, NY 10012"],
            ["Entry Level Java Developer", "SummitWorks Technologies Inc", "us, Boston, MA"],
            ["Lead Software Engineer", "Free From Market", "us, Kansas City, MO"],  # $$$
            ["Software Developer", "Atlas", " Anywhere "]]
    window = guihandler.MainWindow(data)
    window.keyword_input.setText("java")
    window.location_filter.setText("new york")
    window.salary_input.setText("150000")
    # clicking the remote button will filter for remote jobs
    return window

def create_instance():
    if not QApplication.instance():
        qt_app = QApplication(sys.argv)
    else:
        qt_app = QApplication.instance()
    return qt_app
def test_keyword():
    qt_app = create_instance()
    job = guihandler.MainWindow.apply_keyword(create_gui())
    assert len(job) == 1
    assert job[0] == 'Entry Level Java Developer ||| SummitWorks Technologies Inc'
    qt_app.quit()



def test_location():
    qt_app = create_instance()
    job = guihandler.MainWindow.apply_location(create_gui())
    assert len(job) == 1
    assert job[0] == 'Software Engineer, Full Stack ||| Capital One'
    qt_app.quit()
