import logging
from datetime import datetime

from src.models.types import FileType


class MessageModel:
    def __init__(self, id: str, time: datetime, chat_id: str, sender_id: str, sender_name: str, chat_name: str):
        self.id = id
        self.time = time
        self.chat_id = chat_id
        self.sender_id = sender_id
        self.sender_name = sender_name
        self.chat_name = chat_name

    def __str__(self):
        return f"Message: {self.id}\nTime: {self.time}\nChat ID: {self.chat_id}\nSender ID: {self.sender_id}\nSender Name: {self.sender_name}\nChat Name: {self.chat_name}\nClass: {self.__class__.__name__}"


class TextMessageModel(MessageModel):
    def __init__(self, id: str, time: datetime, chat_id: str, text: str, sender_id: str, sender_name: str,
                 chat_name: str):
        super().__init__(id, time, chat_id, sender_id, sender_name, chat_name)
        self.text = text


class FileMessageModel(MessageModel):
    def __init__(self, id: str, time: datetime, chat_id: str, sender_id: str, sender_name: str, chat_name: str,
                 caption: str, file_url: str, file_type: FileType):
        super().__init__(id, time, chat_id, sender_id, sender_name, chat_name)
        self.caption = caption
        self.file_url = file_url
        self.file_type = file_type


class MessageFactory:
    @staticmethod
    def from_json(data) -> MessageModel:
        time = datetime.fromtimestamp(data["timestamp"])
        sender_data = data["senderData"]
        message_data = data["messageData"]
        type_message = message_data["typeMessage"]
        if "text" in type_message.lower():
            if type_message == "textMessage":
                message = message_data["textMessageData"]["textMessage"]
            elif type_message == "extendedTextMessage":
                message = message_data["extendedTextMessageData"]["text"]
            else:
                message = "Данный тип сообщений не поддерживается"
            res = TextMessageModel(
                id=data["idMessage"],
                time=time,
                chat_id=sender_data["chatId"],
                text=message,
                sender_id=sender_data["sender"],
                sender_name=sender_data["senderName"],
                chat_name=sender_data["chatName"]
            )
        elif type_message in ("imageMessage", "videoMessage", "documentMessage", "audioMessage"):
            file_message = message_data["fileMessageData"]
            file_type = FileType.from_str(type_message)
            res = FileMessageModel(
                id=data["idMessage"],
                time=time,
                chat_id=sender_data["chatId"],
                sender_id=sender_data["sender"],
                sender_name=sender_data["senderName"],
                chat_name=sender_data["chatName"],
                caption=file_message["caption"],
                file_type=file_type.from_str,
                file_url=file_message["downloadUrl"]
            )
        else:
            res = TextMessageModel(
                id=data["idMessage"],
                time=time,
                chat_id=sender_data["chatId"],
                text="Данный тип сообщений не поддерживается",
                sender_id=sender_data["sender"],
                sender_name=sender_data["senderName"],
                chat_name=sender_data["chatName"]
            )
        logging.debug(f"Message created: {res}")
        return res
