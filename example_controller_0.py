import bluetooth
import time
import tftlcd, controller
from BleCentral import BleCentral
from UnitPyBoat import UnitPyBoat

def main():
    print("Welcome to pyController!")
    ble = bluetooth.BLE()
    # LCD 初始化
    lcd = tftlcd.LCD15()
    # 手柄按键初始化
    gamepad = controller.CONTROLLER()
    central = BleCentral(ble, lcd, gamepad)
    boat = UnitPyBoat(central)
    central.Scan(boat)
    #
    while not central.IsConnected():
        time.sleep_ms(100)
    #
    while True:
        keys = gamepad.read()
        print("key codes: ", tuple(bytes(keys)))
        # if keys[6] == 16: # back 键
        #    boat.Disconnect()
        #
        boat.Send(keys)
        time.sleep(1)
    #
#

if __name__ == '__main__':
    main()
#
