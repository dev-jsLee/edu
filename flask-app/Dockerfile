FROM python:3.11-slim

WORKDIR /app

# 시스템 패키지 업데이트
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# pip 업그레이드
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Python 의존성 설치 (한국 미러 사용)
COPY requirements.txt .
RUN pip install --no-cache-dir \
    --default-timeout=100 \
    --retries 5 \
    --index-url https://mirror.kakao.com/pypi/simple \
    --trusted-host mirror.kakao.com \
    -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 인스턴스 디렉토리 생성 (SQLite용)
RUN mkdir -p instance

# 포트 노출
EXPOSE 5000

# 환경 변수 설정
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

# 애플리케이션 실행
CMD ["python", "run.py"]

