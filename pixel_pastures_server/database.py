from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import aioredis
import asyncio

DATABASE_URL = "postgresql://admin:admin@localhost:5432/pixel_pastures"

# PostgreSQL Connection Setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to initialize the database tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Redis Connection
redis = None

# Initialize Redis connection
async def init_redis():
    try:
        print("🔄 Redis 연결 시도 중...")
        redis = await aioredis.from_url("redis://localhost:6379", decode_responses=True)
        print("✅ Redis 연결 성공!")
        return redis  # Returns Redis instance to store in FastAPI state
    except Exception as e:
        print(f"❌ Redis 연결 실패: {e}")
        return None

async def close_redis():
    global redis
    if redis:
        await redis.close()
        print("🛑 Redis 연결 종료!")
