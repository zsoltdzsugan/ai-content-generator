from uuid import uuid4, UUID
from enum import Enum
from models.source import Source

class ConfidenceType(Enum):
    LOW     = "low"
    MEDIUM  = "medium"
    HIGH    = "high"
    UNKNOWN = "unknown"


class Fact:
    def __init__(self, statement: str, confidence: ConfidenceType = ConfidenceType.UNKNOWN, sources: list[Source] | None = None) -> None:
        self.__id: UUID = uuid4()
        self.statement: str = statement
        self.confidence: ConfidenceType = confidence
        self.sources: list[Source] = sources if sources is not None else []

    def get_id(self) -> UUID:
        return self.__id

    # SOURCE
    def add_source(self, source: Source) -> None:
        if isinstance(source, Source) and source not in self.sources:
            self.sources.append(source)

    def remove_source(self, source: Source) -> None:
        if isinstance(source, Source) and source in self.sources:
            self.sources.remove(source)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Fact):
           return False
        return self.__id == other.get_id()

    def __repr__(self):
        return f"Fact(statement={self.statement}, confidence={self.confidence}, sources={len(self.sources)})"
