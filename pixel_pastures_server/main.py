# Import FastAPI framework
from fastapi import FastAPI, Depends
# Import PostgreSQL Library
from sqlalchemy.orm import Session
# Import Redis and DB Library
from database import SessionLocal, init_db, init_redis, close_redis, redis
from contextlib import asynccontextmanager
from models import Player
import logging

logging.basicConfig(level=logging.INFO)

# Lifecycle event handler for FastAPI (Runs on startup and shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 FastAPI 서버 시작: Redis 초기화 중...")
    app.state.redis = await init_redis()  # Redis 초기화
    print("✅ Redis 초기화 완료!") 
    yield
    print("🛑 FastAPI 서버 종료: Redis 연결 닫기...")
    await close_redis()  # Redis 종료

# Create a FastAPI application instance
app = FastAPI(lifespan=lifespan)

# Initialize PostgreSQL tables before starting the server
init_db()

# Root Endpoint (Home Page)
# @app.get("/") -> HTTP GET request
@app.get("/") 
def home():
    # When accessing the root URL ("/"), return a JSON response
    return {"message": "Pixel Pastures Server Running!"}

# Run FastAPI server (Only when executed directly)
if __name__ == "__main__":  
    import uvicorn  # Uvicorn: Module for running ASGI Server
    
    # Run FastAPI server with Uvicorn (host: 127.0.0.1, port: 8000)
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True) 

# Database session generator (Dependency injection for FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new player (POST request)
@app.post("/players/")
def create_player(player_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to create a new player in the database.

    - **Input**: `player_id` (Query Parameter)
    - **Process**:
        1. Create a new `Player` object
        2. Save it to the database and commit
        3. Return the stored data
    - **Output**: Player information or error message
    """
    try:
        player = Player(player_id=player_id)
        db.add(player)
        db.commit()
        db.refresh(player)
        return {"message": f"Player {player_id} created!", "player": player}
    except Exception as e:
        logging.info(f"create 오류: {str(e)}")
        return {"error": str(e)}
    
@app.get("/players/all")
async def get_all_players(db: Session = Depends(get_db)):
    redis = app.state.redis  # Get Redis instance

    # Check if cached data exists
    cached_players = await redis.get("players:all")
    if cached_players:
        return {"players": eval(cached_players), "source": "cache"}

    # If not cached, query the database
    players = db.query(Player).all()
    
    if not players:
        return {"error": "No players found"}

    # Convert player data to a list of dictionaries
    players_data = [
        {"player_id": player.player_id, "x": player.x, "y": player.y, "farm_level": player.farm_level}
        for player in players
    ]

    # Store the result in Redis (expire in 60s)
    await redis.setex("players:all", 60, str(players_data))

    return {"players": players_data, "source": "database"}

# Retrieve player data (GET request)
@app.get("/players/{player_id}")
async def get_player(player_id: str, db: Session = Depends(get_db)): #async for await
    """
    Endpoint to retrieve player information (Uses Redis caching).

    - **Input**: `player_id` (Path Parameter)
    - **Process**:
        1. Check Redis for cached player data
        2. If not cached, fetch data from PostgreSQL and store it in Redis
    - **Output**: Player information or error message
    """
    redis = app.state.redis  # Get Redis instance from FastAPI state

    # Check if player data exists in Redis cache
    cached_player = await redis.get(f"player:{player_id}")

    if cached_player:
        return {"player": eval(cached_player), "source": "cache"}

    # If not cached, fetch from the database
    player = db.query(Player).filter(Player.player_id == player_id).first()

    if not player:
        return {"error": "Player not found"}

    # Store fetched data in Redis (expires in 60 seconds)
    await redis.setex(f"player:{player_id}", 60, str({
        "player_id": player.player_id,
        "x": player.x,
        "y": player.y,
        "farm_level": player.farm_level
    }))

    return {"player": player, "source": "database"}

# Redis Debug Endpoint (Check Redis connection status)
@app.get("/debug/redis")
async def debug_redis():
    """
    Debugging endpoint to check Redis connection status.

    - **Output**: Redis connection status and ping response
    """
    redis = app.state.redis # Get Redis instance from FastAPI state
    print(f"🔍 DEBUG: redis 상태 확인 → {redis}")  # ✅ 추가된 로그
    if redis is None:
        return {"error": "❌ Redis가 None 상태입니다!"}
    try:
        pong = await redis.ping()
        return {"message": "✅ Redis 연결 정상!", "ping": pong}
    except Exception as e:
        return {"error": f"❌ Redis 연결 오류: {e}"}

