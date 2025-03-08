# Import FastAPI framework
# FastAPI를 가져와서 사용할 준비를 합니다.
from fastapi import FastAPI

# Create a FastAPI application instance
# FastAPI 서버 인스턴스를 생성합니다.
app = FastAPI()

# Define an endpoint (route)
# @app.get("/") -> HTTP GET 요청을 처리하는 엔드포인트를 정의합니다.
@app.get("/") 
def home():
    # When accessing the root URL ("/"), return a JSON response
    # 루트 경로("/")로 요청이 들어오면 JSON 응답을 반환합니다.
    return {"message": "Pixel Pastures Server Running!"}

# Run the server only if this script is executed directly
# 이 파일이 직접 실행될 때만 실행 (다른 파일에서 import될 경우 실행되지 않음)
if __name__ == "__main__":  
    import uvicorn  # Uvicorn: ASGI 서버 실행을 위한 모듈
    
    # Run FastAPI server with Uvicorn
    # FastAPI 서버 실행 (호스트: 127.0.0.1, 포트: 8000, 코드 변경 시 자동 재시작)
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True) 
