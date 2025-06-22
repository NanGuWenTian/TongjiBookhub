<template>
  <div class="image-wall-container">
    <div 
      v-for="(item, index) in items" 
      :key="index"
      class="image-item"
      :class="{ 'active': activeIndex === index }"
      @mouseenter="handleMouseEnter(index)"
      @mouseleave="handleMouseLeave"
      @click="handleClick(item.id)"
    >
      <div class="image-wrapper">
        <img :src="item.image" :alt="item.title" class="wall-image">
      </div>
      <div class="image-caption">{{ item.title }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';

const props = defineProps({
  items: {
      type: Array,
      default: () => ([
        {
          "id":1,
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
      ])
    }
});
console.log("下面是图片墙所接受到的数据");
console.log(props.items);
const activeIndex = ref(0);

const handleMouseEnter = (index) => {
  activeIndex.value = index;
};

const handleMouseLeave = () => {
  // 保持效果不恢复
};

const handleClick = (url) => {
  window.open(url, '_blank');
};
</script>

<style lang="scss" scoped>
.image-wall-container {
  // background-color: #f8f9fa;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* 自适应列布局 */
  gap: 30px;
  max-width: 1440px;
  margin: 60px auto;
  padding: 20px;
  box-sizing: border-box;
  min-height: 500px; /* 固定最小高度 */

  .image-item {
    margin-bottom: 20px;
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.18); /* 基础阴影 */
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* 弹性过渡 */
    display: flex;
    flex-direction: column;
    height: 100%; // 确保项目填充网格单元格
    
    &:hover {
      z-index: 10;
    }

    &.active {
      transform: scale(1.08); /* 放大效果 */
      box-shadow: 0 8px 24px rgba(0,0,0,0.15); /* 增强阴影 */
    }

    .image-wrapper {
      width: 100%;
      aspect-ratio: 3/4; /* 固定3:4比例 */
      position: relative;
      background-color: aqua;
      .wall-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: top; /* 顶部对齐 */
        transition: transform 0.3s ease;
        
        &:hover, &.active {
          transform: scale(1.03);
        }
      }
    }

    .image-caption {
      padding: 15px 20px;
      text-align: center;
      font-size: 1.25rem;
      font-weight: 600;
      color: #333;
      background: rgba(255,255,255,0.9); /* 半透明背景 */
      backdrop-filter: blur(8px); /* 毛玻璃效果 */
      transition: all 0.3s ease;
      flex-shrink: 0; // 防止标题被压缩
    }
  }
}

// 为图片容器设置固定高度，确保所有图片在不放大时高度统一
.image-wall-container .image-item {
  height: 450px; // 设置统一高度
}

.image-wall-container .image-wrapper {
  height: calc(100% - 60px); // 减去标题高度
}

// 响应式布局
@media (max-width: 1024px) {
  .image-wall-container {
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin: 40px auto;
  }
  
  .image-wall-container .image-item {
    height: 400px; // 调整小屏幕上的高度
  }
}

@media (max-width: 768px) {
  .image-wall-container {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .image-wall-container .image-item {
    height: auto; // 在移动设备上恢复自适应高度
  }
  
  .image-wall-container .image-wrapper {
    height: auto;
    aspect-ratio: 3/4;
  }
}
</style>