# 🎮 Pixel Pastures - Basic Server Setting

## 📌 1. Python Virtual Environment Setup (Python 가상환경 설정)
```bash
# Create a virtual environment (가상환경 생성)
python -m venv venv

# Activate the virtual environment (Windows)
source venv/Scripts/activate

# Activate the virtual environment (Mac/Linux)
source venv/bin/activate
```

---

## 📌 2. Install Essential Libraries (필수 라이브러리 설치)
```bash
pip install fastapi uvicorn grpcio grpcio-tools pydantic psycopg2 aioredis confluent-kafka
```

---

## 📌 3. Run FastAPI Server (FastAPI 서버 실행)
```bash
uvicorn main:app --reload
```
✅ **Check the running server at:**  
🔗 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  

**Expected Response (응답 예시):**
```json
{"message": "Pixel Pastures Server Running!"}
```

---

## 📌 4. Convert `game.proto` to Python (`game.proto` → `game_pb2.py`, `game_pb2_grpc.py`)
```bash
python -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/game.proto
```
✅ **This command generates the following files (다음 파일들이 생성됩니다):**  
- `game_pb2.py`
- `game_pb2_grpc.py`

These files are required for gRPC server and client communication.  
이 파일들은 gRPC 서버 및 클라이언트 통신에 필요합니다.

---

## 📌 5. Run gRPC Server (gRPC 서버 실행)
```bash
python grpc_server.py
```
✅ **If the server is running successfully, the following message will appear in the terminal.**  
✅ **서버가 정상적으로 실행되면, 터미널에 다음 메시지가 출력됩니다.**  
```bash
gRPC Server running on port 50051...
```

---

## 📌 **6. Run PostgreSQL & Redis with Docker Compose (Docker Compose로 PostgreSQL & Redis 실행)**
```bash
docker-compose up -d
```
✅ This command starts both **PostgreSQL** and **Redis** together.  
✅ 이 명령어는 **PostgreSQL**과 **Redis**를 함께 실행합니다.

---

## 📌 **7. Connect to PostgreSQL (PostgreSQL 접속)**
```bash
docker exec -it postgres psql -U admin -d pixel_pastures
```
✅ **Now you can execute SQL commands inside PostgreSQL.**  
✅ **이제 PostgreSQL 내부에서 SQL 명령어를 실행할 수 있습니다.**

#### 🔹 **List all tables (현재 데이터베이스의 테이블 확인)**
```sql
\dt
```
#### 🔹 **Exit PostgreSQL shell (PostgreSQL 셸 종료)**
```sql
\q
```

---

## 📌 **8. Connect to Redis (Redis 접속)**
```bash
docker exec -it redis redis-cli
```
✅ **Now you can execute Redis commands inside the Redis shell.**  
✅ **이제 Redis 내부에서 명령어를 실행할 수 있습니다.**

#### 🔹 **Test Redis Connection (Redis 연결 테스트)**
```bash
ping
```
✅ **If Redis is working properly, it should return:**  
✅ **Redis가 정상적으로 작동하면 다음과 같이 표시됩니다:**  
```bash
PONG
```

---

## 📌 9. Apply Database Migrations in FastAPI (FastAPI에서 데이터베이스 적용)
```bash
uvicorn main:app --reload
```
✅ **If everything is set up correctly, FastAPI will create the required tables in PostgreSQL.**  
✅ **설정이 올바르면, FastAPI가 PostgreSQL에 필요한 테이블을 생성합니다.**

---

## 📌 10. Run gRPC Client (gRPC 클라이언트 실행)
```bash
python grpc_client.py
```
✅ **If the client is running successfully, you should see the following messages in the terminal:**  
✅ **클라이언트가 정상적으로 실행되면, 터미널에 다음 메시지가 출력됩니다:**  

### **📌 When a player exists (플레이어가 존재할 때)**
```bash
Player Found!!
player_id: player123
x: 0.0
y: 0.0
farm_level: 1
```

### **📌 When a player does not exist (플레이어가 존재하지 않을 때)**
```bash
Error: StatusCode.NOT_FOUND - Player 'unknown_player' does not exist!
```

---

## 📌 11. Debug Redis Connection (Redis 연결 디버깅)
```bash
curl -X GET "http://127.0.0.1:8000/debug/redis"
```
✅ **If Redis is working properly, you should see:**  
✅ **Redis가 정상적으로 작동하면, 다음과 같은 응답을 받을 수 있습니다:**  
```json
{"message": "✅ Redis is working properly!", "ping": "PONG"}
```

If Redis is not connected, you may see an error message like:  
Redis가 연결되지 않았다면, 다음과 같은 오류 메시지가 표시될 수 있습니다:  
```json
{"error": "❌ Redis is in None state!"}
```


