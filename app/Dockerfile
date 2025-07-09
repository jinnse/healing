FROM python:3.9-slim

# 작업 디렉토리 생성
WORKDIR /app

# 필요한 파일 복사
COPY app.py .

# 코드와 의존성 파일 복사 / flask에 대한 내용이 안에 있다
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt update && apt install -y curl

# 포트 설정 (선택적)
EXPOSE 5000

# 실행 명령
CMD ["python", "app.py"]
