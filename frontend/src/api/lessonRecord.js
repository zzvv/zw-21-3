import request from './request.js'

export function listLessonRecords(params) {
  return request.get('/lesson-records', { params })
}

export function createLessonRecord(data) {
  return request.post('/lesson-records', data)
}

export function updateLessonRecord(id, data) {
  return request.put(`/lesson-records/${id}`, data)
}

export function deleteLessonRecord(id) {
  return request.delete(`/lesson-records/${id}`)
}
