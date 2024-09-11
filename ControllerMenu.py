from UnitPyCar import UnitPyCar
from UnitPyDrone import UnitPyDrone
from UnitPyBoat import UnitPyBoat

class ControllerLcd:
    def __init__(self, lcd):
        self._lcd = lcd
    #
    def Clear(self):
        self._lcd.fill((255,255,255))
    #
    def Picture(self, x, y, file):
        self._lcd.Picture(x, y, file)
    #
#

class MainMenu:
    def __init__(self, ble, lcd, gamepad):
        self._select = 0
        self._lcd = lcd
        self._gamepad = gamepad
        #
        self._units = [UnitPyCar(ble), UnitPyDrone(ble), UnitPyBoat(ble)]
        lcd.Clear()
        self._lcd.Picture(0, 0, self.GetPicture())
    #
    def GetPicture(self):
        return self._units[self._select].GetPicture()
    #
    def Exec(self):
        keys = self._gamepad.read()
        print("get keys: ", keys)
        if keys[1]>200:
            self._select = (self._select+1) % len(self._units)
            self._lcd.Picture(0, 0, self.GetPicture())
        elif keys[1]<50:
            self._select = (self._select-1) % len(self._units)
            self._lcd.Picture(0, 0, self.GetPicture())
        #
        if keys[6]==32:
            self._units[self._select].OnMenuEnter()
            return
        #
    #
#

class ControllerMenu:
    def __init__(self, lcd, gamepad):
        self._lcd = lcd
        self._gamepad = gamepad
    #
    def Clear(self):
        self._lcd.fill((255,255,255))
    #
#