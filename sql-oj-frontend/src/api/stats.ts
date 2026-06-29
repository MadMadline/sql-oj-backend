import request from './request'

// 整体数据概览
export const getOverview = () => {
  return request.get('/stats/overview/')
}

// 题目通过率统计
export const getQuestionStats = () => {
  return request.get('/stats/questions/')
}

// 学生通过率排名
export const getStudentStats = () => {
  return request.get('/stats/students/')
}