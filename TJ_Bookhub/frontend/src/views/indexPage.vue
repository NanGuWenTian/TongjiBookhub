<template>
  <div class="library-homepage">
    <!-- 轮播图部分 -->
    <div class="carousel-section">
      <div class="carousel-container">
        <div 
          class="carousel-slide"
          v-for="(slide, index) in carouselSlides"
          :key="index"
          :class="{ active: currentSlide === index }"
        >
          <img :src="slide.image" :alt="slide.alt" class="carousel-image" />
          <div class="carousel-caption">
            <h2>{{ slide.title }}</h2>
            <p>{{ slide.description }}</p>
          </div>
        </div>
        
        <button class="carousel-control prev" @click="prevSlide">❮</button>
        <button class="carousel-control next" @click="nextSlide">❯</button>
        
        <div class="carousel-indicators">
          <span
            v-for="(slide, index) in carouselSlides"
            :key="index"
            :class="{ active: currentSlide === index }"
            @click="goToSlide(index)"
          ></span>
        </div>
      </div>
    </div>

    <!-- 图书馆介绍部分 -->
    <section class="intro-section">
      <h2>关于我们</h2>
      <div class="intro-grid">
        <div class="intro-card" v-for="(item, index) in introItems" :key="index">
          <h3>{{ item.title }}</h3>
          <p>{{ item.content }}</p>
        </div>
      </div>
    </section>

    <!-- 服务时间部分 -->
    <section class="hours-section">
      <h2>开放时间</h2>
      <table>
        <thead>
          <tr>
            <th>星期</th>
            <th>开放时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(day, index) in openingHours" :key="index">
            <td>{{ day.day }}</td>
            <td>{{ day.hours }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- 友站链接部分 -->
    <footer class="footer-section">
      <h2>友情链接</h2>
      <div class="friend-links">
        <a 
          v-for="(link, index) in friendLinks" 
          :key="index" 
          :href="link.url" 
          target="_blank"
          class="friend-link"
        >
          {{ link.name }}
        </a>
      </div>
      <div class="copyright">
        &copy; {{ currentYear }} 图书馆版权所有
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

// 轮播图数据
const carouselSlides = ref([
  {
    image: new URL('@/assets/library1.jpg', import.meta.url).href,
    alt: "图书馆正门",
    title: "欢迎来到我们的图书馆",
    description: "知识的海洋，智慧的殿堂"
  },
  {
    image: new URL('@/assets/library2.jpg', import.meta.url).href,
    alt: "图书馆阅览室",
    title: "舒适的阅读环境",
    description: "为您提供安静优雅的阅读空间"
  },
  {
    image: new URL('@/assets/library3.jpg', import.meta.url).href,
    alt: "图书馆藏书区",
    title: "丰富的藏书资源",
    description: "超过50万册藏书任您选择"
  },
  {
    image: new URL('@/assets/library4.jpg', import.meta.url).href,
    alt: "图书馆数字区",
    title: "现代化数字资源",
    description: "电子图书、数据库一应俱全"
  }
]);

const currentSlide = ref(0);
let autoPlayInterval = null;

// 上一张幻灯片
const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + carouselSlides.value.length) % carouselSlides.value.length;
  resetAutoPlay();
};

// 下一张幻灯片
const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % carouselSlides.value.length;
  resetAutoPlay();
};

// 跳转到指定幻灯片
const goToSlide = (index) => {
  currentSlide.value = index;
  resetAutoPlay();
};

// 自动播放
const startAutoPlay = () => {
  autoPlayInterval = setInterval(() => {
    nextSlide();
  }, 5000);
};

// 重置自动播放
const resetAutoPlay = () => {
  clearInterval(autoPlayInterval);
  startAutoPlay();
};

// 组件挂载时开始自动播放
onMounted(() => {
  startAutoPlay();
});

// 组件卸载前清除定时器
onBeforeUnmount(() => {
  clearInterval(autoPlayInterval);
});

