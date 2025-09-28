// API клиент
const API_BASE = 'http://localhost:8000';

// утилиты для форм
const FormUtils = {
    showLoading(button, text = 'Загрузка...') {
        button.disabled = true;
        button.dataset.originalText = button.textContent;
        button.textContent = text;
    },

    hideLoading(button) {
        button.disabled = false;
        button.textContent = button.dataset.originalText || 'Отправить';
    },

    validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    validatePassword(password) {
        // запрещенные символы
        const forbiddenChars = /[!"#$%&'()*+,\-/:;<=>?@\[\\\]^`{|}~]/;
        return !forbiddenChars.test(password);
    },

    formatDate(dateString) {
        if (!dateString) return 'N/A';
        try {
            const date = new Date(dateString);
            return date.toLocaleString('ru-RU');
        } catch (e) {
            return 'N/A';
        }
    }
};

// уведомления
const notifications = {
    show(message, type = 'info', duration = 5000) {
        // создаем уведомление
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        // добавляем стили
        if (!document.getElementById('notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'notification-styles';
            styles.textContent = `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    z-index: 1000;
                    max-width: 400px;
                    padding: 15px;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                    animation: slideIn 0.3s ease-out;
                }
                .notification-success { background: #d4edda; color: #155724; border-left: 4px solid #28a745; }
                .notification-error { background: #f8d7da; color: #721c24; border-left: 4px solid #dc3545; }
                .notification-warning { background: #fff3cd; color: #856404; border-left: 4px solid #ffc107; }
                .notification-info { background: #d1ecf1; color: #0c5460; border-left: 4px solid #17a2b8; }
                .notification-content { display: flex; justify-content: space-between; align-items: center; }
                .notification-close { background: none; border: none; font-size: 18px; cursor: pointer; margin-left: 10px; }
                @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
            `;
            document.head.appendChild(styles);
        }

        // добавляем на страницу
        document.body.appendChild(notification);

        // удаляем через время
        if (duration > 0) {
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, duration);
        }
    }
};

// API клиент
const api = {
    async request(endpoint, options = {}) {
        const url = `${API_BASE}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            let data;
            const contentType = response.headers.get('content-type');
            
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                const text = await response.text();
                data = { error: `Сервер вернул ошибку: ${response.status} ${response.statusText}` };
            }
            
            return {
                success: response.ok,
                data: data,
                status: response.status
            };
        } catch (error) {
            return {
                success: false,
                data: { error: 'Ошибка сети: ' + error.message },
                status: 0
            };
        }
    },

    // авторизация
    async register(login, email, password) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ login, email, password })
        });
    },

    async login(login, email, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ login, email, password })
        });
    },

    async logout() {
        return this.request('/auth/logout', {
            method: 'POST'
        });
    },

    // пользователи
    async createUser(userData) {
        return this.request('/api/users', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },

    async getUsers() {
        return this.request('/api/users');
    },

    async getUser(userId) {
        return this.request(`/api/users/${userId}`);
    },

    async updateUser(userId, userData) {
        return this.request(`/api/users/${userId}`, {
            method: 'PUT',
            body: JSON.stringify(userData)
        });
    },

    // задачи
    async createTask(taskData) {
        return this.request('/api/tasks', {
            method: 'POST',
            body: JSON.stringify(taskData)
        });
    },

    async getTasks() {
        return this.request('/api/tasks');
    },

    async getTask(taskId) {
        return this.request(`/api/tasks/${taskId}`);
    },

    async updateTask(taskId, taskData) {
        return this.request(`/api/tasks/${taskId}`, {
            method: 'PUT',
            body: JSON.stringify(taskData)
        });
    },

    async deleteTask(taskId) {
        return this.request(`/api/tasks/${taskId}`, {
            method: 'DELETE'
        });
    },

    async updateTaskStatus(taskId, status) {
        return this.request(`/api/tasks/${taskId}/status`, {
            method: 'PATCH',
            body: JSON.stringify({ status })
        });
    },

    async assignTask(taskId, assignedTo) {
        return this.request(`/api/tasks/${taskId}/assign`, {
            method: 'PATCH',
            body: JSON.stringify({ assigned_to: assignedTo })
        });
    }
};

// инициализация
document.addEventListener('DOMContentLoaded', function() {
    // обработчики форм
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // блокируем стандартную отправку
            e.preventDefault();
        });
    });

    // показываем готовность
    notifications.show('API клиент загружен и готов к работе!', 'success', 3000);
});
