import axios from 'axios'

export const fetchBooks = (params = {}) => {
  return axios.get('/api/books', {params})
}

export const addBook = (bookData) => {
  return axios.post('/api/books', bookData)
}

export const updateBook = (id, bookData) => {
  return axios.put(`/api/books/${id}`, bookData)
}

export const deleteBook = (id) => {
  return axios.delete(`/api/books/${id}`)
}

export const lookBook = (id) => {
  return axios.get(`/api/books/${id}`)
}