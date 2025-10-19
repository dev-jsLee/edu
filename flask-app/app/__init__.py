"""
Flask 애플리케이션 팩토리
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# 확장 초기화 (앱 인스턴스 없이)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name='default'):
    """
    Flask 애플리케이션 팩토리 함수
    
    Args:
        config_name: 설정 이름 ('development', 'production', 'testing')
    
    Returns:
        Flask 애플리케이션 인스턴스
    """
    # Flask 앱 생성
    app = Flask(__name__, 
                static_folder='../../static',
                template_folder='../../templates')
    
    # 설정 로드
    from app.config import config
    app.config.from_object(config[config_name])
    
    # 확장 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # 블루프린트 등록
    from app.routes.auth import auth_bp
    from app.routes.materials import materials_bp
    from app.routes.submissions import submissions_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(materials_bp, url_prefix='/api/materials')
    app.register_blueprint(submissions_bp, url_prefix='/api/submissions')
    
    # 정적 페이지 라우트
    from app.routes.pages import pages_bp
    app.register_blueprint(pages_bp)
    
    # 데이터베이스 생성
    with app.app_context():
        db.create_all()
    
    return app

