from ControllerInterface import ControlUnit
from BleCentral import BleDevice
# from BleCentral import BleCentral
import time

class UnitPyCar(ControlUnit, BleDevice):
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
        return 'pyCar'
    #
    def GetPicture(self):
        return 'picture/pyCar.jpg'
    #
    def Send(self, data):
        try:
            self._ble.Write(bytes(data), False)
        except:
            print("Tx failed")
        #
    #
    def Disconnect(self):
        self._ble.Disconnect()
    #
    def MenuEntered(self, menu):
        print("Enter pyCar control.")
        menu.Reset()
        menu.DrawTable()
        #
        self._ble.Scan(self)
        # 如果需要自动重连。
        while True:
            if self._mac and self._atype:
                print("Reconnect MAC: ", self._mac)
                self._ble.StopScanAndConnect(self._mac, self._atype)
            else:
                while True:
                    ret = menu.DoSelect(self)
                    if 'Enter'==ret:
                        break
                    #
                    elif 'Cancle'==ret:
                        self._ble.StopScan()
                        self._ble.Reset()
                        print("Return to Main Menu")
                        return
                    #
                    time.sleep_ms(50)
                #
            #
            while not self._ble.IsConnected():
                keys = self._gamepad.read()
                if keys[6] == 16: # back 键返回主菜单。
                    self._ble.Disconnect()
                    print("Return to Main Menu")
                    return
                #
                time.sleep_ms(50)
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
            print("Loss connection, Peripheral MAC: ", self._mac)
        #
        # 如果不自动重连，需要关闭 RSSI 信号强度扫描，并复位蓝牙。
        # self._ble.StopScan()
        # self._ble.Reset()
        # print("Return to Main Menu")
    #
    def OnSelected(self, index):
        name, self._mac, self._atype = super().Select(index)
        print("Select Device: ", name)
        if self._atype is not None and self._mac is not None:
            self._ble.StopScanAndConnect(self._mac, self._atype)
            self._lcd.Clear()
        #
        return 'Enter'
    #
    def OnConnected(self):
        print("pyCar OnConnected")
        self._lcd.Clear()
    #
    def OnDisconnected(self):
        print("pyCar OnDisconnected")
    #
    def OnNotifyRx(self, data):
        print("pyCar OnNotifyRx: ", data[0])
    #
#
