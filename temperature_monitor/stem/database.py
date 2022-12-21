from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import create_engine, Column, FLOAT, select, insert, Integer
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, Session


@dataclass
class SqliteConfig:
    path: str = "test.sqlite"
    echo: bool = True


Base = declarative_base()


class Point(Base):
    __tablename__ = "temperature"
    id = Column("id", Integer, primary_key=True)
    temp = Column(FLOAT)
    time = Column(DATETIME)


class Database:
    def __init__(self, engine: Engine):
        self.engine = create_engine(SqliteConfig.path)

    def add_point(self, point: Point):
        stmt = insert(Point.__tablename__).values(temp=Point.temp, time=Point.time)
        compiled = stmt.compile()
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        

    def get_points(self, from_date: datetime) -> list[Point]:
        pass  # TODO(Assignment 14)

    @staticmethod
    def create_or_connect_sqlite(config: SqliteConfig) -> "Database":
        pass  # TODO(Assignment 14)


if __name__ == "__main__":
    print(Point.temp)