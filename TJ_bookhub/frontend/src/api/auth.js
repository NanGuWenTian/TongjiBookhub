import axios from 'axios'

export const getCaptcha = async (email) => {
  try {
    const response = await axios.post(
      '/api/auth/send_captcha',
      { email },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data;

  } catch (error) {
    console.error('获取验证码失败:', error);
    return { code: 500, msg: '网络错误' };
  }
};


export const register = async (userData) => {
  try {
    const response = await axios.post(
      '/api/auth/register',
      userData,
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data;

  } catch (error) {
    console.error('注册失败:', error);
    return { code: 500, msg: '网络错误' };
  }
};