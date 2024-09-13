import bluetooth
import binascii
# from ControllerInterface import ControlUnit
from ControllerInterface import Table

from ble_advertising import decode_services, decode_name

from micropython import const

# _IRQ_CENTRAL_CONNECT = const(1)
# _IRQ_CENTRAL_DISCONNECT = const(2)
# _IRQ_GATTS_WRITE = const(3)
# _IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
# _IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
# _IRQ_GATTC_DESCRIPTOR_DONE = const(14)
# _IRQ_GATTC_READ_RESULT = const(15)
# _IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
# _IRQ_GATTC_INDICATE = const(19)

# _FLAG_READ = const(0x0002)
# _FLAG_WRITE_NO_RESPONSE = const(0x0004)
# _FLAG_WRITE = const(0x0008)
# _FLAG_NOTIFY = const(0x0010)

_ADV_IND = const(0x00)
_ADV_DIRECT_IND = const(0x01)
_ADV_SCAN_IND = const(0x02)
_ADV_NONCONN_IND = const(0x03)

_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

class BleDeviceInfo:
    def __init__(self, name, mac, atype, rssi):
        self.Name = name
        self.Mac = mac
        self.Type = atype
        self.SetRssi(rssi)
        s = binascii.hexlify(mac)
        self.MacStr = chr(s[0])+chr(s[1])+':' + chr(s[2])+chr(s[3]) + ':' +chr(s[4])+chr(s[5])+':' + \
            chr(s[6])+chr(s[7])+':'+chr(s[8])+chr(s[9])+':'+chr(s[10])+chr(s[11])
    #
    def SetRssi(self, rssi):
        self.Rssi = rssi
        self.RssiStr = str(rssi)
    #
#

class BleDeviceTable(Table):
    def __init__(self):
        self.Clean()
    #
    def Clean(self):
        self._devices = []
        self._devMap = {}
    #
    def Size(self):
        return len(self._devices)
    #
    def PrintInfo(self, lcd, index, position, selected):
        device = self._devices[index]
        lcd.PrintStr(device.Name, 2,2+position*49, color=(0,0,0), size=2)
        lcd.PrintStr(device.RssiStr+' ' if (-10 < device.Rssi) else device.RssiStr, 140, 8+position*49, color=(0,0,0), size=2)
        lcd.PrintStr(device.MacStr, 2, 28+position*49, color=(0,0,0), size=1)
        #
        if -40 <= device.Rssi <0:
            lcd.Picture(180, 2+position*49, 'picture/signal_3.jpg')
        if -75 <= device.Rssi < -40:
            lcd.Picture(180, 2+position*49, 'picture/signal_2.jpg')
        if -99 <= device.Rssi < -75:
            lcd.Picture(180, 2+position*49, 'picture/signal_1.jpg')
    #
    def AddInfo(self, name, mac, atype, rssi):
        if mac not in self._devMap:
            self._devices.append(BleDeviceInfo(name, mac, atype, rssi))
            idx = len(self._devices)-1
            self._devMap[mac] = idx
        else:
            # 如果已经存在则更新信号强度。
            idx = self._devMap[mac]
            self._devices[idx].SetRssi(rssi)
        #
    #
    def Select(self, index):
        device = self._devices[index]
        name = device.Name
        mac = device.Mac
        atype = device.Type
        self.Clean()
        return name, mac, atype
    #
#

