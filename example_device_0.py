import bluetooth
from BlePeripheral import BlePeripheral
import time

def main():
    print("Welcome to pyBoat MicroPython!")
    ble = bluetooth.BLE()
    p = BlePeripheral(ble, name='pyBoat')
    #
    def OnRxData(data):
        print("Rx", tuple(data))
    #
    p.SetRxCb(OnRxData)
    #
    while True:
        time.sleep_ms(100)
    #
#

if __name__ == '__main__':
    main()
#
