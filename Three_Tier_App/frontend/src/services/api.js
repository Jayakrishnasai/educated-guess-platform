import apiClient from './axios-config';

const api = {
    // Content endpoints
    getContent: (params = {}) => {
        return apiClient.get('/content', { params });
    },

    getContentById: (id) => {
        return apiClient.get(`/content/${id}`);
    },

    createContent: (data) => {
        return apiClient.post('/content', data);
    },

    updateContent: (id, data) => {
        return apiClient.put(`/content/${id}`, data);
    },

    deleteContent: (id) => {
        return apiClient.delete(`/content/${id}`);
    },

    // Category endpoints
    getCategories: () => {
        return apiClient.get('/categories');
    },

    getCategoryById: (id) => {
        return apiClient.get(`/categories/${id}`);
    },

    // Auth endpoints
    register: (data) => {
        return apiClient.post('/auth/register', data);
    },

    login: (data) => {
        return apiClient.post('/auth/login', data);
    },

    // Health check
    healthCheck: () => {
        return apiClient.get('/health');
    }
};

export default api;
