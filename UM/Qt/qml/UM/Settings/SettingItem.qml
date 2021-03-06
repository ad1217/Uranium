// Copyright (c) 2015 Ultimaker B.V.
// Uranium is released under the terms of the AGPLv3 or higher.

import QtQuick 2.1
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1

import UM 1.0 as UM

Rectangle {
    id: base;

    property string name;
    property string description;
    property variant value;
    property string unit;
    property int valid;
    property string type;
    property int depth;

    property variant options;
    property int index;
    property variant key;

    property bool overridden;
    property bool perObjectSetting;
    property bool dismissable;

    signal contextMenuRequested();
    signal itemValueChanged(variant value);
    signal showTooltip(variant position);
    signal hideTooltip();
    signal resetRequested();

    property bool hovered: false;

    MouseArea 
    {
        id: mouse;

        anchors.fill: parent;

        acceptedButtons: Qt.RightButton;
        hoverEnabled: true;

        onClicked: base.contextMenuRequested();

        onEntered: {
            hoverTimer.start();
            base.hovered = true;
        }

        onExited: {
            if(controlContainer.item && controlContainer.item.hovered) {
                return;
            }

            base.hovered = false;
            hoverTimer.stop();
            base.hideTooltip();
        }

        Timer {
            id: hoverTimer;
            interval: 500;
            repeat: false;

            onTriggered: base.showTooltip({ x: mouse.mouseX, y: mouse.mouseY });
        }
    }
    property variant style: SettingItemStyle { }

    Rectangle{
        visible: base.depth > 1 ? true : false
        id: separationLine
        width: 2
        height: label.height / 2
        color: UM.Theme.colors.setting_control_depth_line
        anchors.right: label.left
        anchors.rightMargin: UM.Theme.sizes.setting_control_depth_margin.width / 2
        anchors.verticalCenter: parent.verticalCenter
        z: parent.z + 1
    }

    Label
    {
        id: label;
        property int depth: base.depth - 1

        anchors.left: parent.left;
        anchors.leftMargin: base.perObjectSetting ? UM.Theme.sizes.default_margin.width : (UM.Theme.sizes.section_icon_column.width + 5) + (label.depth * UM.Theme.sizes.setting_control_depth_margin.width)
        anchors.right: base.overridden? revertButton.left : controlContainer.left;
        anchors.rightMargin: base.style.spacing;
        anchors.verticalCenter: parent.verticalCenter

        height: UM.Theme.sizes.section.height;
        verticalAlignment: Text.AlignVCenter;

        text: base.name
        elide: Text.ElideMiddle;

        color: base.style.controlTextColor;
        font: base.style.labelFont;
    }

    Button {
        id: revertButton

        anchors {
            right: controlContainer.left
            verticalCenter: parent.verticalCenter;
        }
        visible: !base.perObjectSetting ? base.overridden :  base.dismissable ? true : false
        tooltip: !base.perObjectSetting ? catalog.i18nc("@info:tooltip", "Reset to Default") : catalog.i18nc("@info:tooltip", "Remove Customised Setting")

        height: parent.height - base.style.controlBorderWidth;
        width: height;

        onClicked: !base.perObjectSetting ? base.resetRequested() : UM.ActiveTool.properties.Model.removeSettingOverride(UM.ActiveTool.properties.Model.getItem(base.currentIndex).id, model.key)

        style: ButtonStyle {
            background: Rectangle {
                color: control.hovered ? base.style.controlHighlightColor : base.style.controlColor;
                UM.RecolorImage {
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    width: parent.width/2
                    height: parent.height/2
                    sourceSize.width: width
                    sourceSize.height: width
                    color: UM.Theme.colors.setting_control_revert
                    source: !base.perObjectSetting ? UM.Theme.icons.reset : UM.Theme.icons.cross1
                }
            }
        }
    }

    Loader {
        id: controlContainer;

        anchors.right: parent.right;
        anchors.verticalCenter: parent.verticalCenter

        width: base.style.controlWidth;
        height: base.style.fixedHeight > 0 ? base.style.fixedHeight : parent.height;

        property variant itemStyle: base.style

        source:
        {
            switch(base.type)
            {
                case "int":
                    return "SettingTextField.qml"
                case "float":
                    return "SettingTextField.qml"
                case "double":
                    return "SettingTextField.qml"
                case "enum":
                    return "SettingComboBox.qml"
                case "boolean":
                    return "SettingCheckBox.qml"
                default:
                    return "SettingUnknown.qml"
            }
        }

        Connections {
            target: controlContainer.item;
            onValueChanged: {
                base.itemValueChanged(value);
            }
            onHoveredChanged: {
                if(controlContainer.item.hovered) {
                    hoverTimer.start();
                } else {
                    if(!mouse.containsMouse) {
                        hoverTimer.stop();
                        base.hideTooltip();
                    }
                }
            }
        }
    }
}
