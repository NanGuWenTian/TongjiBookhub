import request from '@/utils/request';

export const getUserInfo = async () => {
  try {
    const response = await request.get('/api/user');
    return response.data;
  } catch (error) {
    console.log(error);
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}