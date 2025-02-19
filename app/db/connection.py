from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.settings import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=True,
)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession)
