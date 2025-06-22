import axios from 'axios'

export const getComments = (id) => {
  return axios.get(`/api/comments/${id}`)
}