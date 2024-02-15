import databaseutils


def main():
    conn, cursor = databaseutils.open_db("JobData.sqlite")
    databaseutils.setup_db(cursor)
    databaseutils.close_db(conn)


if __name__ == "__main__":
    main()
