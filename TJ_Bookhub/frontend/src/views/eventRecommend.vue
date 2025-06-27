<template>
  <div class="event-recommendation-view">
    <!-- 特色活动轮播 -->
    <section class="featured-events"> 
        <div class="page-header">
          <h1>图书馆活动推荐</h1>
        </div>   
      <div class="carousel-container">
        <carouselPart :events="featuredEvents" @item-click="navigateToEventDetail" />
      </div>
    </section>
    
    <!-- 活动搜索区域 -->
    <section class="all-events">
      <div class="section-header">
        <h2>活动搜索</h2>
      </div>
      
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
      
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
        <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
        <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
      </div>
    </section>
    
    <!-- 热门活动 -->
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

    <!-- 往期活动回顾 - 美化后的布局 -->
    <section class="past-events">
      <div class="section-header">
        <h2>往期活动回顾</h2>
      </div>
      
      <div class="past-events-container">
        <div 
          v-for="event in pastEvents" 
          :key="event.id" 
          class="past-event-card"
        >
          <div class="event-details">
            <div class="event-header">
              <h3>{{ event.title }}</h3>
              <div class="event-meta">
                <span><i class="icon-calendar"></i> {{ event.date }}</span>
                <span><i class="icon-users"></i> {{ event.participants }}人参与</span>
              </div>
            </div>
            
            <div class="event-content">
              <p><strong>主办方：</strong>{{ event.organizer }}</p>
              <p><strong>主题：</strong>{{ event.theme }}</p>
            </div>
          </div>
          
          <div class="event-feedback">
            <h4>读者反馈</h4>
            <div class="feedback-container">
              <div 
                v-for="(item, idx) in event.evaluations" 
                :key="idx" 
                class="feedback-item"
              >
                <div class="user-avatar">
                  <span>{{ item.user.charAt(0) }}</span>
                </div>
                <div class="feedback-content">
                  <strong>{{ item.user }}：</strong>
                  <p>"{{ item.comment }}"</p>
                </div>
              </div>
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

  const featuredEvents = ref([]);
  const allEvents = ref([]);
  const hotedEvents = ref([]);

  const eventCategories = ref([]);
  const pastEvents = ref([]);

  // 搜索和筛选功能
  const searchQuery = ref();
  const selectedCategory = ref(0);

  // 分页相关状态
  const currentPage = ref(1);
  const perPage = ref(6);
  const totalPages = ref(1);

  const filteredEvents = computed(() => {
      return allEvents.value;
  });

  //const 获取活动种类
  const fetchEventCategories = async () => { 
    try{
      const response = await axios.get('/api/event_category');
      //先初始化
      eventCategories.value = [{ id: 0, name: '所有类别' }];
      response.data.forEach((category) => {
        eventCategories.value.push(category);
      });

      // 下面是测试信息
      console.log('活动种类列表：', eventCategories.value); 
    } catch (error) {
      console.error('获取活动种类列表时出错：', error);
    }
  };
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

  //获取过去活动
  const getPastEvents = async() =>{
    try {
      const response = await axios.get('/api/event_participation_record/get_past_events',{
        params:{
          event_ids: "[1,2]"
        }
      });
      pastEvents.value = response.data;

      // 下面是测试信息
      console.log('获取过去活动成功,信息如下');
      console.log(pastEvents.value);
    }
    catch(error){
      console.error('获取过去活动失败:', error);
    }
  } 

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
    fetchEventCategories();
    fetchEvents();
    getFeaturedEvents();
    getHotEvents();
    getPastEvents();
    console.log("往期活动数据已加载完毕，具体数据如下：");
    console.log(pastEvents.value);

  });
</script>
  
