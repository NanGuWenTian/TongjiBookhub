import request from '@/utils/request';

export const getBorrowRecords = async () => { 
  try { 
    const response = await request.get('/api/borrow_records');
    return response.data;
  }
  catch (error) { 
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}

export const checkOverdueStatus = async () => {
  try {
    const response = await request.get('/api/borrow_records/overdue_status');
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    return { code: 500, msg: '网络错误' };
  }
}