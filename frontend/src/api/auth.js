import request from './request.js'

export function login(data) {
  return request.post('/auth/login', data, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
}

export function getMe() {
  return request.get('/auth/me')
}
