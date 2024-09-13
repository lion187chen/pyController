import bluetooth
from BlePeripheral import BlePeripheral
import time
from machine import Pin, PWM

def CtrlCutTranscode(code):
    if code > 235:
        code = 235
    #
    if code < 20:
        code = 20
    #
    if code <= 95:
        return (code-95)*100/75
    elif code >= 125:
        return (code-125)*100/110
    else:
        return 0
    #
#

def main():
    print("Welcome to pyBoat MicroPython!")
    pwmLA = PWM(Pin(40), freq=20000, duty=0)
    pwmLB = PWM(Pin(41), freq=20000, duty=0)
    #
    pwmRA = PWM(Pin(38), freq=20000, duty=0)
    pwmRB = PWM(Pin(39), freq=20000, duty=0)
    #
    def MotoLCtrlL(percent):
        percent = percent*1023/100
        if percent>0:
            pwmLA.duty(int(percent))
            pwmLB.duty(0)
        else:
            pwmLA.duty(0)
            pwmLB.duty(int(percent))
        #
    #

    def MotoLCtrlR(percent):
        percent = percent*1023/100
        if percent>0:
            pwmRB.duty(int(percent))
            pwmRA.duty(0)
        else:
            pwmRB.duty(0)
            pwmRA.duty(int(percent))
        #
    #
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
        ly = CtrlCutTranscode(data[2])
        ry = CtrlCutTranscode(data[4])
        MotoLCtrlL(ly)
        MotoLCtrlR(ry)
    #
    peripheral.SetRxCb(OnRxData)
    #
    while True:
        time.sleep_ms(100)
    #
#

if __name__ == '__main__':
    main()
#
