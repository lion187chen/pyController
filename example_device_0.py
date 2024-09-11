import bluetooth
from BlePeripheral import BlePeripheral
import time

def main():
    print("Welcome to pyBoat MicroPython!")
    ble = bluetooth.BLE()
    p = BlePeripheral(ble, name='pyBoat')
    #
    def on_rx(v):
        print("RX", tuple(v))
    #
    p.on_write(on_rx)
    #
    while True:
        time.sleep_ms(100)
    #
#

if __name__ == '__main__':
    main()
#
