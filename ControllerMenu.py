from BleCentral import BleCentral
import bluetooth
import controller
import tftlcd
import time, binascii

from UnitPyCar import UnitPyCar
from UnitPyDrone import UnitPyDrone
from UnitPyBoat import UnitPyBoat

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
DEEPGREEN = (0,139,0) #深绿色

class ControllerLcd:
    def __init__(self):
        self._lcd = tftlcd.LCD15()
    #
    def Clear(self):
        self._lcd.fill((255,255,255))
    #
    def Picture(self, x, y, file):
        self._lcd.Picture(x, y, file)
    #
    def PrintStr(self, text, x, y, color, backcolor=None, size=2):
        self._lcd.printStr(text, x, y, color, backcolor, size)
    #
    def DrawRect(self, x, y, width, height, color, border=1, fillcolor=None):
        self._lcd.drawRect(x, y, width, height, color, border, fillcolor)
#

class MainMenu:
    # (ControllerLcd lcd, controller.CONTROLLER gamepad, BleCentral ble)
    def __init__(self, lcd, gamepad, ble):
        self._select = 0
        self._lcd = lcd
        self._gamepad = gamepad
        #
        self._units = [UnitPyCar(lcd, ble), \
                       UnitPyDrone(lcd, ble), \
                        UnitPyBoat(lcd, ble)]
        self._lcd.Clear()
        self._lcd.Picture(0, 0, self.GetPicture())
    #
    def GetPicture(self):
        return self._units[self._select].GetPicture()
    #
    def DoSelect(self):
        keys = self._gamepad.read()
        if keys[1]>200:
            self._select = (self._select+1) % len(self._units)
            self._lcd.Picture(0, 0, self.GetPicture())
        elif keys[1]<50:
            self._select = (self._select-1) % len(self._units)
            self._lcd.Picture(0, 0, self.GetPicture())
        #
        if keys[2]>200 or keys[2]<50:
            self._lcd.Clear()
            self._units[self._select].OnMenuEnter()
            return self._units[self._select]
        #
        return None
    #
#

class DevSelectMenu:
    # (ControllerLcd lcd, controller.CONTROLLER gamepad)
    def __init__(self, lcd, gamepad):
        self._select = 0
        self._lcd = lcd
        self._gamepad = gamepad
        self._page = 0
    #
    def DrawTable(self):
        for i in range(4):
            # 绘制 4 条两个高的横线，将显示屏分割成 5 个表格。
            self._lcd.DrawRect(0, 48*(i+1), 239, 2, BLACK, border=1, fillcolor=BLACK)
        #
    #
    def DoSelect(self, unit):
        keys = self._gamepad.read()
        if keys[2]>200:
            print("up")
            if self._page+5<unit.Size():
                self._page += 5
                self._select = 0
            #
        elif keys[2]<50:
            print("down")
            if self._page-5 >=0:
                self._page -= 5
                self._select = 0
            #
        #
        for i in range(self._page, self._page+5):
            if i >= unit.Size():
                break
            #
            s = i-self._page
            unit.PrintInfo(self._lcd, i, s, s==self._select)
        #
        if keys[6]==32: # start 键
            print("start")
            unit.Select(self._select)
        #
        time.sleep_ms(50)
    #
#

class Controller(ControllerLcd):
    # (void)
    def __init__(self):
        super().__init__()
        self._gamepad = controller.CONTROLLER()
        self._ble = BleCentral(bluetooth.BLE(), self._gamepad)
        self._dmenu = DevSelectMenu(self, self._gamepad)
        self._mmenu = MainMenu(self, self._gamepad, self._ble)
    #
    def Exec(self):
        unit = self._mmenu.DoSelect()
        if unit:
            self.Clear()
            self._dmenu.DrawTable()
            #
            self._ble.SetCtrlObj(unit)
            self._ble.Scan()
            while not self._ble.IsConnected():
                self._dmenu.DoSelect(unit)
            #
            while True:
                time.sleep(1)
        #
        time.sleep_ms(50)
    #
#
