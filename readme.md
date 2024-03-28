Requires:\
Install all packages inside requirements.txt\
pip install [package name]
****

Description:\
This project provides a GUI handler for the JobData.sqlite database. This database contains software development job listings from serpapi and an excel sheet. To run the GUI, run "guihandler.py" this will generate a list of the jobs from the "listings" and "listings_excel" tables in the database along with a map window marking the job locations. Select a job to get a description in a different window. There are also filters available. Entering a keyword in the "Enter keyword here" text box and hitting apply will update the job list with jobs that contain that keyword. Enter a location in the "Enter location here" text box and hit apply to filter for jobs in that location. Click apply on the "Remote Search" filter to see only jobs that allow remote work. Enter a minimum salary into the "Minimum salary: Enter int" text box and click apply to get jobs that have a minimum salary of the entered integer (no commas). The map will also updated with the filtered jobs whenever a filter is applied.

