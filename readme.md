Jared Plante Project 1: Sprint 1

Requires:\
Python 3.9-3.10\
google-search-results:\
    &nbsp;&nbsp;&nbsp;&nbsp;pip install google-search-results\
serpapi:\
    &nbsp;&nbsp;&nbsp;&nbsp;pip install serpapi\
secrets.py:\
    &nbsp;&nbsp;&nbsp;&nbsp;create a secrets.py file in the project's directory and add this line with your api key:\
    &nbsp;&nbsp;&nbsp;&nbsp;secretkey = "enter key here"\
openpyxl:\
    &nbsp;&nbsp;&nbsp;&nbsp;pip install openpyxl
****

Description:\
This project uses serpapi to grab data from a Google job search for software developer jobs. The data is scraped from the first five pages of results from the Google search.
Once the data is collected, the job listings are inserted into a "listings" and "qualifications" table from the JobData.sqlite database. The listings table includes columns for job number or job_no (primary key), title, company, location, salary, remote (work from home available or not), age (posting age), and description. The qualifications table includes columns for job number or job_no (primary key), title, company, and qualifications. The qualifications table includes foreign keys for the job_no, title, and company columns from the listings table.
To run, run main.py. JobData.sqlite will be created and the job data will be inserted if the database does not already exist.

