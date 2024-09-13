class ControlUnit():
    def __init__(self, lcd, gamepad):
        self._lcd = lcd
        self._gamepad = gamepad
    #
    def GetPicture(self):
        pass
    # (DevSelectMenu menu)
    def MenuEntered(self, menu):
        pass
    #
#

class Table:
    def __init__(self):
        self.Clean()
    #
    def Clean(self):
        pass
    #
    def Size(self):
        pass
    #
    def PrintInfo(self, lcd, index, position, selected):
        pass
    #
    def OnSelected(self, index):
        pass
    #
#
