import databaseutils
import datautils


def main():
    conn, cursor = databaseutils.open_db("JobData.sqlite")
    databaseutils.setup_db(cursor)
    datautils.get_job_results(cursor)
    databaseutils.close_db(conn)


if __name__ == "__main__":
    main()
