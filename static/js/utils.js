/**
 * 유틸리티 함수 모음
 */

/**
 * 로그인 상태 확인
 */
function isLoggedIn() {
    return !!localStorage.getItem('access_token');
}

/**
 * 로그인 필수 체크 (로그인 안 되어 있으면 로그인 페이지로 리다이렉트)
 */
function requireLogin() {
    if (!isLoggedIn()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

/**
 * 현재 사용자 정보 가져오기
 */
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

/**
 * 에러 메시지 표시
 */
function showError(message, containerId = 'error-message') {
    const container = document.getElementById(containerId);
    if (container) {
        container.textContent = message;
        container.style.display = 'block';
        
        // 5초 후 자동 숨김
        setTimeout(() => {
            container.style.display = 'none';
        }, 5000);
    } else {
        alert(message);
    }
}

/**
 * 성공 메시지 표시
 */
function showSuccess(message, containerId = 'success-message') {
    const container = document.getElementById(containerId);
    if (container) {
        container.textContent = message;
        container.style.display = 'block';
        
        // 3초 후 자동 숨김
        setTimeout(() => {
            container.style.display = 'none';
        }, 3000);
    }
}

/**
 * 로딩 상태 표시/숨김
 */
function setLoading(isLoading, buttonId = null) {
    if (buttonId) {
        const button = document.getElementById(buttonId);
        if (button) {
            button.disabled = isLoading;
            button.textContent = isLoading ? '처리 중...' : button.getAttribute('data-original-text') || '제출';
        }
    }
    
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = isLoading ? 'block' : 'none';
    }
}

/**
 * 날짜 포맷팅
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    // 1분 미만
    if (diff < 60000) {
        return '방금 전';
    }
    // 1시간 미만
    if (diff < 3600000) {
        return `${Math.floor(diff / 60000)}분 전`;
    }
    // 24시간 미만
    if (diff < 86400000) {
        return `${Math.floor(diff / 3600000)}시간 전`;
    }
    // 7일 미만
    if (diff < 604800000) {
        return `${Math.floor(diff / 86400000)}일 전`;
    }
    
    // 그 외
    return date.toLocaleDateString('ko-KR');
}

/**
 * 실행 시간 포맷팅
 */
function formatExecutionTime(seconds) {
    if (seconds < 0.001) {
        return '< 1ms';
    }
    if (seconds < 1) {
        return `${(seconds * 1000).toFixed(2)}ms`;
    }
    return `${seconds.toFixed(3)}s`;
}

/**
 * HTML 이스케이프 (XSS 방지)
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * 네비게이션 활성화 상태 설정
 */
function setActiveNav() {
    const path = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === path || 
            (path.startsWith(link.getAttribute('href')) && link.getAttribute('href') !== '/')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * 페이지 초기화 시 실행
 */
document.addEventListener('DOMContentLoaded', () => {
    setActiveNav();
    
    // 사용자 정보 표시 (있는 경우)
    const userDisplay = document.getElementById('user-display');
    if (userDisplay && isLoggedIn()) {
        const user = getCurrentUser();
        userDisplay.textContent = user.username;
    }
});

