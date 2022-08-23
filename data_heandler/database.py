
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from data_heandler.config import Config

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''
@lru_cache()
def get_engine() -> engine.Engine:
    return create_engine(
        Config.SQLALCHEMY_DATABASE_URI,
        # connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )


@contextmanager
def get_db(db_conn=Depends(get_engine)) -> Iterable[Session]:
    # Explicit type because sessionmaker.__call__ stub is Any
    session: Session = sessionmaker(autocommit=False, autoflush=False, bind=db_conn)()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
'''
