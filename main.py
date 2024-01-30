from serpapi import GoogleSearch
import secrets

#pagenum = 0
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


def get_data():
    search = GoogleSearch(params)
    results = search.get_dict()
    return results


def write_data():
    with open('JobData.txt', 'a', encoding='utf-8') as f:
        while params["start"] < 41:
            results = get_data()
            for key, value in results.items():
                if key == 'jobs_results':
                    f.write(f"{value}\n")
                    #for value in key2:
                        #f.write(f"{key2} : {value}\n")
            params["start"] += 10


def main():
    # clear txt
    f = open("JobData.txt", "w")
    f.close()
    write_data()


if __name__ == "__main__":
    main()
