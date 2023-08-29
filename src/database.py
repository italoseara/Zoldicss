import aiosqlite
from dataclasses import dataclass

from settings import *
from user import User


@dataclass
class Database:
    """Database class for the bot

    Args:
        path (str): The path to the database file
        table (str): The name of the table to use"""

    path: str

    def __init__(self, path: str) -> None:
        self.path = path

    async def init(self) -> None:
        """Initialize the database"""
        async with aiosqlite.connect(self.path) as db:
            async with db.cursor() as cursor:
                await cursor.execute(*User.create())
            await db.commit()
            
        await self.update_columns()

    async def get(self, user_id: int, guild_id: int) -> aiosqlite.Row:
        async with aiosqlite.connect(self.path) as db:
            async with db.cursor() as cursor:
                await cursor.execute(
                    *User.select(id=user_id, guild_id=guild_id))
                data = await cursor.fetchone()

                # Create a new user if it doesn't exist
                if data is None:
                    await cursor.execute(
                        *User.insert(id=user_id, guild_id=guild_id))
                    await db.commit()

                    await cursor.execute(
                        *User.select(id=user_id, guild_id=guild_id))
                    data = await cursor.fetchone()

                await cursor.execute(*User.table_info())
                columns = await cursor.fetchall()
                header = [column[1] for column in columns]

        return header, data

    async def update_columns(self) -> None:
        async with aiosqlite.connect(self.path) as db:
            async with db.cursor() as cursor:
                fields = {
                    prop: type_
                    for prop, type_ in User.__annotations__.items()
                    if not prop.startswith("_")
                }

                await cursor.execute(*User.table_info())

                columns = await cursor.fetchall()

                missing_columns = [name for name in fields.keys() if name not in [column[1] for column in columns]]
                deleted_columns = [column[1] for column in columns if column[1] not in fields.keys()]

                if missing_columns:
                    await cursor.execute(*User.add_columns(**{name: fields[name] for name in missing_columns}))

                if deleted_columns:
                    await cursor.execute(*User.drop_columns(*deleted_columns))

                if missing_columns or deleted_columns:
                    await db.commit()

    async def update(self, user: User) -> None:
        """Update a user in the database"""
        async with aiosqlite.connect(self.path) as db:
            async with db.cursor() as cursor:
                await cursor.execute(*User.update(**user.fields))  

            await db.commit()

db = Database(path=DATABASE_PATH)