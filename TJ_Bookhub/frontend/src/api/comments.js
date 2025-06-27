import request from '@/utils/request';

// 获取图书的所有评论
export const getComments = async (id, params) => { 
  try {
    const response = await request.get(`/api/comments/${id}`, { params });
    return response.data;
  }
  catch (error) { 
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}

// 添加评论
export const addComment = async (id, content) => { 
  try { 
    const response = await request.post(`/api/comments/${id}`, { content });
    return response.data;
  }
  catch (error) { 
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}

// 获取用户的所有评论
export const getUserComments = async() => { 
  try { 
    const response = await request.get('/api/comments');
    return response.data;
  }
  catch (error) { 
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}


// 更新评论
export const updateComment = async(id, comment) => { 
  try { 
    const response = await request.put(`/api/comments/${id}`, comment);
    return response.data;
  }
  catch (error) { 
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}


// 删除评论
export const cutComment = async(id) => { 
  try { 
    const response = await request.delete(`/api/comments/${id}`);
    return response.data;
  }
  catch (error) { 
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}