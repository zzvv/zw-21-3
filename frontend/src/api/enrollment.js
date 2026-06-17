import request from './request.js'

export function listEnrollments(params) {
  return request.get('/enrollments', { params })
}

export function createEnrollment(data) {
  return request.post('/enrollments', data)
}

export function consumeLesson(id) {
  return request.post(`/enrollments/${id}/consume`)
}

export function cancelEnrollment(id) {
  return request.post(`/enrollments/${id}/cancel`)
}
