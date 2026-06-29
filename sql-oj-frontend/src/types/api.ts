// 用户相关类型
export interface User {
  id: number
  username: string
  email: string
  user_type: 'student' | 'teacher'
}

// 题目相关类型
export interface Question {
  id: number
  description: string
  difficulty: 'easy' | 'medium' | 'hard'
  sample_input: string
  sample_output: string
  create_table_sql: string
}

// 提交相关类型
export interface Submission {
  id: number
  question: number
  submitted_sql: string
  execution_status: string
  score: number
  created_at: string
}

// API 响应格式（分页）
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}