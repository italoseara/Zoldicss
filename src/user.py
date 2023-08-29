from typing import Self, Any
from util.sqlite import SQLiteTable


class User(SQLiteTable):
    """User class for the bot"""

    _db: Any

    # Primary key
    id: int
    guild_id: int
    _primary_key = ("id", "guild_id")

    # Fields
    xp: int = 0
    level: int = 1
    teste: list = []
    
    def __init__(self, db: Any, id: int, guild_id: int) -> None:
        self._db = db
        self.id = id
        self.guild_id = guild_id

    async def __aenter__(self) -> Self:
        header, data = await self._db.get(self.id, self.guild_id)

        for column, value in zip(header, data):
            type_ = self.__annotations__[column]
            setattr(self, column, eval(value) if type_ in [dict, list] else value)

        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._db.update(self)