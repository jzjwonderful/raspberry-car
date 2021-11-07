import RPi.GPIO as io
import time
import sys

GPIO_0 = 11
GPIO_1 = 12
GPIO_2 = 13
GPIO_3 = 15


class RobotCar:
    status = "stop"

    @staticmethod
    def statusChanged(new_status):
        if new_status != RobotCar.status:
            RobotCar.status = new_status
            if RobotCar.on_status_changed is not None:
                RobotCar.on_status_changed(new_status)

    @staticmethod
    def __init__():
        io.setmode(io.BOARD)
        io.setup(GPIO_0, io.OUT)
        io.setup(GPIO_1, io.OUT)
        io.setup(GPIO_2, io.OUT)
        io.setup(GPIO_3, io.OUT)
        io.output(GPIO_0, False)
        io.output(GPIO_1, False)
        io.output(GPIO_2, False)
        io.output(GPIO_3, False)

    def __del__(self):
        io.cleanup()

    @staticmethod
    def forward():
        io.output(GPIO_0, False)
        io.output(GPIO_1, True)
        io.output(GPIO_2, True)
        io.output(GPIO_3, False)
        RobotCar.statusChanged("forward")

    @staticmethod
    def back():
        io.output(GPIO_0, True)
        io.output(GPIO_1, False)
        io.output(GPIO_2, False)
        io.output(GPIO_3, True)
        RobotCar.statusChanged("back")

    @staticmethod
    def stop():
        io.output(GPIO_0, False)
        io.output(GPIO_1, False)
        io.output(GPIO_2, False)
        io.output(GPIO_3, False)
        RobotCar.statusChanged("stop")

    @staticmethod
    def left():
        io.output(GPIO_0, False)
        io.output(GPIO_1, True)
        io.output(GPIO_2, False)
        io.output(GPIO_3, False)
        RobotCar.statusChanged("left")

    @staticmethod
    def right():
        io.output(GPIO_0, False)
        io.output(GPIO_1, False)
        io.output(GPIO_2, True)
        io.output(GPIO_3, False)
        RobotCar.statusChanged("right")


RobotCar.__init__()

def __run_car(direction):
    """
    Driving car with direction and duration time(sec)
    :param direction:l == go to left;r == right f == forward b == back
    :return:
    """
    if 'forward' == direction:
        RobotCar.forward()
    elif 'back' == direction:
        RobotCar.back()
    elif 'left' == direction:
        RobotCar.left()
    elif 'right' == direction:
        RobotCar.right()
    elif 'stop' == direction:
        RobotCar.stop()


if __name__ == '__main__':
    __run_car("forward")
