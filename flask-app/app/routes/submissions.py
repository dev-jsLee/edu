"""
문제 풀이 제출 API 라우트
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.submission import Submission
from app.services.code_runner_service import CodeRunnerService
from app.utils.decorators import jwt_required_with_user
from app.utils.validators import validate_code

submissions_bp = Blueprint('submissions', __name__)


@submissions_bp.route('/execute', methods=['POST'])
@jwt_required_with_user
def execute_code(current_user):
    """코드 실행 (제출하지 않고 테스트)"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': '요청 데이터가 없습니다'
        }), 400
    
    code = data.get('code')
    
    # 코드 검증
    is_valid, error = validate_code(code)
    if not is_valid:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    # 코드 실행
    success, result, error = CodeRunnerService.execute_code(code)
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 500
    
    return jsonify({
        'success': True,
        'data': result
    }), 200


@submissions_bp.route('', methods=['POST'])
@jwt_required_with_user
def submit_code(current_user):
    """코드 제출 및 실행"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': '요청 데이터가 없습니다'
        }), 400
    
    code = data.get('code')
    problem_id = data.get('problem_id')
    
    if not problem_id:
        return jsonify({
            'success': False,
            'error': '문제 ID가 필요합니다'
        }), 400
    
    # 코드 검증
    is_valid, error = validate_code(code)
    if not is_valid:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    # 코드 실행
    success, result, error = CodeRunnerService.execute_code(code)
    
    # 제출 기록 저장
    submission = Submission(
        user_id=current_user.id,
        problem_id=problem_id,
        code=code,
        output=result.get('output') if success else None,
        error=result.get('error') if success else error,
        status='success' if success and result.get('success') else 'error',
        execution_time=result.get('execution_time') if success else None
    )
    
    try:
        db.session.add(submission)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'제출 저장 중 오류가 발생했습니다: {str(e)}'
        }), 500
    
    return jsonify({
        'success': True,
        'data': {
            'submission': submission.to_dict(),
            'execution_result': result if success else None
        }
    }), 201


@submissions_bp.route('/my', methods=['GET'])
@jwt_required_with_user
def get_my_submissions(current_user):
    """내 제출 기록 조회"""
    problem_id = request.args.get('problem_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Submission.query.filter_by(user_id=current_user.id)
    
    if problem_id:
        query = query.filter_by(problem_id=problem_id)
    
    query = query.order_by(Submission.submitted_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'success': True,
        'data': {
            'submissions': [submission.to_dict() for submission in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }
    }), 200


@submissions_bp.route('/<int:submission_id>', methods=['GET'])
@jwt_required_with_user
def get_submission(current_user, submission_id):
    """제출 상세 조회"""
    submission = Submission.query.filter_by(
        id=submission_id,
        user_id=current_user.id
    ).first()
    
    if not submission:
        return jsonify({
            'success': False,
            'error': '제출을 찾을 수 없습니다'
        }), 404
    
    return jsonify({
        'success': True,
        'data': submission.to_dict()
    }), 200

