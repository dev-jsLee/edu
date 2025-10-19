"""
코드 실행 서비스
"""
import requests
from typing import Dict, Tuple, Optional
from flask import current_app


class CodeRunnerService:
    """코드 실행 관련 비즈니스 로직"""
    
    @staticmethod
    def execute_code(code: str, timeout: Optional[int] = None) -> Tuple[bool, Dict, Optional[str]]:
        """
        코드 실행 요청
        
        Args:
            code: 실행할 Python 코드
            timeout: 타임아웃 (초), None이면 설정값 사용
        
        Returns:
            (success, result_data, error_message)
        """
        if timeout is None:
            timeout = current_app.config['CODE_EXECUTION_TIMEOUT']
        
        code_runner_url = current_app.config['CODE_RUNNER_URL']
        
        try:
            response = requests.post(
                f'{code_runner_url}/execute',
                json={'code': code, 'timeout': timeout},
                timeout=timeout + 5  # 여유를 두고 HTTP 타임아웃 설정
            )
            
            if response.status_code == 200:
                data = response.json()
                return True, data, None
            else:
                return False, {}, f'코드 실행 서비스 오류: {response.status_code}'
        
        except requests.exceptions.Timeout:
            return False, {}, '코드 실행 시간이 초과되었습니다'
        
        except requests.exceptions.ConnectionError:
            return False, {}, '코드 실행 서비스에 연결할 수 없습니다'
        
        except Exception as e:
            return False, {}, f'코드 실행 중 오류가 발생했습니다: {str(e)}'
    
    @staticmethod
    def check_service_health() -> bool:
        """코드 러너 서비스 상태 확인"""
        code_runner_url = current_app.config['CODE_RUNNER_URL']
        
        try:
            response = requests.get(f'{code_runner_url}/health', timeout=5)
            return response.status_code == 200
        except:
            return False

