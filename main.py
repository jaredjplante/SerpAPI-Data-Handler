from serpapi import GoogleSearch
import sqlite3
from typing import Tuple
import secrets

params = {
    "engine": "google_jobs",
    "google_domain": "google.com",
    "q": "software developer",
    "hl": "en",
    "gl": "us",
    "location": "United States",
    "start": 0,
    "api_key": secrets.secretkey
}


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
    age TEXT NOT NULL,
    description TEXT NOT NULL
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS qualifications(
    job_no INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    qualifications TEXT NOT NULL,
    FOREIGN KEY (job_no) REFERENCES listings (job_no)
    ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (title, company) REFERENCES listings (title, company)
    ON DELETE CASCADE ON UPDATE NO ACTION
    );''')


def get_data():  # add comment to test workflow
    search = GoogleSearch(params)
    results = search.get_dict()
    return results


def format_data(cursor: sqlite3.Cursor):
    while params["start"] < 41:
        results = get_data()
        for key, value in results.items():
            if key == 'jobs_results':
                for item in value:
                    title = 'na'
                    company = 'na'
                    location = 'na'
                    age = 'na'
                    description = 'na'
                    salary = 'Not Specified'
                    remote = 'Not Specified'
                    qualif = 'Not Specified'
                    for key2 in item.keys():
                        if key2 == 'title':
                            title = item.get(key2)
                        elif key2 == 'company_name':
                            company = item.get(key2)
                        elif key2 == 'location':
                            location = item.get(key2)
                        elif key2 == 'description':
                            description = item.get(key2)
                        elif key2 == 'extensions':
                            age = item.get(key2)[0]
                            if len(item.get(key2)) >= 2:
                                if item.get(key2)[1] == 'Work from home':
                                    remote = 'yes'
                        elif key2 == 'job_highlights':
                            qualifdict = item.get(key2)[0]
                            if qualifdict.get('title') == 'Qualifications':
                                qualiflist = qualifdict.get('items')
                                qualif = "\n".join(qualiflist)
                    write_to_database(title, company, location, age, description, salary, remote, qualif, cursor)

        params["start"] += 10


def write_to_database(title, company, location, age, description, salary, remote, qualif, cursor: sqlite3.Cursor):
    cursor.execute(f'''INSERT INTO LISTINGS (title, company, location, salary, remote, age, description)
    VALUES(?, ?, ?, ?, ?, ?, ?)''',
                   (title, company, location, salary, remote, age, description))
    cursor.execute(f'''INSERT INTO QUALIFICATIONS (title, company, qualifications)
    VALUES(?, ?, ?)''',
                   (title, company, qualif,))


def main():
    conn, cursor = open_db("JobData.sqlite")
    setup_db(cursor)
    format_data(cursor)
    close_db(conn)


if __name__ == "__main__":
    main()
