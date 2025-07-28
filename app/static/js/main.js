// Toast notification system
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Utility function to format dates for datetime-local inputs
function formatDateForInput(dateString) {
    if (!dateString) return '';
    
    // Convert DD/MM/YYYY HH:MM:SS to YYYY-MM-DDTHH:MM
    const parts = dateString.split(' ')[0].split('/');
    const time = dateString.split(' ')[1];
    
    if (parts.length === 3) {
        const day = parts[0].padStart(2, '0');
        const month = parts[1].padStart(2, '0');
        const year = parts[2];
        const timePart = time ? time.substring(0, 5) : '00:00';
        
        return `${year}-${month}-${day}T${timePart}`;
    }
    
    return '';
}

// Initialize date inputs with proper formatting
document.addEventListener('DOMContentLoaded', function() {
    // Format existing date values in datetime-local inputs
    const dateInputs = document.querySelectorAll('input[type="datetime-local"]');
    dateInputs.forEach(input => {
        if (input.value) {
            input.value = formatDateForInput(input.value);
        }
    });
    
    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                
                // Re-enable after a delay (in case of errors)
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fas fa-search"></i> Filter';
                }, 5000);
            }
        });
    });
});

// AJAX functions for dynamic content loading
function loadMessages(channelId = '', page = 1, filters = {}) {
    const params = new URLSearchParams({
        page: page,
        ...filters
    });
    
    if (channelId) {
        params.append('channel_id', channelId);
    }
    
    fetch(`/api/messages/filter?${params}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateMessagesList(data.data);
                updatePagination(data.pagination);
            } else {
                showToast('Error loading messages', 'error');
            }
        })
        .catch(error => {
            showToast('Connection error', 'error');
        });
}

function updateMessagesList(messages) {
    const messagesList = document.getElementById('messages-list');
    if (!messagesList) return;
    
    messagesList.innerHTML = messages.map(message => `
        <div class="message-item" data-message-id="${message.id || Date.now()}">
            <div class="message-header">
                <span class="message-author">${message.user_name}</span>
                <span class="message-timestamp">${message.timestamp}</span>
                <div class="message-actions">
                    <label class="maintain-toggle">
                        <input type="checkbox" 
                               class="maintain-checkbox" 
                               data-timestamp="${message.timestamp}"
                               data-channel-id="${message.channel_id}"
                               data-user-id="${message.user_id}"
                               data-message="${message.message}"
                               ${message.to_maintain === 'True' ? 'checked' : ''}>
                        <span class="toggle-label">Mantieni</span>
                    </label>
                </div>
            </div>
            <div class="message-content">
                ${message.message}
            </div>
            <div class="message-meta">
                <span class="channel-badge">${message.channel_name}</span>
                <span class="user-id">ID: ${message.user_id}</span>
            </div>
        </div>
    `).join('');
    
    // Re-attach event listeners
    attachMessageEventListeners();
}

function updatePagination(pagination) {
    const paginationContainer = document.querySelector('.messages-pagination');
    if (!paginationContainer || pagination.total_pages <= 1) return;
    
    let paginationHTML = '';
    
    if (pagination.page > 1) {
        paginationHTML += `<a href="?page=${pagination.page - 1}&${new URLSearchParams(window.location.search)}" class="pagination-link">
            <i class="fas fa-chevron-left"></i> Precedente
        </a>`;
    }
    
    paginationHTML += `<span class="pagination-info">
        Pagina ${pagination.page} di ${pagination.total_pages}
    </span>`;
    
    if (pagination.page < pagination.total_pages) {
        paginationHTML += `<a href="?page=${pagination.page + 1}&${new URLSearchParams(window.location.search)}" class="pagination-link">
            Successiva <i class="fas fa-chevron-right"></i>
        </a>`;
    }
    
    paginationContainer.innerHTML = paginationHTML;
}

function attachMessageEventListeners() {
    const checkboxes = document.querySelectorAll('.maintain-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const data = {
                timestamp: this.dataset.timestamp,
                channel_id: this.dataset.channelId,
                user_id: this.dataset.userId,
                message: this.dataset.message,
                to_maintain: this.checked
            };
            
            fetch(`/api/messages/${Date.now()}/toggle_maintain`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast('Stato messaggio aggiornato!', 'success');
                } else {
                    showToast('Errore nell\'aggiornamento: ' + data.error, 'error');
                    this.checked = !this.checked; // Revert checkbox
                }
            })
            .catch(error => {
                showToast('Errore di connessione', 'error');
                this.checked = !this.checked; // Revert checkbox
            });
        });
    });
}

// Export functionality placeholder
function exportTable() {
    showToast('Export functionality coming soon!', 'info');
}

// Clear filters function
function clearFilters() {
    const form = document.getElementById('filters-form') || document.getElementById('messages-filters-form');
    if (form) {
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            if (input.type === 'datetime-local' || input.type === 'text') {
                input.value = '';
            } else if (input.tagName === 'SELECT') {
                input.value = input.querySelector('option[value="all"]') ? 'all' : '';
            }
        });
        form.submit();
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="text"], input[placeholder*="Filtra"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to clear filters
    if (e.key === 'Escape') {
        const activeElement = document.activeElement;
        if (activeElement && activeElement.tagName === 'INPUT') {
            activeElement.blur();
        }
    }
});

// Auto-refresh functionality for messages (optional)
let autoRefreshInterval = null;

function startAutoRefresh(interval = 30000) { // 30 seconds
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    
    autoRefreshInterval = setInterval(() => {
        // Only refresh if we're on the messages page
        if (window.location.pathname === '/messages') {
            location.reload();
        }
    }, interval);
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

// Start auto-refresh when on messages page
if (window.location.pathname === '/messages') {
    startAutoRefresh();
} 