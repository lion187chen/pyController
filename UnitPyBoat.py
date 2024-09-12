from ControllerInterface import ControlUnit
from BleCentral import BleDeviceTable
from BleCentral import BleCentral

class UnitPyBoat(ControlUnit, BleDeviceTable):
    # (ControllerLcd lcd, BleCentral ble)
    def __init__(self, lcd, ble):
        super().__init__()
        self._lcd = lcd
        self._ble = ble
    #
    def GetName(self):
        return 'pyBoat'
    #
    def GetPicture(self):
        return 'picture/pyBoat.jpg'
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
