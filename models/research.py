from uuid import uuid4, UUID
from datetime import datetime, UTC
from enum import Enum
from models.source import Source
from models.fact import Fact

class ResearchStatus(Enum):
    CREATED     = "created"
    INPROGRESS  = "in_progress"
    COMPLETED   = "completed"
    FAILED      = "failed"


class Research():
    def __init__(self, topic: str, status: ResearchStatus = ResearchStatus.CREATED, sources: list[Source] | None = None, facts: list[Fact] | None = None) -> None:
        self.__id: UUID = uuid4()
        self.topic: str = topic
        self.status: ResearchStatus = status
        self.sources: list[Source] = sources if sources is not None else []
        self.facts: list[Fact] = facts if facts is not None else []
        self.created_at: datetime = datetime.now(UTC)
        self.finished_at: datetime | None = None

    # GET
    def get_id(self) -> UUID:
        return self.__id

    # SOURCE
    def add_source(self, source: Source) -> None:
        if isinstance(source, Source) and source not in self.sources:
            self.sources.append(source)

    def remove_source(self, source: Source) -> None:
        if isinstance(source, Source) and source in self.sources:
            self.sources.remove(source)

    # FACT
    def add_fact(self, fact: Fact) -> None:
        if isinstance(fact, Fact) and fact not in self.facts:
            self.facts.append(fact)

    def remove_fact(self, fact: Fact) -> None:
        if isinstance(fact, Fact) and fact in self.facts:
            self.facts.remove(fact)

    # STATUS
    def is_started(self) -> bool:
        return self.status == ResearchStatus.INPROGRESS

    def is_completed(self) -> bool:
        return self.status == ResearchStatus.COMPLETED

    def is_failed(self) -> bool:
        return self.status == ResearchStatus.FAILED

    def start(self) -> None:
        self.status = ResearchStatus.INPROGRESS

    def complete(self) -> None:
        self.status = ResearchStatus.COMPLETED
        self.finished_at = dt.datetime.now(UTC)

    def fail(self) -> None:
        self.status = ResearchStatus.FAILED
        self.finished_at = dt.datetime.now(UTC)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Research):
            return False
        return self.__id == other.get_id()

    def __repr__(self) -> str:
        return f"Research(topic={self.topic}, status={self.status}, created_at={self.created_at}, finished_at={self.finished_at}, sources={len(self.sources)}, facts={len(self.facts)})"
