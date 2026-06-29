import request from './request'

// 获取题目列表
export const getQuestions = (params?: { page?: number }) => {
  return request.get('/questions/', { params })
}

// 获取题目详情
export const getQuestionDetail = (id: number) => {
  return request.get(`/questions/${id}/`)
}

// 创建题目
export const createQuestion = (data: any) => {
  return request.post('/questions/', data)
}

// 更新题目
export const updateQuestion = (id: number, data: any) => {
  return request.put(`/questions/${id}/`, data)
}

// 删除题目
export const deleteQuestion = (id: number) => {
  return request.delete(`/questions/${id}/`)
}