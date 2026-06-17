import request from './request.js'

export function listTeachers(params) {
  return request.get('/teachers', { params })
}

export function createTeacher(data) {
  return request.post('/teachers', data)
}

export function updateTeacher(id, data) {
  return request.put(`/teachers/${id}`, data)
}

export function deleteTeacher(id) {
  return request.delete(`/teachers/${id}`)
}
