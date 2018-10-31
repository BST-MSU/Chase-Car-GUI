from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os

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
    top_bar_layout.addWidget(car_range_left)
    top_bar_layout.addWidget(car_efficiency)
    top_bar_layout.addWidget(car_solar_power)
    '''########################## End Top Bar ###########################'''
    main_layout.addWidget(top_bar, 1, 1)

    '''############################ Graphs ############################'''
    graphs = QWidget()
    bottom_layout = QGridLayout()
    bottom_layout.setContentsMargins(0, 0, 0, 0)
    graphs.setLayout(bottom_layout)

    # TODO add colored legend to map
    data_plot = PlotCanvas("Solar Power, Motor Power, Battery Temperature", {}, 8, 6)
    data_plot.set_data("Solar Power,b--", [0, 2, 4, 6, 8, 7, 6])
    data_plot.set_data("Motor Power,g--", [0, 1, 2, 3, 2, 3, 4, 3, 2, 0])
    data_plot.set_data("Battery Temperature,r--", [0, 0.5, 1, 1.5, 2, 2.5, 3, 3])
    map = MapHolder("Map goes here", 0, 0, 1, 1)

    bottom_layout.addWidget(data_plot, 1, 1, 1, 1, Qt.AlignCenter)
    bottom_layout.addWidget(map, 1, 2, 1, 1, Qt.AlignCenter)

    bottom_layout.setColumnStretch(1, 0.33)
    bottom_layout.setColumnStretch(2, 0.67)
    '''########################## End Graphs ###########################'''
    main_layout.addWidget(graphs, 2, 1, 4, 1)
    '''############################ Right Panel ############################'''
    right_panel = QWidget()
    right_panel_layout = QGridLayout()
    right_panel.setLayout(right_panel_layout)
    right_panel_layout.addWidget(QPushButton("Right Control Panel Placeholder"))
    '''########################## End Right Panel ###########################'''
   # main_layout.addWidget(right_panel, 1, 2, 5, 5)

    handle.car_speed = car_speed
    handle.car_power = car_power
    handle.car_capacity = car_capacity
    handle.car_solar_power = car_solar_power
    handle.car_efficiency = car_efficiency
    handle.car_range_left = car_range_left
    handle.car_map = map

    window.setMinimumSize(1200, 700)
    window.setLayout(main_layout)
    window.show()
    app.mainWindow = window
    return app

# TODO add support for larger / tiled maps
# TODO don't zoom out on entire map
class MapHolder(QWidget):
    def __init__(self, title, start_x, start_y, end_x, end_y):
        super(MapHolder, self).__init__()
        self.title = title
        self.start_x = start_x
        self.start_y = start_y
        self.pos_x = start_x
        self.pos_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.map = False
        self.fg = QColor(255, 127, 15)
        self.bg = QColor(0, 0, 0)
        QWidget.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(500, 500)

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def set_map(self, map):
        self.map = map

    def load_map(self, path):
        if not path.startswith("/"):
            path = os.path.dirname(os.path.realpath(__file__)) + "/" + path
        reader = QImageReader(path)
        image = reader.read()
        self.set_map(image)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        width = self.width()
        height = self.height()

        #qp.fillRect(0, 0, width, height, self.bg)
        if self.map:
            qp.drawImage(0, 0, self.map.scaled(width, height))
        else:
            qp.drawText(0, 0, width, height, Qt.AlignCenter, "NO MAP AVAILABLE")

        x = (self.pos_x - self.start_x) / (self.end_x - self.start_x)
        y = (self.pos_y - self.start_y) / (self.end_y - self.start_y)
        qp.fillRect(x * width - (width / 30), y * height - (height / 30), width / 15, height / 15, self.bg)
        qp.fillRect(x * width - (width / 40), y * height - (height / 40), width / 20, height / 20, self.fg)


class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self, title, data = {},  width=6, height=5, dpi=80):
        self.title = title
        self.data = data
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, fig)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)
        self.plot()

    def set_data(self, key, data):
        self.data[key] = data;
        self.plot()

    def plot(self):
        ax = self.axes
        ax.set_title(self.title);
        for title in self.data:
            data = self.data[title]
            ax.plot(data, title.split(",")[1]);
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

    # Testing code
    handle.car_speed.update_value(22)
    handle.car_power.update_value(1.5)
    handle.car_capacity.update_value(85)
    handle.car_solar_power.update_value(650)
    handle.car_efficiency.update_value(15)
    handle.car_range_left.update_value(124)
    handle.car_map.set_pos(0.56, 0.4)
    handle.car_map.load_map("map.png")

    '''
    The following values are references to GUI components

    handle.car_speed = DashDisplay - Car Speed
    handle.car_power = DashDisplay - Car Output power
    handle.car_capacity = DashDisplay - Car Battery percentage
    handle.car_solar_power = DashDisplay - Car solar power
    handle.car_efficiency = DashDisplay - Car efficiency (Wh/Mi)
    handle.car_range_left = DashDisplay - Car range left on battery
    handle.car_map = MapHolder - Map of the course and the car

    '''
    applet.exec_()


if __name__ == "__main__":
    main()