// 图书馆介绍项目
const introItems = ref([
  {
    title: "丰富的藏书",
    content: "我们拥有超过50万册藏书，涵盖文学、科学、艺术、历史等多个领域，满足您的各种阅读需求。"
  },
  {
    title: "舒适的环境",
    content: "图书馆提供宽敞明亮的阅读空间，配备舒适的座椅和充足的自然光线，为您创造理想的阅读环境。"
  },
  {
    title: "数字资源",
    content: "除了纸质书籍，我们还提供大量电子资源和数据库，让您随时随地获取知识。"
  },
  {
    title: "文化活动",
    content: "定期举办读书会、讲座和展览等文化活动，丰富读者的精神生活。"
  }
]);

// 开放时间
const openingHours = ref([
  { day: "周一至周五", hours: "8:30 - 21:00" },
  { day: "周六", hours: "9:00 - 20:00" },
  { day: "周日", hours: "9:00 - 17:00" },
  { day: "法定节假日", hours: "10:00 - 16:00" }
]);

// 友情链接
const friendLinks = ref([
  { name: "国家图书馆", url: "https://www.nlc.cn/" },
  { name: "中国图书馆学会", url: "https://www.lsc.org.cn/" },
  { name: "世界数字图书馆", url: "https://www.wdl.org/" },
  { name: "1系统", url: "https://www.1.tongji.edu.cn/" }
]);

// 当前年份计算
const currentYear = computed(() => new Date().getFullYear());
</script>

<style scoped>
.library-homepage {
  max-width: 1100px;
  width: 80%;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
  color: #333;
  padding-top: 20px;
}

/* 轮播图样式 */
.carousel-section {
  margin-bottom: 2rem;
}

.carousel-container {
  position: relative;
  width: 100%;
  height: 500px;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.carousel-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 1s ease-in-out;
}

.carousel-slide.active {
  opacity: 1;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-caption {
  position: absolute;
  bottom: 2rem;
  left: 2rem;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
  max-width: 50%;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 1rem;
  border-radius: 8px;
}

.carousel-caption h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.carousel-caption p {
  font-size: 1.2rem;
}

.carousel-control {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  padding: 1rem;
  font-size: 1.5rem;
  cursor: pointer;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
}

.carousel-control:hover {
  background-color: rgba(0, 0, 0, 0.8);
}

.carousel-control.prev {
  left: 1rem;
}

.carousel-control.next {
  right: 1rem;
}

.carousel-indicators {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;
}

.carousel-indicators span {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: background-color 0.3s;
}

.carousel-indicators span.active {
  background-color: white;
}

.carousel-indicators span:hover {
  background-color: rgba(255, 255, 255, 0.8);
}

/* 介绍部分样式 */
.intro-section {
  margin: 3rem 0;
  padding: 0 1rem;
}

.intro-section h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.intro-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.4rem;
}

.intro-card {
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.intro-card:hover {
  transform: translateY(-5px);
}

.intro-card h3 {
  color: #3498db;
  margin-bottom: 0.8rem;
}

/* 开放时间样式 */
.hours-section {
  margin: 3rem 0;
  padding: 0 1rem;
}

.hours-section h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 0 auto;
  max-width: 600px;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
}

tr:hover {
  background-color: #f5f5f5;
}

/* 页脚样式 */
.footer-section {
  background-color: #2c3e50;
  color: white;
  padding: 2rem 1rem;
  margin-top: 3rem;
  text-align: center;
}

.footer-section h2 {
  margin-bottom: 1.5rem;
}

.friend-links {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.friend-link {
  color: #3498db;
  text-decoration: none;
  transition: color 0.3s ease;
}

.friend-link:hover {
  color: #2980b9;
  text-decoration: underline;
}

.copyright {
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #bdc3c7;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .carousel-container {
    height: 350px;
  }
  
  .carousel-caption {
    max-width: 80%;
    bottom: 1rem;
    left: 1rem;
  }
  
  .carousel-caption h2 {
    font-size: 1.5rem;
  }
  
  .carousel-caption p {
    font-size: 1rem;
  }
  
  .carousel-control {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
    padding: 0.8rem;
  }
  
  .intro-grid {
    grid-template-columns: 1fr;
  }
}
</style>