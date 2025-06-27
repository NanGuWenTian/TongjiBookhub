<template>
  <div class="welcome-container">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="navbar-left">
        <div class="logo-container">
          <img src="@/assets/logo.png" alt="TJBookhub Logo" class="logo">
          <div class="site-name">
            <h1>TJBookhub</h1>
            <p class="tagline">智能图书管理系统</p>
          </div>
        </div>
      </div>
      <div class="navbar-right">
        <div class="dropdown">
          <button class="dropbtn">登录/注册</button>
          <div class="dropdown-content">
            <a href="#" @click.prevent="showLogin">登录</a>
            <a href="#" @click.prevent="showRegister">注册</a>
          </div>
        </div>
        <a href="#about-section" class="about-link">关于我们</a>
      </div>
    </nav>

    <!-- 主要内容 -->
    <main class="main-content">
      <div class="hero-section">
        <h2 class="slogan animate__animated animate__fadeInDown">"探索无界 · 智慧阅读"</h2>
        <p class="sub-slogan animate__animated animate__fadeIn animate__delay-1s">TJBookhub - 您的个性化智能图书管家</p>
        <button class="start-button animate__animated animate__fadeInUp animate__delay-2s" @click="showLogin">Start Now</button>
        
        <!-- 添加动画元素 -->
        <div class="floating-books">
          <img src="@/assets/book1.png" alt="Book" class="book animate__animated animate__fadeInLeft animate__delay-1s">
          <img src="@/assets/book2.png" alt="Book" class="book animate__animated animate__fadeInRight animate__delay-1s">
          <img src="@/assets/book3.png" alt="Book" class="book animate__animated animate__fadeInLeft animate__delay-2s">
          <img src="@/assets/book4.png" alt="Book" class="book animate__animated animate__fadeInRight animate__delay-2s">
        </div>
      </div>
      
      <!-- 关于我们部分 -->
      <section id="about-section" class="about-section">
        <h2 class="section-title">关于 TJBookhub</h2>
        <div class="about-content">
          <div class="about-text animate__animated animate__fadeInLeft">
            <h3>我们的使命</h3>
            <p>TJBookhub 是一个智能图书管理系统，致力于为读者提供便捷、个性化的阅读体验，让知识触手可及。</p>
            
            <h3>核心功能</h3>
            <ul>
              <li><i class="fas fa-book-open"></i> 智能图书推荐系统</li>
              <li><i class="fas fa-calendar-check"></i> 个性化阅读计划</li>
              <li><i class="fas fa-exchange-alt"></i> 便捷的借阅管理</li>
              <li><i class="fas fa-database"></i> 丰富的图书资源</li>
              <li><i class="fas fa-chart-line"></i> 阅读数据分析</li>
            </ul>
          </div>
          <div class="about-image animate__animated animate__fadeInRight">
            <img src="@/assets/library-image.jpg" alt="Library">
          </div>
        </div>
        
        <div class="team-section">
          <h3>我们的团队</h3>
          <div class="team-members">
            <div class="member animate__animated animate__fadeInUp" v-for="(member, index) in teamMembers" :key="index">
              <img :src="member.avatar" :alt="member.name">
              <h4>{{ member.name }}</h4>
              <p>{{ member.position }}</p>
            </div>
          </div>
        </div>
        
        <div class="contact-section animate__animated animate__fadeIn">
          <h3>联系我们</h3>
          <div class="contact-methods">
            <div class="contact-method">
              <i class="fas fa-envelope"></i>
              <span>2251734@tongji.edu.cn</span>
            </div>
            <div class="contact-method">
              <i class="fas fa-phone"></i>
              <span>181-5419-7872</span>
            </div>
            <div class="contact-method">
              <i class="fas fa-map-marker-alt"></i>
              <span>上海市嘉定区曹安公路4800号</span>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 登录模态框 -->
    <LoginModal v-if="showLoginModal" @close="closeModal" @switch-to-register="showRegister" />
    
    <!-- 注册模态框 -->
    <RegisterModal v-if="showRegisterModal" @close="closeModal" @switch-to-login="showLogin" />
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue';
import LoginModal from '@/components/loginModal.vue';
import RegisterModal from '@/components/registerModal.vue';
import 'animate.css';
import '@fortawesome/fontawesome-free/css/all.css'

const showLoginModal = ref(false);
const showRegisterModal = ref(false);

const teamMembers = ref([
  {
    name: '许刚',
    position: '组长',
    avatar: require('@/assets/team1.jpg')
  },
  {
    name: '代文波',
    position: '组员',
    avatar: require('@/assets/team2.jpg')
  },
  {
    name: '胡沛荻',
    position: '组员',
    avatar: require('@/assets/team3.jpg')
  },
  {
    name: '樊明晨',
    position: '组员',
    avatar: require('@/assets/team4.jpg')
  }
]);

const showLogin = () => {
  showLoginModal.value = true;
  showRegisterModal.value = false;
};

const showRegister = () => {
  showRegisterModal.value = true;
  showLoginModal.value = false;
};

const closeModal = () => {
  showLoginModal.value = false;
  showRegisterModal.value = false;
};

function preventBodyScroll() {
  const scrollBarWidth = window.innerWidth - document.documentElement.clientWidth
  document.body.style.overflow = 'hidden'
  if (scrollBarWidth > 0) {
    document.body.style.paddingRight = scrollBarWidth + 'px'
  }
}

function restoreBodyScroll() {
  document.body.style.overflow = '';
  document.body.style.paddingRight = '';
}

watch(
  () => showLoginModal.value || showRegisterModal.value,
  (visible) => {
    if (visible) {
      preventBodyScroll();
    } else {
      restoreBodyScroll();
    }
  }
);

