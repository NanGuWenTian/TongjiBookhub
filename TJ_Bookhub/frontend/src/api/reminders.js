import request from '@/utils/request';

export const getReminders = async () => { 
  try { 
    const response = await request.get('/api/reminders');
    return response.data;
  }
  catch (error) { 
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}

export const markReminderAsRead = async (id) => { 
  try { 
    const response = await request.put(`/api/reminders/${id}`);
    return response.data;
  }
  catch (error) { 
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}