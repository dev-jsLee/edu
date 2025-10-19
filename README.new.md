# Python 학습 플랫폼 - Flask 버전

IT학원 학생들을 위한 Python 학습 플랫폼입니다. Flask 기반 백엔드와 순수 HTML/CSS/JavaScript 프론트엔드로 구성되어 있습니다.

## 🎯 주요 기능

- **회원가입 및 로그인**: JWT 기반 인증
- **수업 자료**: 카테고리별, 난이도별 정리된 학습 자료
- **코드 실행**: 브라우저에서 Python 코드 작성 및 실시간 실행
- **제출 기록**: 내가 작성한 코드와 실행 결과 저장 및 조회

## 🛠 기술 스택

### 백엔드
- **Flask 3.0**: Python 웹 프레임워크
- **SQLAlchemy**: ORM (SQLite → PostgreSQL 마이그레이션 대비)
- **Flask-JWT-Extended**: JWT 인증
- **Werkzeug**: 비밀번호 해싱

### 프론트엔드
- **HTML5**: 시맨틱 마크업
- **CSS3**: Flexbox/Grid, CSS 변수
- **JavaScript (ES6+)**: Fetch API, async/await

### 인프라
- **Docker & Docker Compose**: 컨테이너화
- **Code Runner**: 격리된 Python 코드 실행 서비스

## 📁 프로젝트 구조

```
solution/
├── flask-app/              # Flask 백엔드
│   ├── app/
│   │   ├── __init__.py    # 앱 팩토리
│   │   ├── config.py      # 설정
│   │   ├── models/        # 데이터베이스 모델
│   │   ├── routes/        # API 라우트
│   │   ├── services/      # 비즈니스 로직
│   │   └── utils/         # 유틸리티
│   ├── requirements.txt
│   ├── run.py            # 앱 실행
│   └── Dockerfile
│
├── static/                # 프론트엔드 정적 파일
│   ├── css/              # 스타일시트
│   │   ├── common.css
│   │   ├── auth.css
│   │   ├── materials.css
│   │   └── practice.css
│   └── js/               # JavaScript
│       ├── api.js        # API 통신
│       ├── utils.js      # 유틸리티
│       ├── auth.js
│       ├── materials.js
│       └── practice.js
│
├── templates/             # HTML 템플릿
│   ├── index.html
│   ├── auth/
│   ├── materials/
│   ├── practice/
│   └── profile/
│
├── code-runner/           # 코드 실행 서비스
│   ├── runner.py
│   ├── requirements.txt
│   └── Dockerfile.simple
│
├── docker-compose.new.yml
├── .cursorrules          # AI Agent 개발 규칙
└── README.new.md
```

## 🚀 시작하기

### 사전 요구사항
- Docker & Docker Compose
- (선택) Python 3.11+

### 1. Docker Compose로 실행 (권장)

```bash
# docker-compose.new.yml 사용
docker-compose -f docker-compose.new.yml up -d

# 로그 확인
docker-compose -f docker-compose.new.yml logs -f
```

**서비스 접속:**
- 웹 애플리케이션: http://localhost:5000
- 코드 러너 API: http://localhost:8080

### 2. 로컬 개발 (Docker 없이)

```bash
# 1. Flask 앱 실행
cd flask-app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py

# 2. 코드 러너 실행 (별도 터미널)
cd code-runner
pip install -r requirements.txt
python runner.py
```

## 📖 API 문서

### 인증 API

#### 회원가입
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "student1",
  "email": "student1@example.com",
  "password": "password123",
  "full_name": "홍길동"
}
```

#### 로그인
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "student1",
  "password": "password123"
}
```

#### 현재 사용자 정보
```http
GET /api/auth/me
Authorization: Bearer {token}
```

### 수업 자료 API

#### 자료 목록 조회
```http
GET /api/materials?category=기초문법&difficulty=beginner
```

#### 자료 상세 조회
```http
GET /api/materials/{id}
```

### 문제 풀이 API

#### 코드 실행 (제출 안 함)
```http
POST /api/submissions/execute
Authorization: Bearer {token}
Content-Type: application/json

{
  "code": "print('Hello, World!')"
}
```

#### 코드 제출
```http
POST /api/submissions
Authorization: Bearer {token}
Content-Type: application/json

{
  "code": "print('Hello, World!')",
  "problem_id": 1
}
```

#### 내 제출 기록
```http
GET /api/submissions/my?page=1&per_page=20
Authorization: Bearer {token}
```

## 🔧 개발 가이드

### 파일 구조 규칙
- **한 파일당 최대 300줄**
- **HTML/CSS/JS 완전 분리** (인라인 스타일/스크립트 금지)
- **모듈별 파일 분리** (routes, services, models)

### 코딩 컨벤션
- **Python**: PEP 8, 타입 힌팅
- **JavaScript**: ES6+, camelCase
- **CSS**: BEM 네이밍 또는 명확한 클래스명

자세한 내용은 `.cursorrules` 파일을 참조하세요.

## 🗄 데이터베이스

### 현재: SQLite
- 개발 및 테스트용
- 파일 기반: `flask-app/instance/app.db`

### 향후: PostgreSQL 마이그레이션
```yaml
# docker-compose.new.yml 주석 해제
postgres:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: python_learning
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres123
```

설정 변경:
```python
# flask-app/app/config.py
DATABASE_URL = 'postgresql://postgres:postgres123@postgres:5432/python_learning'
```

## 🔐 보안

- 비밀번호: Werkzeug 해싱
- 인증: JWT (24시간 만료)
- 코드 실행: 격리된 Docker 컨테이너
- 입력 검증: 모든 API 엔드포인트

## 🧪 테스트

```bash
cd flask-app
pytest
```

## 📝 환경 변수

`.env` 파일 생성:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///instance/app.db
CODE_RUNNER_URL=http://localhost:8080
CODE_EXECUTION_TIMEOUT=30
```

## 🐛 문제 해결

### 포트 충돌
```bash
# 다른 포트 사용
docker-compose -f docker-compose.new.yml up -d
# 또는 docker-compose.new.yml 파일에서 포트 변경
```

### 데이터베이스 초기화
```bash
docker-compose -f docker-compose.new.yml down -v
docker-compose -f docker-compose.new.yml up -d
```

### 코드 러너 연결 실패
```bash
# 코드 러너 로그 확인
docker logs python-learning-code-runner
```

## 📚 추가 개발 계획

- [ ] 관리자 페이지 (자료 관리)
- [ ] 마크다운 에디터 (수업 자료 작성)
- [ ] 코드 하이라이팅 (Prism.js)
- [ ] 실시간 채팅 (WebSocket)
- [ ] 진도율 대시보드
- [ ] 문제 자동 채점
- [ ] PostgreSQL 마이그레이션

## 👥 기여

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

MIT License

## 📞 문의

프로젝트 관련 문의사항이 있으시면 이슈를 등록해주세요.

