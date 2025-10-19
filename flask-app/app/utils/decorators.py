"""
커스텀 데코레이터
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User


def jwt_required_with_user(fn):
    """
    JWT 인증 필수 데코레이터 (사용자 객체 자동 로드)
    
    데코레이팅된 함수는 첫 번째 인자로 current_user를 받습니다.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': '사용자를 찾을 수 없거나 비활성화되었습니다'
            }), 401
        
        return fn(user, *args, **kwargs)
    
    return wrapper


def admin_required(fn):
    """
    관리자 권한 필수 데코레이터
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': '사용자를 찾을 수 없거나 비활성화되었습니다'
            }), 401
        
        if not user.is_admin:
            return jsonify({
                'success': False,
                'error': '관리자 권한이 필요합니다'
            }), 403
        
        return fn(user, *args, **kwargs)
    
    return wrapper

