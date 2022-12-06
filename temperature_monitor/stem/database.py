from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import create_engine, Column, FLOAT, select
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
    # TODO(Assignment 14)


class Database:
    def __init__(self, engine: Engine):
        pass  # TODO(Assignment 14)

    def add_point(self, point: Point):
        pass  # TODO(Assignment 14)

    def get_points(self, from_date: datetime) -> list[Point]:
        pass  # TODO(Assignment 14)

    @staticmethod
    def create_or_connect_sqlite(config: SqliteConfig) -> "Database":
        pass  # TODO(Assignment 14)