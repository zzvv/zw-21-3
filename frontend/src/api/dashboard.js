import request from './request.js'

export function getDashboard() {
  return request.get('/dashboard')
}
