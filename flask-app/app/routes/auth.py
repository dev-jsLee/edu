"""
인증 API 라우트
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.utils.decorators import jwt_required_with_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """회원가입"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': '요청 데이터가 없습니다'
        }), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    
    success, user, error = AuthService.register_user(username, email, password, full_name)
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    # JWT 토큰 생성
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'success': True,
        'data': {
            'user': user.to_dict(include_email=True),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """로그인"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': '요청 데이터가 없습니다'
        }), 400
    
    username = data.get('username')
    password = data.get('password')
    
    success, user, error = AuthService.authenticate_user(username, password)
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 401
    
    # JWT 토큰 생성
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'success': True,
        'data': {
            'user': user.to_dict(include_email=True),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required_with_user
def get_current_user(current_user):
    """현재 사용자 정보 조회"""
    return jsonify({
        'success': True,
        'data': current_user.to_dict(include_email=True)
    }), 200


@auth_bp.route('/me', methods=['PUT'])
@jwt_required_with_user
def update_profile(current_user):
    """프로필 업데이트"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': '요청 데이터가 없습니다'
        }), 400
    
    success, error = AuthService.update_user_profile(current_user, data)
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': current_user.to_dict(include_email=True)
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """토큰 갱신"""
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    
    return jsonify({
        'success': True,
        'data': {
            'access_token': access_token
        }
    }), 200

