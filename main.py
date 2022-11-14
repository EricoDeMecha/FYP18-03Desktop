import os
import sys

from PySide2.QtCore import QObject, Slot, QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class Backend(QObject):
    def __init__(self, parent=None):
        super(Backend, self).__init__(parent)

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


def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Bind the backend object in qml
    backend = Backend()
    engine.rootContext().setContextProperty('backend', backend)

    # Load the target .qml file
    engine.load(QUrl.fromLocalFile(os.path.join(CURRENT_DIR, 'main.qml')))

    if not engine.rootObjects():
        return -1

    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())