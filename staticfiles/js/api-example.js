/**
 * Book Catalog API Example
 * 
 * This file demonstrates how to use the Book Catalog REST API
 * with JavaScript fetch requests. It includes examples for all
 * major API operations.
 */

// Base API URL
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// API Client Class
class BookCatalogAPI {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.isAuthenticated = false;
        this.currentUser = null;
    }

    /**
     * Make an authenticated API request
     */
    async makeRequest(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            credentials: 'include', // Include session cookies
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const requestOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, requestOptions);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    }

    /**
     * Register a new user
     */
    async register(userData) {
        const response = await this.makeRequest('/auth/register/', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
        
        console.log('User registered:', response);
        return response;
    }

    /**
     * Login user
     */
    async login(username, password) {
        const response = await this.makeRequest('/auth/login/', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        this.isAuthenticated = true;
        this.currentUser = response.user;
        console.log('Login successful:', response);
        return response;
    }

    /**
     * Logout user
     */
    async logout() {
        const response = await this.makeRequest('/auth/logout/', {
            method: 'POST'
        });
        
        this.isAuthenticated = false;
        this.currentUser = null;
        console.log('Logout successful:', response);
        return response;
    }

    /**
     * Get all books
     */
    async getBooks(filters = {}) {
        const queryParams = new URLSearchParams(filters);
        const endpoint = `/books/${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
        
        const response = await this.makeRequest(endpoint);
        console.log('Books retrieved:', response);
        return response;
    }

    /**
     * Get a single book by ID
     */
    async getBook(bookId) {
        const response = await this.makeRequest(`/books/${bookId}/`);
        console.log('Book retrieved:', response);
        return response;
    }

    /**
     * Create a new book
     */
    async createBook(bookData) {
        const response = await this.makeRequest('/books/', {
            method: 'POST',
            body: JSON.stringify(bookData)
        });
        
        console.log('Book created:', response);
        return response;
    }

    /**
     * Update a book
     */
    async updateBook(bookId, bookData) {
        const response = await this.makeRequest(`/books/${bookId}/`, {
            method: 'PUT',
            body: JSON.stringify(bookData)
        });
        
        console.log('Book updated:', response);
        return response;
    }

    /**
     * Delete a book
     */
    async deleteBook(bookId) {
        const response = await this.makeRequest(`/books/${bookId}/`, {
            method: 'DELETE'
        });
        
        console.log('Book deleted:', response);
        return response;
    }

    /**
     * Toggle book read status
     */
    async toggleBookRead(bookId) {
        const response = await this.makeRequest(`/books/${bookId}/toggle_read/`, {
            method: 'POST'
        });
        
        console.log('Book read status toggled:', response);
        return response;
    }

    /**
     * Get read books
     */
    async getReadBooks() {
        const response = await this.makeRequest('/books/read_books/');
        console.log('Read books:', response);
        return response;
    }

    /**
     * Get unread books
     */
    async getUnreadBooks() {
        const response = await this.makeRequest('/books/unread_books/');
        console.log('Unread books:', response);
        return response;
    }

    /**
     * Get book statistics
     */
    async getBookStatistics() {
        const response = await this.makeRequest('/books/statistics/');
        console.log('Book statistics:', response);
        return response;
    }

    /**
     * Get all notifications
     */
    async getNotifications() {
        const response = await this.makeRequest('/notifications/');
        console.log('Notifications:', response);
        return response;
    }

    /**
     * Mark notification as read
     */
    async markNotificationRead(notificationId) {
        const response = await this.makeRequest(`/notifications/${notificationId}/mark_read/`, {
            method: 'POST'
        });
        
        console.log('Notification marked as read:', response);
        return response;
    }

    /**
     * Mark all notifications as read
     */
    async markAllNotificationsRead() {
        const response = await this.makeRequest('/notifications/mark_all_read/', {
            method: 'POST'
        });
        
        console.log('All notifications marked as read:', response);
        return response;
    }

    /**
     * Get unread notification count
     */
    async getUnreadNotificationCount() {
        const response = await this.makeRequest('/notifications/unread_count/');
        console.log('Unread notification count:', response);
        return response;
    }

    /**
     * Get system statistics (admin only)
     */
    async getSystemStatistics() {
        const response = await this.makeRequest('/statistics/');
        console.log('System statistics:', response);
        return response;
    }

    /**
     * Change password
     */
    async changePassword(currentPassword, newPassword, confirmPassword) {
        const response = await this.makeRequest('/auth/change_password/', {
            method: 'POST',
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword,
                confirm_new_password: confirmPassword
            })
        });
        
        console.log('Password changed:', response);
        return response;
    }
}

// Example usage functions
async function exampleUsage() {
    const api = new BookCatalogAPI();
    
    try {
        // 1. Login
        await api.login('admin', 'admin');
        
        // 2. Get all books
        const books = await api.getBooks();
        console.log('All books:', books);
        
        // 3. Get books with filters
        const unreadBooks = await api.getBooks({ is_read: 'false' });
        console.log('Unread books:', unreadBooks);
        
        // 4. Search books
        const searchResults = await api.getBooks({ search: 'fantasy' });
        console.log('Search results:', searchResults);
        
        // 5. Create a new book
        const newBook = await api.createBook({
            title: 'The Lord of the Rings',
            author: 'J.R.R. Tolkien',
            description: 'An epic fantasy novel about the quest to destroy a powerful ring.',
            published_date: '1954-07-29',
            isbn: '978-0547928210',
            is_read: false
        });
        console.log('New book created:', newBook);
        
        // 6. Toggle book read status
        if (newBook.id) {
            await api.toggleBookRead(newBook.id);
        }
        
        // 7. Get book statistics
        const stats = await api.getBookStatistics();
        console.log('Book statistics:', stats);
        
        // 8. Get notifications
        const notifications = await api.getNotifications();
        console.log('Notifications:', notifications);
        
        // 9. Get system statistics (admin only)
        const systemStats = await api.getSystemStatistics();
        console.log('System statistics:', systemStats);
        
        // 10. Logout
        await api.logout();
        
    } catch (error) {
        console.error('Example usage failed:', error);
    }
}

// DOM-ready function for browser usage
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Book Catalog API Example loaded');
        console.log('Run exampleUsage() to see the API in action');
        
        // Make API available globally
        window.BookCatalogAPI = BookCatalogAPI;
        window.exampleUsage = exampleUsage;
    });
}

// Export for Node.js usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BookCatalogAPI;
} 