import axios from 'axios'

export const getCaptcha = async (email) => {
  try {
    const response = await axios.post(
      '/api/auth/send_captcha',
      { 'email': email }
    );

    return response.data;

  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
};


export const register = async (userData) => {
  try {
    const response = await axios.post(
      '/api/auth/register',
      userData
    );

    return response.data;

  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
};

export const login = async (userData) => {
  try {
    const response = await axios.post('/api/auth/login', userData);
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
};