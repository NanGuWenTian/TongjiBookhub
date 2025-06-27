<template>
  <div id="chat-container">
    <header class="chat-header">
      <button @click="goBack" class="back-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-arrow-left" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z"/>
        </svg>
      </button>
      <h1>AI助手</h1>
      <button @click="resetConversation" class="reset-button" :disabled="isLoading">新对话</button>
    </header>

    <div class="chat-window" ref="chatWindow">
      <div v-if="conversation.length === 0" class="no-messages">
        <p>有什么可以帮忙的？</p>
      </div>
      
      <div v-else v-for="(message, index) in conversation" :key="index" :class="['message-bubble', message.sender]">
        <p><strong>{{ message.sender === 'user' ? '我' : 'AI助手' }}:</strong></p>
        <p>{{ message.text }}</p>
      </div>

      <div v-if="isLoading" class="message-bubble ai typing">
        <div class="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>

    <div class="chat-input-area">
      <textarea
        v-model="userInput"
        @keyup.enter.prevent="sendMessage"
        placeholder="给AI助手发送消息..."
        :disabled="isLoading"
        ref="inputArea"
      ></textarea>
      <button @click="sendMessage" :disabled="isLoading || !userInput.trim()">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-send-fill" viewBox="0 0 16 16">
          <path d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855H.766l-.452.18a.5.5 0 0 0-.082.887l.41.26.001.002 4.995 3.178 3.178 4.995.002.002.26.41a.5.5 0 0 0 .886-.083l4.995-14.185Z"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

const userInput = ref('');
const conversation = ref([]); // 存储对话消息 { sender: 'user'/'ai', text: 'message' }
const isLoading = ref(false);
const chatWindow = ref(null); // 用于自动滚动
const typewriterDelay = ref(50); // 打字机效果延迟时间（毫秒）
const currentTypewriterTimer = ref(null); // 存储当前打字机定时器

const scrollToBottom = () => {
  nextTick(() => {
    if (chatWindow.value) {
      chatWindow.value.scrollTop = chatWindow.value.scrollHeight;
    }
  });
};

// 打字机效果函数
const typewriterEffect = (fullText, messageIndex) => {
  return new Promise((resolve) => {
    let currentIndex = 0;
    
    // 清除之前的定时器（如果存在）
    if (currentTypewriterTimer.value) {
      clearInterval(currentTypewriterTimer.value);
    }
    
    const timer = setInterval(() => {
      if (currentIndex <= fullText.length) {
        // 更新对话中对应消息的文本
        conversation.value[messageIndex].text = fullText.substring(0, currentIndex);
        scrollToBottom();
        currentIndex++;
      } else {
        clearInterval(timer);
        currentTypewriterTimer.value = null;
        resolve();
      }
    }, typewriterDelay.value);
    
    currentTypewriterTimer.value = timer;
  });
};

async function sendMessage() {
  const query = userInput.value.trim();
  if (!query || isLoading.value) return;

  // 清除可能正在进行的打字机效果
  if (currentTypewriterTimer.value) {
    clearInterval(currentTypewriterTimer.value);
    currentTypewriterTimer.value = null;
  }

  isLoading.value = true;
  conversation.value.push({ sender: 'user', text: query });
  scrollToBottom();
  userInput.value = ''; // 发送后清空输入框

  try {
    const response = await axios.post('api/ai/chat', { query: query });
    console.log('AI响应数据如下:');
    console.log(response.data);

    const data = response.data;
    
    // 先添加一个空的AI消息到对话中
    const aiMessageIndex = conversation.value.length;
    conversation.value.push({ sender: 'ai', text: '' });
    
    // 结束加载状态
    isLoading.value = false;
    
    // 开始打字机效果
    await typewriterEffect(data.ai_response, aiMessageIndex);

  } catch (error) {
    console.error('Error sending message:', error);
    const errorMessage = `Error: ${error.response?.data?.error || 'Could not get response.'}`;
    
    // 对错误消息也使用打字机效果
    const errorMessageIndex = conversation.value.length;
    conversation.value.push({ sender: 'ai', text: '' });
    isLoading.value = false;
    await typewriterEffect(errorMessage, errorMessageIndex);
  }
}

