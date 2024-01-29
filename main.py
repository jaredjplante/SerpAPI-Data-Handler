from serpapi import GoogleSearch
import secrets
params = {
  "engine": "google_jobs",
  "google_domain": "google.com",
  "q": "software developer",
  "hl": "en",
  "gl": "us",
  "location": "United States",
  "api_key": secrets.secretkey
}

search = GoogleSearch(params)
results = search.get_dict()