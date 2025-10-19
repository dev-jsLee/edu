/**
 * 수업 자료 관련 JavaScript
 */

/**
 * 자료 목록 렌더링
 */
async function loadMaterials(category = null, difficulty = null) {
    try {
        setLoading(true);
        const response = await MaterialsAPI.getAll(category, difficulty);
        
        if (response.success) {
            renderMaterials(response.data);
        }
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

/**
 * 자료 목록 HTML 생성
 */
function renderMaterials(materials) {
    const container = document.getElementById('materials-list');
    
    if (!materials || materials.length === 0) {
        container.innerHTML = '<p class="text-center">자료가 없습니다.</p>';
        return;
    }
    
    container.innerHTML = materials.map(material => `
        <div class="material-card" onclick="location.href='/materials/${material.id}'">
            <div class="material-card-header">
                <div>
                    <h3>${escapeHtml(material.title)}</h3>
                    ${material.difficulty ? `<span class="material-badge badge-${material.difficulty}">${getDifficultyText(material.difficulty)}</span>` : ''}
                </div>
                <span class="material-badge" style="background-color: var(--bg-secondary);">${escapeHtml(material.category)}</span>
            </div>
            ${material.description ? `<p class="material-description">${escapeHtml(material.description)}</p>` : ''}
            <div class="material-meta">
                <span>📅 ${formatDate(material.created_at)}</span>
            </div>
            ${material.tags && material.tags.length > 0 ? `
                <div class="material-tags">
                    ${material.tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('')}
                </div>
            ` : ''}
        </div>
    `).join('');
}

/**
 * 난이도 텍스트 변환
 */
function getDifficultyText(difficulty) {
    const map = {
        'beginner': '초급',
        'intermediate': '중급',
        'advanced': '고급'
    };
    return map[difficulty] || difficulty;
}

/**
 * 자료 상세 로드
 */
async function loadMaterialDetail(materialId) {
    try {
        setLoading(true);
        const response = await MaterialsAPI.getById(materialId);
        
        if (response.success) {
            renderMaterialDetail(response.data);
        }
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

/**
 * 자료 상세 HTML 생성
 */
function renderMaterialDetail(material) {
    const container = document.getElementById('material-detail');
    
    container.innerHTML = `
        <div class="material-content">
            <h1>${escapeHtml(material.title)}</h1>
            <div class="material-meta mb-3">
                <span>📂 ${escapeHtml(material.category)}</span>
                ${material.difficulty ? `<span>📊 ${getDifficultyText(material.difficulty)}</span>` : ''}
                <span>📅 ${formatDate(material.created_at)}</span>
            </div>
            <div id="content-markdown">${escapeHtml(material.content)}</div>
        </div>
    `;
    
    // Markdown 렌더링 (간단하게 pre 태그로 표시, 필요시 marked.js 등 사용)
    const contentDiv = document.getElementById('content-markdown');
    contentDiv.innerHTML = renderMarkdown(material.content);
}

/**
 * 간단한 Markdown 렌더링
 */
function renderMarkdown(text) {
    // 매우 간단한 Markdown 렌더링 (실제로는 marked.js 등 사용 권장)
    return text
        .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/\*([^*]+)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}

