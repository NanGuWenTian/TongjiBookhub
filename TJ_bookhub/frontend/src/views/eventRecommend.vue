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
        <!-- <div class="section-header">
          <h2>特色推荐活动</h2>
        </div> -->
        
        <div class="carousel-container">
          <carouselPart :items="featuredEvents" @item-click="navigateToEventDetail" />
        </div>
      </section>
      
      <!-- 活动搜索和筛选 -->
      <section class="event-filter">
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜索活动..." 
            @submit="searchEvents"
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
      
      <!-- 所有活动列表 -->
      <section class="all-events">
        <div class="section-header">
          <!-- <h2>所有活动</h2> -->
        </div>
        
        <div class="event-grid">
          <eventCard 
            v-for="event in filteredEvents" 
            :key="event.id" 
            :event="event" 
            @click="navigateToEventDetail(event.id)"
          />
        </div>
      </section>
      
      <section class="class-events">
        <div class="section-header">
          <h2>热门活动</h2>
        </div>
        <div class="class-events-container">
          <pictureWall 
            :items="classEvents" 
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
  import { ref, computed } from 'vue';
  import carouselPart from '@/components/carouselPart.vue';
  import eventCard from '@/components/eventCard.vue';
  import pictureWall from '@/components/pictureWall.vue';

  // 特色活动数据，作为模拟，这里暂时没用
  const featuredEvents = ref([
    {
      id: 1,
      title: '古籍修复技艺展示',
      url: '@/assets/event_1.jpg',
      date: '2023-06-15',
      location: '图书馆一楼大厅',
      description: '邀请国家级古籍修复专家现场展示古籍修复技艺'
    },
    {
      id: 2,
      title: '国学经典诵读会',
      url: '@/assets/event_2.jpg',
      date: '2023-06-22',
      location: '图书馆三楼报告厅',
      description: '与国学大师一起诵读经典，领悟传统文化精髓'
    },
    {
      id: 3,
      title: '古籍修复技艺展示',
      type: '传统文化',
      date: '2023-06-15',
      location: '图书馆一楼大厅',
      brief: '国家级古籍修复专家现场展示'
    },
    {
      id: 4,
      title: '数字资源使用讲座',
      type: '技术培训',
      date: '2023-06-29',
      location: '图书馆电子阅览室',
      brief: '学习如何高效利用图书馆数字资源'
    }
  ]);

  const allEvents = ref([
    {
      id: 1,
      title: '古籍修复技艺展示',
      type: '传统文化',
      url: "https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_10.png",
      date: '2023-06-15',
      location: '图书馆一楼大厅',
      brief: '国家级古籍修复专家现场展示'
    },
    {
      id: 2,
      title: '古籍修复技艺展示',
      type: '艺术展览',
      url:"https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_9.jpg",
      date: '2023-06-15',
      location: '图书馆一楼大厅',
      brief: '国家级古籍修复专家现场展示'
    },
    {
      id: 3,
      title: '古籍修复技艺展示',
      type: '技术讲座',
      url:"https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_4.jpg",
      date: '2023-06-15',
      location: '图书馆一楼大厅',
      brief: '国家级古籍修复专家现场展示'
    },
    {
      id: 4,
      title: '数字资源使用讲座',
      type: '创新实践',
      url:"https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_3.jpg",
      date: '2023-06-29',
      location: '图书馆电子阅览室',
      brief: '学习如何高效利用图书馆数字资源'
    },
    {
      id: 5,
      title: '古籍修复技艺展示',
      type: '技术讲座',
      url:"https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_4.jpg",
      date: '2023-06-15',
      location: '图书馆一楼大厅',
      brief: '国家级古籍修复专家现场展示'
    },
    {
      id: 6,
      title: '数字资源使用讲座',
      type: '创新实践',
      url:"https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_3.jpg",
      date: '2023-06-29',
      location: '图书馆电子阅览室',
      brief: '学习如何高效利用图书馆数字资源'
    },
    {
      id: 7,
      title: '古籍修复技艺展示',
      type: '传统文化',
      url: "https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_10.png",
      date: '2023-06-15',
      location: '图书馆一楼大厅',
      brief: '国家级古籍修复专家现场展示'
    },
    {
      id: 8,
      title: '古籍修复技艺展示',
      type: '艺术展览',
      url:"https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_9.jpg",
      date: '2023-06-15',
      location: '图书馆一楼大厅',
      brief: '国家级古籍修复专家现场展示'
    }
  ]);

  const eventCategories = ref([
    { id: 0, name: '所有类别' },
    { id: 1, name: '传统文化' },
    { id: 2, name: '艺术展览' },
    { id: 3, name: '技术讲座' },
    { id: 4, name: '创新实践' }
  ]);

  const pastEvents = ref([
    {
      id: 101,
      title: '春季读书月开幕式',
      organizer: '图书馆阅读推广部',
      theme: '书香满园',
      date: '2023-03-01',
      participants: 120,
      evaluations: [
        { user: '张同学', comment: '活动组织得很好，收获很大！' },
        { user: '李老师', comment: '希望多举办类似活动' }
      ]
    }
  ]);

  // 搜索和筛选功能
  const searchQuery = ref('');
  const selectedCategory = ref(0);

  const filteredEvents = computed(() => {
    return allEvents.value.filter(event => {
      // const matchesSearch = event.title.toLowerCase().includes(searchQuery.value.toLowerCase()) && searchQuery.value;
      const matchesCategory = !selectedCategory.value || event.type ===eventCategories.value[selectedCategory.value].name;
      return matchesCategory;
    });
  });

  //实现搜索功能
  const searchEvents =()=>{
    console.log('您已点击了提交了搜索内容');
    console.log(searchQuery.value);
  }

  //实现筛选功能
  const filterEvents =()=>{
    console.log('您已点击了筛选,当前类别为');
    console.log(selectedCategory.value);
  }
  //实现页面跳转
  const navigateToEventDetail = (eventId) => {
    console.log('您已点击了活动卡片');
    console.log(eventId);
  }
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