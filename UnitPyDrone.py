from ControlUnit import ControlUnit
from BleCentral import BleCentral

class UnitPyDrone(ControlUnit):
    def __init__(self, ble):
        self._ble = ble
    #
    def GetName(self):
        return 'pyDrone'
    #
    def GetPicture(self):
        return 'picture/pyDrone.jpg'
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
        print("Enter pyDrone control.")
    #
    def OnConnected(self):
        print("pyDrone OnConnected")
    #
    def OnDisconnected(self):
        print("pyDrone OnDisconnected")
    #
    def OnNotifyRx(self, data):
        print("pyDrone OnNotifyRx: ", data[0])
    #
#
