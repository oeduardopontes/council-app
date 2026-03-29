// Global state
let agents = [];
let contextCounter = 0;

// Load agents on page load
document.addEventListener('DOMContentLoaded', () => {
    loadAgents();
    initializeUI();
});

// Initialize UI enhancements
function initializeUI() {
    const textarea = document.getElementById('question');
    if (textarea) {
        // Add character counter
        textarea.addEventListener('input', updateCharCount);

        // Add auto-resize
        textarea.addEventListener('input', autoResize);

        // Keyboard shortcuts
        textarea.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
                e.preventDefault();
                submitDeliberation();
            }
        });
    }
}

// Auto-resize textarea
function autoResize() {
    const textarea = document.getElementById('question');
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 300) + 'px';
}

// Update character count
function updateCharCount() {
    const textarea = document.getElementById('question');
    const length = textarea.value.length;

    // Show character count if text exists
    let counter = document.querySelector('.char-count');
    if (!counter && length > 0) {
        counter = document.createElement('div');
        counter.className = 'char-count';
        textarea.parentElement.appendChild(counter);
    }

    if (counter) {
        counter.textContent = `${length} `+t("form.character_count")+``;
        counter.style.display = length > 0 ? 'block' : 'none';
    }
}

// Load available agents from API
async function loadAgents() {
    try {
        const response = await fetch('/api/agents');
        const data = await response.json();
        agents = data.agents;
        renderAgents();
    } catch (error) {
        console.error('Erro ao carregar agentes:', error);
        showError('Falha ao carregar agentes. Por favor, atualize a página.');
    }
}

// Render agent checkboxes
function renderAgents() {
    const agentsList = document.getElementById('agents-list');
    agentsList.innerHTML = '';

    agents.forEach(agent => {
        const label = document.createElement('label');
        label.className = 'agent-option';
        label.innerHTML = `
            <input type="checkbox" value="${agent.id}" class="agent-checkbox">
            <strong>${agent.role}</strong>
            <small>${agent.expertise.join(', ')}</small>
        `;
        agentsList.appendChild(label);
    });
}

// Toggle all agents
function toggleAll() {
    const selectAll = document.getElementById('select-all');
    const checkboxes = document.querySelectorAll('.agent-checkbox');
    checkboxes.forEach(cb => cb.checked = selectAll.checked);
}

// Add context item
function addContextItem() {
    const container = document.getElementById('context-items');
    const item = document.createElement('div');
    item.className = 'context-item';
    item.id = `context-${contextCounter}`;
    item.innerHTML = `
        <input type="text" placeholder="Chave (ex: Orçamento)" class="context-key">
        <input type="text" placeholder="Valor (ex: R$ 500 mil)" class="context-value">
        <button class="btn-remove" onclick="removeContextItem(${contextCounter})">Remover</button>
    `;
    container.appendChild(item);
    contextCounter++;
}

// Remove context item
function removeContextItem(id) {
    const item = document.getElementById(`context-${id}`);
    item.remove();
}

// Collect context from form
function getContext() {
    const context = {};
    const items = document.querySelectorAll('.context-item');

    items.forEach(item => {
        const key = item.querySelector('.context-key').value.trim();
        const value = item.querySelector('.context-value').value.trim();
        if (key && value) {
            context[key] = value;
        }
    });

    return Object.keys(context).length > 0 ? context : null;
}

// Get selected agents
function getSelectedAgents() {
    const selectAll = document.getElementById('select-all');
    if (selectAll.checked) {
        return null; // null means all agents
    }

    const checkboxes = document.querySelectorAll('.agent-checkbox:checked');
    const selected = Array.from(checkboxes).map(cb => cb.value);
    return selected.length > 0 ? selected : null;
}

// Create progress bar
function createProgressBar() {
    const loadingEl = document.getElementById('loading');

    // Remove existing progress if any
    const existing = loadingEl.querySelector('.progress-container');
    if (existing) existing.remove();

    const progressHtml = `
        <div class="progress-container">
            <div class="progress-text">${t('form.progress_consulting')}</div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" id="progress-fill"></div>
            </div>
            <div class="progress-details" id="progress-details">
                ${t('form.progress_consulting')}
            </div>
        </div>
    `;

    const spinner = loadingEl.querySelector('.spinner');
    if (spinner) spinner.style.display = 'none';

    const existingText = loadingEl.querySelector('p');
    if (existingText) existingText.style.display = 'none';

    loadingEl.insertAdjacentHTML('beforeend', progressHtml);
}

