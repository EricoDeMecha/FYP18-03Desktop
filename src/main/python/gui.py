import os
import sys

from fbs_runtime.application_context.PySide2 import ApplicationContext
from PySide2 import QtCore
from PySide2.QtCore import QObject, Slot, QUrl, QAbstractTableModel, QModelIndex, Signal, Property
# from PySide2.QtGui import QGuiApplication, QIcon
from PySide2.QtQml import QQmlApplicationEngine


QML_PATH = os.path.dirname(os.path.abspath(__file__))


class Backend(QObject):
    modelChanged = Signal()
    def __init__(self, parent=None):
        super(Backend, self).__init__(parent)
        self._model = DataTableModel()
        self.data = {}

    @Slot(int)
    def valveValueChanged(self, value):
        # print(f"{value}")
        self.data['valve'] = value

    @Slot(int)
    def stepsSliderValueChanged(self, value):
        # print(f"{value}")
        self.data['n_steps'] = value
    @Slot(int)
    def timeSliderValueChanged(self, value):
        # print(f"{value}")
        self.data['t_steps'] = value
    @Slot(bool)
    def diverterStateChanged(self, value):
        self.data['diverter'] = value
        # if(value):
        #     print("true")
        # else:
        #     print("False")

    @Slot(bool)
    def startButtonPressed(self, value):
        self.data['start_btn'] = value
        # if (value):
        #     print("true")
        # else:
        #     print("False")

    @Slot(bool)
    def resetButtonPressed(self, value):
        self.data['reset_btn'] = value
        # if (value):
        #     print("true")
        # else:
        #     print("False")

    @Slot(bool)
    def nextStepButtonPressed(self, value):
        self.data['next_btn'] = value
        self._model._table_data.append([self.get_weight(), self.get_temperature(), self.get_time()])
        # if (value):
        #     print("true")
        # else:
        #     print("False")


    def get_temperature(self):
        return self.data['temperature']

    def get_weight(self):
        return self.data['weight']

    def get_time(self):
        return self.data['time_interval']


    @Property(QObject, constant=False, notify=modelChanged)
    def model(self):
        return self._model


class DataTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._header = { 0: "Weight (kg)", 1: "Temperature (°C)", 2: "Time (s)"}
        self._table_data = list()

    def columnCount(self, parent=QModelIndex()):
        return len(self._header)

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._table_data)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        i = index.row()
        j = index.column()
        if role == QtCore.Qt.DisplayRole:
            # return "{}-{}".format(i, j)
            try:
                return self._table_data[i][j]
            except:
                return 0

    @Slot(int, QtCore.Qt.Orientation, result="QVariant")
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._header[section]
            else:
                return str(section)

    @Slot()
    def appendRow(self):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        # self._table_data.append([randrange(0,100) for _ in range(len(self._header))])
        self.endInsertRows()

    @Slot()
    def resetTableData(self):
        self._table_data.clear()


def run(data):
    # app = QGuiApplication(sys.argv)
    app = ApplicationContext()
    engine = QQmlApplicationEngine()

    # app.setWindowIcon(QIcon('icons/mainIcon.ico'))

    # Bind the backend object in qml
    backend = Backend()
    backend.data = data
    engine.rootContext().setContextProperty('backend', backend)
    # Load the target .qml file
    engine.load(QUrl.fromLocalFile(os.path.join(QML_PATH, '../qml/main.qml')))

    if not engine.rootObjects():
        return -1
    # sys.exit(app.exec_())
    # return app.exec_()