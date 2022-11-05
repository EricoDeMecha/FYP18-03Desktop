import sys
import os

from PySide2.QtCore import QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtQuick import QQuickView
from PySide2.QtQuickControls2 import QQuickStyle

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeViewToRootObject)
    QQuickStyle.setStyle("Material")
    engine = QQmlApplicationEngine()

    qml_file = os.path.join(os.path.dirname(__file__), 'main.qml')

    view.setSource(QUrl.fromLocalFile(os.path.abspath(qml_file)))
    if view.status() == QQuickView.Error:
        sys.exit(-1)

    view.show()
    app.exec_()
    del view
