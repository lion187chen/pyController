import bluetooth
import time
import tftlcd, controller
from BleCentral import BleCentral
# from UnitPyBoat import UnitPyBoat
from ControllerMenu import ControllerLcd
from ControllerMenu import MainMenu

def main():
    print("Welcome to pyController!")
    ble = bluetooth.BLE()
    # LCD 初始化
    lcd = tftlcd.LCD15()
    # 手柄按键初始化
    gamepad = controller.CONTROLLER()
    central = BleCentral(ble, lcd, gamepad)
    clcd = ControllerLcd(lcd)
    mm = MainMenu(ble, clcd, gamepad)
    #
    while True:
        unit = mm.Exec()
        if unit:
            print("start scan")
            central.SetCtrlObj(unit)
            central.Scan()
            while not central.IsConnected():
                time.sleep_ms(100)
            #
            while True:
                key_value = gamepad.read()
                print("key_value: ", tuple(bytes(key_value)))
                unit.Send(key_value)
                time.sleep(1)
            #
        time.sleep_ms(50)
    #
#

if __name__ == '__main__':
    main()
#
