from ControllerInterface import ControlUnit
from BleCentral import BleDeviceTable
from BleCentral import BleCentral

class UnitPyDrone(ControlUnit, BleDeviceTable):
    # (ControllerLcd lcd, BleCentral ble)
    def __init__(self, lcd, ble):
        super().__init__()
        self._lcd = lcd
        self._ble = ble
    #
    def GetName(self):
        return 'pyDrone'
    #
    def GetPicture(self):
        return 'picture/pyDrone.jpg'
    #
    def Select(self, index):
        self._lcd.Clear()
        name, mac, type = super().Select(index)
        self._ble.StopScan(name, mac, type)
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
