from uuid import uuid4, UUID
from datetime import datetime, UTC
from enum import Enum

class SourceType(Enum):
    OFFICIAL    = "official"
    NEWS        = "news"
    DATABASE    = "database"
    WIKI        = "wikipedia"
    REVIEW      = "review"
    OTHER       = "other"

class Source():
    def __init__(self, title: str, url: str = "", source_type: SourceType = SourceType.OTHER, content: str = "") -> None:
        self.__id: UUID = uuid4()
        self.title: str = title
        self.type: SourceType = source_type
        self.url: str = url
        self.created_at: datetime = datetime.now(UTC)
        self.content: str = content

    def get_id(self) -> UUID:
        return self.__id

    def __eq__(self, other) -> bool:
        if not isinstance(other, Source):
           return False
        return self.__id == other.get_id()

    def __repr__(self) -> str:
        return f"Source(title={self.title}, type={self.type}, url={self.url}, created_at={self.created_at}, content={len(self.content)})"
