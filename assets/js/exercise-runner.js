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
            const response = await fetch('http://localhost:5001/api/demo/selectors');
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
            this.showError('Failed to start demo. Make sure the backend server is running on port 5000.');
        }
    }

    showDemoInterface() {
        const modal = document.createElement('div');
        modal.className = 'exercise-modal';
        modal.innerHTML = `
            <div class="exercise-overlay" onclick="closeDemo()"></div>
            <div class="exercise-content">
                <div class="exercise-header">
                    <h2>Exercise 1: Selector Strategy Demo</h2>
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
            const response = await fetch('http://localhost:5001/api/demo/test-selector', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    selector: selector.selector,
                    version: selector.url.split('_')[-1].replace('.html', ''),
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