import time, json
from threading import Lock
from car import RobotCar
from mqtt import Mqtt

current_client_id = None
user_lock = Lock()
current_status = ""
mqtt = Mqtt()


def on_message(msg):
    global current_client_id
    user_lock.acquire()
    try:

        direction = json.loads(msg).get("direction")
        client_id = json.loads(msg).get("clientId")
        if direction is None or client_id is None:
            return

        if current_client_id is not None and client_id != current_client_id:
            mqtt.publish_to_client("The car is being controlled by others", client_id=client_id)
            return

        current_client_id = client_id
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
            current_client_id = None

    except Exception as e:
        print(e)
    finally:
        user_lock.release()


def on_car_status_changed(status):
    if status != "stop":
        mqtt.publish_all("The car is running to the " + status)
    else:
        mqtt.publish_all("The cas is stopped")
    global current_status
    current_status = status


mqtt.on_message = on_message
RobotCar.on_status_changed = on_car_status_changed


def run():
    while True:
        time.sleep(2)


if __name__ == "__main__":
    run()
