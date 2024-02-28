import sys

from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from PySide6.QtWidgets import QApplication, QListWidget, QListWidgetItem, QWidget

import databaseutils


class MainWindow(QWidget):
    def __init__(self, data_to_show):
        super().__init__()
        self.list_control = None
        self.data = data_to_show
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("Software Developer Job Listings")
        list = QListWidget(self)
        self.list_control = list
        for item1, item2 in self.data:
            list_item = QListWidgetItem(f"{item1}, {item2}", listview=self.list_control)
        list.resize(500, 450)
        self.show()


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
