from ControlUnit import ControlUnit
from BleCentral import BleCentral

class UnitPyBoat(ControlUnit):
    def __init__(self, ble):
        self._ble = ble
    #
    def GetName(self):
        return 'pyBoat'
    #
    def GetPicture(self):
        return 'picture/pyBoat.jpg'
    #
    def Send(self, code8):
        try:
            self._ble.Write(bytes(code8), False)
        except:
            print("TX failed")
        #
    #
    def Disconnect(self):
        self._ble.Disconnect()
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
