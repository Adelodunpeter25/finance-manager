export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  currency?: string;
  timezone?: string;
  created_at?: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  confirm_password: string;
  first_name?: string;
  last_name?: string;
}

export interface AuthResponse {
  user: User;
  access: string;
  refresh: string;
}
