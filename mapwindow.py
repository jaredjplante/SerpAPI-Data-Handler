import io
from PySide6.QtWidgets import QWidget, QVBoxLayout
import folium
from PySide6.QtWebEngineWidgets import QWebEngineView
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from folium.plugins import MarkerCluster



class mapwindow(QWidget):
    def __init__(self, data_to_display):
        super().__init__()
        self.data_to_display = data_to_display
        self.map = self.build_map()
        self.setup_window()

    def setup_window(self):
        self.layout = QVBoxLayout(self)
        self.webview = QWebEngineView()

        self.webview.setHtml(self.map.getvalue().decode("utf-8"))
        self.layout.addWidget(self.webview)
        self.setLayout(self.layout)
        self.resize(800, 800)
        self.show()


    def build_map(self):
        address = 'Brockton, MA'
        geolocator = Nominatim(user_agent="Comp490MapDemo2024")
        Bos_location = geolocator.geocode(address)
        temp_demo_map = folium.Map(
            location=[Bos_location.latitude, Bos_location.longitude], zoom_start=2
        )
        in_memory_file = io.BytesIO()
        # modified from folium docs
        # https://python-visualization.github.io/folium/latest/user_guide/plugins/marker_cluster.html
        map_data_markers = MarkerCluster().add_to(temp_demo_map)
        for location in self.data_to_display:
            try:
                job_loc_geocoded = geolocator.geocode(location, timeout=10)  # this might need try/catch for small towns
                if job_loc_geocoded is not None:
                    folium.Marker(
                        location=[job_loc_geocoded.latitude, job_loc_geocoded.longitude],
                    ).add_to(map_data_markers)
            except GeocoderTimedOut as e:
                print("Error: geocode failed on input %s" % (location))
        temp_demo_map.save(in_memory_file, close_file=False)
        return in_memory_file
