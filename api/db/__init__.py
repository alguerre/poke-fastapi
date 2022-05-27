from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Database:
    def __init__(self, db_url_async: str, db_url_sync: str) -> None:
        self._engine = create_async_engine(db_url_async)
        self._engine_sync = create_engine(db_url_sync)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autoflush=True,
                bind=self._engine,
                class_=AsyncSession
            )
        )

    def drop_existing_tables(self) -> None:
        Base.metadata.drop_all(self._engine_sync)

    def create_new_tables(self) -> None:
        conn = self._engine_sync.connect()
        if not self._engine_sync.dialect.has_table(connection=conn,
                                                   table_name="pokemon"):
            Base.metadata.create_all(self._engine_sync)
        conn.close()

    @contextmanager
    def session(self) -> Generator:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
