
class ControlUnit():
    def __init__(self, a):
        print("ControlUnit a=", a)
    #
    def GetPicture(self):
        pass
    # (DevSelectMenu menu)
    def MenuEntered(self, menu):
        pass
    #
#

class Table:
    def __init__(self, b, c):
        print("Table b=", b)
        print("Table c=", c)
        self.Clean()
    #
    def Clean(self):
        print("Table Clean")
    #
    def Size(self):
        pass
    #
    def PrintInfo(self, lcd, index, position, selected):
        pass
    #
    def OnSelected(self, index):
        pass
    #
#

class UnitNesGame(ControlUnit, Table):
    def __init__(self, a, b, c):
        print("UnitNesGame")
        ControlUnit.__init__(self, a)
        Table.__init__(self, b, c)
    #
    def Clean(self):
        print("UnitNesGame Clean")
    #
    def Print(self):
        print("Empty")
#

def main():
    print("Welcome to pyBoat MicroPython!")
    demo = UnitNesGame(1, 2, 3)
    demo.Print()
#

if __name__ == '__main__':
    main()
#