# 테스트 가이드

Flask 기반 Python 학습 플랫폼의 기능 테스트 가이드입니다.

## 사전 준비

### 1. 환경 실행
```bash
# Docker Compose 사용
docker-compose -f docker-compose.new.yml up -d

# 데이터베이스 초기화
docker exec python-learning-flask python init_db.py
```

### 2. 서비스 확인
- Flask 앱: http://localhost:5000
- 코드 러너: http://localhost:8080/health

## 기능별 테스트

### 1. 회원가입 테스트

#### 웹 UI 테스트
1. http://localhost:5000/register 접속
2. 다음 정보 입력:
   - 사용자명: test_user
   - 이메일: test@example.com
   - 이름: 테스트 사용자 (선택)
   - 비밀번호: test123
   - 비밀번호 확인: test123
3. "회원가입" 버튼 클릭
4. 자동으로 로그인되고 메인 페이지로 이동

#### API 테스트 (PowerShell)
```powershell
$body = @{
    username = "api_user"
    email = "api@example.com"
    password = "api123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/auth/register" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

**예상 결과:**
```json
{
  "success": true,
  "data": {
    "user": { ... },
    "access_token": "...",
    "refresh_token": "..."
  }
}
```

### 2. 로그인 테스트

#### 웹 UI 테스트
1. http://localhost:5000/login 접속
2. 샘플 계정으로 로그인:
   - 사용자명: student1
   - 비밀번호: student123
3. "로그인" 버튼 클릭
4. 메인 페이지로 이동

#### API 테스트
```powershell
$body = @{
    username = "student1"
    password = "student123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/api/auth/login" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

# 토큰 저장
$token = $response.data.access_token
Write-Host "Token: $token"
```

### 3. 수업 자료 조회 테스트

#### 웹 UI 테스트
1. 상단 메뉴에서 "수업 자료" 클릭
2. 5개의 샘플 자료 확인:
   - Python 소개
   - 변수와 데이터 타입
   - 조건문과 반복문
   - 리스트와 딕셔너리
   - 함수 정의와 활용
3. 자료 카드 클릭하여 상세 내용 확인
4. 카테고리/난이도 필터 테스트

#### API 테스트
```powershell
# 전체 목록
Invoke-RestMethod -Uri "http://localhost:5000/api/materials"

# 카테고리 필터
Invoke-RestMethod -Uri "http://localhost:5000/api/materials?category=기초문법"

# 난이도 필터
Invoke-RestMethod -Uri "http://localhost:5000/api/materials?difficulty=beginner"

# 특정 자료 조회
Invoke-RestMethod -Uri "http://localhost:5000/api/materials/1"
```

### 4. 코드 실행 테스트

#### 웹 UI 테스트
1. "문제 풀이" 메뉴 클릭
2. "문제 1: Hello World 출력하기" 선택
3. 코드 에디터에 다음 입력:
   ```python
   print("Hello, World!")
   ```
4. "실행" 버튼 클릭
5. 실행 결과 확인:
   - 출력: Hello, World!
   - 실행 시간 표시

#### API 테스트
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$body = @{
    code = 'print("Hello from API!")'
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/submissions/execute" `
    -Method Post `
    -Headers $headers `
    -Body $body
```

**예상 결과:**
```json
{
  "success": true,
  "data": {
    "success": true,
    "output": "Hello from API!\n",
    "error": null,
    "execution_time": 0.003
  }
}
```

### 5. 코드 제출 테스트

#### 웹 UI 테스트
1. 문제 페이지에서 코드 작성
2. "제출" 버튼 클릭
3. 확인 대화상자에서 "확인"
4. 제출 완료 메시지 확인
5. "내 기록" 메뉴에서 제출 내역 확인

#### API 테스트
```powershell
$body = @{
    code = @"
def add(a, b):
    return a + b

print(add(3, 5))
"@
    problem_id = 1
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/submissions" `
    -Method Post `
    -Headers $headers `
    -Body $body
```

### 6. 제출 기록 조회 테스트

#### 웹 UI 테스트
1. "내 기록" 메뉴 클릭
2. 제출한 코드 목록 확인
3. 각 카드에 표시된 정보 확인:
   - 성공/실패 상태
   - 문제 번호
   - 제출 시간
   - 실행 시간
   - 코드 미리보기
4. 카드 클릭하여 상세 정보 확인

#### API 테스트
```powershell
# 전체 기록
Invoke-RestMethod -Uri "http://localhost:5000/api/submissions/my" `
    -Headers $headers

# 특정 문제의 기록
Invoke-RestMethod -Uri "http://localhost:5000/api/submissions/my?problem_id=1" `
    -Headers $headers

# 페이지네이션
Invoke-RestMethod -Uri "http://localhost:5000/api/submissions/my?page=1&per_page=10" `
    -Headers $headers
```

## 에러 케이스 테스트

### 1. 인증 실패
```powershell
# 잘못된 비밀번호
$body = @{
    username = "student1"
    password = "wrongpassword"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/auth/login" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```
**예상:** 401 에러, "사용자명 또는 비밀번호가 올바르지 않습니다"

### 2. 중복 회원가입
```powershell
# 이미 존재하는 사용자명
$body = @{
    username = "student1"
    email = "new@example.com"
    password = "test123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/auth/register" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```
**예상:** 400 에러, "이미 사용 중인 사용자명입니다"

### 3. 코드 실행 에러
```powershell
$body = @{
    code = 'print(undefined_variable)'
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/submissions/execute" `
    -Method Post `
    -Headers $headers `
    -Body $body
```
**예상:** success: false, error에 NameError 메시지

### 4. 인증 없이 보호된 API 접근
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/submissions/my"
```
**예상:** 401 에러, 인증 필요

## 성능 테스트

### 1. 코드 실행 타임아웃
```python
# 30초 이상 실행되는 코드
import time
time.sleep(40)
```
**예상:** 타임아웃 에러

### 2. 대용량 코드 제출
10,000자 이상의 코드 제출 시도
**예상:** 400 에러, "코드가 너무 깁니다"

## 브라우저 호환성 테스트

- Chrome (권장)
- Firefox
- Edge
- Safari (부분 테스트)

## 모바일 반응형 테스트

1. 브라우저 개발자 도구에서 모바일 뷰 전환
2. 주요 페이지 레이아웃 확인
3. 터치 인터랙션 테스트

## 테스트 체크리스트

### 인증
- [ ] 회원가입 성공
- [ ] 중복 회원가입 방지
- [ ] 로그인 성공
- [ ] 잘못된 비밀번호 로그인 실패
- [ ] JWT 토큰 발급
- [ ] 토큰으로 보호된 API 접근
- [ ] 로그아웃 기능

### 수업 자료
- [ ] 자료 목록 조회
- [ ] 자료 상세 조회
- [ ] 카테고리 필터링
- [ ] 난이도 필터링
- [ ] Markdown 렌더링

### 코드 실행
- [ ] 정상 코드 실행
- [ ] 에러 코드 실행
- [ ] 실행 시간 표시
- [ ] 출력 결과 표시
- [ ] 에러 메시지 표시

### 코드 제출
- [ ] 제출 성공
- [ ] 제출 기록 저장
- [ ] 내 기록 조회
- [ ] 페이지네이션
- [ ] 제출 상세 조회

### UI/UX
- [ ] 네비게이션 메뉴 작동
- [ ] 로그인 상태 표시
- [ ] 에러 메시지 표시
- [ ] 성공 메시지 표시
- [ ] 로딩 상태 표시
- [ ] 반응형 레이아웃

## 문제 해결

### 코드 러너 연결 실패
```bash
docker logs python-learning-code-runner
```

### 데이터베이스 초기화
```bash
docker exec python-learning-flask rm -f instance/app.db
docker exec python-learning-flask python init_db.py
```

### 포트 충돌
docker-compose.new.yml에서 포트 변경

## 테스트 결과 보고

테스트 완료 후 다음 정보를 기록하세요:
- 테스트 일시
- 테스트 환경 (OS, 브라우저)
- 통과한 테스트
- 실패한 테스트
- 발견된 버그
- 개선 사항

