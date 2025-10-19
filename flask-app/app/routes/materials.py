"""
수업 자료 API 라우트
"""
from flask import Blueprint, request, jsonify
from app.services.material_service import MaterialService
from app.utils.decorators import admin_required

materials_bp = Blueprint('materials', __name__)


@materials_bp.route('', methods=['GET'])
def get_materials():
    """수업 자료 목록 조회"""
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    
    materials = MaterialService.get_all_materials(category, difficulty)
    
    return jsonify({
        'success': True,
        'data': [material.to_dict(include_content=False) for material in materials]
    }), 200


@materials_bp.route('/<int:material_id>', methods=['GET'])
def get_material(material_id):
    """수업 자료 상세 조회"""
    material = MaterialService.get_material_by_id(material_id)
    
    if not material:
        return jsonify({
            'success': False,
            'error': '자료를 찾을 수 없습니다'
        }), 404
    
    return jsonify({
        'success': True,
        'data': material.to_dict(include_content=True)
    }), 200


@materials_bp.route('/categories', methods=['GET'])
def get_categories():
    """카테고리 목록 조회"""
    categories = MaterialService.get_categories()
    
    return jsonify({
        'success': True,
        'data': categories
    }), 200


@materials_bp.route('', methods=['POST'])
@admin_required
def create_material(current_user):
    """수업 자료 생성 (관리자 전용)"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': '요청 데이터가 없습니다'
        }), 400
    
    success, material, error = MaterialService.create_material(
        title=data.get('title'),
        content=data.get('content'),
        category=data.get('category'),
        difficulty=data.get('difficulty'),
        description=data.get('description'),
        tags=data.get('tags')
    )
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': material.to_dict()
    }), 201


@materials_bp.route('/<int:material_id>', methods=['PUT'])
@admin_required
def update_material(current_user, material_id):
    """수업 자료 수정 (관리자 전용)"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': '요청 데이터가 없습니다'
        }), 400
    
    success, error = MaterialService.update_material(material_id, data)
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': {'message': '자료가 수정되었습니다'}
    }), 200

