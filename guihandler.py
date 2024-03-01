import sys

from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from PySide6.QtWidgets import QApplication, QListWidget, QListWidgetItem, QWidget, QTextEdit, QLineEdit, QPushButton

import mapwindow
import databaseutils

class job():
    def __init__(self, data_to_show):
        super().__init__()
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
        self.salarytime = "Not Specified"
        self.qualifications = "Not Specified"
        self.maplist = []
        self.data = data_to_show
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("Software Developer Job Listings")
        self.setGeometry(250,275,850,500)
        # job list
        list = QListWidget(self)
        self.list_control = list
        for item1, item2, item3 in self.data:
            list_item = QListWidgetItem(f"{item1} ||| {item2}", listview=self.list_control)
            self.maplist.append(item3)
        self.list_control.currentItemChanged.connect(self.write_job_info)
        list.resize(600, 500)
        # info text box
        self.job_info = QTextEdit()
        self.job_info.setReadOnly(True)
        self.job_info.setGeometry(1250, 275, 500, 500)
        # map creation
        self.mapwindow = mapwindow.mapwindow(self.maplist)
        # filters
        self.keyword_input = QLineEdit(self)
        self.keyword_input.setPlaceholderText("Enter keyword here")
        self.keyword_input.setGeometry(600, 10, 180, 30)

        self.filter_button = QPushButton("Apply", self)
        self.filter_button.setGeometry(775, 10, 50, 30)
        self.filter_button.clicked.connect(self.apply_keyword)

        self.location_filter = QLineEdit(self)
        self.location_filter.setPlaceholderText("Enter location here")
        self.location_filter.setGeometry(600, 50, 180, 30)

        self.filter_button = QPushButton("Apply", self)
        self.filter_button.setGeometry(775, 50, 50, 30)
        self.filter_button.clicked.connect(self.apply_location)

        self.remote_filter = QLineEdit(self)
        self.remote_filter.setPlaceholderText("Remote Search")
        self.remote_filter.setGeometry(600, 90, 180, 30)

        self.filter_button = QPushButton("Apply", self)
        self.filter_button.setGeometry(775, 90, 50, 30)
        self.filter_button.clicked.connect(self.apply_remote)

        self.salary_input = QLineEdit(self)
        self.salary_input.setPlaceholderText("Minimum salary: Enter int")
        self.salary_input.setGeometry(600, 130, 180, 30)

        self.filter_button = QPushButton("Apply", self)
        self.filter_button.setGeometry(775, 130, 50, 30)
        self.filter_button.clicked.connect(self.apply_salary)

        # show
        self.show()
        self.mapwindow.show()
        self.job_info.show()


    def apply_keyword(self):
        jobs_to_keep = []
        keyword = self.keyword_input.text()
        for index in range(self.list_control.count()):
            item = self.list_control.item(index)
            item.setHidden(keyword.lower() not in item.text().lower())
            if not self.list_control.item(index).isHidden():
                job_text = self.list_control.item(index).text()
                jobs_to_keep.append(job_text)
        self.map_filter()
        return jobs_to_keep



    def apply_location(self):
        jobs_to_keep = []
        location = self.location_filter.text()
        for index in range(self.list_control.count()):
            if not self.list_control.item(index).isHidden():
                item = self.list_control.item(index).text()
                data_values = item.split(" ||| ")
                self.get_job_info(data_values[0], data_values[1])
                self.job_info.clear()
                if location.lower() in self.location.lower():
                    jobs_to_keep.append(f"{data_values[0]} ||| {data_values[1]}")
        self.list_control.clear()
        for item in jobs_to_keep:
            list_item = QListWidgetItem(item, listview=self.list_control)
        self.map_filter()
        return jobs_to_keep


    def apply_remote(self):
        jobs_to_keep = []
        for index in range(self.list_control.count()):
            if not self.list_control.item(index).isHidden():
                item = self.list_control.item(index).text()
                data_values = item.split(" ||| ")
                self.get_job_info(data_values[0], data_values[1])
                self.job_info.clear()
                if self.remote == "Yes":
                    jobs_to_keep.append(f"{data_values[0]} ||| {data_values[1]}")
        self.list_control.clear()
        for item in jobs_to_keep:
            list_item = QListWidgetItem(item, listview=self.list_control)
        self.map_filter()
        return jobs_to_keep


    def apply_salary(self):
        jobs_to_keep = []
        int_compare_salary = 999999999
        salary = self.salary_input.text()
        try:
            int_salary = int(salary)
        except ValueError as e:
            self.job_info.clear()
            self.job_info.setText("Enter an int!")
            return
        for index in range(self.list_control.count()):
            if not self.list_control.item(index).isHidden():
                item = self.list_control.item(index).text()
                data_values = item.split(" ||| ")
                self.get_job_info(data_values[0], data_values[1])
                self.job_info.clear()
                try:
                    int_compare_salary = int(self.salary)
                except ValueError as e:
                    try:
                        int_compare_salary = int(self.mins)
                    except ValueError as e:
                        continue
                if int_compare_salary > int_salary:
                    jobs_to_keep.append(f"{data_values[0]} ||| {data_values[1]}")
        self.list_control.clear()
        for item in jobs_to_keep:
            list_item = QListWidgetItem(item, listview=self.list_control)
        self.map_filter()
        return jobs_to_keep

    def map_filter(self):
        jobs_to_keep = []
        for index in range(self.list_control.count()):
            if not self.list_control.item(index).isHidden():
                item = self.list_control.item(index).text()
                data_values = item.split(" ||| ")
                self.get_job_info(data_values[0], data_values[1])
                self.job_info.clear()
                jobs_to_keep.append(self.location)
        self.mapwindow.filter_map(jobs_to_keep)


    def write_job_info(self, selection):
        try:
            selected_data = selection.data(0)
            data_values = selected_data.split(" ||| ")
            self.get_job_info(data_values[0], data_values[1])
        except AttributeError as e:
            pass

    def get_job_info(self, title, company):
        conn, cursor = databaseutils.open_db("JobData.sqlite")
        cursor.execute("SELECT location, age, remote, salary FROM listings WHERE title = ? AND company = ?",
                       (title, company))
        results = cursor.fetchone()
        if results:
            self.location, self.age, self.remote, self.salary = results
            cursor.execute("SELECT qualifications FROM qualifications WHERE title = ? AND company = ?",
                           (title, company))
            self.qualifications = cursor.fetchone()
            self.job_info.setText(
                f"Location: {self.location}, Age: {self.age}, Remote: {self.remote}, Salary: {self.salary} \n Qualifications: {self.qualifications}")
        else:
            cursor.execute(
                "SELECT location, posted_at, min_salary, max_salary, salary_time FROM listings_excel WHERE job_title = ? AND "
                "company_name = ?",
                (title, company))
            results = cursor.fetchone()
            self.location, self.age, self.mins, self.maxs, self.salarytime = results
            self.job_info.setText(
                f"Location: {self.location}, Age: {self.age}, Remote: Not Specified, Salary: {self.mins} to {self.maxs} {self.salarytime}")
        databaseutils.close_db(conn)


def get_job_titles():
    conn, cursor = databaseutils.open_db("JobData.sqlite")
    cursor.execute("SELECT title, company, location FROM listings")
    title_data = cursor.fetchall()
    cursor.execute("SELECT job_title, company_name, location FROM listings_excel")
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
