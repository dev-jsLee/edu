"""
데이터베이스 초기화 및 샘플 데이터 생성 스크립트
"""
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.material import Material

def init_database():
    """데이터베이스 초기화 및 샘플 데이터 생성"""
    app = create_app('development')
    
    with app.app_context():
        # 테이블 생성
        print("데이터베이스 테이블 생성 중...")
        db.create_all()
        
        # 샘플 사용자 생성
        print("샘플 사용자 생성 중...")
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                full_name='관리자',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        if not User.query.filter_by(username='student1').first():
            student = User(
                username='student1',
                email='student1@example.com',
                full_name='학생1'
            )
            student.set_password('student123')
            db.session.add(student)
        
        # 샘플 수업 자료 생성
        print("샘플 수업 자료 생성 중...")
        materials_data = [
            {
                'title': 'Python 소개',
                'content': '''# Python 소개

Python은 배우기 쉽고 강력한 프로그래밍 언어입니다.

## 특징
- 간결하고 읽기 쉬운 문법
- 다양한 라이브러리와 프레임워크
- 웹, 데이터 분석, AI 등 다양한 분야에서 사용

## 첫 번째 프로그램

```python
print("Hello, World!")
```

Python에서는 `print()` 함수로 화면에 출력할 수 있습니다.''',
                'category': '기초문법',
                'difficulty': 'beginner',
                'description': 'Python 프로그래밍 언어의 기본 개념과 특징을 배웁니다.',
                'tags': 'python,입문,기초',
                'order': 1
            },
            {
                'title': '변수와 데이터 타입',
                'content': '''# 변수와 데이터 타입

## 변수 선언
Python에서 변수는 간단하게 선언할 수 있습니다.

```python
name = "홍길동"
age = 20
height = 175.5
is_student = True
```

## 기본 데이터 타입
- **문자열 (str)**: `"Hello"`
- **정수 (int)**: `42`
- **실수 (float)**: `3.14`
- **불린 (bool)**: `True`, `False`

## 타입 확인
```python
print(type(name))  # <class 'str'>
print(type(age))   # <class 'int'>
```''',
                'category': '기초문법',
                'difficulty': 'beginner',
                'description': 'Python의 변수 선언과 기본 데이터 타입을 학습합니다.',
                'tags': 'python,변수,데이터타입',
                'order': 2
            },
            {
                'title': '조건문과 반복문',
                'content': '''# 조건문과 반복문

## if 문
```python
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C")
```

## for 반복문
```python
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

fruits = ["사과", "바나나", "오렌지"]
for fruit in fruits:
    print(fruit)
```

## while 반복문
```python
count = 0
while count < 5:
    print(count)
    count += 1
```''',
                'category': '기초문법',
                'difficulty': 'beginner',
                'description': '조건문(if)과 반복문(for, while)의 사용법을 배웁니다.',
                'tags': 'python,조건문,반복문',
                'order': 3
            },
            {
                'title': '리스트와 딕셔너리',
                'content': '''# 리스트와 딕셔너리

## 리스트 (List)
순서가 있는 데이터 모음입니다.

```python
numbers = [1, 2, 3, 4, 5]
print(numbers[0])  # 1

numbers.append(6)  # 추가
numbers.remove(3)  # 제거
```

## 딕셔너리 (Dictionary)
키-값 쌍으로 데이터를 저장합니다.

```python
student = {
    "name": "홍길동",
    "age": 20,
    "major": "컴퓨터공학"
}

print(student["name"])  # 홍길동
student["grade"] = "A"  # 추가
```

## 리스트 컴프리헨션
```python
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```''',
                'category': '기초문법',
                'difficulty': 'intermediate',
                'description': '리스트와 딕셔너리의 사용법과 활용 방법을 학습합니다.',
                'tags': 'python,리스트,딕셔너리',
                'order': 4
            },
            {
                'title': '함수 정의와 활용',
                'content': '''# 함수 정의와 활용

## 기본 함수
```python
def greet(name):
    return f"안녕하세요, {name}님!"

message = greet("홍길동")
print(message)  # 안녕하세요, 홍길동님!
```

## 매개변수
```python
def add(a, b=0):  # 기본값 설정
    return a + b

print(add(5, 3))  # 8
print(add(5))     # 5
```

## 여러 값 반환
```python
def get_stats(numbers):
    return sum(numbers), len(numbers), sum(numbers) / len(numbers)

total, count, average = get_stats([1, 2, 3, 4, 5])
```

## 람다 함수
```python
square = lambda x: x ** 2
print(square(5))  # 25
```''',
                'category': '기초문법',
                'difficulty': 'intermediate',
                'description': '함수의 정의, 매개변수, 반환값 등을 배웁니다.',
                'tags': 'python,함수,람다',
                'order': 5
            }
        ]
        
        for mat_data in materials_data:
            if not Material.query.filter_by(title=mat_data['title']).first():
                material = Material(**mat_data)
                db.session.add(material)
        
        # 변경사항 저장
        try:
            db.session.commit()
            print("✓ 데이터베이스 초기화 완료!")
            print("\n생성된 계정:")
            print("  관리자: admin / admin123")
            print("  학생: student1 / student123")
        except Exception as e:
            db.session.rollback()
            print(f"✗ 오류 발생: {e}")

if __name__ == '__main__':
    init_database()

