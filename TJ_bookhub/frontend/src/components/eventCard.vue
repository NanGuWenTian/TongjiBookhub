<template>
  <div class="event-card" @click="handleClick(event.id)">
    <div class="event-image">
      <img :src="event.url || 'https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_10.png'" :alt="event.title">
    </div>
    <div class="event-content">
      <h3>{{ event.title }}</h3>
      <div class="event-meta">
        <span class="event-type">{{ event.type }}</span>
        <span class="event-date">{{ event.date }}</span>
      </div>
      <p class="event-brief">{{ event.brief }}</p>
      <div class="event-location">
        <i class="icon">📍</i> {{ event.location }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  event: {
    type: Object,
    default: () => ({
      id: 1,
      title: '默认活动',
      type: '讲座',
      date: '2023-01-01',
      brief: '这是一个默认活动描述，用于展示活动卡片的基本样式和功能。',
      location: '图书馆报告厅',
      image: './assets/event_1.jpg'
    })
  }
});

const handleClick = (id) => {
  console.log('点击了活动卡片，ID:', id);
  // 这里可以添加后续的点击处理逻辑
  // 但不再包含与数据库交互的代码
};  
</script>

<style scoped>
.event-card {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0d8c8;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.event-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.event-image {
  height: 180px;
  overflow: hidden;
}

.event-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.event-card:hover .event-image img {
  transform: scale(1.05);
}

.event-content {
  padding: 1.25rem;
}

.event-content h3 {
  margin: 0 0 0.5rem 0;
  color: #5a4a3a;
  font-size: 1.2rem;
}

.event-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  font-size: 0.85rem;
  color: #7a6b5a;
}

.event-type {
  background-color: #e8e0d0;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.event-brief {
  margin: 0.75rem 0;
  color: #5a4a3a;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.event-location {
  font-size: 0.9rem;
  color: #7a6b5a;
  margin-top: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
</style>