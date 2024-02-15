import sqlite3
from typing import Tuple


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS listings(
    job_no INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    salary TEXT NOT NULL DEFAULT 'Not Specified',
    remote TEXT NOT NULL DEFAULT 'Not Specified',
    age TEXT NOT NULL DEFAULT 'Not Specified',
    description TEXT NOT NULL
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS qualifications(
    job_no INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    qualifications TEXT NOT NULL DEFAULT 'Not Specified',
    FOREIGN KEY (job_no) REFERENCES listings (job_no)
    ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (title, company) REFERENCES listings (title, company)
    ON DELETE CASCADE ON UPDATE NO ACTION
    );''')


def write_to_database(title, company, location, age, description, salary, remote, qualif, cursor: sqlite3.Cursor):
    cursor.execute('''INSERT INTO LISTINGS (title, company, location, salary, remote, age, description)
    VALUES(?, ?, ?, ?, ?, ?, ?)''',
                   (title, company, location, salary, remote, age, description))
    cursor.execute('''INSERT INTO QUALIFICATIONS (title, company, qualifications)
    VALUES(?, ?, ?)''',
                   (title, company, qualif,))
