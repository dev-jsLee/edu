# Flask 기반 학습 플랫폼 리팩토링 계획

## 프로젝트 목표

IT학원 학생용 학습 플랫폼을 Flask 기반으로 완전히 새롭게 구축합니다. 회원가입/로그인, 수업 자료 조회, 문제 풀이 기록 관리 기능을 제공하며, 파일 구조를 체계적으로 관리합니다.

## 핵심 요구사항

- **프론트엔드**: 순수 HTML/CSS/JS (파일 분리 관리)
- **백엔드**: Flask (CSR 방식 - REST API 제공)
- **데이터베이스**: SQLite (PostgreSQL 마이그레이션 대비)
- **코드 실행**: 기존 code-runner 컨테이너 재활용
- **파일 관리**: 한 파일당 최대 300줄
- **AI Agent Rulebook**: 개발 규칙 문서화

## 1. 프로젝트 구조 설계

### 새로운 디렉토리 구조

```
solution/
├── flask-app/                    # Flask 백엔드
│   ├── app/
│   │   ├── __init__.py          # Flask 앱 팩토리
│   │   ├── config.py            # 설정 관리
│   │   ├── models/              # SQLAlchemy 모델
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # 사용자 모델
│   │   │   ├── material.py      # 수업 자료 모델
│   │   │   └── submission.py    # 문제 풀이 기록
│   │   ├── routes/              # API 라우트
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # 인증 (회원가입/로그인)
│   │   │   ├── materials.py     # 수업 자료
│   │   │   └── submissions.py   # 문제 풀이
│   │   ├── services/            # 비즈니스 로직
│   │   │   ├── auth_service.py
│   │   │   ├── material_service.py
│   │   │   └── code_runner_service.py
│   │   └── utils/               # 유틸리티
│   │       ├── validators.py
│   │       └── decorators.py    # JWT 데코레이터
│   ├── migrations/              # Alembic 마이그레이션
│   ├── requirements.txt
│   └── run.py                   # 앱 실행
│
├── static/                       # 프론트엔드 정적 파일
│   ├── css/
│   │   ├── common.css           # 공통 스타일
│   │   ├── auth.css             # 로그인/회원가입
│   │   ├── materials.css        # 수업 자료
│   │   └── practice.css         # 문제 풀이
│   ├── js/
│   │   ├── api.js               # API 통신 공통 모듈
│   │   ├── auth.js              # 인증 로직
│   │   ├── materials.js         # 수업 자료 로직
│   │   ├── practice.js          # 문제 풀이 로직
│   │   └── utils.js             # 유틸리티
│   └── images/
│
├── templates/                    # HTML 템플릿
│   ├── index.html               # 메인 페이지
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── materials/
│   │   ├── list.html            # 자료 목록
│   │   └── view.html            # 자료 상세
│   ├── practice/
│   │   ├── list.html            # 문제 목록
│   │   └── solve.html           # 문제 풀기
│   └── profile/
│       └── history.html         # 내 풀이 기록
│
├── code-runner/                  # 기존 유지 (독립 서비스)
│   ├── Dockerfile.simple
│   ├── requirements.txt
│   └── runner.py
│
├── docker-compose.yml           # 재구성
├── .cursorrules                 # AI Agent Rulebook
└── README.md
```

## 2. 기술 스택 및 의존성

### Flask 백엔드

- **Flask**: 웹 프레임워크
- **Flask-SQLAlchemy**: ORM
- **Flask-Migrate**: DB 마이그레이션
- **Flask-JWT-Extended**: JWT 인증
- **Flask-CORS**: CORS 처리
- **Werkzeug**: 비밀번호 해싱

### 프론트엔드

- **순수 HTML5**: 시맨틱 마크업
- **순수 CSS3**: Flexbox/Grid 레이아웃
- **순수 JavaScript (ES6+)**: Fetch API, async/await
- **선택사항**: Prism.js (코드 하이라이팅)

### 데이터베이스

- **초기**: SQLite3 (flask-app/instance/app.db)
- **확장 대비**: PostgreSQL 마이그레이션 고려한 SQLAlchemy 설계

## 3. 주요 기능 구현

### 3.1 인증 시스템

**파일**: `flask-app/app/routes/auth.py`, `static/js/auth.js`

- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인 (JWT 토큰 발급)
- `POST /api/auth/logout` - 로그아웃
- `GET /api/auth/me` - 현재 사용자 정보

**프론트엔드**: JWT를 localStorage에 저장, 인증 필요 시 헤더에 포함

