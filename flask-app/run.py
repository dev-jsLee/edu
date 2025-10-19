"""
Flask 애플리케이션 실행 스크립트
"""
import os
from app import create_app

# 환경 설정 (환경 변수에서 가져오거나 기본값 사용)
config_name = os.environ.get('FLASK_ENV', 'development')

# 앱 생성
app = create_app(config_name)

if __name__ == '__main__':
    # 개발 서버 실행
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )

