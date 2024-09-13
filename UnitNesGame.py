from ControllerInterface import ControlUnit
from ControllerInterface import Table
# from BleCentral import BleCentral
import game, os, time

class UnitNesGame(ControlUnit, Table):
    def __init__(self, lcd, gamepad):
        ControlUnit.__init__(self, lcd, gamepad)
        Table.__init__(self)
        self._nes = game.NES()
        self._games = os.listdir('/nes')
    #
    def GetPicture(self):
        return 'picture/GAME.jpg'
    #
    def MenuEntered(self, menu):
        menu.Reset()
        menu.DrawTable()
        while 'Cancle'!=menu.DoSelect(self):
            time.sleep_ms(50)
        #
        print("Return to Main Menu")
    #
    def Clean(self):
        pass
    #
    def Size(self):
        return len(self._games)
    #
    def PrintInfo(self, lcd, index, position, selected):
        game = self._games[index]
        lcd.PrintStr(game, 2,6+position*49, color=(0,0,0), size=3)
    #
    def OnSelected(self, index):
        game = self._games[index]
        self._nes.start('/nes/'+game)
        return 'Cancle'
    #
#
