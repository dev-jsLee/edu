# 파이썬 학습 플랫폼

실습 중심의 인터랙티브한 파이썬 학습 웹 플랫폼입니다. Docker Compose를 사용하여 쉽게 실행할 수 있습니다.

## 🚀 주요 기능

- **브라우저에서 바로 파이썬 코드 실행**
- **단계별 학습 모듈**
- **실시간 코드 피드백**
- **개인 학습 진도 관리**
- **안전한 코드 실행 환경**

## 🛠 기술 스택

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python
- **Database**: PostgreSQL
- **Cache**: Redis
- **Code Execution**: Docker (격리된 환경)

## 📋 시스템 요구사항

- Docker
- Docker Compose
- 최소 4GB RAM
- 포트 52040-52044 사용 가능

## 🔧 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd python-learning-platform
```

### 2. 환경 설정
```bash
# 환경 변수 파일 복사
cp env.example .env

# 필요시 .env 파일 수정
```

### 3. Docker Compose로 실행
```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

### 4. 서비스 접근

- **메인 웹사이트**: http://localhost:52040
- **API 문서**: http://localhost:52041/docs
- **관리자 대시보드**: http://localhost:52041/admin

## 🔌 포트 구성

| 서비스 | 포트 | 설명 |
|--------|------|------|
| Frontend | 52040 | React 웹 인터페이스 |
| Backend | 52041 | FastAPI 서버 |
| Code Runner | 52042 | 파이썬 코드 실행 서비스 |
| PostgreSQL | 52043 | 데이터베이스 |
| Redis | 52044 | 캐시 서버 |

## 📁 프로젝트 구조

```
python-learning-platform/
├── docker-compose.yml          # Docker Compose 설정
├── env.example                 # 환경 변수 템플릿
├── README.md                   # 프로젝트 문서
│
├── frontend/                   # React 프론트엔드
│   ├── Dockerfile
│   ├── package.json
│   ├── src/
│   │   ├── components/         # 재사용 가능한 컴포넌트
│   │   ├── pages/              # 페이지 컴포넌트
│   │   └── App.tsx             # 메인 앱 컴포넌트
│   └── public/
│
├── backend/                    # FastAPI 백엔드
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py             # FastAPI 앱 진입점
│   │   ├── models/             # 데이터베이스 모델
│   │   ├── routers/            # API 라우터
│   │   ├── services/           # 비즈니스 로직
│   │   └── utils/              # 유틸리티 함수
│   └── alembic/                # 데이터베이스 마이그레이션
│
├── code-runner/                # 코드 실행 서비스
│   ├── Dockerfile
│   ├── requirements.txt
│   └── runner.py               # 코드 실행 서버
│
└── database/                   # 데이터베이스 설정
    └── init.sql                # 초기 스키마 및 데이터
```

## 🐛 개발 모드

개발 중에는 다음 명령어로 서비스를 개별적으로 관리할 수 있습니다:

```bash
# 특정 서비스만 재시작
docker-compose restart backend

# 특정 서비스 로그 확인
docker-compose logs -f frontend

# 서비스 중지
docker-compose down

# 볼륨까지 삭제 (데이터베이스 초기화)
docker-compose down -v
```

## 🔒 보안 고려사항

- 코드 실행은 격리된 Docker 컨테이너에서 수행
- 실행 시간 및 메모리 사용량 제한
- 파일 시스템 접근 제한
- 네트워크 접근 차단

## 📝 개발 계획

### Phase 1: 기본 인프라 ✅
- [x] Docker Compose 환경 설정
- [x] 기본 프론트엔드/백엔드 구조
- [x] 데이터베이스 스키마 설계

### Phase 2: 핵심 기능 (진행 예정)
- [ ] 사용자 인증 시스템
- [ ] 코드 에디터 통합 (Monaco Editor)
- [ ] 실제 코드 실행 시스템
- [ ] 학습 콘텐츠 관리

### Phase 3: 고급 기능 (계획)
- [ ] 실습 문제 시스템
- [ ] 사용자 대시보드
- [ ] 커뮤니티 기능
- [ ] Gemini AI 통합

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🆘 문제 해결

### 포트 충돌 시
```bash
# 사용 중인 포트 확인
netstat -tulpn | grep :52040

# 다른 포트 사용 시 docker-compose.yml 수정
```

### 데이터베이스 초기화
```bash
# 볼륨 삭제 후 재시작
docker-compose down -v
docker-compose up -d
```

### 로그 확인
```bash
# 모든 서비스 로그
docker-compose logs

# 특정 서비스 로그
docker-compose logs backend
```
