```markdown
# 🎮 Pixel Pastures - Setup Guide (설치 가이드)

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
✅ **This command generates the following files:**  
✅ **다음 파일들이 생성됩니다:**  
- `game_pb2.py`
- `game_pb2_grpc.py`

These files are required for gRPC server and client communication.  
이 파일들은 gRPC 서버 및 클라이언트 통신에 필요합니다.

---

## 📌 5. Run gRPC Server (gRPC 서버 실행)
```bash
python grpc_server.py
```
✅ **If the server is running successfully, you should see the following message in the terminal:**  
✅ **정상적으로 실행되면 터미널에서 다음 메시지를 확인할 수 있습니다:**  
```bash
✅ gRPC Server running on port 50051...
```


```
