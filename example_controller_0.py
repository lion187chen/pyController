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
        key_value = gamepad.read()
        print("key_value: ", tuple(bytes(key_value)))
        # if key_value[6] == 16: # back 键
        #    boat.Disconnect()
        #
        boat.Send(key_value)
        time.sleep(1)
    #
#

if __name__ == '__main__':
    main()
#
