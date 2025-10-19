"""
입력 검증 유틸리티
"""
import re
from typing import Tuple, Optional


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    이메일 형식 검증
    
    Returns:
        (is_valid, error_message)
    """
    if not email:
        return False, "이메일을 입력해주세요"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "올바른 이메일 형식이 아닙니다"
    
    return True, None


def validate_username(username: str) -> Tuple[bool, Optional[str]]:
    """
    사용자명 검증 (3-20자, 영문/숫자/언더스코어만)
    
    Returns:
        (is_valid, error_message)
    """
    if not username:
        return False, "사용자명을 입력해주세요"
    
    if len(username) < 3 or len(username) > 20:
        return False, "사용자명은 3-20자 사이여야 합니다"
    
    pattern = r'^[a-zA-Z0-9_]+$'
    if not re.match(pattern, username):
        return False, "사용자명은 영문, 숫자, 언더스코어만 사용 가능합니다"
    
    return True, None


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    비밀번호 검증 (최소 6자)
    
    Returns:
        (is_valid, error_message)
    """
    if not password:
        return False, "비밀번호를 입력해주세요"
    
    if len(password) < 6:
        return False, "비밀번호는 최소 6자 이상이어야 합니다"
    
    return True, None


def validate_code(code: str) -> Tuple[bool, Optional[str]]:
    """
    제출 코드 검증
    
    Returns:
        (is_valid, error_message)
    """
    if not code or not code.strip():
        return False, "코드를 입력해주세요"
    
    if len(code) > 10000:
        return False, "코드가 너무 깁니다 (최대 10,000자)"
    
    return True, None

