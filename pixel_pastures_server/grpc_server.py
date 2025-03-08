import grpc  # gRPC를 위한 라이브러리 # gRPC library for server-client communication
from concurrent import futures  # 멀티스레딩 서버 실행을 위해 사용 # For handling multiple requests simultaneously
import game_pb2  # proto 파일에서 생성된 메시지 관련 모듈 # Generated from game.proto (contains message structures)
import game_pb2_grpc  # proto 파일에서 생성된 gRPC 서비스 모듈 # Generated from game.proto (contains gRPC service classes)

# gRPC 서비스 구현 (GameService 정의) # Define the gRPC Service (GameService Implementation)
class GameService(game_pb2_grpc.GameServiceServicer):
    # GameServiceServicer: gRPC 서비스 로직을 구현하는 클래스
    # GameServiceServicer: Implements gRPC service logic

    def GetPlayerState(self, request, context):
        # GetPlayerState 메서드 구현: 클라이언트에서 요청을 받으면 응답을 반환
        # GetPlayerState method: Handles client requests and returns a response
        print(f"Received request for player_id: {request.player_id}")

        # 응답 메시지 생성 # Create and return the response message
        return game_pb2.PlayerResponse(
            player_id=request.player_id,
            x=100.5,  # 가상의 x 좌표 # Simulated x-coordinate
            y=200.0,  # 가상의 y 좌표 # Simulated y-coordinate
            farm_level=1  # 플레이어의 초기 농장 레벨 # Initial farm level
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
