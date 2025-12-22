from src.models.message import MessageModel


class ReceiptModel:
    id: int
    message: MessageModel

    def __init__(self, id, message):
        self.id = id
        self.message = message
