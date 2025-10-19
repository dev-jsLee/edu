"""
인증 서비스
"""
from typing import Tuple, Optional, Dict
from app import db
from app.models.user import User
from app.utils.validators import validate_email, validate_username, validate_password


class AuthService:
    """인증 관련 비즈니스 로직"""
    
    @staticmethod
    def register_user(username: str, email: str, password: str, 
                     full_name: Optional[str] = None) -> Tuple[bool, Optional[User], Optional[str]]:
        """
        사용자 회원가입
        
        Returns:
            (success, user, error_message)
        """
        # 입력 검증
        is_valid, error = validate_username(username)
        if not is_valid:
            return False, None, error
        
        is_valid, error = validate_email(email)
        if not is_valid:
            return False, None, error
        
        is_valid, error = validate_password(password)
        if not is_valid:
            return False, None, error
        
        # 중복 확인
        if User.query.filter_by(username=username).first():
            return False, None, "이미 사용 중인 사용자명입니다"
        
        if User.query.filter_by(email=email).first():
            return False, None, "이미 사용 중인 이메일입니다"
        
        # 사용자 생성
        user = User(username=username, email=email, full_name=full_name)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            return True, user, None
        except Exception as e:
            db.session.rollback()
            return False, None, f"회원가입 중 오류가 발생했습니다: {str(e)}"
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Tuple[bool, Optional[User], Optional[str]]:
        """
        사용자 인증
        
        Returns:
            (success, user, error_message)
        """
        if not username or not password:
            return False, None, "사용자명과 비밀번호를 입력해주세요"
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return False, None, "사용자명 또는 비밀번호가 올바르지 않습니다"
        
        if not user.is_active:
            return False, None, "비활성화된 계정입니다"
        
        if not user.check_password(password):
            return False, None, "사용자명 또는 비밀번호가 올바르지 않습니다"
        
        return True, user, None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """ID로 사용자 조회"""
        return User.query.get(user_id)
    
    @staticmethod
    def update_user_profile(user: User, data: Dict) -> Tuple[bool, Optional[str]]:
        """
        사용자 프로필 업데이트
        
        Returns:
            (success, error_message)
        """
        try:
            if 'full_name' in data:
                user.full_name = data['full_name']
            if 'bio' in data:
                user.bio = data['bio']
            
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f"프로필 업데이트 중 오류가 발생했습니다: {str(e)}"