async function resetConversation() {
  // 清除正在进行的打字机效果
  if (currentTypewriterTimer.value) {
    clearInterval(currentTypewriterTimer.value);
    currentTypewriterTimer.value = null;
  }
  
  isLoading.value = true;
  try {
    const response = await axios.post('api/ai/reset_conversation');
    console.log("对话清空完毕，api返回", response.data);

    conversation.value = []; // 前端清空对话
    alert("Conversation has been reset.");
  } catch (error) {
    console.error('Error resetting conversation:', error);
    alert(`Error resetting conversation: ${error.response?.data?.error || 'Unknown error'}`);
  } finally {
    isLoading.value = false;
  }
}

const goBack = () => {
  // 这里可以添加返回逻辑，例如返回上一页
  window.history.back();
};

// 组件卸载时清理定时器
onMounted(() => {
  // 可以在这里设置不同的打字速度
  // typewriterDelay.value = 30; // 更快的打字速度
});

// 如果使用 Vue 3 Composition API，需要在组件卸载时清理
onUnmounted(() => {
  if (currentTypewriterTimer.value) {
    clearInterval(currentTypewriterTimer.value);
  }
});
</script>

<style lang="scss" scoped>
/* --- 全局与根元素 --- */
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  background-color: #f4f7f9;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  color: #333;
}

#app {
  width: 100%;
  max-width: 700px;
  height: 90vh;
  max-height: 800px;
  display: flex;
  flex-direction: column;
}

/* --- 聊天主容器 --- */
#chat-container {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.07);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100vh;
  border: 1px solid #e8eaf0;
}

/* --- 聊天头部 --- */
.chat-header {
  background-image: linear-gradient(to right, #007bff, #0056b3);
  color: white;
  padding: 15px 20px;
  text-align: center;
  font-size: 1.2em;
  border-bottom: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h1 {
  margin: 0;
  font-size: 1.4rem;
}

.reset-button {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}

.reset-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.reset-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.back-button {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 8px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

/* --- 聊天窗口 --- */
.chat-window {
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f9fafc;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.no-messages {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #aaa;
  font-size: 1.1rem;
}

/* --- 消息气泡 --- */
.message-bubble {
  padding: 12px 18px;
  border-radius: 20px;
  max-width: 70%;
  word-wrap: break-word;
  line-height: 1.5;
  animation: message-fade-in 0.5s ease-out;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.message-bubble:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.message-bubble.user {
  background-image: linear-gradient(45deg, #007bff, #0056b3);
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 5px;
}

.message-bubble.ai {
  background-color: #ffffff;
  color: #333;
  align-self: flex-start;
  border-bottom-left-radius: 5px;
  border: 1px solid #e9ecef;
}

.message-bubble p {
  margin: 0;
}

.message-bubble p strong {
  display: block;
  margin-bottom: 4px;
  font-size: 0.9em;
  color: inherit;
  opacity: 0.7;
}

/* --- 输入区域 --- */
.chat-input-area {
  display: flex;
  padding: 15px;
  border-top: 1px solid #e8eaf0;
  background-color: #ffffff;
  align-items: center;

}

.chat-input-area textarea {
  flex-grow: 1;
  padding: 12px 18px;
  border: 1px solid #dbe2e9;
  border-radius: 22px;
  resize: none;
  font-family: inherit;
  font-size: 1rem;
  min-height: 25px;
  max-height: 100px;
  overflow-y: auto;
  line-height: 1.4;
  margin-right: 10px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.chat-input-area textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.15);
}

.chat-input-area button {
  background-color: #007bff;
  color: white;
  border: none;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: bold;
  transition: background-color 0.3s ease;
  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-input-area button:hover {
  background-color: #0056b3;
}

.chat-input-area button:disabled {
  background-color: #a9cce3;
  cursor: not-allowed;
}

/* --- 动画定义 --- */
@keyframes message-fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-bubble.typing {
  display: flex;
  align-items: center;
  padding: 15px 18px;
}

.typing-indicator {
  display: flex;
  align-items: center;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  margin: 0 2px;
  background-color: #a9cce3;
  border-radius: 50%;
  display: inline-block;
  animation: typing-bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing-bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1.0);
  }
}

/* --- 滚动条美化 (可选) --- */
.chat-window::-webkit-scrollbar {
  width: 8px;
}
.chat-window::-webkit-scrollbar-track {
  background: transparent;
}
.chat-window::-webkit-scrollbar-thumb {
  background-color: #dbe2e9;
  border-radius: 10px;
}
.chat-window::-webkit-scrollbar-thumb:hover {
  background-color: #c8d0d8;
}
</style>