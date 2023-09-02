from util.autosqlite import Table, Column
from datetime import datetime


class User(Table):
    __tablename__ = "users"

    id: int = Column("id", int, primary_key=True)
    guild: int = Column("guild", int, primary_key=True)

    created_at: datetime = Column("created_at", datetime, default=datetime.now())
    inventory: dict[str, int] = Column("inventory", dict[str, int], default={})

    def __init__(self, id: int = None, guild: int = None) -> None:
        super().__init__()

        self.id = id
        self.guild = guild

    def __str__(self) -> str:
        return str(self.__dict__)
