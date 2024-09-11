import bluetooth
import binascii
from ControlUnit import ControlUnit

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

#存放搜索到的蓝牙设备数据
macs = []
macs_str = []
names=[]
rssis=[]
addr_types=[]
select = 0 # 蓝牙设备选择

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
DEEPGREEN = (0,139,0) #深绿色

class ControllerMenu:
    def __init__(self, lcd, gamepad):
        self._lcd = lcd
        self._gamepad = gamepad
    # __init__
    def Clear(self):
        self._lcd.fill((255,255,255))
    # Clear
# ControllerMenu

class BleCentral:
    def __init__(self, ble, lcd, gamepad):
        self._ble = ble
        self._lcd = lcd
        self._gamepad = gamepad
        self._ble.active(True)
        self._ble.irq(self.OnIrq)
        self._reset()
    # __init__
    def _reset(self):
        self._obj = None
        self._back = False
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
        # 清屏，白色
        self._lcd.fill((255,255,255))
        # 画线框
        for i in range(4):
            self._lcd.drawRect(0, 48*(i+1), 239, 2, BLACK, border=1, fillcolor=BLACK)
    # _reset
    def SetCtrlObj(self, obj):
        self._obj = obj
    # SetCtrlObj
    def OnIrq(self, event, data):
        global select
        #
        if event == _IRQ_SCAN_RESULT:
            if not self._obj:
                return
            #
            key_value = self._gamepad.read()
            if key_value[6] == 16: # back 键
                self._back = True
                self._ble.gap_scan(None)
            #
            addr_type, addr, adv_type, rssi, adv_data = data
            if adv_type in (_ADV_IND, _ADV_DIRECT_IND) and _UART_SERVICE_UUID in decode_services(adv_data) and (self._obj.GetName() in decode_name(adv_data)):
                # Found a potential device, remember it and stop scanning.                
                if bytes(addr) not in macs :
                    addr_types.append(addr_type)
                    macs.append(bytes(addr))
                    s = binascii.hexlify(addr)
                    macs_str.append(chr(s[0])+chr(s[1])+':' + chr(s[2])+chr(s[3]) + ':' +chr(s[4])+chr(s[5])+':' + \
                            chr(s[6])+chr(s[7])+':'+chr(s[8])+chr(s[9])+':'+chr(s[10])+chr(s[11]))
                    # print(macs_str)
                    names.append(decode_name(adv_data))
                    # print(names)
                    rssis.append(str(rssi))
                #
                rssis[macs.index(bytes(addr))]=str(rssi) #刷新RSSI
                #列表显示,最多显示5个
                for i in range(min(len(macs),5)):
                    self._lcd.printStr(names[i],2,2+i*49,color=(0,0,0),size=2)
                    self._lcd.printStr(rssis[i]+' ' if (-10 < rssi) else rssis[i],140,8+i*49,color=(0,0,0),size=2)
                    self._lcd.printStr(macs_str[i],2,28+i*49,color=(0,0,0),size=1)
                #
                if -40 <= rssi <0:
                    self._lcd.Picture(180, 2+macs.index(bytes(addr))*49, 'picture/signal_3.jpg')
                if -75 <= rssi < -40:
                    self._lcd.Picture(180, 2+macs.index(bytes(addr))*49, 'picture/signal_2.jpg')
                if -99 <= rssi < -75:
                    self._lcd.Picture(180, 2+macs.index(bytes(addr))*49, 'picture/signal_1.jpg')
                #
                if select==0:
                    self._lcd.Picture(219, 9+0*49, 'picture/arrow.jpg')                    
                #
                if key_value[5] == 0 : #上键
                    self._lcd.Picture(219, 9+select*49, 'picture/arrow_none.jpg')
                    select = select - 1            
                    if select < 0:
                        select =0
                    self._lcd.Picture(219, 9+select*49, 'picture/arrow.jpg')
                #
                if key_value[5] == 4 : #下键
                    self._lcd.Picture(219, 9+select*49, 'picture/arrow_none.jpg')
                    select = select + 1            
                    if select>min(len(macs)-1,4):                
                        select = min(len(macs)-1,4)
                    self._lcd.Picture(219, 9+select*49, 'picture/arrow.jpg')
                #
                if key_value[6] == 32: # start 键
                    print(select)
                    self._addr_type = addr_types[select]
                    self._addr = macs[select] # Note: addr buffer is owned by caller so need to copy it.
                    self._name = names[select] or "?"
                    self._ble.gap_scan(None)
                #
            #
        elif event == _IRQ_SCAN_DONE:
            if self._addr and not self._back:
                # Found a device during the scan (and the scan was explicitly stopped).
                self.ScanDone(self._addr_type, self._addr, self._name)
            else:
                # Scan timed out.
                # TODO: return to main menu
                print("Return to Main Menu")
            #
        elif event == _IRQ_PERIPHERAL_CONNECT:
            # Connect successful.
            conn_handle, addr_type, addr = data
            if addr_type == self._addr_type and addr == self._addr:
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
                self._reset()
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
            print("TX complete")
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
    def Scan(self):
        # Find a device advertising the environmental sensor service.
        self._addr_type = None
        self._addr = None
        #self._ble.gap_scan(2000, 30000, 30000)
        self._ble.gap_scan(0, 30000, 30000) #一直扫描，不停止。
    #
    def ScanDone(self, addr_type, addr, name):
        if addr_type is not None:
            print("Found peripheral:", addr_type, addr, name)
            self.Connect()
        else:
            global not_found
            not_found = True
            print("No peripheral found.")
        #
    #
    def Connect(self, addr_type=None, addr=None):
        # Connect to the specified device (otherwise use cached address from a scan).
        self._addr_type = addr_type or self._addr_type
        self._addr = addr or self._addr
        if self._addr_type is None or self._addr is None:
            return False
        self._ble.gap_connect(self._addr_type, self._addr)
        return True
    #
    def Disconnect(self):
        # Disconnect from current device.
        if not self._conn_handle:
            return
        self._ble.gap_disconnect(self._conn_handle)
        self._reset()
    #
    def Write(self, v, response=False):
    # Send data over the UART
        if not self.IsConnected():
            return
        self._ble.gattc_write(self._conn_handle, self._rx_handle, v, 1 if response else 0)
    #
#
