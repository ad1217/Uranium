from Cura.Tool import Tool
from Cura.Event import Event

from . import ScaleToolHandle

class ScaleTool(Tool):
    def __init__(self):
        super().__init__()
        self._handle = ScaleToolHandle.ScaleToolHandle()

    def event(self, event):
        if event.type == Event.ToolActivateEvent:
            self._handle.setParent(self.getController().getScene().getRoot())

        if event.type == Event.ToolDeactivateEvent:
            self._handle.setParent(None)

    def getIconName(self):
        return 'scale.png'