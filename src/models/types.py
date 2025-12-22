from enum import Enum


class FileType(Enum):
    IMAGE = "imageMessage"
    VIDEO = "videoMessage"
    DOCUMENT = "documentMessage"
    AUDIO = "audioMessage"

    @classmethod
    def from_str(cls, value: str):
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"Invalid value: {value}")
