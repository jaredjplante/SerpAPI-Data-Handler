import databaseutils
import excelutils


def main():
    conn, cursor = databaseutils.open_db("JobData.sqlite")
    databaseutils.setup_db(cursor)
    databaseutils.close_db(conn)
    data = excelutils.get_excel_data("Sprint3Data.xlsx")
    print(data)


if __name__ == "__main__":
    main()
