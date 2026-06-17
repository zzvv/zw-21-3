import request from './request.js'

export function listInstruments(params) {
  return request.get('/instruments', { params })
}

export function createInstrument(data) {
  return request.post('/instruments', data)
}

export function updateInstrument(id, data) {
  return request.put(`/instruments/${id}`, data)
}

export function updateInstrumentStatus(id, status) {
  return request.post(`/instruments/${id}/status`, null, { params: { status } })
}

export function deleteInstrument(id) {
  return request.delete(`/instruments/${id}`)
}
