import QtQuick 2.14
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.14
import QtQuick.Dialogs 1.3
import QtQuick.Shapes 1.14
import QtQuick.Extras 1.4
import Qt.labs.qmlmodels 1.0
import QtQuick.Controls.Material 2.12

import "controls"



ApplicationWindow {
    id: root
    width: 800
    height: 600
    maximumWidth: 800
    maximumHeight: 600
    visible: true
    title: "FYP18-03 Auto-Application"

    Rectangle {
        id: mainPage

        property real newVal: 0
        property real steps: 0
        property real time: 0
        property real m_width: 800
        property real m_height: 600
        property var horizontal_header_data: ["Step No.", "Weight", "Temperature", "Time"] // table header
        anchors.fill: parent
        color: "#09203f"
        gradient: Gradient {
            orientation: Gradient.Vertical
            GradientStop {
                position: 0
                color: "#09203f"
            }

            GradientStop {
                position: 1
                color: "#537895"
            }
        }

        Text {
            id: titleHeader
            anchors {
                top: mainPage.top
                horizontalCenter: mainPage.horizontalCenter
            }
            width: mainPage.m_width*(154/mainPage.m_width)
            height: mainPage.m_height*(29/mainPage.m_height)

            color: "#ffffff"
            text: qsTr("FYP18-03  S.H.E.M Automation")
            font.pixelSize: 20
            scale: 1.3
        }

        CircularSlider {
            id: slider1
           anchors {
                top: titleHeader.baseline
                topMargin: 40
                left: mainPage.left
            }
            value: mainPage.newVal
            onValueChanged: {
                 mainPage.newVal = value
                 backend.valveValueChanged(Number(slider1.value).toFixed())
            }

            width: mainPage.m_width * 0.4
            height: mainPage.m_height * 0.4
            startAngle: 40
            endAngle: 320
            rotation: 180
            trackWidth: 5
            progressWidth: 20
            minValue: 0
            maxValue: 90
            progressColor: "#50FA7B"
            capStyle: Qt.FlatCap

            Label {
                anchors.centerIn: parent
                anchors.verticalCenterOffset: 40
                rotation: 180
                font.pointSize: 16
                color: "#FEFEFE"
                text: "Valve"
            }
            handle: Rectangle {
                transform: Translate {
                    x: (slider1.handleWidth - width) / 2
                    y: slider1.handleHeight / 2
                }

                width: 10
                height: slider1.height / 2
                color: "#FFac89"
                radius: width / 2
                antialiasing: true
            }

            Label {
                anchors.centerIn: parent
                anchors.verticalCenterOffset: -40
                rotation: 180
                font.pointSize: 26
                color: "#FEFEFE"
                text: (Number(slider1.value).toFixed()) + "°"
            }
        }

        Text {
            id: numberOfStepsTxt
            anchors {
                top: slider1.top
                topMargin: 50
                left: slider1.right
            }
            width: mainPage.m_width * 0.1
            height: mainPage.m_height * 0.03
            color: "#ffffff"
            text: qsTr("Number of Steps")
            font.pixelSize: 18
        }
        Slider {
            id: stepsSlider
            width: mainPage.m_width * 0.25
            height: mainPage.m_height * 0.06
            anchors {
                top: numberOfStepsTxt.baseline
                left: slider1.right
                leftMargin: 60
                topMargin:  10
            }

            scale: 1.5
            from: 0
            to: 20
            value: mainPage.steps
            stepSize: 1
            onValueChanged: {
                mainPage.steps = value
                backend.stepsSliderValueChanged(value)
            }


            CLabel {
                id: stepsLabel
                width: 20
                height: 18
                anchors {
                    left: stepsSlider.right
                    baseline: stepsSlider.verticalCenter
                }
                text: stepsSlider.value
            }
        }

        Text {
            id: timeIntervalTxt
            anchors {
                top: slider1.verticalCenter
                left: slider1.right
            }

            width: mainPage.m_width * 0.09
            height: mainPage.m_height * 0.02
            color: "#ffffff"
            text: qsTr("Time Interval")
            font.pixelSize: 18
        }
        Slider {
            id: timeSlider
            width: mainPage.m_width * 0.25
            height: mainPage.m_height * 0.06
            anchors {
                top: timeIntervalTxt.baseline
                left: slider1.right
                leftMargin: 60
                topMargin:  10
            }
            opacity: 1
            focus: true
            antialiasing: true
            scale: 1.5
            stepSize: 1
            value: mainPage.time
            to: 100
            from: 0
            onValueChanged: {
                mainPage.time = value
                backend.timeSliderValueChanged(value)
            }
            CLabel {
                id: timeLabel
                width: 20
                height: 18
                anchors {
                    left: timeSlider.right
                    baseline: timeSlider.verticalCenter
                }
                text: timeSlider.value
            }
        }



        ToggleButton {
            id: diverter
            anchors {
                top: slider1.bottom
                horizontalCenter: slider1.horizontalCenter
            }
            onPressedChanged: {
                backend.diverterStateChanged(diverter.checked)
            }

            text: qsTr("Diverter")
        }

        Button {
            id:startBtn
            text: qsTr("Start")
            anchors {
                top: timeSlider.bottom
                topMargin: 60
                left: slider1.right
                leftMargin: 60
            }
            onClicked: {
                backend.startButtonPressed(startBtn.clicked)
            }

            background: Rectangle {
                implicitWidth: mainPage.m_width * 0.1
                implicitHeight: mainPage.m_height  * 0.06
                border.width: startBtn.activeFocus ? 2 : 1
                border.color: "#888"
                radius: 8
                gradient: Gradient {
                    GradientStop { position: 0 ; color: startBtn.pressed ? "#ccc" : "#eee" }
                    GradientStop { position: 1 ; color: startBtn.pressed ? "#aaa" : "#ccc" }
                }
            }
        }

        Button {
            id: resetBtn
            text: qsTr("Reset")
            anchors {
                left: startBtn.right
                leftMargin: 40
                verticalCenter: startBtn.verticalCenter
            }
            onClicked: {
                backend.stopButtonPressed(resetBtn.clicked)
                stepsSlider.value = 0
                timeSlider.value = 0
            }
            background: Rectangle {
                implicitWidth: mainPage.m_width * 0.1
                implicitHeight: mainPage.m_height  * 0.06
                border.width: resetBtn.activeFocus ? 2 : 1
                border.color: "#888"
                radius: 8
                gradient: Gradient {
                    GradientStop { position: 0 ; color: resetBtn.pressed ? "#ccc" : "#eee" }
                    GradientStop { position: 1 ; color: resetBtn.pressed ? "#aaa" : "#ccc" }
                }
            }
        }
        Label {
            id: temperatureTitleLabel
            anchors {
                left: diverter.right
                top: startBtn.bottom
                topMargin: 20
                leftMargin: 40
            }
            text: "Temperature:"
            color: "#FFFFFF"
            font.pixelSize: 16
            Label {
                id: temperatureLabel
                anchors {
                    left: parent.right
                    leftMargin: 20
                    verticalCenter: parent.verticalCenter
                }
                text: "0 °C"
                color: parent.color
                font.pixelSize: parent.font.pixelSize
            }
        }
         Label {
            id: weightTitleLabel
            anchors {
                left: diverter.right
                top: temperatureTitleLabel.baseline
                topMargin: 10
                leftMargin: 40
            }
            text: "Weight:"
            color: "#FFFFFF"
            font.pixelSize: 16
            Label {
                id: weightLabel
                anchors {
                    left: parent.right
                    leftMargin: 20
                    verticalCenter: parent.verticalCenter
                }
                text: "0 Kg"
                color: parent.color
                font.pixelSize: parent.font.pixelSize
            }
        }
        Button {
            id:nextBtn
            text: qsTr("Next Step")
            anchors{
                top: resetBtn.bottom
                topMargin: 20
                horizontalCenter: resetBtn.horizontalCenter
            }
            onClicked: {
                backend.nextStepButtonPressed(nextBtn.clicked)
            }
            background: Rectangle {
                implicitWidth: mainPage.m_width * 0.1
                implicitHeight: mainPage.m_height  * 0.06
                border.width: nextBtn.activeFocus ? 2 : 1
                border.color: "#888"
                radius: 8
                gradient: Gradient {
                    GradientStop { position: 0 ; color: nextBtn.pressed ? "#ccc" : "#eee" }
                    GradientStop { position: 1 ; color: nextBtn.pressed ? "#aaa" : "#ccc" }
                }
            }
            
        }


        Rectangle {
            id: tableQ
            anchors {
                horizontalCenter: mainPage.horizontalCenter
                bottom: mainPage.bottom
                bottomMargin: 40
            }
            width: mainPage.m_width - 100
            height: mainPage.m_height - (diverter.y + diverter.height + 50)

            TableView {
                id: table
                anchors.fill: parent
                columnSpacing: 4; rowSpacing: 4

                columnWidthProvider: function(column) { return headerRepeater.itemAt(column).width }

                delegate: DelegateChooser {
                    role: "type"
                    DelegateChoice {
                        roleValue: "readonly"
                        Rectangle {
                            color: "grey"
                            implicitHeight: readonlyText.implicitHeight
                            Text {
                                id: readonlyText
                                text: model.display
                                width: parent.width
                                elide: Text.ElideRight
                                font.preferShaping: false
                            }
                        }
                    }
                    DelegateChoice {
                        roleValue: "id"
                        Rectangle {
                            color: "yellow"
                            implicitHeight: idText.implicitHeight
                            Text {
                                id: idText
                                text: model.display
                                width: parent.width
                                elide: Text.ElideRight
                                font.preferShaping: false
                            }
                        }
                    }
                    DelegateChoice {
                        roleValue: "string"
                        Rectangle {
                            color: "#0048BA"
                            implicitHeight: stringText.implicitHeight *1.5

                            Text {
                                id: stringText
                                color: "white"
                                text: model.display
                                width: parent.width
                                elide: Text.ElideRight
                                font.preferShaping: false
                            }
                        }
                    }
                    DelegateChoice {
                        Rectangle {
                            color: "#EEE"
                            implicitHeight: defaultText.implicitHeight
                            Text {
                                id: defaultText
                                text: model.display
                                width: parent.width
                                elide: Text.ElideRight
                                horizontalAlignment: Text.AlignRight
                                font.preferShaping: false
                            }
                        }
                    }
                }
                ScrollBar.horizontal: ScrollBar { }
                ScrollBar.vertical: ScrollBar { }
            }
        }
    }
}


