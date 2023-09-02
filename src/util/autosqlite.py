import asyncio
import aiosqlite
from typing import Any, Self
from datetime import datetime


class SQLiteType:
    @staticmethod
    def to(var) -> Any:
        match type(var).__name__:
            case "str" | "list" | "dict" | "tuple" | "set":
                return f"'{var}'"
            case "datetime":
                return f"'{var.strftime('%Y-%m-%d %H:%M:%S')}'"
            case _:
                return var

    @staticmethod
    def from_(type_: type, var: str) -> Any:
        match type_.__name__:
            case "list" | "dict" | "tuple" | "set":
                return eval(var.strip("'"))
            case "str":
                return var.strip("'")
            case "datetime":
                return datetime.strptime(var, "'%Y-%m-%d %H:%M:%S'")
            case _:
                return var


class Column:
    name: str
    type_: type
    default: Any = None
    primary_key: bool = False
    nullable: bool = True

    def __init__(self, name: str, type_: type, default: Any = None, primary_key: bool = False,
                 nullable: bool = True) -> None:
        self.type_ = type_
        self.name = name
        self.default = default
        self.primary_key = primary_key
        self.nullable = nullable

    def _create(self) -> str:
        query = f"{self.name} {self._type()}"
        if self.default is not None:
            query += f" DEFAULT {SQLiteType.to(self.default)}"
        if not self.nullable:
            query += " NOT NULL"
        
        return query

    def _type(self) -> str:
        match self.type_.__name__:
            case "bool" | "int": 
                return "INTEGER"
            case "float": 
                return "REAL"
            case "str" | "list" | "dict" | "tuple" | "set": 
                return "TEXT"
            case "datetime":
                return "DATETIME"
            case _:
                return "BLOB"


class Table:
    __tablename__: str = None
    __columns__: list["Column"] = None
    __primary_keys__: list[str] = None

    def __init__(self) -> None:
        self.__columns__ = []
        self.__primary_keys__ = []
        
        for key in self.__annotations__.keys():
            value = self.__getattribute__(key)
            
            if isinstance(value, Column):
                self.__columns__.append(value)
                if value.primary_key:
                    self.__primary_keys__.append(value.name)
                setattr(self, key, value.default)

    @classmethod
    def load(cls, data: tuple) -> Self:
        instance = cls()
        for key, type_, value in zip(cls.__annotations__.keys(), cls.__annotations__.values(), data):
            setattr(instance, key, SQLiteType.from_(type_, value))

        return instance

    @classmethod
    def _get_columns(self) -> tuple[list, list]:
        columns = []
        primary_keys = []
        for key in self.__annotations__.keys():
            value = getattr(self, key)
            if isinstance(value, Column):
                columns.append(value)
                if value.primary_key:
                    primary_keys.append(value.name)

        return columns, primary_keys

    @classmethod
    def _create(self) -> str:
        columns, primary_keys = self._get_columns()

        columns = ",\n\t".join([column._create() for column in columns])
        primary_keys = ", ".join(primary_keys)

        return f"CREATE TABLE IF NOT EXISTS {self.__tablename__} (\n\t{columns}, \n\tPRIMARY KEY ({primary_keys})\n);", tuple()

    @classmethod
    def _select(cls, **kwargs) -> tuple[str, tuple]:
        # Get the list of parameters.
        parameters = tuple(kwargs.values())

        # Get the list of filters.
        filters = [f"{k} = ?" for k in kwargs.keys()]

        # Generate the query.
        query = f"SELECT * FROM {cls.__tablename__} WHERE {' AND '.join(filters)};"
        
        return query, parameters

    @classmethod
    def _add_columns(cls, *args) -> str:
        columns = [getattr(cls, column) for column in args]
        return f"ALTER TABLE {cls.__tablename__} ADD COLUMN {', '.join([column._create() for column in columns])};", tuple()

    @classmethod
    def _drop_columns(cls, *args) -> str:
        return f"ALTER TABLE {cls.__tablename__} DROP COLUMN {', '.join(args)};", tuple()

    @classmethod
    def _drop_all(cls) -> str:
        return f"DROP TABLE IF EXISTS {cls.__tablename__};", tuple()

    @classmethod
    def _pragma(cls) -> str:
        return f"PRAGMA table_info({cls.__tablename__});", tuple()

    def _insert(self) -> tuple[str, tuple]:
        columns = ", ".join([column.name for column in self.__columns__])
        values = [SQLiteType.to(getattr(self, column.name)) for column in self.__columns__]
        placeholders = ", ".join(["?" for _ in range(len(values))])

        return f"INSERT INTO {self.__tablename__} ({columns}) VALUES ({placeholders});", tuple(values)

    def _update(self) -> tuple[str, tuple]:
        update = []
        parameters = []
        primary_keys = []
        for key in self.__annotations__.keys():
            value = getattr(self, key)
            if key not in self.__primary_keys__:
                parameters.append(SQLiteType.to(value))
                update.append(f"{key} = ?")
            else:
                primary_keys.append(f"{key} = {value}")

        update = ", ".join(update)
        primary_keys = " AND ".join(primary_keys)

        return f"UPDATE {self.__tablename__} SET {update} WHERE {primary_keys};", tuple(parameters)


class Session:
    path: str
    _db: aiosqlite.Connection
    _cursor: aiosqlite.Cursor

    def __init__(self, path: str) -> None:
        self.path = path

    async def __aenter__(self) -> Self:
        self._db = await aiosqlite.connect(self.path)
        self._cursor = await self._db.cursor()

        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._db.commit()
        await self._cursor.close()
        await self._db.close()

    async def update(self, table: Table) -> None:
        await self._cursor.execute(*table._update())

    async def create(self, table: Table) -> None:
        await self._cursor.execute(*table._create())

    async def drop(self, table: Table) -> None:
        await self._cursor.execute(*table._drop_all())

    async def check(self, table: Table) -> None:
        await self._cursor.execute(*table._pragma())

        table_columns = [column[1] for column in await self._cursor.fetchall()]
        columns, _ = table._get_columns()

        missing = [column.name for column in columns if column.name not in table_columns]
        removed = [column for column in table_columns if column not in [column.name for column in columns]]

        if missing:
            await self._cursor.execute(*table._add_columns(*missing))
        if removed:
            await self._cursor.execute(*table._drop_columns(*removed))

    async def add(self, table: Table) -> None:
        await self._cursor.execute(*table._insert())

    async def get(self, table: Table, **kwargs) -> Table:
        await self._cursor.execute(*table._select(**kwargs))
        data = await self._cursor.fetchone()

        if data is None:
            await self.add(table(**kwargs))
            return await self.get(table, **kwargs)

        return table.load(data)


session = Session("data/database.db")
