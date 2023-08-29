from typing import Tuple

class SQLiteTable:
    _primary_key: tuple[str] = ("id",)

    @property
    def fields(self) -> tuple:
        return {
            prop: getattr(self, prop)
            for prop in self.__annotations__.keys() 
            if not prop.startswith("_")
        }

    @property
    def primary_key(self) -> tuple:
        return {
            prop: getattr(self, prop)
            for prop in self._primary_key
        }

    @staticmethod
    def _sqlite_type(type_) -> str:
        return {
            bool: "INTEGER",
            int: "INTEGER",
            float: "REAL",
            str: "TEXT",
            list: "TEXT",
            dict: "TEXT",
        }.get(eval(type_) if isinstance(type_, str) else type_, "TEXT")

    @classmethod
    def select(cls, *args, **kwargs) -> Tuple[str, tuple]:
        """
        Select records from the database.

        Args:
            *args: The columns to be selected.
            **kwargs: The filters for the selection.

        Returns:
            A tuple of the SQLite query and the list of parameters.
        """

        # Get the list of columns.
        columns = ', '.join(args) if args else '*'

        # Get the list of parameters.
        parameters = tuple(kwargs.values())

        # Get the list of filters.
        filters = [f"{k} = ?" for k in kwargs.keys()]

        # Generate the SQLite query.
        query = f"SELECT {columns} FROM {cls.__name__.lower()} "
        query += f"WHERE {' AND '.join(filters)};"

        return query, parameters

    @classmethod
    def insert(cls, **kwargs) -> Tuple[str, tuple]:
        """
        Insert a record into the database.

        Args:
            **kwargs: The key-value pairs of the record to be inserted.

        Returns:
            A tuple of the SQLite query and the list of parameters.
        """

        # Get the list of columns.
        columns = [prop.lower() for prop in kwargs.keys()]

        # Get the list of parameters.
        parameters = tuple(str(v) for v in kwargs.values())

        # Get the list of placeholders.
        placeholders = ["?" for _ in range(len(columns))]

        # Generate the SQLite query.
        query = f"INSERT INTO {cls.__name__.lower()} ({', '.join(columns)}) VALUES ({', '.join(placeholders)});"

        # Return the query and the parameters.
        return query, parameters

    @classmethod
    def update(cls, **kwargs) -> tuple:
        """
        Update a record in the database.

        Args:
            **kwargs: The key-value pairs of the record to be updated.

        Returns:
            A tuple of the SQLite query and the list of parameters.
        """
    
        query = f"UPDATE {cls.__name__.lower()} SET "

        # Generate the list of columns to be updated.
        updated_columns = [k for k in kwargs.keys() if k not in cls._primary_key]

        # Generate the list of parameters.
        parameters = tuple(str(kwargs[k]) for k in updated_columns)

        query += ', '.join(f'{c} = ?' for c in updated_columns)
        query += f" WHERE {' AND '.join(f'{k} = {v}' for k, v in kwargs.items() if k in cls._primary_key)}"

        return query, parameters

    @classmethod
    def create(cls) -> Tuple[str, tuple]:
        """
        Create the table in the database.

        Returns:
            A tuple of the SQLite query and the list of parameters.
        """
        
        query = f"CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} ("
        
        for prop, type_ in cls.__annotations__.items():
            if prop.startswith("_"):
                continue

            sql_type = cls._sqlite_type(type_)
            query += f"{prop} {sql_type}"

            # Add the default value if necessary.
            if (default := getattr(cls, prop, None)) is not None:
                default = f'"{default}"' if sql_type == "TEXT" else default
                query += f" DEFAULT {default}"

            query += ", "

        query += f"PRIMARY KEY ({', '.join(cls._primary_key)}));"
        return query, tuple()

    @classmethod
    def drop(cls) -> Tuple[str, tuple]:
        """
        Drop the table from the database.
        """
        
        return f"DROP TABLE IF EXISTS {cls.__name__.lower()};", tuple()

    @classmethod
    def add_columns(cls, **kwargs) -> Tuple[str, tuple]:
        """
        Add a column to the table.

        Args:
            **kwargs: The name and type of the column to be added.

        Returns:
            A tuple of the SQLite query and the list of parameters.
        """
        
        query = f"ALTER TABLE {cls.__name__.lower()} ADD "

        for prop, type_ in kwargs.items():
            sql_type = cls._sqlite_type(type_)
            query += f"{prop} {sql_type}"

            # Add the default value if necessary.
            if (default := getattr(cls, prop, None)) is not None:
                default = f'"{default}"' if sql_type == "TEXT" else default
                query += f" DEFAULT {default}"
                
            query += ", "

        query = query[:-2] + ";"
        return query, tuple()

    @classmethod
    def drop_columns(cls, *args) -> Tuple[str, tuple]:
        """
        Drop a column from the table.

        Args:
            *args: The name of the column to be dropped.

        Returns:
            A tuple of the SQLite query and the list of parameters.
        """
        
        query = f"ALTER TABLE {cls.__name__.lower()} DROP COLUMN {', '.join(args)};"
        return query, tuple()

    @classmethod
    def table_info(cls) -> Tuple[str, tuple]:
        """
        Get the table info.

        Returns:
            A tuple of the SQLite query and the list of parameters.
        """
        
        return f"PRAGMA table_info({cls.__name__.lower()});", tuple()
