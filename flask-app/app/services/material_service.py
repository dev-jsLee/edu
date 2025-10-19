"""
수업 자료 서비스
"""
from typing import List, Optional, Tuple
from app import db
from app.models.material import Material


class MaterialService:
    """수업 자료 관련 비즈니스 로직"""
    
    @staticmethod
    def get_all_materials(category: Optional[str] = None, 
                         difficulty: Optional[str] = None) -> List[Material]:
        """
        수업 자료 목록 조회 (필터링 옵션 포함)
        """
        query = Material.query.filter_by(is_published=True)
        
        if category:
            query = query.filter_by(category=category)
        
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        
        return query.order_by(Material.order, Material.created_at.desc()).all()
    
    @staticmethod
    def get_material_by_id(material_id: int) -> Optional[Material]:
        """ID로 자료 조회"""
        return Material.query.filter_by(id=material_id, is_published=True).first()
    
    @staticmethod
    def create_material(title: str, content: str, category: str,
                       difficulty: Optional[str] = None,
                       description: Optional[str] = None,
                       tags: Optional[str] = None) -> Tuple[bool, Optional[Material], Optional[str]]:
        """
        수업 자료 생성 (관리자용)
        
        Returns:
            (success, material, error_message)
        """
        if not title or not content or not category:
            return False, None, "제목, 내용, 카테고리는 필수입니다"
        
        material = Material(
            title=title,
            content=content,
            category=category,
            difficulty=difficulty,
            description=description,
            tags=tags
        )
        
        try:
            db.session.add(material)
            db.session.commit()
            return True, material, None
        except Exception as e:
            db.session.rollback()
            return False, None, f"자료 생성 중 오류가 발생했습니다: {str(e)}"
    
    @staticmethod
    def update_material(material_id: int, data: dict) -> Tuple[bool, Optional[str]]:
        """
        수업 자료 업데이트 (관리자용)
        
        Returns:
            (success, error_message)
        """
        material = Material.query.get(material_id)
        if not material:
            return False, "자료를 찾을 수 없습니다"
        
        try:
            for key in ['title', 'content', 'category', 'difficulty', 
                       'description', 'tags', 'order', 'is_published']:
                if key in data:
                    setattr(material, key, data[key])
            
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f"자료 업데이트 중 오류가 발생했습니다: {str(e)}"
    
    @staticmethod
    def get_categories() -> List[str]:
        """카테고리 목록 조회"""
        categories = db.session.query(Material.category).distinct().all()
        return [cat[0] for cat in categories]