onBeforeUnmount(() => {
  restoreBodyScroll();
});
</script>

<style scoped>
/* 基础样式 */
.welcome-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f9f9f9;
}

/* 导航栏样式 */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  height: 50px;
  width: auto;
}

.site-name h1 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.8rem;
  font-weight: 700;
}

.tagline {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 2rem;
}

/* 下拉菜单样式 */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropbtn {
  background-color: transparent;
  color: #2c3e50;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.dropbtn:hover {
  background-color: #f1f1f1;
}

.dropdown-content {
  display: none;
  position: absolute;
  right: 0;
  background-color: #f9f9f9;
  min-width: 120px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
  border-radius: 4px;
}

.dropdown-content a {
  color: #2c3e50;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  transition: background-color 0.3s;
}

.dropdown-content a:hover {
  background-color: #e0e0e0;
}

.dropdown:hover .dropdown-content {
  display: block;
}

.about-link {
  color: #2c3e50;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.about-link:hover {
  background-color: #f1f1f1;
}

/* 主要内容样式 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.hero-section {
  text-align: center;
  min-width: 1200px;
  padding: 4rem 2rem;
  margin: 0 auto;
  position: relative;
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.slogan {
  font-size: 3.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-weight: 700;
  line-height: 1.2;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}

.sub-slogan {
  font-size: 1.8rem;
  color: #7f8c8d;
  margin-bottom: 3rem;
  max-width: 800px;
}

.start-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 1rem 3rem;
  font-size: 1.3rem;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
  position: relative;
  z-index: 2;
}

.start-button:hover {
  background-color: #2980b9;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(52, 152, 219, 0.6);
}

.start-button:active {
  transform: translateY(0);
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
}

/* 浮动书本动画 */
.floating-books {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}

.book {
  position: absolute;
  width: 80px;
  height: auto;
  opacity: 0.8;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
}

.book:nth-child(1) {
  top: 20%;
  left: 10%;
  animation-name: float1;
  animation-duration: 15s;
}

.book:nth-child(2) {
  top: 30%;
  right: 15%;
  animation-name: float2;
  animation-duration: 18s;
}

.book:nth-child(3) {
  bottom: 25%;
  left: 20%;
  animation-name: float3;
  animation-duration: 20s;
}

.book:nth-child(4) {
  bottom: 15%;
  right: 10%;
  animation-name: float4;
  animation-duration: 16s;
}

@keyframes float1 {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-30px) rotate(5deg); }
}

@keyframes float2 {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-40px) rotate(-5deg); }
}

@keyframes float3 {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(30px) rotate(8deg); }
}

@keyframes float4 {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(40px) rotate(-8deg); }
}

/* 关于我们部分 */
.about-section {
  padding: 5rem 2rem;
  background-color: white;
  scroll-margin-top: 80px;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 3rem;
  position: relative;
}

.section-title::after {
  content: '';
  display: block;
  width: 80px;
  height: 4px;
  background-color: #3498db;
  margin: 1rem auto;
  border-radius: 2px;
}

.about-content {
  display: flex;
  flex-wrap: wrap;
  gap: 3rem;
  justify-content: center;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.about-text {
  flex: 1;
  min-width: 300px;
  max-width: 600px;
}

.about-image {
  flex: 1;
  min-width: 300px;
  max-width: 500px;
}

.about-image img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

h3 {
  color: #2c3e50;
  font-size: 1.8rem;
  margin-top: 2rem;
  margin-bottom: 1.5rem;
}

ul {
  padding-left: 1.5rem;
  list-style-type: none;
}

li {
  margin-bottom: 1rem;
  position: relative;
  padding-left: 2rem;
  font-size: 1.1rem;
  color: #34495e;
}

li i {
  position: absolute;
  left: 0;
  top: 0.2rem;
  color: #3498db;
}

/* 团队部分 */
.team-section {
  max-width: 1200px;
  margin: 4rem auto;
  text-align: center;
}

.team-members {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
}

.member {
  flex: 1;
  min-width: 200px;
  max-width: 250px;
  background-color: #f8f9fa;
  padding: 2rem 1.5rem;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  transition: transform 0.3s, box-shadow 0.3s;
}

.member:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.member img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1.5rem;
  border: 3px solid #3498db;
}

.member h4 {
  margin: 0.5rem 0;
  color: #2c3e50;
}

.member p {
  color: #7f8c8d;
  margin: 0;
}

/* 联系部分 */
.contact-section {
  max-width: 800px;
  margin: 4rem auto;
  text-align: center;
}

.contact-methods {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
}

.contact-method {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 1rem 2rem;
  background-color: #f8f9fa;
  border-radius: 50px;
  transition: all 0.3s;
}

.contact-method:hover {
  background-color: #e9f5ff;
  transform: translateY(-3px);
}

.contact-method i {
  font-size: 1.5rem;
  color: #3498db;
}

.contact-method span {
  font-size: 1.1rem;
  color: #34495e;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    padding: 1rem;
  }
  
  .navbar-left, .navbar-right {
    width: 100%;
    justify-content: center;
  }
  
  .navbar-right {
    margin-top: 1rem;
  }
  
  .slogan {
    font-size: 2.2rem;
  }
  
  .sub-slogan {
    font-size: 1.3rem;
  }
  
  .about-content {
    flex-direction: column;
  }
  
  .book {
    width: 60px;
  }
}

@media (max-width: 480px) {
  .slogan {
    font-size: 1.8rem;
  }
  
  .sub-slogan {
    font-size: 1.1rem;
  }
  
  .start-button {
    padding: 0.8rem 2rem;
    font-size: 1.1rem;
  }
  
  .book {
    width: 50px;
  }
}
</style>