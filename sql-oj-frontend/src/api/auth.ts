import request from './request'

interface LoginData {
  username: string
  password: string
}

interface RegisterData {
  username: string
  email: string
  password: string
  user_type: 'student' | 'teacher'
}

export const login = (data: LoginData) => {
  return request.post('/auth/login/', data)
}

export const register = (data: RegisterData) => {
  return request.post('/auth/register/', data)
}

export const getCurrentUser = () => {
  return request.get('/users/me/')
}