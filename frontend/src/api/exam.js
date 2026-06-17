import request from './request.js'

export function listExams(params) {
  return request.get('/exams', { params })
}

export function createExam(data) {
  return request.post('/exams', data)
}

export function updateExam(id, data) {
  return request.put(`/exams/${id}`, data)
}

export function deleteExam(id) {
  return request.delete(`/exams/${id}`)
}
