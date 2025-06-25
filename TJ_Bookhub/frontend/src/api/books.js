import request from '@/utils/request';

// 获取所有书籍，包含分页和搜索参数
export const getBooks = async (params) => {
  try {
    const response = await request.get('/api/books', {params});
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}

// 获取书籍详情
export const getBookDetails = async (id) => {
  try {
    const response = await request.get(`/api/books/${id}`);
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}

// 查看这个书有没有被借过
export const getBookStatus = async (id) => { 
  try {
    const response = await request.get(`/api/books/${id}/status`);
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}

// 借书
export const getBookBorrowed = async (id, during) => { 
  try {
    const response = await request.post(`/api/books/${id}/borrow/${during}`);
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}

// 还书
export const getBookFinished = async (id) => { 
  try {
    const response = await request.post(`/api/books/${id}/return`);
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}





// export const addBook = (bookData) => {
//   return axios.post('/api/books', bookData)
// }

// export const updateBook = (id, bookData) => {
//   return axios.put(`/api/books/${id}`, bookData)
// }

// export const deleteBook = (id) => {
//   return axios.delete(`/api/books/${id}`)
// }
// return axios.get(`/api/books/${id}`)
