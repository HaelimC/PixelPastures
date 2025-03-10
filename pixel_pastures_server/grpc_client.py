import grpc
import game_pb2, game_pb2_grpc

# gRPC 채널을 생성하여 서버와 연결
# Create a gRPC channel to connect with the server
channel = grpc.insecure_channel("localhost:50051")

# gRPC 서비스 스텁 생성 (클라이언트 역할)
# Create a gRPC service stub (acts as the client)
stub = game_pb2_grpc.GameServiceStub(channel)

# 조회할 플레이어 ID 지정
# Set the player ID to retrieve
player_id = "player123"

try:
    # gRPC 서버에 요청을 보내서 플레이어 상태 가져오기
    # Send request to gRPC server to get player state
    response = stub.GetPlayerState(game_pb2.PlayerRequest(player_id=player_id))

    # 서버에서 받은 응답 출력
    # Print the response from the server
    print(f"Player Found!! \n{response}")

except grpc.RpcError as e:
    # gRPC 서버에서 에러 응답이 왔을 때 예외 처리
    # Handle exceptions if the gRPC server returns an error
    print(f"Error: {e.code()} - {e.details()}")