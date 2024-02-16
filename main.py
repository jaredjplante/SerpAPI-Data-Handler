import databaseutils
import excelutils


def main():
    conn, cursor = databaseutils.open_db("JobData.sqlite")
    databaseutils.setup_db(cursor)
    data = excelutils.get_excel_data("Sprint3Data.xlsx")
    excelutils.write_excel_data(data, cursor)
    databaseutils.close_db(conn)


if __name__ == "__main__":
    main()
