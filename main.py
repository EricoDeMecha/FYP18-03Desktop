import os
from random import randrange
import sys

from PySide2 import QtCore
from PySide2.QtCore import QObject, Slot, QUrl, QAbstractTableModel, QModelIndex, Signal, Property
from PySide2.QtGui import QGuiApplication, QIcon
from PySide2.QtQml import QQmlApplicationEngine

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class Backend(QObject):
    modelChanged = Signal()
    def __init__(self, parent=None):
        super(Backend, self).__init__(parent)
        self._model = DataTableModel()

    @Slot(int)
    def valveValueChanged(self, value):
        print(f"{value}")

    @Slot(int)
    def stepsSliderValueChanged(self, value):
        print(f"{value}")

    @Slot(int)
    def timeSliderValueChanged(self, value):
        print(f"{value}")

    @Slot(bool)
    def diverterStateChanged(self, value):
        if(value):
            print("true")
        else:
            print("False")

    @Slot(bool)
    def startButtonPressed(self, value):
        if (value):
            print("true")
        else:
            print("False")

    @Slot(bool)
    def stopButtonPressed(self, value):
        if (value):
            print("true")
        else:
            print("False")

    @Slot(bool)
    def nextStepButtonPressed(self, value):
        if (value):
            print("true")
        else:
            print("False")

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
        self._table_data.append([randrange(0,100) for _ in range(len(self._header))])
        self.endInsertRows()

def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    app.setWindowIcon(QIcon('icons/mainIcon.png'))
    # Bind the backend object in qml
    backend = Backend()
    # tableModel._table_data.extend([[randrange(0,100) for _ in range(len(tableModel._header))] for _ in range(100) ])

    engine.rootContext().setContextProperty('backend', backend)
    # Load the target .qml file
    engine.load(QUrl.fromLocalFile(os.path.join(CURRENT_DIR, 'main.qml')))

    if not engine.rootObjects():
        return -1

    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())