# Import FastAPI framework
from fastapi import FastAPI, Depends
# Import PostgreSQL Library
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Player
import logging

logging.basicConfig(level=logging.INFO)
# Create a FastAPI application instance
app = FastAPI(debug=True)

# create DB before server running (don't forget!)
init_db()

# Define an endpoint (route)
# @app.get("/") -> HTTP GET request
@app.get("/") 
def home():
    # When accessing the root URL ("/"), return a JSON response
    return {"message": "Pixel Pastures Server Running!"}

# Run the server only if this script is executed directly
if __name__ == "__main__":  
    import uvicorn  # Uvicorn: Module for running ASGI Server
    
    # Run FastAPI server with Uvicorn (host: 127.0.0.1, port: 8000)
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True) 

# get DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# save player data (POST)
@app.post("/players/")
def create_player(player_id: str, db: Session = Depends(get_db)):
    try:
        player = Player(player_id=player_id)
        db.add(player)
        db.commit()
        db.refresh(player)
        return {"message": f"Player {player_id} created!", "player": player}
    except Exception as e:
        logging.info(f"create 오류: {str(e)}")
        return {"error": str(e)}

# get player data (GET)
@app.get("/players/{player_id}")
def get_player(player_id: str, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if not player:
        return {"error": "Player not found"}
    return {"player": player}