<style scoped lang="scss">
.event-recommendation-view {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem;
  font-family: 'Noto Sans SC', 'PingFang SC', sans-serif;
  color: #2c3e50;
  background-color: #f5f9ff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(74, 137, 220, 0.1);

  .page-header {
    text-align: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #e6f0fd;
    
    h1 {
      font-size: 2rem;
      font-weight: 600;
      color: #2c3e50;
      margin: 0;
      background: linear-gradient(135deg, #4a89dc 0%, #3b7dd8 100%);
      background-clip: text; 
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }

  .section-header {
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #e6f0fd;
    
    h2 {
      font-size: 1.5rem;
      font-weight: 600;
      color: #4a89dc;
      margin: 0;
    }
  }

  .featured-events,
  .all-events,
  .class-events,
  .past-events {
    background-color: #fff;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 12px rgba(74, 137, 220, 0.1);
    border: 1px solid #e6f0fd;
  }

  .carousel-container {
    margin: 0 auto;
    max-width: 1000px;
  }

  .event-filter {
    margin-bottom: 1.5rem;
  }

  .search-box {
    display: flex;
    gap: 1rem;
    max-width: 1200px;
    margin: 0 auto;

    input {
      flex: 1;
      padding: 0.6rem 1rem;
      border: 1px solid #e6f0fd;
      border-radius: 6px;
      font-size: 0.95rem;
      transition: all 0.3s ease;
      background-color: #f5f9ff;
      
      &:focus {
        outline: none;
        border-color: #4a89dc;
        box-shadow: 0 0 0 2px rgba(74, 137, 220, 0.1);
      }
    }

    select {
      padding: 0.6rem;
      border: 1px solid #e6f0fd;
      border-radius: 6px;
      font-size: 0.95rem;
      background-color: #f5f9ff;
      transition: all 0.3s ease;
      min-width: 150px;
      
      &:focus {
        outline: none;
        border-color: #4a89dc;
      }
    }
  }

  .event-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.2rem;
    margin-bottom: 1.5rem;
  }
  
  .pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.8rem;
    margin-top: 1.5rem;
    
    button {
      padding: 0.5rem 1rem;
      background-color: #4a89dc;
      color: white;
      border: none;
      border-radius: 6px;
      font-size: 0.9rem;
      cursor: pointer;
      transition: all 0.3s ease;
      box-shadow: 0 2px 6px rgba(74, 137, 220, 0.2);
      
      &:hover:not(:disabled) {
        background-color: #3b7dd8;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(74, 137, 220, 0.3);
      }
      
      &:disabled {
        background-color: #b8c2cc;
        cursor: not-allowed;
        box-shadow: none;
      }
    }
    
    span {
      font-size: 0.9rem;
      color: #5d6d7e;
    }
  }

  /* 往期活动回顾样式 */
  .past-events-container {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .past-event-card {
    display: flex;
    flex-direction: column;
    background: linear-gradient(to bottom, #f5f9ff, #e6f0fd);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(74, 137, 220, 0.1);
    transition: all 0.3s ease;
    border: 1px solid #e6f0fd;
    
    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 6px 16px rgba(74, 137, 220, 0.15);
    }
  }

  .event-details {
    padding: 1.2rem;
    border-bottom: 1px dashed #d4e1f8;
  }

  .event-header {
    margin-bottom: 0.8rem;
    
    h3 {
      color: #4a89dc;
      margin: 0 0 0.5rem;
      font-size: 1.2rem;
      font-weight: 600;
    }
    
    .event-meta {
      display: flex;
      gap: 1rem;
      color: #8ba3c7;
      font-size: 0.85rem;
      
      span {
        display: flex;
        align-items: center;
        
        i {
          margin-right: 0.3rem;
          font-size: 0.9rem;
        }
      }
    }
  }

  .event-content {
    p {
      margin: 0.5rem 0;
      font-size: 0.95rem;
      line-height: 1.5;
      color: #5d6d7e;
      
      strong {
        color: #4a89dc;
        font-weight: 500;
      }
    }
  }

  .event-feedback {
    padding: 1.2rem;
    
    h4 {
      color: #4a89dc;
      margin: 0 0 1rem;
      font-size: 1.1rem;
      font-weight: 600;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid #e6f0fd;
    }
  }

  .feedback-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
  }

  .feedback-item {
    display: flex;
    gap: 0.8rem;
    padding: 0.8rem;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(74, 137, 220, 0.1);
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-3px);
      box-shadow: 0 4px 10px rgba(74, 137, 220, 0.15);
    }
  }

  .user-avatar {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: #4a89dc;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.95rem;
  }

  .feedback-content {
    flex: 1;
    
    strong {
      color: #3b7dd8;
      font-weight: 500;
      font-size: 0.95rem;
    }
    
    p {
      margin: 0.3rem 0 0;
      font-style: italic;
      color: #5d6d7e;
      font-size: 0.9rem;
      line-height: 1.4;
    }
  }

  .class-events-container {
    margin-top: 1rem;
  }

  /* 响应式设计 */
  @media (max-width: 768px) {
    .event-recommendation-view {
      width: 95%;
      padding: 1rem;
    }
    
    .search-box {
      flex-direction: column;
      gap: 0.8rem;
      
      select {
        width: 100%;
      }
    }
    
    .event-grid {
      grid-template-columns: 1fr;
    }
    
    .pagination {
      flex-wrap: wrap;
    }
    
    .feedback-container {
      grid-template-columns: 1fr;
    }
    
    .page-header h1 {
      font-size: 1.8rem;
    }
    
    .section-header h2 {
      font-size: 1.3rem;
    }
  }
}
</style>