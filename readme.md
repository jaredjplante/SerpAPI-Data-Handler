Jared Plante Project 1: Sprint 1

Requires:\
Python 3.9-3.10\
google-search-results:\
    &nbsp;&nbsp;&nbsp;&nbsp;pip install google-search-results\
serpapi:\
    &nbsp;&nbsp;&nbsp;&nbsp;pip install serpapi\
secrets.py:\
    &nbsp;&nbsp;&nbsp;&nbsp;create a secrets.py file in the project's directory and add this line with your api key:\
    &nbsp;&nbsp;&nbsp;&nbsp;secretkey = "enter key here"

Description:\
This project uses serpapi to grab data from a Google job search for software developer jobs. The data is scraped from the first five pages of results from the Google search.
Once the data is collected, the job listings are put into a readable format into a textfile called "JobData.txt".
To run, run main.py. The JobData.txt will be created or cleared if it already exists and will be overwritten with the scraped data.

