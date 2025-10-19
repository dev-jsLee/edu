"""
정적 페이지 라우트
"""
from flask import Blueprint, send_from_directory, current_app
import os

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def index():
    """메인 페이지"""
    template_dir = current_app.template_folder
    return send_from_directory(template_dir, 'index.html')


@pages_bp.route('/login')
def login_page():
    """로그인 페이지"""
    template_dir = current_app.template_folder
    return send_from_directory(os.path.join(template_dir, 'auth'), 'login.html')


@pages_bp.route('/register')
def register_page():
    """회원가입 페이지"""
    template_dir = current_app.template_folder
    return send_from_directory(os.path.join(template_dir, 'auth'), 'register.html')


@pages_bp.route('/materials')
def materials_page():
    """수업 자료 목록 페이지"""
    template_dir = current_app.template_folder
    return send_from_directory(os.path.join(template_dir, 'materials'), 'list.html')


@pages_bp.route('/materials/<int:material_id>')
def material_view_page(material_id):
    """수업 자료 상세 페이지"""
    template_dir = current_app.template_folder
    return send_from_directory(os.path.join(template_dir, 'materials'), 'view.html')


@pages_bp.route('/practice')
def practice_page():
    """문제 목록 페이지"""
    template_dir = current_app.template_folder
    return send_from_directory(os.path.join(template_dir, 'practice'), 'list.html')


@pages_bp.route('/practice/<int:problem_id>')
def solve_page(problem_id):
    """문제 풀이 페이지"""
    template_dir = current_app.template_folder
    return send_from_directory(os.path.join(template_dir, 'practice'), 'solve.html')


@pages_bp.route('/profile/history')
def history_page():
    """내 풀이 기록 페이지"""
    template_dir = current_app.template_folder
    return send_from_directory(os.path.join(template_dir, 'profile'), 'history.html')

