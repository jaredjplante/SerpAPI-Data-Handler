import sys

from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from PySide6.QtWidgets import QApplication, QListWidget, QListWidgetItem, QWidget, QTextEdit

import databaseutils


class MainWindow(QWidget):
    def __init__(self, data_to_show):
        super().__init__()
        self.list_control = None
        self.job_info = None
        self.location = "Not Specified"
        self.age = "Not Specified"
        self.remote = "Not Specified"
        self.salary = "Not Specified"
        self.mins = "Not Specified"
        self.maxs = "Not Specified"
        self.data = data_to_show
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("Software Developer Job Listings")
        # job list
        list = QListWidget(self)
        self.list_control = list
        for item1, item2 in self.data:
            list_item = QListWidgetItem(f"{item1} ||| {item2}", listview=self.list_control)
        self.list_control.currentItemChanged.connect(self.write_job_info)
        list.resize(600, 500)
        # info text box
        self.job_info = QTextEdit()
        self.job_info.setReadOnly(True)
        self.job_info.setGeometry(1250, 275, 500, 500)
        self.show()
        self.job_info.show()

    def write_job_info(self, selection):
        selected_data = selection.data(0)
        data_values = selected_data.split(" ||| ")
        self.get_job_info(data_values[0], data_values[1])

    def get_job_info(self, title, company):
        conn, cursor = databaseutils.open_db("JobData.sqlite")
        cursor.execute("SELECT location, age, remote, salary FROM listings WHERE title = ? AND company = ?",
                       (title, company))
        results = cursor.fetchone()
        if results:
            self.location, self.age, self.remote, self.salary = results
            self.job_info.setText(
                f"Location: {self.location}, Age: {self.age}, Remote: {self.remote}, Salary: {self.salary}")
        else:
            cursor.execute(
                "SELECT location, posted_at, min_salary, max_salary FROM listings_excel WHERE job_title = ? AND "
                "company_name = ?",
                (title, company))
            results = cursor.fetchone()
            self.location, self.age, self.mins, self.maxs = results
            self.job_info.setText(
                f"Location: {self.location}, Age: {self.age}, Remote: Not Specified, Salary: {self.mins} to {self.maxs}")


def get_job_titles():
    conn, cursor = databaseutils.open_db("JobData.sqlite")
    cursor.execute("SELECT title, company FROM listings")
    title_data = cursor.fetchall()
    cursor.execute("SELECT job_title, company_name FROM listings_excel")
    title_data_excel = cursor.fetchall()
    databaseutils.close_db(conn)
    return title_data + title_data_excel


def main():
    QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.Software)
    data = get_job_titles()
    qt_app = QApplication(sys.argv)
    window = MainWindow(data)
    sys.exit(qt_app.exec())


if __name__ == '__main__':
    main()