// Update progress bar
function updateProgress(current, total, agent, status) {
    const progressFill = document.getElementById('progress-fill');
    const progressDetails = document.getElementById('progress-details');

    if (!progressFill || !progressDetails) return;

    const percentage = (current / total) * 100;
    progressFill.style.width = percentage + '%';

    if (status === 'processing') {
        progressDetails.textContent = `[${current}/${total}] ${t('form.progress_waiting', { agent })}`;
    } else if (status === 'completed') {
        progressDetails.textContent = `[${current}/${total}] ${t('form.progress_responded', { agent })}`;
    }
}

// Submit deliberation with progress tracking
async function submitDeliberation() {
    const question = document.getElementById('question').value.trim();

    if (!question) {
        const textarea = document.getElementById('question');
        textarea.style.borderColor = '#ef4444';
        textarea.focus();
        showError('Por favor, insira uma pergunta para o conselho deliberar.');

        setTimeout(() => {
            textarea.style.borderColor = '';
        }, 3000);
        return;
    }

    const context = getContext();
    const selectedAgents = getSelectedAgents();
    const sessionId = 'session_' + Date.now();

    const loadingEl = document.getElementById('loading');
    const submitBtn = document.getElementById('submit-btn');
    const resultsSection = document.getElementById('results-section');

    loadingEl.style.display = 'flex';
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ ' + t('form.submit_button_loading');
    resultsSection.style.display = 'none';

    // Create progress bar
    createProgressBar();

    // Start progress tracking with EventSource
    const eventSource = new EventSource(`/api/progress/${sessionId}`);

    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.status === 'done') {
            eventSource.close();
        } else if (data.current && data.total) {
            updateProgress(data.current, data.total, data.agent, data.status);
        }
    };

    eventSource.onerror = function() {
        eventSource.close();
    };

    try {
        const response = await fetch('/api/deliberate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                context: context,
                agents: selectedAgents,
                session_id: sessionId
            })
        });

        const data = await response.json();

        // Close event source
        eventSource.close();

        if (response.ok) {
            showResults(data.recommendation);
            submitBtn.textContent = '✓ ' + t('form.submit_button_success');
            setTimeout(() => {
                submitBtn.textContent = '🚀 ' + t('form.submit_button');
            }, 3000);
        } else {
            if (response.status === 503) {
                showError(data.error + ' ⏳');
            } else {
                showError(data.error || t('errors.deliberation_error'));
            }
            submitBtn.textContent = '🚀 ' + t('form.submit_button');
        }
    } catch (error) {
        console.error('Erro:', error);
        eventSource.close();
        showError(t('errors.connection_error'));
        submitBtn.textContent = '🚀 ' + t('form.submit_button');
    } finally {
        loadingEl.style.display = 'none';
        submitBtn.disabled = false;
    }
}

// Show results
function showResults(recommendation) {
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results');

    resultsContent.textContent = recommendation;
    resultsSection.style.display = 'block';

    // Add fade-in animation
    resultsSection.style.opacity = '0';
    resultsSection.style.transform = 'translateY(20px)';

    setTimeout(() => {
        resultsSection.style.transition = 'all 0.4s ease';
        resultsSection.style.opacity = '1';
        resultsSection.style.transform = 'translateY(0)';
    }, 10);

    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);

    // Add copy button
    addCopyButton(resultsContent);
}

// Add copy button to results
function addCopyButton(resultsContent) {
    // Remove existing copy button if any
    const existingBtn = resultsContent.parentElement.querySelector('.copy-btn');
    if (existingBtn) existingBtn.remove();

    const copyBtn = document.createElement('button');
    copyBtn.className = 'btn-secondary copy-btn';
    copyBtn.textContent = '📋 ' + t('form.copy_button');
    copyBtn.style.marginTop = '1rem';
    copyBtn.onclick = () => {
        navigator.clipboard.writeText(resultsContent.textContent).then(() => {
            copyBtn.textContent = '✓ ' + t('form.copy_success');
            setTimeout(() => {
                copyBtn.textContent = '📋 ' + t('form.copy_button');
            }, 2000);
        });
    };

    resultsContent.parentElement.appendChild(copyBtn);
}

// Show error
function showError(message) {
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results');

    resultsContent.innerHTML = `<div class="error">❌ ${message}</div>`;
    resultsSection.style.display = 'block';

    // Scroll to error
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}
