import time
from paho.mqtt import client as mqtt_client
import uuid

broker = 'broker.emqx.io'
port = 1883
pub_notify_property_changed_topic = "397d8a08-67c1-48f5-8142-e589ceefb408"
sub_control_topic = "12df2614-5d91-4c6b-bb94-f27de18ac0e6"


class Mqtt:
    def __init__(self):
        self.client_id = str(uuid.uuid1())
        self.client = mqtt_client.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_recv_messag
        self.client.connect(broker, port)
        self.client.subscribe(sub_control_topic)
        self.client.loop_start()

        self.on_message = None

    def __del__(self):
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            print("cannot connect to %s" % broker)
            self.client = None
            return
        else:
            print("successful to connect to %s:userdata:%s" % (broker, userdata))

    def on_publish(self, client, userdata, mid):
        """
        :param client: the client instance for this callback
        :param userdata: the private user data as set in Client() or userdata_set()
        :param mid: matches the mid variable returned from the corresponding
                    publish() call, to allow outgoing messages to be tracked.
        :return:
        """
        # print("on_publish: userdata:%s,mid:%d" % (userdata, mid))
        pass

    def on_subscribe(self, client, userdata, mid, granted_qos):
        """
        :param client: the client instance for this callback
        :param userdata: the private user data as set in Client() or userdata_set()
        :param mid: matches the mid variable returned from the corresponding
                    publish() call, to allow outgoing messages to be tracked.
        :return:
        """
        # print("on_subscribe: userdata:%s,mid:%d" % (userdata, mid))
        pass

    def on_recv_messag(self, client, userdata, msg):
        if self.on_message is not None:
            self.on_message(msg.payload.decode())

    def publish_all(self, msg):
        self.client.publish(pub_notify_property_changed_topic, msg)

    def publish_to_client(self, msg, client_id):
        self.client.publish(pub_notify_property_changed_topic + client_id, msg)


if __name__ == "__main__":
    mqtt = Mqtt()


    def on_recv_messag(msg):
        print("on_message: %s" % msg)


    mqtt.on_message = on_recv_messag
    while True:
        time.sleep(2)
        mqtt.publish_all("heasda")
