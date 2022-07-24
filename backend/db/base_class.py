from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    Каждая модель наследует этот базовый класс, и он будет использован для создания всех таблиц
    БД. Также здесь будем сохранять всю общую логику, связанную с таблицами, в этом «базовом» классе.
    Например, все таблицы таблиц будут иметь поле идентификатора. Это будет использоваться для уникальной
    идентификации каждой строки/записи.
    """
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


a = Base()
print(Base.__tablename__)
