// api/borrows.js
import axios from 'axios'

export const fetchUserBorrows = (userId) => {
  return axios.get('/api/borrows', { params: { user_id: userId } })
}

export const fetchAllBorrows = () => {
  return axios.get('/api/borrows')
}

export const fetchOverdueBorrows = () => {
  return axios.get('/api/borrows/overdue')
}

export const borrowBook = (bookId) => {
  return axios.post('/api/borrows', { book_id: bookId })
}

export const returnBook = (recordId) => {
  return axios.post(`/api/borrows/${recordId}/return`)
}