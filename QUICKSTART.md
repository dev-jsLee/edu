# 빠른 시작 가이드

## 1. Docker Compose로 실행 (추천)

```bash
# 1. docker-compose.new.yml을 docker-compose.yml로 복사 (또는 직접 사용)
cp docker-compose.new.yml docker-compose.yml

# 2. 서비스 시작
docker-compose up -d

# 3. 데이터베이스 초기화 (샘플 데이터 생성)
docker exec python-learning-flask python init_db.py

# 4. 브라우저에서 접속
# http://localhost:5000
```

## 2. 로컬에서 실행 (개발용)

### Flask 앱 실행

```bash
cd flask-app

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 초기화
python init_db.py

# Flask 앱 실행
python run.py
```

### 코드 러너 실행 (별도 터미널)

```bash
cd code-runner

# 의존성 설치
pip install -r requirements.txt

# 코드 러너 실행
python runner.py
```

### 브라우저 접속
- 메인 앱: http://localhost:5000
- 코드 러너: http://localhost:8080

## 3. 샘플 계정

초기 데이터베이스 생성 시 다음 계정이 자동으로 생성됩니다:

- **관리자**
  - 사용자명: `admin`
  - 비밀번호: `admin123`

- **학생**
  - 사용자명: `student1`
  - 비밀번호: `student123`

## 4. 테스트

### 회원가입
1. http://localhost:5000/register 접속
2. 사용자명, 이메일, 비밀번호 입력
3. 회원가입 버튼 클릭

### 로그인
1. http://localhost:5000/login 접속
2. 사용자명과 비밀번호 입력
3. 로그인 버튼 클릭

### 수업 자료 보기
1. 상단 메뉴에서 "수업 자료" 클릭
2. 자료 카드를 클릭하여 상세 내용 확인

### 코드 실행하기
1. 상단 메뉴에서 "문제 풀이" 클릭
2. 문제를 선택
3. 코드 에디터에 Python 코드 작성
4. "실행" 버튼으로 테스트
5. "제출" 버튼으로 저장

### 내 기록 보기
1. 상단 메뉴에서 "내 기록" 클릭
2. 제출한 코드 목록 확인

## 5. 문제 해결

### 포트가 이미 사용 중인 경우
```bash
# docker-compose.yml 파일에서 포트 변경
ports:
  - "5001:5000"  # 5000 대신 5001 사용
```

### 데이터베이스 초기화
```bash
# Docker 사용 시
docker-compose down -v
docker-compose up -d
docker exec python-learning-flask python init_db.py

# 로컬 실행 시
rm flask-app/instance/app.db
python flask-app/init_db.py
```

### 코드 러너 연결 실패
```bash
# 코드 러너 상태 확인
docker logs python-learning-code-runner

# 또는 로컬에서 직접 실행
cd code-runner
python runner.py
```

## 6. 개발 팁

### 파일 수정 시 자동 재시작
- Flask는 개발 모드에서 자동으로 재시작됩니다
- Docker 사용 시 볼륨 마운트가 설정되어 있어 코드 수정이 즉시 반영됩니다

### API 테스트
```bash
# curl로 API 테스트
curl http://localhost:5000/api/materials

# 로그인
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","password":"student123"}'
```

### 로그 확인
```bash
# Docker 로그
docker-compose logs -f flask-backend
docker-compose logs -f code-runner

# 또는 특정 컨테이너
docker logs python-learning-flask -f
```

## 7. 다음 단계

- 수업 자료 추가 (관리자 기능 구현 필요)
- 문제 데이터베이스 구축
- 자동 채점 시스템 구현
- PostgreSQL로 마이그레이션

자세한 내용은 `README.new.md`를 참조하세요.

