import os
import json
import logging
import uuid

from pyee import EventEmitter
from websocket import (
WebSocketApp,
WebSocketConnectionClosedException,
WebSocketException)

def str2uuid(string):
    return uuid.UUID(string)

class Message:
    """
    Attributes:
        type (str): type of the data sent within the message
        data(dict): data sent within the message

    """
    def __init__(self,event, data=None):
        data = data or {}
        self.event = event
        self.data = data


    def serialize(self):
        return json.dumps({
            "type": self.type,
            "data": self.data,

        })

    @staticmethod
    def deserialize(payload):
        obj = json.loads(message)
        return Message(obj.get("type"), obj.get("data"))



class WebsocketClient(object):
    def __init__(self, host=None, port=None, ssl=None, client_name=None):
        host = host or os.getenv('WebsocketHost')
        port = port or os.getenv('WebsocketPort')
        ssl = ssl or os.getenv('SSL')
        self.client_name = client_name
        self.emitter = self.EventEmitter()
        self.client = self.create_client()
        self.started_running = False
        self.retry = 5

        self.url = WebsocketClient(host, port, ssl)
        self.logger = logging.getLogger(self.client_name)
        self.logger.setLevel(logging.DEBUG)


    @staticmethod
    def build_url(host, port, ssl):
        scheme = "wss" if ssl else "ws"
        return "{}://{}:{}".format(scheme, host, str(port))

    def create_client(self):
        return WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message
        )

    def on_close(self, ws):
        self.logger.info("Closing connection")
        self.emitter.emit('close')

    def on_open(self, ws):
        self.logger.info("Connected")
        self.emitter.emit("open")

    def on_error(self, ws, error):
        if isinstance(error, WebSocketConnectionClosedException):
            self.logger.warn("Could not send message because message connection has closed")
        else:
            self.logger.critical("=== " + repr(error) + " ===")
        try:
            self.emitter.emit("error", error)
            if self.client.keep_running:
                self.client.close()
        except Exception as e:
            self.logger.error("Exception closing websocket: " + repr(e))

        self.logger.warn("WS Client will reconnect in %d seconds." % self.retry)
        time.sleep(self.retry)
        self.retry = min(self.retry * 2, 60)

        try:
            self.client = self.create_client()
            self.run_forever()
        except WebSocketException:
            pass

    def on_message(self, ws, message):
        parsed_message = Message.deserialize(message)
        self.emitter.emit(parsed_message.event, parsed_message)

    def on(self, event_name, func):
        self.emitter.on(event_name, func)

    def once(self, event_name, func):
        self.emitter.once(event_name, func)


    def run_forever(self):
        self.client.run_forever()

    def close(self):
        self.client.close()
        self.connected_event.clear()