class BleCentral:
    def __init__(self, ble, gamepad):
        self._ble = ble
        self._gamepad = gamepad
        self._ble.active(True)
        self._ble.irq(self.OnIrq)
        self.Reset()
    #
    def Reset(self):
        self._obj = None
        self._rssicb = None
        # self._back = False
        # Cached name and address from a successful scan.
        self._name = None
        self._addr_type = None
        self._addr = None
        # Callbacks for completion of various operations.
        # These reset back to None after being invoked.
        self._read_callback = None
        # Connected device.
        self._conn_handle = None
        self._start_handle = None
        self._end_handle = None
        self._tx_handle = None
        self._rx_handle = None
    #
    def OnIrq(self, event, data):
        # global select
        #
        if event == _IRQ_SCAN_RESULT:
            if self._addr is None:
                # 非 ScanPeripheralRssi 模式需要判断 self._obj 有效性。
                if not self._obj:
                    return
                #
                # 非 ScanPeripheralRssi 模式可以通过按钮取消。
                # kcodes = self._gamepad.read()
                # if kcodes[6] == 16: # back 键
                    # self._back = True
                    # self._ble.gap_scan(None)
                #
            #
            addr_type, mac, adv_type, rssi, adv_data = data
            if adv_type in (_ADV_IND, _ADV_DIRECT_IND) and _UART_SERVICE_UUID in decode_services(adv_data) and (self._obj.GetName() in decode_name(adv_data)):
                if self._addr:
                    if self._addr==mac and self._rssicb:
                        # ScanPeripheralRssi 模式
                        self._rssicb(rssi)
                    #
                elif self._obj:
                    self._obj.AddInfo(decode_name(adv_data), bytes(mac), addr_type, rssi)
                #
            #
        elif event == _IRQ_SCAN_DONE:
            if self._addr: # and not self._back:
                # Found a device during the scan (and the scan was explicitly stopped).
                self.ScanDone()
            else:
                # Scan timed out.
                # TODO: return to main menu
                print("Return to Main Menu")
            #
        elif event == _IRQ_PERIPHERAL_CONNECT:
            # Connect successful.
            conn_handle, addr_type, mac = data
            if addr_type == self._addr_type and mac == self._addr:
                self._conn_handle = conn_handle
                self._ble.gattc_discover_services(self._conn_handle)
            #
        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            # Disconnect (either initiated by us or the remote end).
            conn_handle, _, _ = data
            if conn_handle == self._conn_handle:
                # If it was initiated by us, it'll already be reset.
                if self._obj:
                    self._obj.OnDisconnected()
                #
                self.Reset()
                #
            #
        elif event == _IRQ_GATTC_SERVICE_RESULT:
            # Connected device returned a service.
            conn_handle, start_handle, end_handle, uuid = data
            print("service", data)
            if conn_handle == self._conn_handle and uuid == _UART_SERVICE_UUID:
                self._start_handle, self._end_handle = start_handle, end_handle
            #
        elif event == _IRQ_GATTC_SERVICE_DONE:
            # Service query complete.
            if self._start_handle and self._end_handle:
                self._ble.gattc_discover_characteristics(
                    self._conn_handle, self._start_handle, self._end_handle
                )
            else:
                print("Failed to find uart service.")
            #
        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            # Connected device returned a characteristic.
            conn_handle, def_handle, value_handle, properties, uuid = data
            if conn_handle == self._conn_handle and uuid == _UART_RX_CHAR_UUID:
                self._rx_handle = value_handle
            if conn_handle == self._conn_handle and uuid == _UART_TX_CHAR_UUID:
                self._tx_handle = value_handle
            #
        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            if self._tx_handle is not None and self._rx_handle is not None:
                # We've finished connecting and discovering device, fire the connect callback.
                if self._obj:
                    self._obj.OnConnected()
                #
            else:
                print("Failed to find uart rx characteristic.")
            #
        elif event == _IRQ_GATTC_WRITE_DONE:
            conn_handle, value_handle, status = data
            print("Tx complete")
        elif event == _IRQ_GATTC_NOTIFY:
            conn_handle, value_handle, notify_data = data
            if conn_handle == self._conn_handle and value_handle == self._tx_handle:
                if self._obj:
                    self._obj.OnNotifyRx(notify_data)
                #
            #
        #
    #
    def IsConnected(self):
        # Returns true if we've successfully connected and discovered characteristics.
        return (
            self._conn_handle is not None
            and self._tx_handle is not None
            and self._rx_handle is not None
        )
    #
    def Scan(self, obj):
        self._obj = obj
        # Find a device advertising the environmental sensor service.
        self._addr_type = None
        self._addr = None
        # self._ble.gap_scan(2000, 30000, 30000)
        self._ble.gap_scan(0, 30000, 30000) # 一直扫描，不停止。
    #
    def ScanPeripheralRssi(self, mac, callback):
        # Find a device advertising the environmental sensor service.
        self._addr_type = None
        self._addr = mac
        self._rssicb = callback
        # self._ble.gap_scan(2000, 30000, 30000)
        self._ble.gap_scan(0, 30000, 30000) # 一直扫描，不停止。
    #
    def StopScan(self):
        self._addr_type = None
        self._addr = None
        self._ble.gap_scan(None)
    #
    def StopScanAndConnect(self, mac, atype):
        self._addr_type = atype
        self._addr = mac # Note: addr buffer is owned by caller so need to copy it.
        self._ble.gap_scan(None)
    #
    def ScanDone(self):
        self.Connect()
    #
    def Connect(self, addr_type=None, mac=None):
        # Connect to the specified device (otherwise use cached address from a scan).
        self._addr_type = addr_type or self._addr_type
        self._addr = mac or self._addr
        if self._addr_type is None or self._addr is None:
            return False
        #
        self._ble.gap_connect(self._addr_type, self._addr)
        return True
    #
    def Disconnect(self):
        # Disconnect from current device.
        if not self._conn_handle:
            return
        #
        self._ble.gap_disconnect(self._conn_handle)
        self.Reset()
    #
    def Write(self, data, response=False):
        # Send data over the UART
        if not self.IsConnected():
            return
        #
        self._ble.gattc_write(self._conn_handle, self._rx_handle, data, 1 if response else 0)
    #
#
