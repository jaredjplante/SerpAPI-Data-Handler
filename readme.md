Jared Plante Project 1

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
This project's purpose is to manage the JobData.sqlite database. The database includes the tables "listings", "qualifications", and "listings_excel". These tables contain job listings. For the listings and qualifications table, serpapi is used to grab data from a Google job search for software developer jobs. The data is scraped from the first five pages of results from the Google search.
Once the data is collected, the job listings are inserted into the listings and qualifications table from the JobData.sqlite database. The listings table includes columns for job number or job_no (primary key), title, company, location, salary, remote (work from home available or not), age (posting age), and description. The qualifications table includes columns for job number or job_no (primary key), title, company, and qualifications. The qualifications table includes foreign keys for the job_no, title, and company columns from the listings table. The "listings_excel" table in the JobData.sqlite database is created using the Sprint3Data.xlsx excel sheet. The data from the excel sheet is read in using openpyxl and written to the listings_excel table in the JobData.sqlite database. The listings_excel table includes columns for job_id (primary key), job_title, company_name, location, min_salary, max_salary, salary_time, and posted_at. Each row in the table represents the job information from the excel sheet. 
To run, run main.py. JobData.sqlite should already exist with the listings, qualifications, and listings_excel tables. main.py will setup the JobData.sqlite database and fill the listings_excel table values if they do not exist.

