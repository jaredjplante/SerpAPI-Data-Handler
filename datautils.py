from serpapi import GoogleSearch
import databaseutils
import secrets2
import sqlite3

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


def get_data():  # add comment to test workflow
    results = []
    while params["start"] < 41:
        search = GoogleSearch(params)
        results.append(search.get_dict())
        params["start"] += 10
    return results


def get_job_results(cursor: sqlite3.Cursor):
    results = get_data()
    for query in results:
        for key, value in query.items():
            if key == 'jobs_results':
                for item in value:
                    get_job_data(item, cursor)


def get_job_data(item, cursor: sqlite3.Cursor):
    title = item.get('title', 'na')
    company = item.get('company_name', 'na')
    location = item.get('location', 'na')
    description = item.get('description', 'na')
    age = 'Not Specified'
    salary = 'Not Specified'
    remote = 'Not Specified'
    qualif = 'Not Specified'
    extdict = item.get('detected_extensions', {})
    age = extdict.get('posted_at', age)
    if 'work_from_home' in extdict.keys():
        remote = 'Yes'
    salary = extdict.get('salary', salary)
    qualifdict = item.get('job_highlights')[0]
    if qualifdict.get('title') == 'Qualifications':
        qualiflist = qualifdict.get('items')
        qualif = "\n".join(qualiflist)
    databaseutils.write_to_tables(title, company, location, age, description, salary, remote, qualif, cursor)
