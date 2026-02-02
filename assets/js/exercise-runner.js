// Determine API base URL - supports both local dev and GitHub Codespaces
function getApiBaseUrl() {
    const hostname = window.location.hostname;
    if (hostname.endsWith('.app.github.dev')) {
        // GitHub Codespaces: hostname is <codespace-name>-<port>.app.github.dev
        // Replace the Live Server port with the backend port (8080)
        const newHostname = hostname.replace(/-\d+\.app\.github\.dev$/, '-8080.app.github.dev');
        return `https://${newHostname}`;
    }
    return 'http://127.0.0.1:8080';
}

const API_BASE = getApiBaseUrl();

// Selector Strategy Demo
class SelectorDemo {
    constructor() {
        this.currentSelectorIndex = 0;
        this.selectors = [];
        this.results = [];
        this.autoRun = false;
    }

    async startDemo() {
        console.log('Starting selector demo...');

        try {
            // Load selectors from API
            const response = await fetch(`${API_BASE}/api/demo/selectors`);
            const data = await response.json();

            if (data.selectors) {
                this.selectors = data.selectors;
                console.log(`Loaded ${this.selectors.length} selectors`);
                this.showDemoInterface();
                this.runNextSelector();
            } else {
                this.showError('Failed to load selectors');
            }
        } catch (error) {
            console.error('Failed to start demo:', error);
            this.showError('Failed to start demo. Make sure the backend server is running on port 8080.');
        }
    }

    showDemoInterface() {
        const modal = document.createElement('div');
        modal.className = 'exercise-modal';
        modal.innerHTML = `
            <div class="exercise-overlay" onclick="closeDemo()"></div>
            <div class="exercise-content">
                <div class="exercise-header">
                    <h2>🎬 Instructor Demo: Testing Selectors Step-by-Step</h2>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: normal;">Watch how each selector is tested against the HTML versions</p>
                    <button class="close-btn" onclick="closeDemo()">×</button>
                </div>
                <div class="exercise-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progress-fill" style="width: 0%"></div>
                    </div>
                    <span class="progress-text" id="progress-text">Testing selector 1 of ${this.selectors.length}</span>
                </div>
                <div class="demo-body">
                    <div class="selector-info">
                        <h3 id="selector-name">Loading...</h3>
                        <div class="selector-details">
                            <p><strong>Selector:</strong> <code id="selector-code"></code></p>
                            <p><strong>Priority:</strong> <span id="selector-priority"></span></p>
                            <p><strong>Target:</strong> <span id="selector-target"></span></p>
                            <p id="selector-comment"></p>
                        </div>
                    </div>
                    <div class="results-section">
                        <h4>Test Results</h4>
                        <div class="result-status" id="result-status">
                            <div class="status-indicator" id="status-indicator">Testing...</div>
                        </div>
                        <div class="data-table-container" id="data-table-container" style="display: none;">
                            <h5>Extracted Data</h5>
                            <table class="sample-table" id="results-table">
                                <thead>
                                    <tr>
                                        <th>Indicator</th>
                                        <th>Value</th>
                                        <th>Change</th>
                                    </tr>
                                </thead>
                                <tbody id="results-body">
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="demo-controls">
                    <button id="prev-btn" onclick="prevSelector()" disabled>Previous</button>
                    <button id="next-btn" onclick="nextSelector()" disabled>Next Selector</button>
                    <button id="auto-run-btn" onclick="toggleAutoRun()">Auto Run</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    async runNextSelector() {
        if (this.currentSelectorIndex >= this.selectors.length) {
            this.showCompletion();
            return;
        }

        const selector = this.selectors[this.currentSelectorIndex];
        this.displaySelectorInfo(selector);
        await this.testSelector(selector);

        // Update progress
        const progress = ((this.currentSelectorIndex + 1) / this.selectors.length) * 100;
        document.getElementById('progress-fill').style.width = progress + '%';
        document.getElementById('progress-text').textContent =
            `Testing selector ${this.currentSelectorIndex + 1} of ${this.selectors.length}`;

        // Update navigation buttons
        document.getElementById('prev-btn').disabled = this.currentSelectorIndex === 0;
        document.getElementById('next-btn').disabled = this.currentSelectorIndex === this.selectors.length - 1;

        if (this.autoRun) {
            setTimeout(() => {
                this.currentSelectorIndex++;
                this.runNextSelector();
            }, 3000); // 3 second delay between tests
        }
    }

    displaySelectorInfo(selector) {
        document.getElementById('selector-name').textContent = selector.selector_name;
        document.getElementById('selector-code').textContent = selector.selector;
        document.getElementById('selector-priority').textContent = selector.priority;
        document.getElementById('selector-target').textContent = selector.url.replace('data/website_sample_', '').replace('.html', '');

        const commentEl = document.getElementById('selector-comment');
        if (selector.comment) {
            commentEl.textContent = selector.comment;
        } else {
            commentEl.textContent = '';
        }
    }

    async testSelector(selector) {
        const statusEl = document.getElementById('result-status');
        const indicatorEl = document.getElementById('status-indicator');
        const tableContainer = document.getElementById('data-table-container');

        // Show testing status
        indicatorEl.className = 'status-indicator testing';
        indicatorEl.textContent = 'Testing selector...';
        tableContainer.style.display = 'none';

        try {
            const response = await fetch(`${API_BASE}/api/demo/test-selector`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    selector: selector.selector,
                    version: selector.url.split('_').pop().replace('.html', ''),
                    selector_name: selector.selector_name
                })
            });

            const result = await response.json();
            this.results.push(result);

            if (result.success) {
                indicatorEl.className = 'status-indicator success';
                indicatorEl.textContent = `✓ ${result.message}`;
                this.displayDataTable(result.data);
            } else {
                indicatorEl.className = 'status-indicator failure';
                indicatorEl.textContent = `✗ ${result.message || result.error}`;
                if (result.data && result.data.length > 0) {
                    this.displayDataTable(result.data);
                }
            }

        } catch (error) {
            console.error('Test failed:', error);
            indicatorEl.className = 'status-indicator error';
            indicatorEl.textContent = `Error: ${error.message}`;
        }
    }

    displayDataTable(data) {
        const tableContainer = document.getElementById('data-table-container');
        const tbody = document.getElementById('results-body');

        tbody.innerHTML = '';

        if (data && data.length > 0) {
            data.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${row.indicator || ''}</td>
                    <td>${row.value || ''}</td>
                    <td>${row.change || ''}</td>
                `;
                tbody.appendChild(tr);
            });
            tableContainer.style.display = 'block';
        }
    }

    showCompletion() {
        const statusEl = document.getElementById('result-status');
        const indicatorEl = document.getElementById('status-indicator');

        indicatorEl.className = 'status-indicator completion';
        indicatorEl.textContent = 'Demo completed! All selectors tested.';

        document.getElementById('auto-run-btn').textContent = 'Restart Demo';
        document.getElementById('auto-run-btn').onclick = () => this.restartDemo();
    }

    restartDemo() {
        this.currentSelectorIndex = 0;
        this.results = [];
        document.getElementById('auto-run-btn').textContent = 'Auto Run';
        document.getElementById('auto-run-btn').onclick = () => this.toggleAutoRun();
        this.runNextSelector();
    }

    toggleAutoRun() {
        this.autoRun = !this.autoRun;
        const btn = document.getElementById('auto-run-btn');

        if (this.autoRun) {
            btn.textContent = 'Stop Auto';
            this.currentSelectorIndex++;
            this.runNextSelector();
        } else {
            btn.textContent = 'Auto Run';
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }
}

