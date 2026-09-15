from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# 建立数据库连接
ASYNC_DATABASE_URI = "mysql+aiomysql://root:root@127.0.0.1:3306/toutiao_db?charset=utf8mb4"
engine = create_async_engine(
            ASYNC_DATABASE_URI,
            echo=True,
    )

# 创建会话工厂
AsyncSessionLocal = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession
    )

# 创建依赖项，获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
