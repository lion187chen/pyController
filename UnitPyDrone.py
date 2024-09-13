from ControllerInterface import ControlUnit
from BleCentral import BleDeviceTable
# from BleCentral import BleCentral
import time

class UnitPyDrone(ControlUnit, BleDeviceTable):
    # (ControllerLcd lcd, controller.CONTROLLER gamepad, BleCentral ble)
    def __init__(self, lcd, gamepad, ble):
        super().__init__()
        self._lcd = lcd
        self._gamepad = gamepad
        self._ble = ble
        self._mac = None
        self._atype = None
    #
    def GetName(self):
        return 'pyDrone'
    #
    def GetPicture(self):
        return 'picture/pyDrone.jpg'
    #
    def Select(self, index):
        name, self._mac, self._atype = super().Select(index)
        print("Select Device: ", name)
        if self._atype is not None and self._mac is not None:
            self._ble.StopScanAndConnect(self._mac, self._atype)
            self._lcd.Clear()
        #
    #
    def Send(self, kcodes):
        try:
            self._ble.Write(bytes(kcodes), False)
        except:
            print("Tx failed")
        #
    #
    def Disconnect(self):
        self._ble.Disconnect()
    #
    def MenuEntered(self, menu):
        print("Enter pyDrone control.")
        #
        self._ble.Scan(self)
        # 如果需要自动重连。
        while True:
            if self._mac and self._atype:
                print("Reconnect MAC: ", self._mac)
                self._ble.StopScanAndConnect(self._mac, self._atype)
            #
            while not self._ble.IsConnected():
                # 允许使用 back 键停止扫描并返回主菜单。
                kcodes = self._gamepad.read()
                if kcodes[6] == 16: # back 键
                    self._ble.StopScan()
                    self._ble.Reset()
                    print("Return to Main Menu")
                    return
                #
                menu.DoSelect(self)
            #
            def OnRssi(rssi):
                print("RSSI: ", rssi)
            #
            if self._mac:
                self._ble.ScanPeripheralRssi(OnRssi)
            #
            while self._ble.IsConnected():
                self.Send(self._gamepad.read())
                time.sleep_ms(100)
            #
            print("Loss connection Peripheral MAC: ", self._mac)
        #
        # 如果不自动重连，需要关闭 RSSI 信号强度扫描，并复位蓝牙。
        # self._ble.StopScan()
        # self._ble.Reset()
        # print("Return to Main Menu")
    #
    def OnConnected(self):
        print("pyDrone OnConnected")
        self._lcd.Clear()
    #
    def OnDisconnected(self):
        print("pyDrone OnDisconnected")
    #
    def OnNotifyRx(self, data):
        print("pyDrone OnNotifyRx: ", data[0])
    #
#
