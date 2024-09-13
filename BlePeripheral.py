import bluetooth
import time
import binascii
from ble_advertising import advertising_payload

from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
# _IRQ_GATTS_READ_REQUEST = const(4)
# _IRQ_SCAN_RESULT = const(5)
# _IRQ_SCAN_DONE = const(6)
# _IRQ_PERIPHERAL_CONNECT = const(7)
# _IRQ_PERIPHERAL_DISCONNECT = const(8)
# _IRQ_GATTC_SERVICE_RESULT = const(9)
# _IRQ_GATTC_SERVICE_DONE = const(10)
# _IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
# _IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
# _IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
# _IRQ_GATTC_DESCRIPTOR_DONE = const(14)
# _IRQ_GATTC_READ_RESULT = const(15)
# _IRQ_GATTC_READ_DONE = const(16)
# _IRQ_GATTC_WRITE_DONE = const(17)
# _IRQ_GATTC_NOTIFY = const(18)
# _IRQ_GATTC_INDICATE = const(19)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

# _ADV_IND = const(0x00)
# _ADV_DIRECT_IND = const(0x01)
# _ADV_SCAN_IND = const(0x02)
# _ADV_NONCONN_IND = const(0x03)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)

class BlePeripheral:
    def __init__(self, ble, name='mpy-uart'):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self.OnIrq)
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()
        self._rxcb = None
        self._disconnect = None
        #
        # 获取 mac 地址
        mac = binascii.hexlify(ble.config('mac')[1])
        mac_str = chr(mac[0])+chr(mac[1])+':' + chr(mac[2])+chr(mac[3]) + ':' +chr(mac[4])+chr(mac[5])+':' + \
                            chr(mac[6])+chr(mac[7])+':'+chr(mac[8])+chr(mac[9])+':'+chr(mac[10])+chr(mac[11])
        print('MAC: ', mac_str)      
        #
        self.Advertise(name)
    #
    def Advertise(self, name, interval_us=100000):
        self._payload = advertising_payload(name=name, services=[_UART_UUID])
        print("Starting advertising")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
    #
    def OnIrq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            if self._disconnect:
                self._disconnect()
            #
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._rxcb:
                self._rxcb(value)
            #
        #
    #
    def Write(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, data)
        #
    #
    def IsConnected(self):
        return len(self._connections) > 0
    #
    def SetRxCb(self, callback):
        self._rxcb = callback
    #
    def SetDisconnectCb(self, callback):
        self._disconnect = callback
    #
#

def demo():
    ble = bluetooth.BLE()
    peripheral = BlePeripheral(ble, name='pyBoat')
    def OnDisconnected():
        # Start advertising again to allow a new connection.
        peripheral.Advertise()
    #
    peripheral.SetDisconnectCb(OnDisconnected)
    #
    def OnRxData(data):
        print("Rx", tuple(data))
    #
    peripheral.SetRxCb(OnRxData)
    #
    i = 0
    while True:
        if peripheral.IsConnected():
            # Short burst of queued notifications.
            for _ in range(3):
                data = str(i) + "_"
                print("Tx", data)
                peripheral.Write(data)
                i += 1
            #
        #
        time.sleep_ms(100)
    #
#

if __name__ == "__main__":
    demo()
#
