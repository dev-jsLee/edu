"""
사용자 모델
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    """사용자 모델"""
    __tablename__ = 'users'
    
    # 기본 필드
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # 프로필 정보
    full_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    
    # 상태
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # 타임스탬프
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow, nullable=False)
    
    # 관계
    submissions = db.relationship('Submission', backref='user', lazy='dynamic',
                                 cascade='all, delete-orphan')
    
    def set_password(self, password: str) -> None:
        """비밀번호 해싱 및 저장"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """비밀번호 확인"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_email: bool = False) -> dict:
        """사용자 정보를 딕셔너리로 변환"""
        data = {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'bio': self.bio,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'

