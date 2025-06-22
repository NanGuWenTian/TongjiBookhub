<template>
  <div class="modal-overlay">
    <div class="modal">
      <button class="close-button" @click="$emit('close')">×</button>
      <h2>注册 TJBookhub 账号</h2>
      
      <form @submit.prevent="handleRegister">
        <!-- 用户名输入 -->
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="form.username" 
            required
            placeholder="请输入4-16位字母、数字或下划线"
            @input="validateUsername"
          >
          <span class="error-message" v-if="errors.username">{{ errors.username }}</span>
        </div>
        
        <!-- 邮箱输入 -->
        <div class="form-group">
          <label for="email">邮箱</label>
          <input 
            type="email" 
            id="email" 
            v-model="form.email" 
            required
            placeholder="请输入有效邮箱地址"
            @input="validateEmail"
          >
          <span class="error-message" v-if="errors.email">{{ errors.email }}</span>
        </div>
        
        <!-- 密码输入 -->
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="form.password" 
            required
            placeholder="请输入6-20位密码"
            @input="validatePassword"
          >
          <span class="error-message" v-if="errors.password">{{ errors.password }}</span>
        </div>
        
        <!-- 确认密码 -->
        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="form.confirmPassword" 
            required
            placeholder="请再次输入密码"
            @input="validateConfirmPassword"
          >
          <span class="error-message" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</span>
        </div>
        
        <!-- 验证码 -->
        <div class="form-group">
          <label for="captcha">验证码</label>
          <div class="captcha-container">
            <input 
              type="text" 
              id="captcha" 
              v-model="form.captcha" 
              required
              placeholder="请输入验证码"
              class="captcha-input"
            >
            <button 
              type="button" 
              class="captcha-button" 
              :disabled="captchaCooldown > 0"
              @click="sendCaptcha"
            >
              {{ captchaButtonText }}
            </button>
          </div>
          <span class="error-message" v-if="errors.captcha">{{ errors.captcha }}</span>
        </div>
        
        <!-- 自动登录选项 -->
        <div class="form-options">
          <label class="checkbox-container">
            <input type="checkbox" v-model="form.autoLogin">
            <span class="checkmark"></span>
            注册后自动登录
          </label>
        </div>
        
        <!-- 注册按钮 -->
        <button 
          type="submit" 
          class="submit-button"
          :disabled="!formValid"
        >
          注册
        </button>
        
        <!-- 已有账号链接 -->
        <p class="switch-text">
          已有账号？
          <a href="#" @click.prevent="$emit('switch-to-login')">立即登录</a>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch, emit } from 'vue';
import { getCaptcha } from '../api/auth';


// 表单数据
const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  captcha: '',
  autoLogin: true
});

// 错误信息
const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  captcha: ''
});

// 验证码相关状态
const captchaCooldown = ref(0);
const captchaButtonText = computed(() => 
  captchaCooldown.value > 0 ? `${captchaCooldown.value}s后重新获取` : '获取验证码'
);

// 表单验证状态
const formValid = computed(() => {
  return (
    form.username && 
    form.email && 
    form.password && 
    form.confirmPassword && 
    form.captcha &&
    !errors.username &&
    !errors.email &&
    !errors.password &&
    !errors.confirmPassword
  );
});

// 验证用户名
const validateUsername = () => {
  const regex = /^[a-zA-Z0-9_]{4,16}$/;
  if (!regex.test(form.username)) {
    errors.username = '用户名需4-16位字母、数字或下划线';
  } else {
    errors.username = '';
  }
};

// 验证邮箱
const validateEmail = () => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!regex.test(form.email)) {
    errors.email = '请输入有效的邮箱地址';
  } else {
    errors.email = '';
  }
};

// 验证密码
const validatePassword = () => {
  if (form.password.length < 6 || form.password.length > 20) {
    errors.password = '密码长度需6-20位';
  } else {
    errors.password = '';
    validateConfirmPassword(); // 密码修改后重新验证确认密码
  }
};

// 验证确认密码
const validateConfirmPassword = () => {
  if (form.confirmPassword !== form.password) {
    errors.confirmPassword = '两次输入的密码不一致';
  } else {
    errors.confirmPassword = '';
  }
};

// 发送验证码
const sendCaptcha = async () => {
  if (!form.email) {
    errors.email = '请先输入邮箱地址';
    return;
  }

  const result = await getCaptcha(form.email);
  if (result.code === 429) {
    alert(result.msg);
    return;
  }
  if (result.code !== 200) {
    alert(result.msg || '发送失败');
    return;
  }
  alert('验证码已发送，请查收。');

  // 设置60秒冷却
  captchaCooldown.value = 60;
  const timer = setInterval(() => {
    captchaCooldown.value--;
    if (captchaCooldown.value <= 0) {
      clearInterval(timer);
    }
  }, 1000);
};

// 处理注册
const handleRegister = () => {
  if (!formValid.value) return;
  
  console.log('注册信息:', form);
  // 这里应该调用注册API
  // 注册成功后根据autoLogin决定是否自动登录
  
  // 模拟注册成功
  alert('注册成功!');
  if (form.autoLogin) {
    // 自动登录逻辑
    console.log('自动登录中...');
  }
  
  // 关闭模态框
  emit('close');
};

// 监听表单变化
watch(
  () => [form.username, form.email, form.password, form.confirmPassword],
  () => {
    validateUsername();
    validateEmail();
    validatePassword();
    validateConfirmPassword();
  }
);
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
  z-index: 1000;
}

.modal {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  max-height: 100vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  font-size: 0.95rem;
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
  transition: color 0.3s;
}

.close-button:hover {
  color: #2c3e50;
}

h2 {
  margin-top: 0;
  color: #2c3e50;
  text-align: center;
  font-size: 1.2rem;
  margin-bottom: 1.2rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  color: #2c3e50;
  font-weight: 500;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.95rem;
  transition: border-color 0.3s;
  box-sizing: border-box;
}


input:focus {
  border-color: #3498db;
  outline: none;
}

input::placeholder {
  color: #bbb;
}

.error-message {
  display: block;
  color: #e74c3c;
  font-size: 0.8rem;
  margin-top: 0.3rem;
}

/* 验证码容器 */
.captcha-container {
  display: flex;
  gap: 0.5rem;
}

.captcha-input {
  flex: 1;
}

.captcha-button {
  padding: 0 1rem;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.captcha-button:hover {
  background-color: #e9ecef;
}

.captcha-button:disabled {
  background-color: #f8f9fa;
  color: #adb5bd;
  cursor: not-allowed;
}

/* 自动登录选项 */
.form-options {
  margin: 1.5rem 0;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  color: #495057;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: relative;
  height: 18px;
  width: 18px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 3px;
  margin-right: 0.5rem;
}

.checkbox-container:hover input ~ .checkmark {
  background-color: #f1f1f1;
}

.checkbox-container input:checked ~ .checkmark {
  background-color: #3498db;
  border-color: #3498db;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-container .checkmark:after {
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

/* 提交按钮 */
.submit-button {
  width: 100%;
  padding: 0.6rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 0.5rem;
}

.submit-button:hover {
  background-color: #2980b9;
}

.submit-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

/* 切换文本 */
.switch-text {
  text-align: center;
  margin-top: 1.5rem;
  color: #7f8c8d;
}

.switch-text a {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.switch-text a:hover {
  text-decoration: underline;
}
</style>