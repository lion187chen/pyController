import time
from ControllerMenu import Controller

def main():
    print("Welcome to pyController!")
    control = Controller()
    #
    while True:
        control.Exec()
        time.sleep_ms(50)
    #
#

if __name__ == '__main__':
    main()
#
