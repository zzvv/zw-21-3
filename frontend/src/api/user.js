import request from './request.js'

export function listUsers() {
  return request.get('/users')
}

export function createUser(data) {
  return request.post('/users', data)
}

export function deleteUser(id) {
  return request.delete(`/users/${id}`)
}
