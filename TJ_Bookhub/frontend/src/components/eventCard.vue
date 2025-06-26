<template>
  <div class="event-card" @click="handleClick(event.id)">
    <div class="event-image">
      <img :src="event.image" :alt="event.title">
    </div>
    <div class="event-content">
      <div class="event-head">
        <h3>{{ event.title }}</h3>
        <span class="event-type">{{ event.category.name }}</span>
      </div>
      <div class="event-meta">
        <!-- <span class="event-date">{{ event.start_time }}-{{ event.end_time }}</span> -->
        <span class="event-date">
          {{ formatDateTime(event.start_time) }} - {{ formatDateTime(event.end_time) }}
        </span>
      </div>
      <p class="event-brief">{{ event.brief }}</p>
      <div class="event-location">
        <i class="icon">📍</i> {{ event.location }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { toRefs } from 'vue';

const props = defineProps({
  event: {
    type: Object,
    default: () => (
      {
          "title": "Test Event",
          "type_id": 1,
          "image": "test_image.jpg",
          "start_time": "2024-01-01T12:00:00",
          "end_time": "2024-01-02T12:00:00",
          "location": "Test Location",
          "brief": "Test brief",
          "organizer": "Test Organizer",
          "theme": "Test Theme",
          "is_featured": true
        }
  )
  }
});

const {event} = toRefs(props);
// 格式化日期时间的函数
const formatDateTime = (dateTime) => {
  const date = new Date(dateTime);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};
const handleClick = (id) => {
  console.log('点击了活动卡片，ID:', id);
  // 这里可以添加后续的点击处理逻辑
  // 但不再包含与数据库交互的代码
  console.log("所对应的活动信息如下：");
  console.log(event.value);
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
.event-head {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
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