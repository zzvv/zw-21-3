import request from './request.js'

export function listClassrooms(params) {
  return request.get('/classrooms', { params })
}

export function createClassroom(data) {
  return request.post('/classrooms', data)
}

export function updateClassroom(id, data) {
  return request.put(`/classrooms/${id}`, data)
}

export function updateClassroomStatus(id, status) {
  return request.post(`/classrooms/${id}/status`, null, { params: { status } })
}

export function deleteClassroom(id) {
  return request.delete(`/classrooms/${id}`)
}
