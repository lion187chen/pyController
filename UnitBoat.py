from ControlUnit import ControlUnit
from BleCentral import BleCentral

class UnitBoat(ControlUnit):
    def __init__(self, central):
        self._central = central
    #
    def GetName(self):
        return 'pyBoat'
    #
    def GetPicture(self):
        return 'picture/Car.jpg'
    #
    def Send(self, code8):
        try:
            self._central.Write(bytes(code8), False)
        except:
            print("TX failed")
        #
    #
    def Disconnect(self):
        self._central.Disconnect()
    #
    def OnMenuEnter(self):
        print("Enter pyBoat control.")
    #
    def OnConnected(self):
        print("pyBoat OnConnected")
    #
    def OnDisconnected(self):
        print("pyBoat OnDisconnected")
    #
    def OnNotifyRx(self, data):
        print("pyBoat OnNotifyRx: ", data[0])
    #
#
