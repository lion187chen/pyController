from ControllerInterface import ControlUnit
from BleCentral import BleDeviceTable
# from BleCentral import BleCentral
import time

class UnitPyCar(ControlUnit, BleDeviceTable):
    # (ControllerLcd lcd, BleCentral ble)
    def __init__(self, lcd, ble):
        super().__init__()
        self._lcd = lcd
        self._ble = ble
    #
    def GetName(self):
        return 'pyCar'
    #
    def GetPicture(self):
        return 'picture/pyCar.jpg'
    #
    def Select(self, index):
        name, mac, atype = super().Select(index)
        print("Select Device: ", name)
        if atype is not None and mac is not None:
            self._ble.StopScanAndConnect(mac, atype)
            self._lcd.Clear()
        #
    #
    def Send(self, kcode):
        try:
            self._ble.Write(bytes(kcode), False)
        except:
            print("Tx failed")
        #
    #
    def Disconnect(self):
        self._ble.Disconnect()
    #
    def MenuEntered(self, menu):
        print("Enter pyCar control.")
        #
        self._ble.Scan(self)
        while not self._ble.IsConnected():
            menu.DoSelect(self)
        #
        while self._ble.IsConnected():
            time.sleep(1)
        #
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
