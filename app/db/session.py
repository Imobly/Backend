from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base

# Criar engine do banco de dados com configurações de pool
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=True,  # Testa conexão antes de usar (evita conexões mortas)
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency para obter sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Função para criar tabelas
def create_tables():
    # Importar todos os modelos para registrá-los com SQLAlchemy
    import app.db.all_models  # noqa

    Base.metadata.create_all(bind=engine)
