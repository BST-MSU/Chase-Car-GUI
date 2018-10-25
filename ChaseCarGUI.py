from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot


############################# Beginning of GUI code #################################

# Create and show the main GUI window
# Arguments:
#   style - str - string passed to qt to set the stylesheet
#   palette - QPalette - palette to use for the color theme
def create_and_show_gui(style, palette, handle):
    app = QApplication([])
    app.setStyle("Fusion")
    app.setPalette(palette)
    app.setStyleSheet(style)
    window = QWidget()
    window.resize(900, 600)

    window.setWindowTitle("ChaseCarGUI")
    main_layout = QGridLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)

    '''############################ Top Bar ############################'''
    top_bar = QWidget()
    top_bar_layout = QHBoxLayout()
    top_bar.setLayout(top_bar_layout)
    car_speed = DashDisplay("Speed", "", 0.4)
    car_power = DashDisplay("Power Kw", "...", 0.4)
    car_capacity = DashDisplay("Capacity", "...", 0.4)
    car_solar_power = DashDisplay("Solar watts", "...", 0.4)
    car_efficiency = DashDisplay("WH / Mi", "...", 0.4)
    car_range_left = DashDisplay("Range Left", "...", 0.4)
    top_bar_layout.addWidget(car_speed)
    top_bar_layout.addWidget(car_power)
    top_bar_layout.addWidget(car_capacity)
    top_bar_layout.addWidget(car_solar_power)
    top_bar_layout.addWidget(car_efficiency)
    top_bar_layout.addWidget(car_range_left)
    '''########################## End Top Bar ###########################'''
    main_layout.addWidget(top_bar, 1, 1)

    '''############################ Graphs ############################'''
    graphs = QWidget()
    graphs_layout = QGridLayout()
    graphs_layout.setContentsMargins(0, 0, 0, 0)
    graphs.setLayout(graphs_layout)
    solar_power_plot = PlotCanvas("Solar Power")
    speed_plot = PlotCanvas("Speed")
    batt_temp_plot = PlotCanvas("Battery Temperature")
    car_map = MapHolder("Map Goes here", 0.5)
    graphs_layout.addWidget(solar_power_plot, 1, 1)
    graphs_layout.addWidget(speed_plot, 2, 1)
    graphs_layout.addWidget(batt_temp_plot, 3, 1)
    graphs_layout.addWidget(car_map, 1, 2, 3, 1)
    '''########################## End Graphs ###########################'''
    main_layout.addWidget(graphs, 2, 1, 4, 1)
    '''############################ Right Panel ############################'''
    right_panel = QWidget()
    right_panel_layout = QGridLayout()
    right_panel.setLayout(right_panel_layout)
    right_panel_layout.addWidget(QPushButton("Right Control Panel Placeholder"))
    '''########################## End Right Panel ###########################'''
    main_layout.addWidget(right_panel, 1, 2, 5, 5)

    handle.car_speed = car_speed
    handle.car_power = car_power
    handle.car_capacity = car_capacity
    handle.car_solar_power = car_solar_power
    handle.car_efficiency = car_efficiency
    handle.car_range_left = car_range_left
    handle.car_map = car_map


    window.setLayout(main_layout)
    window.show()
    app.mainWindow = window
    return app

# Place holder for the map
class MapHolder(QWidget):
    def __init__(self, content = "Content", scale=1.0):
        super(MapHolder, self).__init__()
        self.init_ui(content, scale)

    def init_ui(self, content, scale):
        layout = QGridLayout()
        layout.setSpacing(1)
        self.content = QLabel(str(content))
        font = self.content.font()
        font.setPointSize(72 * scale)
        self.content.setFont(font)
        self.content.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.content, 0, 0)
        self.setLayout(layout)
        self.setStyleSheet("QLabel {background: palette(button)}")





class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self, title = "Unnamed Plot", data = [0],  width=5, height=4, dpi=100):
        self.title = title
        self.data = data
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, fig)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)
        self.plot()

    def set_data(self, data):
        self.data = data
        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.plot(self.data, 'r-')
        ax.set_title(self.title)
        self.draw()


class DashDisplay(QWidget):
    def __init__(self, title, content, scale=1.0):
        super(DashDisplay, self).__init__()
        self.init_ui(title, content, scale)

    def init_ui(self, title, content, scale):
        layout = QGridLayout()
        layout.setSpacing(1)
        self.top = QLabel(str(title))
        self.top.setAlignment(Qt.AlignCenter)
        self.bottom = QLabel(str(content))
        font = self.bottom.font()
        font.setPointSize(72 * scale)
        self.bottom.setFont(font)
        self.bottom.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.top, 1, 1)
        layout.addWidget(self.bottom, 2, 1, 5, 1)
        self.setLayout(layout)
        self.setStyleSheet("QLabel {background: palette(button)}")

    def update_value(self, value):
        self.bottom.setText(str(value))

    def update_name(self, name):
        self.top.setText(str(name))


def message_box(str="untitled"):
    alert = QMessageBox()
    alert.setModal(True)
    alert.setText(str)
    alert.exec_()

############################# End of UI code #################################


class Handle(object):
    pass


def main():
    print("Chase car GUI for MSU Solar Car 2018-19")
    palette = QPalette();
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Button, QColor(0, 40, 60))
    palette.setColor(QPalette.Background, QColor(20, 30, 35))

    handle = Handle()
    applet = create_and_show_gui("", palette, handle)

    '''
    The following values are references to GUI components

    handle.car_speed = DashDisplay - Car Speed
    handle.car_power = DashDisplay - Car Output power
    handle.car_capacity = DashDisplay - Car Battery percentage
    handle.car_solar_power = DashDisplay - Car solar power
    handle.car_efficiency = DashDisplay - Car efficiency (Wh/Mi)
    handle.car_range_left = DashDisplay - Car range left on battery
    handle.car_map = MapHolder - Map of the course with the car on it

    '''
    applet.exec_()


main()


