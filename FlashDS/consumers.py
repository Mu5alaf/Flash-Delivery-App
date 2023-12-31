import json
from . import models
from channels.generic.websocket import WebsocketConsumer


class TaskConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        task = text_data_json["task"]
        print('task',task)
        # self.send(text_data=json.dumps({"message": message}))
