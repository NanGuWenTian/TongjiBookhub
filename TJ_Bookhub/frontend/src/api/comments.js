import request from '@/utils/request';

// 获取图书评论
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