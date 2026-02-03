import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  is_superuser: boolean;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface Document {
  id: number;
  filename: string;
  original_filename: string;
  file_type: string;
  file_size: number;
  is_company_policy: boolean;
  uploaded_by: number;
  status: string;
  created_at: string;
  updated_at?: string;
}

export interface RAGSettings {
  id: number;
  chunk_size: number;
  chunk_overlap: number;
  temperature: number;
  top_p: number;
  top_k: number;
  model_name: string;
}

export interface ChatRequest {
  query: string;
  document_id?: string;  // MongoDB ObjectId as string
  use_company_policy: boolean;
}

export interface ChatResponse {
  answer: string;
  source_documents: string[];
  return_source_documents?: boolean;
}

// Auth API
export const authApi = {
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const formData = new URLSearchParams();
    formData.append('username', data.username);
    formData.append('password', data.password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },
  
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Users API
export const usersApi = {
  getUsers: async (): Promise<User[]> => {
    const response = await api.get('/users');
    return response.data;
  },
  
  createUser: async (data: any): Promise<User> => {
    const response = await api.post('/users', data);
    return response.data;
  },
  
  updateUser: async (id: number, data: any): Promise<User> => {
    const response = await api.put(`/users/${id}`, data);
    return response.data;
  },
  
  deleteUser: async (id: number): Promise<void> => {
    await api.delete(`/users/${id}`);
  },
};

// Documents API
export const documentsApi = {
  getDocuments: async (): Promise<Document[]> => {
    const response = await api.get('/documents');
    return response.data;
  },
  
  uploadDocument: async (file: File, isCompanyPolicy: boolean): Promise<Document> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('is_company_policy', isCompanyPolicy.toString());
    
    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
  
  deleteDocument: async (id: number): Promise<void> => {
    await api.delete(`/documents/${id}`);
  },
};

// Settings API
export const settingsApi = {
  getSettings: async (): Promise<RAGSettings> => {
    const response = await api.get('/settings');
    return response.data;
  },
  
  updateSettings: async (data: Partial<RAGSettings>): Promise<RAGSettings> => {
    const response = await api.put('/settings', data);
    return response.data;
  },
};

// Chat API
export const chatApi = {
  chat: async (data: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post('/chat/', data);  // Add trailing slash
    return response.data;
  },
};

// Auth helpers
export const setToken = (token: string) => {
  localStorage.setItem('token', token);
};

export const getToken = () => {
  return localStorage.getItem('token');
};

export const removeToken = () => {
  localStorage.removeItem('token');
};

export const isTokenValid = (): boolean => {
  const token = getToken();
  if (!token) return false;
  
  try {
    const decoded: any = jwtDecode(token);
    return decoded.exp * 1000 > Date.now();
  } catch {
    return false;
  }
};
