import data as dt

class Model():

    def __init__(self, messages = None):
        self.messages = messages
        self.data=dt.Data(messages)
