// Copyright (c) 2015 Ultimaker B.V.
// Uranium is released under the terms of the AGPLv3 or higher.

import QtQuick 2.2
import QtQuick.Controls 1.2

import UM 1.1 as UM

Item
{
    width: Math.max(14 * UM.Theme.sizes.line.width, childrenRect.width);
    height: Math.max(4.5 * UM.Theme.sizes.line.height, childrenRect.height);
    UM.I18nCatalog { id: catalog; name:"uranium"}
    Button
    {
        id: resetRotationButton

        //: Reset Rotation tool button
        text: catalog.i18nc("@action:button","Reset")
        iconSource: UM.Theme.icons.rotate_reset;
        //: Reset Rotation tool button tooltip
        tooltip: catalog.i18nc("@info:tooltip","Reset the rotation of the current selection.");

        style: UM.Theme.styles.tool_button;

        onClicked: UM.ActiveTool.triggerAction("resetRotation");
    }

    CheckBox
    {
        anchors.left: resetRotationButton.right;
        anchors.leftMargin: UM.Theme.sizes.default_margin.width;
        anchors.bottom: resetRotationButton.bottom;

        //: Snap Rotation checkbox
        text: catalog.i18nc("@action:checkbox","Snap Rotation");

        style: UM.Theme.styles.checkbox;

        checked: UM.ActiveTool.properties.RotationSnap;
        onClicked: UM.ActiveTool.setProperty("RotationSnap", checked);
    }
}
