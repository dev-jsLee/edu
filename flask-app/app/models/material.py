"""
수업 자료 모델
"""
from datetime import datetime
from app import db


class Material(db.Model):
    """수업 자료 모델"""
    __tablename__ = 'materials'
    
    # 기본 필드
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # 분류
    category = db.Column(db.String(50), nullable=False, index=True)
    difficulty = db.Column(db.String(20))  # 'beginner', 'intermediate', 'advanced'
    
    # 순서 및 표시
    order = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)
    
    # 메타데이터
    description = db.Column(db.String(500))
    tags = db.Column(db.String(200))  # 쉼표로 구분된 태그
    
    # 타임스탬프
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self, include_content: bool = True) -> dict:
        """자료 정보를 딕셔너리로 변환"""
        data = {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'difficulty': self.difficulty,
            'description': self.description,
            'tags': self.tags.split(',') if self.tags else [],
            'order': self.order,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_content:
            data['content'] = self.content
        return data
    
    def __repr__(self):
        return f'<Material {self.title}>'

