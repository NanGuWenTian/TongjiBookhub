import request from '@/utils/request';


export const getUserInfoBrief = async () => {
  try {
    const response = await request.get('/api/user/brief');
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}


export const getUserInfo = async () => {
  try {
    const response = await request.get('/api/user');
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}


export const uploadAvatar = async (file) => {
  try {
    const formData = new FormData();
    formData.append('avatar', file);
    const response = await request.post('/api/user/upload/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}


export const updateUserInfo = async (userInfo) => { 
  try {
    const response = await request.put('/api/user/update/userInfo', userInfo);
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}