// Global demo instance
let selectorDemo = new SelectorDemo();

// Global functions for HTML onclick handlers
function runExercise(exerciseId) {
    if (exerciseId === 1) {
        selectorDemo.startDemo();
    }
}

function closeDemo() {
    const modal = document.querySelector('.exercise-modal');
    if (modal) {
        modal.remove();
    }
}

function nextSelector() {
    selectorDemo.currentSelectorIndex++;
    selectorDemo.runNextSelector();
}

function prevSelector() {
    selectorDemo.currentSelectorIndex--;
    selectorDemo.runNextSelector();
}

function toggleAutoRun() {
    selectorDemo.toggleAutoRun();
}

// Selector Fallback Strategy Demo
async function runPlaywrightDemo() {
    const version = document.getElementById('demo-version').value;
    const resultsDiv = document.getElementById('demo-results');
    const outputDiv = document.getElementById('demo-output');

    // Show loading state
    resultsDiv.style.display = 'block';
    outputDiv.innerHTML = '<p>Testing selector strategies... This may take a few seconds.</p>';

    try {
        const response = await fetch(`${API_BASE}/api/demo/selector-fallback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                version: version
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Build step-by-step demonstration
            let html = `
                <div class="fallback-demo">
                    <div class="demo-header">
                        <h5>🎯 Testing ${data.version.toUpperCase()}: ${getVersionName(data.version)}</h5>
                        <p><strong>Strategy:</strong> ${data.explanation.strategy}</p>
                        <p><strong>Why it works:</strong> ${data.explanation.why_it_works}</p>
                        <div style="margin-top: 1rem; padding: 0.75rem; background: white; border-radius: 6px;">
                            <strong>Results:</strong>
                            <span style="color: #059669; margin-left: 0.5rem;">✓ ${data.successes} succeeded</span>
                            <span style="color: #dc2626; margin-left: 1rem;">✗ ${data.failures} failed</span>
                        </div>
                    </div>

                    <div class="selector-attempts">
                        <h5>Selector Testing Progress</h5>
                        <p style="margin-bottom: 1em;"><strong>Watch the fallback strategy in action:</strong> The scraper tries each selector until one succeeds. Failed selectors are shown in red, successful ones in green.</p>
                        ${data.attempts.map((attempt) => {
                            const isFirstSuccess = data.first_success &&
                                                  attempt.selector === data.first_success.selector;
                            const statusIcon = attempt.success ? '✅' : '❌';
                            const statusClass = attempt.success ? 'success' : 'failed';
                            const highlightClass = isFirstSuccess ? 'first-success' : '';

                            return `
                                <div class="selector-attempt ${statusClass} ${highlightClass}">
                                    <div class="attempt-header">
                                        <span class="priority-badge">Priority ${attempt.priority}</span>
                                        <span class="status-icon">${statusIcon}</span>
                                        <strong>${attempt.selector_name}</strong>
                                        ${isFirstSuccess ? '<span class="winner-badge">✨ FIRST SUCCESS - Used this!</span>' : ''}
                                    </div>
                                    <div class="attempt-details">
                                        <code>${attempt.selector}</code>
                                        <p class="comment">${attempt.comment}</p>
                                        ${attempt.success ?
                                            `<p class="result-success">✓ Found ${attempt.rows_found} rows</p>` :
                                            `<p class="result-failed">✗ Selector found no elements</p>`
                                        }
                                        ${isFirstSuccess && attempt.data_sample.length > 0 ? `
                                            <details class="data-sample">
                                                <summary>View extracted data (first 2 rows)</summary>
                                                <table>
                                                    <thead>
                                                        <tr>
                                                            <th>Indicator</th>
                                                            <th>Value</th>
                                                            <th>Change</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        ${attempt.data_sample.map(row => `
                                                            <tr>
                                                                <td>${row.indicator}</td>
                                                                <td>${row.value}</td>
                                                                <td>${row.change}</td>
                                                            </tr>
                                                        `).join('')}
                                                    </tbody>
                                                </table>
                                            </details>
                                        ` : ''}
                                    </div>
                                </div>
                            `;
                        }).join('')}
                    </div>

                    <div class="demo-summary">
                        <h5>📊 Summary</h5>
                        <ul>
                            <li><strong>Selectors tested:</strong> ${data.total_selectors}</li>
                            <li><strong>First success:</strong> ${data.first_success ? `${data.first_success.selector_name} (Priority ${data.first_success.priority})` : 'None'}</li>
                            <li><strong>Data extracted:</strong> ${data.first_success ? `${data.first_success.rows_found} rows` : '0 rows'}</li>
                        </ul>
                        <p class="key-insight">
                            <strong>💡 Key Insight:</strong>
                            ${getVersionInsight(data.version, data.first_success)}
                        </p>
                    </div>
                </div>
            `;

            outputDiv.innerHTML = html;
        } else {
            outputDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        }
    } catch (error) {
        console.error('Selector fallback demo error:', error);
        outputDiv.innerHTML = `
            <p class="error">Failed to run demo. Make sure the backend server is running on port 8080.</p>
            <p>Error: ${error.message}</p>
        `;
    }
}

function getVersionName(version) {
    const names = {
        'v1': 'Original Design',
        'v2': 'Redesigned Layout',
        'v3': 'Major Redesign'
    };
    return names[version] || version;
}

function getVersionInsight(version, firstSuccess) {
    if (!firstSuccess) {
        return 'No selectors worked! The HTML structure may have changed too much, or none of the selectors match this version.';
    }

    const insights = {
        'v1': `The original v1 ID selector (#statistics-table) worked immediately. But notice how v2 and v3 selectors failed on v1 - showing that ID selectors are version-specific and fragile.`,
        'v2': `The v1 selectors FAILED on the redesigned page! The v1 ID (#statistics-table) no longer exists. But the v2 ID (#stats-data-grid) and ARIA role selectors still work. This shows why fallback strategies matter - when one breaks, another succeeds!`,
        'v3': `After the major redesign, most old selectors FAILED! Only the data-attribute selector and v3-specific selectors work. This demonstrates that semantic attributes (data-*, aria-*) are the most stable across major redesigns. ID and class selectors broke, but semantic attributes survived!`
    };

    return insights[version] || 'Fallback strategy successfully found working selector.';
}