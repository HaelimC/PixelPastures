import grpc  # gRPC를 위한 라이브러리 # gRPC library for server-client communication
from concurrent import futures  # 멀티스레딩 서버 실행을 위해 사용 # For handling multiple requests simultaneously
import game_pb2  # proto 파일에서 생성된 메시지 관련 모듈 # Generated from game.proto (contains message structures)
import game_pb2_grpc  # proto 파일에서 생성된 gRPC 서비스 모듈 # Generated from game.proto (contains gRPC service classes)
from database import SessionLocal # DB 연동 # DB Connect
from models import Player # Player Class
import logging

logging.basicConfig(level=logging.INFO)

# gRPC 서비스 구현 (GameService 정의) # Define the gRPC Service (GameService Implementation)
class GameService(game_pb2_grpc.GameServiceServicer):
    # GameServiceServicer: gRPC 서비스 로직을 구현하는 클래스
    # GameServiceServicer: Implements gRPC service logic

    def GetPlayerState(self, request, context):
        # 플레이어 상태를 조회하는 gRPC 메서드
        # 요청된 player_id를 DB에서 검색하여 해당 플레이어의 위치(x, y) 및 농장 레벨을 반환한다.
        # 만약 플레이어가 존재하지 않는다면 기본값(0.0, 0.0, 1)을 반환한다.
        # gRPC method to retrieve player state
        # Searches for the requested player_id in the database and returns the player's location (x, y) and farm level.
        # If the player does not exist, it returns default values (0.0, 0.0, 1).
                
        # 데이터베이스 세션 생성
        # Create a database session
        db = SessionLocal()
        
        # 요청된 player_id에 해당하는 플레이어 검색
        # Query the player based on the requested player_id
        player = db.query(Player).filter(Player.player_id == request.player_id).first()

        # 플레이어가 존재하지 않을 경우 에러 메세지 반환
        # If the player does not exist, return error message
        if not player:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Player '{request.player_id}' does not exist!")

        # 플레이어가 존재하면 해당 데이터를 반환
        # If the player exists, return their stored data
        return game_pb2.PlayerResponse(
            player_id=player.player_id,  # 플레이어 ID (Player ID)
            x=player.x,  # 플레이어 X 좌표 (Player's X coordinate)
            y=player.y,  # 플레이어 Y 좌표 (Player's Y coordinate)
            farm_level=player.farm_level  # 농장 레벨 (Farm Level)
        )

# gRPC 서버 실행 함수 # Function to start the gRPC server
def serve():
    # gRPC 서버를 실행하는 함수
    # Starts the gRPC server
    
    # gRPC 서버 생성 (멀티스레딩 방식)
    # Create a gRPC server with multithreading
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # GameService를 서버에 등록
    # Register the GameService with the gRPC server
    game_pb2_grpc.add_GameServiceServicer_to_server(GameService(), server)

    # 서버를 50051번 포트에서 실행
    # Set the server to run on port 50051
    server.add_insecure_port("[::]:50051")

    # 서버 시작
    # Start the server
    server.start()
    print("gRPC Server running on port 50051...")

    # 서버가 계속 실행되도록 대기
    # Keep the server running indefinitely
    server.wait_for_termination()

# 실행 코드 (이 파일이 직접 실행될 때만 서버 실행) # Run the server only if this file is executed directly
if __name__ == "__main__":
    serve()
