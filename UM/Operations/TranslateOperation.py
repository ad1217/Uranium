# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the AGPLv3 or higher.

from UM.Scene.SceneNode import SceneNode

from . import Operation

class TranslateOperation(Operation.Operation):
    def __init__(self, node, translation):
        super().__init__()
        self._node = node
        self._old_position = node.getPosition()
        self._translation = translation

    def undo(self):
        self._node.setPosition(self._old_position)

    def redo(self):
        self._node.translate(self._translation, SceneNode.TransformSpace.World)

    def mergeWith(self, other):
        if type(other) is not TranslateOperation:
            return False

        if other._node != self._node:
            return False

        op = TranslateOperation(self._node, self._translation + other._translation)
        op._old_position = other._old_position
        return op

    def __repr__(self):
        return "TranslateOperation(node = {0}, translation={1})".format(self._node, self._translation)
