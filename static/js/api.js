/**
 * API 통신 공통 모듈
 */

const API_BASE = window.location.origin + '/api';

/**
 * API 요청 함수
 */
async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers: { ...headers, ...options.headers }
        });
        
        const data = await response.json();
        
        // 토큰 만료 시 로그인 페이지로 리다이렉트
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }
        
        if (!response.ok) {
            throw new Error(data.error || '요청 처리 중 오류가 발생했습니다');
        }
        
        return data;
    } catch (error) {
        if (error instanceof TypeError) {
            throw new Error('서버에 연결할 수 없습니다');
        }
        throw error;
    }
}

/**
 * 인증 API
 */
const AuthAPI = {
    async register(username, email, password, fullName) {
        const response = await apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password, full_name: fullName })
        });
        
        if (response.success) {
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
        
        return response;
    },
    
    async login(username, password) {
        const response = await apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        if (response.success) {
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
        
        return response;
    },
    
    async getCurrentUser() {
        return await apiRequest('/auth/me');
    },
    
    async updateProfile(data) {
        return await apiRequest('/auth/me', {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
    }
};

/**
 * 수업 자료 API
 */
const MaterialsAPI = {
    async getAll(category = null, difficulty = null) {
        let url = '/materials';
        const params = new URLSearchParams();
        if (category) params.append('category', category);
        if (difficulty) params.append('difficulty', difficulty);
        
        if (params.toString()) {
            url += '?' + params.toString();
        }
        
        return await apiRequest(url);
    },
    
    async getById(id) {
        return await apiRequest(`/materials/${id}`);
    },
    
    async getCategories() {
        return await apiRequest('/materials/categories');
    }
};

/**
 * 문제 풀이 API
 */
const SubmissionsAPI = {
    async executeCode(code) {
        return await apiRequest('/submissions/execute', {
            method: 'POST',
            body: JSON.stringify({ code })
        });
    },
    
    async submitCode(code, problemId) {
        return await apiRequest('/submissions', {
            method: 'POST',
            body: JSON.stringify({ code, problem_id: problemId })
        });
    },
    
    async getMySubmissions(problemId = null, page = 1, perPage = 20) {
        let url = `/submissions/my?page=${page}&per_page=${perPage}`;
        if (problemId) {
            url += `&problem_id=${problemId}`;
        }
        
        return await apiRequest(url);
    },
    
    async getById(id) {
        return await apiRequest(`/submissions/${id}`);
    }
};