### 3.2 수업 자료 관리

**파일**: `flask-app/app/routes/materials.py`, `static/js/materials.js`

- `GET /api/materials` - 자료 목록 조회
- `GET /api/materials/<id>` - 자료 상세 조회
- 자료는 Markdown 형식으로 저장, 프론트엔드에서 렌더링

### 3.3 문제 풀이

**파일**: `flask-app/app/routes/submissions.py`, `static/js/practice.js`

- `GET /api/problems` - 문제 목록
- `POST /api/submissions` - 코드 제출
- `GET /api/submissions/my` - 내 풀이 기록
- code-runner 서비스로 코드 실행 위임

### 3.4 코드 러너 통합

**파일**: `flask-app/app/services/code_runner_service.py`

- 기존 `code-runner` 컨테이너를 마이크로서비스로 활용
- Flask가 HTTP로 코드 실행 요청
- 실행 결과를 JSON으로 반환

## 4. 데이터베이스 설계

### User 테이블

```python
id, username, email, password_hash, created_at, updated_at
```

### Material 테이블

```python
id, title, content (Markdown), category, created_at
```

### Submission 테이블

```python
id, user_id, problem_id, code, result, status, submitted_at
```

**마이그레이션 전략**: SQLAlchemy 사용으로 DB 교체 시 최소 수정

## 5. Docker 구성

### docker-compose.yml 재구성

```yaml
services:
  flask-backend:
    build: ./flask-app
    ports:
      - "5000:5000"
    volumes:
      - ./flask-app:/app
      - ./static:/app/static
      - ./templates:/app/templates
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=sqlite:///instance/app.db
      - CODE_RUNNER_URL=http://code-runner:8080

  code-runner:
    build: ./code-runner
    ports:
      - "8080:8080"
```

**PostgreSQL 확장 계획**: 주석으로 postgres 서비스 정의 추가

## 6. AI Agent Rulebook (.cursorrules)

### 파일 구조 규칙

1. **한 파일 최대 300줄**: 초과 시 모듈 분리
2. **HTML/CSS/JS 분리**: 인라인 스타일/스크립트 금지
3. **명확한 디렉토리 구조**: routes/services/models 분리

### 코딩 컨벤션

1. **Python**: PEP 8, 타입 힌팅 권장
2. **JavaScript**: ES6+ 문법, async/await 사용
3. **CSS**: BEM 네이밍 또는 명확한 클래스명

### API 설계

1. **RESTful 원칙**: 자원 기반 URL
2. **일관된 응답 형식**: `{success, data, error}`
3. **에러 처리**: HTTP 상태 코드 + 메시지

### 보안

1. **비밀번호**: Werkzeug로 해싱
2. **JWT**: HttpOnly 쿠키 또는 localStorage (학습용)
3. **입력 검증**: 모든 API 엔드포인트

## 7. 구현 우선순위

### Phase 1: 인프라 및 인증

- Flask 앱 기본 구조
- 데이터베이스 모델 정의
- 회원가입/로그인 API + UI

### Phase 2: 수업 자료

- 자료 CRUD API
- 자료 목록/상세 페이지
- Markdown 렌더링

### Phase 3: 문제 풀이

- code-runner 통합
- 문제 제출 API
- 코드 에디터 UI (textarea 또는 경량 라이브러리)

### Phase 4: 사용자 대시보드

- 내 풀이 기록 조회
- 진도율 표시

### Phase 5: 문서화 및 배포

- README 작성
- .cursorrules 완성
- Docker 최적화

## 주요 파일 예시

### flask-app/app/**init**.py (50줄)

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    from app.routes import auth, materials, submissions
    app.register_blueprint(auth.bp)
    app.register_blueprint(materials.bp)
    app.register_blueprint(submissions.bp)
    
    return app
```

### static/js/api.js (80줄)

```javascript
const API_BASE = 'http://localhost:5000/api';

async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };
    
    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers: { ...headers, ...options.headers }
    });
    
    const data = await response.json();
    if (!response.ok) throw new Error(data.error);
    return data;
}
```

## 성공 기준

- ✅ 회원가입/로그인 정상 작동
- ✅ 수업 자료 CRUD 완료
- ✅ 코드 실행 및 결과 표시
- ✅ 모든 파일 300줄 이하
- ✅ HTML/CSS/JS 완전 분리
- ✅ .cursorrules 문서화 완료
- ✅ Docker Compose로 원클릭 실행