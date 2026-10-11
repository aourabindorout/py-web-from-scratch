from database.db import get_connection


class Model:
    table_name = ""
    primary_key = "id"

    def __init__(self, **attributes):
        self._attributes = {}
        for key, value in attributes.items():
            self._attributes[key] = value

    def __getattr__(self, name):
        if "_attributes" in self.__dict__ and name in self._attributes:
            return self._attributes[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name in ("_attributes", "table_name", "primary_key"):
            super().__setattr__(name, value)
        else:
            if "_attributes" not in self.__dict__:
                super().__setattr__(name, value)
            else:
                self._attributes[name] = value

    def __getitem__(self, key):
        return self._attributes[key]

    def __setitem__(self, key, value):
        self._attributes[key] = value

    def __contains__(self, key):
        return key in self._attributes

    def keys(self):
        return self._attributes.keys()

    def values(self):
        return self._attributes.values()

    def items(self):
        return self._attributes.items()

    def get(self, key, default=None):
        return self._attributes.get(key, default)

    def to_dict(self):
        return dict(self._attributes)

    @classmethod
    def _get_table_name(cls):
        if cls.table_name:
            return cls.table_name
        return cls.__name__.lower() + "s"

    @classmethod
    def all(cls, order_by=None):
        table = cls._get_table_name()
        query = f"SELECT * FROM {table}"
        if order_by:
            query += f" ORDER BY {order_by}"
        else:
            query += f" ORDER BY {cls.primary_key} DESC"

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return [cls(**dict(row)) for row in rows]

    @classmethod
    def find(cls, pk_value):
        if pk_value is None:
            return None

        table = cls._get_table_name()
        query = f"SELECT * FROM {table} WHERE {cls.primary_key} = ? LIMIT 1"

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (pk_value,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(**dict(row))
        return None

    @classmethod
    def where(cls, **conditions):
        table = cls._get_table_name()
        if not conditions:
            return cls.all()

        where_clauses = [f"{k} = ?" for k in conditions.keys()]
        where_str = " AND ".join(where_clauses)
        query = f"SELECT * FROM {table} WHERE {where_str}"

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, tuple(conditions.values()))
        rows = cursor.fetchall()
        conn.close()
        return [cls(**dict(row)) for row in rows]

    @classmethod
    def first(cls, **conditions):
        records = cls.where(**conditions)
        return records[0] if records else None

    @classmethod
    def create(cls, **attributes):
        instance = cls(**attributes)
        instance.save()
        return instance

    def save(self):
        table = self._get_table_name()
        pk = self.primary_key
        pk_value = self._attributes.get(pk)

        conn = get_connection()
        cursor = conn.cursor()

        if pk_value is None:
            # INSERT
            cols = [k for k in self._attributes.keys() if k != pk]
            if cols:
                placeholders = ", ".join(["?"] * len(cols))
                col_names = ", ".join(cols)
                values = [self._attributes[c] for c in cols]
                query = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
                cursor.execute(query, tuple(values))
            else:
                cursor.execute(f"INSERT INTO {table} DEFAULT VALUES")
            conn.commit()
            self._attributes[pk] = cursor.lastrowid
        else:
            # UPDATE
            cols = [k for k in self._attributes.keys() if k != pk]
            if cols:
                set_clauses = [f"{c} = ?" for c in cols]
                set_str = ", ".join(set_clauses)
                values = [self._attributes[c] for c in cols] + [pk_value]
                query = f"UPDATE {table} SET {set_str} WHERE {pk} = ?"
                cursor.execute(query, tuple(values))
                conn.commit()

        conn.close()
        return self

    def update(self, **attributes):
        for key, value in attributes.items():
            self._attributes[key] = value
        return self.save()

    def delete(self):
        pk = self.primary_key
        pk_value = self._attributes.get(pk)
        if pk_value is None:
            return False

        table = self._get_table_name()
        query = f"DELETE FROM {table} WHERE {pk} = ?"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (pk_value,))
        conn.commit()
        conn.close()

        self._attributes[pk] = None
        return True

    def __repr__(self):
        items = ", ".join(f"{k}={v!r}" for k, v in self._attributes.items())
        return f"<{self.__class__.__name__} {items}>"

