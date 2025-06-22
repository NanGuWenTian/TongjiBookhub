<template>
    <div class="event-recommendation-view">
      <!-- 顶部导航栏 -->
      <nav class="top-nav">
        <router-link to="/" >书籍借阅统计</router-link>
        <router-link to="/event" class="active">活动推荐</router-link>
      </nav>
      
      <!-- 页面标题 -->
      <div class="page-header">
        <h1>图书馆活动推荐</h1>
      </div>
      
      <!-- 特色活动轮播 -->
      <section class="featured-events">     
        <div class="carousel-container">
          <carouselPart :events="featuredEvents" @item-click="navigateToEventDetail" />
        </div>
      </section>
      
      <!-- 活动搜索和筛选
      <section class="event-filter">
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜索活动..." 
            @keyup.enter="searchEvents"
          >
          <select v-model="selectedCategory" @change="filterEvents">
            <option 
              v-for="category in eventCategories" 
              :key="category.id" 
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>
      </section> -->
      
       <section class="all-events">
          <div class="section-header">
            <h2>活动搜索</h2>
          </div>
          <!-- 活动搜索和筛选 -->

          <section class="event-filter">
            <div class="search-box">
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="搜索活动..." 
                @keyup.enter="searchEvents"
              >
              <select v-model="selectedCategory" @change="filterEvents">
                <option 
                  v-for="category in eventCategories" 
                  :key="category.id" 
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
        </div>
      </section>


          <div class="event-grid">
              <eventCard 
                  v-for="event in filteredEvents" 
                  :key="event.id" 
                  :event="event" 
                  @click="navigateToEventDetail(event.id)"
              />
          </div>
          <!-- 添加分页按钮 -->
          <div class="pagination">
              <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
              <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
              <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
          </div>
        </section>
      
      <section class="class-events">
        <div class="section-header">
          <h2>热门活动</h2>
        </div>
        <div class="class-events-container">
          <pictureWall 
            :items="hotedEvents" 
          />
        </div>
      </section>

      <!-- 往期活动回顾 -->
      <section class="past-events">
        <div class="section-header">
          <h2>往期活动回顾</h2>
        </div>
        
        <div class="past-events-container">
          <div class="past-events-details">
            <div v-for="event in pastEvents" :key="event.id" class="past-event-item">
              <h3>{{ event.title }}</h3>
              <p><strong>主办方:</strong> {{ event.organizer }}</p>
              <p><strong>主题:</strong> {{ event.theme }}</p>
              <p><strong>时间:</strong> {{ event.date }}</p>
              <p><strong>参与人数:</strong> {{ event.participants }}</p>
            </div>
          </div>
          
          <div class="past-events-feedback">
            <div v-for="event in pastEvents" :key="event.id" class="feedback-item">
              <h3>{{ event.title }} - 读者反馈</h3>
              <div v-for="(item, idx) in event.evaluations" :key="idx" class="evaluation">
                <p class="user">{{ item.user }}:</p>
                <p class="comment">"{{ item.comment }}"</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
