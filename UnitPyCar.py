from ControlUnit import ControlUnit
from BleCentral import BleCentral

class UnitPyCar(ControlUnit):
    def __init__(self, ble):
        self._ble = ble
    #
    def GetName(self):
        return 'pyCar'
    #
    def GetPicture(self):
        return 'picture/pyCar.jpg'
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
        print("Enter pyCar control.")
    #
    def OnConnected(self):
        print("pyCar OnConnected")
    #
    def OnDisconnected(self):
        print("pyCar OnDisconnected")
    #
    def OnNotifyRx(self, data):
        print("pyCar OnNotifyRx: ", data[0])
    #
#
