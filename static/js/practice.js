/**
 * 문제 풀이 관련 JavaScript
 */

let currentProblemId = null;

/**
 * 코드 실행 (제출하지 않음)
 */
async function executeCode() {
    const code = document.getElementById('code-editor').value;
    
    if (!code.trim()) {
        showError('코드를 입력해주세요');
        return;
    }
    
    try {
        setLoading(true, 'run-btn');
        const response = await SubmissionsAPI.executeCode(code);
        
        if (response.success) {
            displayOutput(response.data);
        }
    } catch (error) {
        showError(error.message);
        displayOutput({ success: false, error: error.message });
    } finally {
        setLoading(false, 'run-btn');
    }
}

/**
 * 코드 제출
 */
async function submitCode() {
    const code = document.getElementById('code-editor').value;
    
    if (!code.trim()) {
        showError('코드를 입력해주세요');
        return;
    }
    
    if (!currentProblemId) {
        showError('문제 ID가 설정되지 않았습니다');
        return;
    }
    
    if (!confirm('코드를 제출하시겠습니까?')) {
        return;
    }
    
    try {
        setLoading(true, 'submit-btn');
        const response = await SubmissionsAPI.submitCode(code, currentProblemId);
        
        if (response.success) {
            showSuccess('제출이 완료되었습니다!');
            displayOutput(response.data.execution_result);
        }
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false, 'submit-btn');
    }
}

/**
 * 실행 결과 표시
 */
function displayOutput(result) {
    const outputDiv = document.getElementById('output-content');
    const timeSpan = document.getElementById('execution-time');
    
    if (!outputDiv) return;
    
    // 실행 시간 표시
    if (result.execution_time !== undefined && timeSpan) {
        timeSpan.textContent = `실행 시간: ${formatExecutionTime(result.execution_time)}`;
    }
    
    // 결과 표시
    if (result.success) {
        outputDiv.className = 'output-content output-success';
        outputDiv.textContent = result.output || '(출력 없음)';
        
        if (result.error) {
            outputDiv.innerHTML += `\n\n<span class="output-error">Warning:\n${escapeHtml(result.error)}</span>`;
        }
    } else {
        outputDiv.className = 'output-content output-error';
        outputDiv.textContent = result.error || '실행 중 오류가 발생했습니다';
    }
    
    // 출력 섹션 스크롤
    outputDiv.scrollTop = 0;
}

/**
 * 내 제출 기록 로드
 */
async function loadMySubmissions(problemId = null, page = 1) {
    try {
        setLoading(true);
        const response = await SubmissionsAPI.getMySubmissions(problemId, page);
        
        if (response.success) {
            renderSubmissions(response.data);
        }
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

/**
 * 제출 기록 렌더링
 */
function renderSubmissions(data) {
    const container = document.getElementById('submissions-list');
    
    if (!data.submissions || data.submissions.length === 0) {
        container.innerHTML = '<p class="text-center">제출 기록이 없습니다.</p>';
        return;
    }
    
    container.innerHTML = data.submissions.map(submission => `
        <div class="submission-card" onclick="viewSubmission(${submission.id})">
            <div class="submission-header">
                <div>
                    <span class="submission-status status-${submission.status}">
                        ${submission.status === 'success' ? '✓ 성공' : '✗ 실패'}
                    </span>
                    <span style="margin-left: 1rem;">문제 #${submission.problem_id}</span>
                </div>
                <span>${formatDate(submission.submitted_at)}</span>
            </div>
            <div class="submission-meta">
                <span>⏱️ ${formatExecutionTime(submission.execution_time || 0)}</span>
                <span>📝 ${submission.code.length}자</span>
            </div>
            <div class="submission-code">
                <code>${escapeHtml(submission.code.substring(0, 200))}${submission.code.length > 200 ? '...' : ''}</code>
            </div>
        </div>
    `).join('');
    
    // 페이지네이션 표시 (간단하게)
    if (data.pages > 1) {
        const pagination = document.getElementById('pagination');
        if (pagination) {
            pagination.innerHTML = `
                <div style="text-align: center; margin-top: 2rem;">
                    페이지 ${data.page} / ${data.pages}
                </div>
            `;
        }
    }
}

/**
 * 제출 상세 보기
 */
async function viewSubmission(submissionId) {
    try {
        const response = await SubmissionsAPI.getById(submissionId);
        
        if (response.success) {
            // 모달 또는 새 페이지로 표시 (여기서는 alert)
            const sub = response.data;
            alert(`제출 ID: ${sub.id}\n상태: ${sub.status}\n\n코드:\n${sub.code}\n\n출력:\n${sub.output || '없음'}\n\n에러:\n${sub.error || '없음'}`);
        }
    } catch (error) {
        showError(error.message);
    }
}

/**
 * 코드 예제 로드
 */
function loadCodeExample(example) {
    const editor = document.getElementById('code-editor');
    if (editor) {
        editor.value = example;
    }
}

