# Docker 빌드 문제 해결 가이드

## pip install Retrying 문제

### 현상
```
Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None))
```

### 원인
- PyPI 서버 연결 타임아웃
- 네트워크 불안정
- 방화벽/프록시 문제

### 해결 방법

#### 1. 한국 미러 사용 (현재 적용됨)

**Kakao 미러** (기본 설정):
```dockerfile
RUN pip install --no-cache-dir \
    --index-url https://mirror.kakao.com/pypi/simple \
    --trusted-host mirror.kakao.com \
    -r requirements.txt
```

#### 2. 다른 미러 옵션

**KAIST 미러**:
```dockerfile
RUN pip install --no-cache-dir \
    --index-url https://ftp.kaist.ac.kr/pypi/simple \
    --trusted-host ftp.kaist.ac.kr \
    -r requirements.txt
```

**네이버 클라우드 미러**:
```dockerfile
RUN pip install --no-cache-dir \
    --index-url https://mirror.navercorp.com/pypi/simple \
    --trusted-host mirror.navercorp.com \
    -r requirements.txt
```

**알리바바 클라우드 미러** (아시아 지역):
```dockerfile
RUN pip install --no-cache-dir \
    --index-url https://mirrors.aliyun.com/pypi/simple \
    --trusted-host mirrors.aliyun.com \
    -r requirements.txt
```

#### 3. pip 설정 파일 사용

`flask-app/pip.conf` 생성:
```ini
[global]
index-url = https://mirror.kakao.com/pypi/simple
trusted-host = mirror.kakao.com
timeout = 100
retries = 5
```

Dockerfile에 추가:
```dockerfile
COPY pip.conf /etc/pip.conf
```

#### 4. 로컬에서 패키지 다운로드 후 복사

```bash
# 호스트에서 패키지 다운로드
cd flask-app
pip download -r requirements.txt -d packages/

# Dockerfile 수정
COPY packages/ /tmp/packages/
RUN pip install --no-index --find-links=/tmp/packages -r requirements.txt
```

#### 5. Docker 빌드 시 프록시 설정

```bash
docker build \
    --build-arg HTTP_PROXY=http://proxy.example.com:8080 \
    --build-arg HTTPS_PROXY=http://proxy.example.com:8080 \
    -t flask-app .
```

#### 6. DNS 문제 해결

Dockerfile에 추가:
```dockerfile
# DNS 설정
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf
RUN echo "nameserver 8.8.4.4" >> /etc/resolv.conf
```

### 빌드 테스트

```bash
# 캐시 없이 빌드
docker build --no-cache -t flask-app ./flask-app

# 자세한 로그 출력
docker build --progress=plain -t flask-app ./flask-app

# 특정 단계부터 빌드
docker build --target [stage] -t flask-app ./flask-app
```

### docker-compose에서 빌드

```bash
# 캐시 없이 빌드
docker-compose build --no-cache flask-backend

# 병렬 빌드
docker-compose build --parallel
```

## 네트워크 연결 테스트

### 컨테이너 내부에서 테스트

```bash
# 컨테이너 실행
docker run -it python:3.11-slim /bin/bash

# PyPI 연결 테스트
ping pypi.org
curl -I https://pypi.org/simple/

# 한국 미러 연결 테스트
curl -I https://mirror.kakao.com/pypi/simple/
```

## 대안: 멀티 스테이지 빌드

```dockerfile
# 빌더 스테이지
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir --user \
    --index-url https://mirror.kakao.com/pypi/simple \
    --trusted-host mirror.kakao.com \
    -r requirements.txt

# 실행 스테이지
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
CMD ["python", "run.py"]
```

## 최종 권장 사항

1. **한국 미러 사용** (현재 적용됨) - 가장 빠르고 안정적
2. **타임아웃 증가** (100초) - 느린 네트워크 대응
3. **재시도 횟수 증가** (5회) - 일시적 실패 대응
4. **pip/setuptools/wheel 업그레이드** - 호환성 개선

## 문제 지속 시

### 로컬 설치 후 이미지 빌드

```bash
# 1. 로컬에서 Flask 앱 실행 (Docker 없이)
cd flask-app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py

# 2. 작동 확인 후 Docker 빌드
docker build -t flask-app .
```

### 최소 요구사항으로 테스트

`requirements-minimal.txt`:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
```

빌드 테스트:
```bash
docker build --build-arg REQUIREMENTS=requirements-minimal.txt -t flask-app-test .
```