<script setup>
  import { ref, computed,onMounted} from 'vue';
  import axios from 'axios';
  import carouselPart from '@/components/carouselPart.vue';
  import eventCard from '@/components/eventCard.vue';
  import pictureWall from '@/components/pictureWall.vue';

  // 特色活动数据，作为模拟，这里暂时没用
  const featuredEvents = ref([]);
  const allEvents = ref([]);
  const hotedEvents = ref([]);

  const eventCategories = ref([
      { id: 0, name: '所有类别' },
      { id: 1, name: '书香雅集' },
      { id: 2, name: '传统文化' },
      { id: 3, name: '艺术展览' },
      { id: 4, name: '创新实践' },
      { id: 5, name: '艺术展览' }
  ]);
  const pastEvents = ref([]);

  // 搜索和筛选功能
  const searchQuery = ref();
  const selectedCategory = ref(0);

  // 分页相关状态
  const currentPage = ref(1);
  const perPage = ref(8);
  const totalPages = ref(1);

  const filteredEvents = computed(() => {
      return allEvents.value;
  });

  // 获取活动列表
  const fetchEvents = async () => {
      try {
          const response = await axios.get('/api/events', {
              params: {
                  title: searchQuery.value,
                  type_id: selectedCategory.value === 0 ? null : selectedCategory.value,
                  page: currentPage.value,
                  per_page: perPage.value
              }
          });
          allEvents.value = response.data.event_items;
          totalPages.value = response.data.pages;

          // 下面是测试信息
          console.log('获取活动列表成功,信息如下');
          console.log(allEvents.value);
      } catch (error) {
          console.error('获取活动列表失败:', error);
      }
  };

  //获取特色活动-轮播图部分
  const getFeaturedEvents = async () => { 
      try {
          const response = await axios.get('/api/events', {
              params: {
                  is_featured:'true'
              }
          });
          featuredEvents.value = response.data.event_items;

          // 下面是测试信息
          console.log('获取特色活动成功,信息如下');
          console.log(featuredEvents.value);
      }
      catch (error) {
          console.error('获取特色活动失败:', error);
      }
  };

  // 获取热门活动
  const getHotEvents = async () => { 
    try{
      const response = await axios.get('/api/events/hot_events');
      hotedEvents.value = response.data.hot_events;

      // 下面是测试信息
      console.log('获取热门活动成功,信息如下');
      console.log(hotedEvents.value);
    }
    catch(error){
      console.error('获取热门活动失败:', error);
    }
  };
  //实现搜索功能
  const searchEvents = async () => {
      console.log('您已点击了提交了搜索内容');
      console.log(searchQuery.value);
      currentPage.value = 1; // 搜索时重置页码
      await fetchEvents();
  };

  //实现筛选功能
  const filterEvents = async () => {
      console.log('您已点击了筛选,当前类别为');
      console.log(selectedCategory.value);
      currentPage.value = 1; // 筛选时重置页码
      await fetchEvents();
  };

  // 上一页
  const prevPage = async () => {
      if (currentPage.value > 1) {
          currentPage.value--;
          await fetchEvents();
      }
  };

  // 下一页
  const nextPage = async () => {
      if (currentPage.value < totalPages.value) {
          currentPage.value++;
          await fetchEvents();
      }
  };

  //实现页面跳转
  const navigateToEventDetail = (eventId) => {
      console.log('您已点击了活动卡片-组件外部');
      console.log(eventId);
  };

  onMounted(() => {
    fetchEvents();
    getFeaturedEvents();
    getHotEvents();
  });
</script>
  
  <style scoped lang="scss">
  .event-recommendation-view {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
    font-family: 'Noto Serif SC', serif;
    color: #3a3226;
    background-color: #f9f5eb;

    .top-nav {
      display: flex;
      justify-content: center;
      margin-bottom: 2rem;
      padding: 1rem 0;
      background-color: #8d6e63;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

      a {
        color: #f9f5eb;
        text-decoration: none;
        padding: 0.8rem 2rem;
        margin: 0 0.5rem;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        border-radius: 4px;
        font-weight: 500;

        &:hover {
          background-color: rgba(255, 255, 255, 0.2);
        }

        &.active {
          background-color: #5d4037;
        }
      }
    }

    .page-header {
      text-align: center;
      margin-bottom: 3rem;
      padding-bottom: 1.5rem;
      border-bottom: 1px solid #d4c9b8;

      h1 {
        font-size: 2.5rem;
        font-weight: 500;
        color: #5a4a3a;
        margin-bottom: 0.5rem;
      }
    }

    .subtitle {
      font-size: 1.2rem;
      color: #7a6b5a;
      font-style: italic;
    }

    .section-header {
      margin-bottom: 1.5rem;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid #d4c9b8;

      h2 {
        font-size: 1.8rem;
        font-weight: 500;
        color: #5a4a3a;
      }
    }

    .carousel-container {
      margin-bottom: 3rem;
    }

    .event-filter {
      margin-bottom: 2rem;
    }

    .search-box {
      display: flex;
      gap: 1rem;

      input {
        flex: 1;
        padding: 0.75rem;
        border: 1px solid #d4c9b8;
        border-radius: 4px;
        font-family: inherit;
      }

      select {
        padding: 0.75rem;
        border: 1px solid #d4c9b8;
        border-radius: 4px;
        font-family: inherit;
        background-color: #fff;
      }
    }

    .event-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1.5rem;
      margin-bottom: 3rem;
    }
    .pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
    }

    .past-events-container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
      background-color: #fff;
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      border: 1px solid #e0d8c8;

      .past-event-item {
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px dashed #d4c9b8;

        &:last-child {
          border-bottom: none;
        }

        h3 {
          color: #8d6e63;
          margin-bottom: 0.5rem;
        }

        p {
          margin: 0.25rem 0;
        }
      }

      .feedback-item {
        margin-bottom: 1.5rem;

        h3 {
          color: #8d6e63;
          margin-bottom: 0.5rem;
        }

        .evaluation {
          background-color: #f5efe6;
          padding: 1rem;
          border-radius: 4px;
          margin-bottom: 1rem;

          .user {
            font-weight: 500;
            margin: 0 0 0.25rem 0;
          }

          .comment {
            margin: 0;
            font-style: italic;
          }
        }
      }
    }
  }
  </style>