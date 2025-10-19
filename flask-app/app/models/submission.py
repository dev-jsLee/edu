"""
문제 풀이 제출 모델
"""
from datetime import datetime
from app import db


class Submission(db.Model):
    """문제 풀이 제출 모델"""
    __tablename__ = 'submissions'
    
    # 기본 필드
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    problem_id = db.Column(db.Integer, nullable=False, index=True)
    
    # 코드 및 결과
    code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(20), default='python')
    
    # 실행 결과
    output = db.Column(db.Text)
    error = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False)  # 'success', 'error', 'timeout'
    execution_time = db.Column(db.Float)  # 초 단위
    
    # 채점 (추후 확장용)
    score = db.Column(db.Integer)
    is_correct = db.Column(db.Boolean)
    
    # 타임스탬프
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def to_dict(self) -> dict:
        """제출 정보를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'problem_id': self.problem_id,
            'code': self.code,
            'language': self.language,
            'output': self.output,
            'error': self.error,
            'status': self.status,
            'execution_time': self.execution_time,
            'score': self.score,
            'is_correct': self.is_correct,
            'submitted_at': self.submitted_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Submission {self.id} by User {self.user_id}>'

