import grpc  # gRPC를 위한 라이브러리 # gRPC library for server-client communication
from concurrent import futures  # 멀티스레딩 서버 실행을 위해 사용 # For handling multiple requests simultaneously
import game_pb2  # proto 파일에서 생성된 메시지 관련 모듈 # Generated from game.proto (contains message structures)
import game_pb2_grpc  # proto 파일에서 생성된 gRPC 서비스 모듈 # Generated from game.proto (contains gRPC service classes)
from database import SessionLocal, redis # DB 연동 # DB Connect
from models import Player # Player Class
import logging

logging.basicConfig(level=logging.INFO)

# gRPC 서비스 구현 (GameService 정의) # Define the gRPC Service (GameService Implementation)
class GameService(game_pb2_grpc.GameServiceServicer):
    """
    gRPC Service that provides player state retrieval functionality.
    """

    def GetPlayerState(self, request, context):
        """
        Handles the request to retrieve player state.
        - Checks Redis cache first.
        - If not found in Redis, retrieves data from PostgreSQL and caches it.

        **Input**: PlayerRequest (`player_id`)
        **Output**: PlayerResponse (`player_id`, `x`, `y`, `farm_level`)
        """
        
        # Create a database session
        db = SessionLocal()

        # Check if Redis is initialized
        if redis is None:
            print("❌ Redis가 None 상태입니다. init_redis()가 호출되지 않았을 가능성이 있습니다.")

        # Try fetching player data from Redis cache
        cached_player = redis.get(f"player:{request.player_id}")

        if cached_player:
            player_data = eval(cached_player)
            return game_pb2.PlayerResponse(
                player_id=player_data["player_id"],
                x=player_data["x"],
                y=player_data["y"],
                farm_level=player_data["farm_level"]
            )
        
        # If not cached, fetch from the database
        player = db.query(Player).filter(Player.player_id == request.player_id).first()

        # If the player does not exist, return error message
        if not player:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Player '{request.player_id}' does not exist!")

        # Cache the retrieved data in Redis (expires in 60 seconds)
        redis.setex(f"player:{request.player_id}", 60, str({
            "player_id": player.player_id,
            "x": player.x,
            "y": player.y,
            "farm_level": player.farm_level
        }))

        # If the player exists, return their stored data
        return game_pb2.PlayerResponse(
            player_id=player.player_id,  # 플레이어 ID (Player ID)
            x=player.x,  # 플레이어 X 좌표 (Player's X coordinate)
            y=player.y,  # 플레이어 Y 좌표 (Player's Y coordinate)
            farm_level=player.farm_level  # 농장 레벨 (Farm Level)
        )

# gRPC 서버 실행 함수 # Function to start the gRPC server
def serve():
    """
    Starts the gRPC server with multi-threading support.
    """    
    # Create a gRPC server with multithreading
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register the GameService with the gRPC server
    game_pb2_grpc.add_GameServiceServicer_to_server(GameService(), server)

    # Set the server to run on port 50051
    server.add_insecure_port("[::]:50051")

    # Start the server
    server.start()
    print("gRPC Server running on port 50051...")

    # Keep the server running indefinitely
    server.wait_for_termination()

# 실행 코드 (이 파일이 직접 실행될 때만 서버 실행) # Run the server only if this file is executed directly
if __name__ == "__main__":
    serve()
