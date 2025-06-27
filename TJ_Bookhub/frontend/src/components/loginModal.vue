<template>
  <div class="modal-overlay">
    <div class="modal">
      <button class="close-button" @click="$emit('close')">×</button>
      <h2>登录到 TJBookhub</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="account">用户名/邮箱</label>
          <input type="text" id="account" v-model="account" required>
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="password" required>
        </div>
        <button type="submit" class="submit-button">登录</button>
      </form>
      <p class="switch-text">还没有账号？<a href="#" @click.prevent="$emit('switch-to-register')">立即注册</a></p>
      <div v-if="isLogining" class="loading-overlay">
        <div class="loading-spinner"></div>
        <p>登录中，请稍候...</p>
      </div>
    </div>
  </div>
  <Vcode :show="isShow" @success="onSuccess" @close="onClose"/>
</template>

<script setup>
import { ref } from 'vue';
import { login} from '../api/auth';
import { useRouter } from 'vue-router';
import Vcode from "vue3-puzzle-vcode";
import { ElMessage } from 'element-plus'
import { checkOverdueStatus } from '@/api/borrow_records';

const account = ref('');
const password = ref('');
const router = useRouter();
const isShow = ref(false);
const isLogining = ref(false);


const onClose = () => {
  isShow.value = false;
};

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const onSuccess = async () => {
  onClose();
  isLogining.value = true;
  const result = await login({ account: account.value, password: password.value });
  await sleep(500);
  isLogining.value = false;
  if (result.code !== 200) {
    ElMessage.error(result.msg || '登录失败');
    return;
  }
  
  ElMessage.success('登录成功！');
  localStorage.setItem('access_token', result.data.access_token);
  localStorage.setItem('refresh_token', result.data.refresh_token);
  if (result.data.is_admin) {
    router.push('/admin');
    return;
  }

  const response = await checkOverdueStatus();
  if (response.code !== 200) {
    ElMessage.error(response.msg || '检查状态失败');
    return;
  }

  if (response.hasOverdue) {
    ElMessage.warning('您有超时借阅的图书，请及时归还');
  }

  router.push('/index');
};

const handleLogin = async () => {
  if (!account.value || !password.value) {
    ElMessage.warning('请填写账号和密码!');
    return;
  }
  isShow.value = true;
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 101;
}

.modal {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
}

h2 {
  margin-top: 0;
  color: #2c3e50;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

input {
  width: 100%;
  padding: 0.8rem 0.6em;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.submit-button {
  width: 100%;
  padding: 0.8rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #2980b9;
}

.switch-text {
  text-align: center;
  margin-top: 1rem;
  color: #7f8c8d;
}

.switch-text a {
  color: #3498db;
  text-decoration: none;
}

.switch-text a:hover {
  text-decoration: underline;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.loading-spinner {
  border: 4px solid #ccc;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>