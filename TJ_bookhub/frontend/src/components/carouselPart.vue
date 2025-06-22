<template>
  <div class="carousel">
    <div class="carousel-inner" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
      <div 
        v-for="item in events" 
        :key="item.id" 
        class="carousel-item"
        @click="handleClick(item.id)"
      >
        <img :src="item.image" :alt="item.title" class="carousel-image">
        <div class="carousel-caption">
          <h3>{{ item.title }}</h3>
          <p>{{ item.brief }}</p>
          <div class="event-meta">
            <span>{{ item.start_time }} - {{ item.end_time }}</span>
            <span>{{ item.location }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <button class="carousel-control prev" @click="prev">
      &lt;
    </button>
    <button class="carousel-control next" @click="next">
      &gt;
    </button>
    
    <div class="carousel-indicators">
      <button 
        v-for="(item,index) in events" 
        :key="item.id" 
        :class="{ active: currentIndex === index }"
        @click="goTo(index)"
      ></button>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted, defineProps } from 'vue';
  const { events } = defineProps({
    events: {
      type: Array,
      default: () => ([
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
      ])
    }
  });

  const handleClick = (event_id) => {
    console.log("您已点击活动卡片");
    console.log(event_id);
  }

  const currentIndex = ref(0);
  // let autoPlayInterval;

  const next = () => {
    currentIndex.value = (currentIndex.value + 1) % events.length;
  };

  const prev = () => {
    currentIndex.value = (currentIndex.value - 1 + events.length) % events.length;
  };

  const goTo = (index) => {
    currentIndex.value = index;
  };

  // 如果需要自动播放，可以取消下面的注释
  // const startAutoPlay = () => {
  //   autoPlayInterval = setInterval(next, 5000);
  // };

  onMounted(() => {
    // startAutoPlay();
    // return () => clearInterval(autoPlayInterval);
  });

</script>
<style scoped lang="scss">
  .carousel {
    position: relative;
    width: 100%;
    height: 540px;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);

    .carousel-inner {
      display: flex;
      height: 100%;
      transition: transform 0.5s ease;

      .carousel-item {
        min-width: 100%;
        position: relative;
        cursor: pointer;

        .carousel-image {
          width: 100%;
          height: 100%;
          object-fit: cover;
          filter: brightness(0.6);
        }

        .carousel-caption {
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          padding: 2rem;
          color: white;
          background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);

          h3 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
          }

          p {
            margin-bottom: 1rem;
            font-size: 1.1rem;
            line-height: 1.4;
          }

          .event-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.9rem;
            opacity: 0.8;
          }
        }
      }
    }

    .carousel-control {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background: rgba(255, 255, 255, 0.3);
      border: none;
      color: white;
      font-size: 1.5rem;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;

      &:hover {
        background: rgba(255, 255, 255, 0.5);
      }

      &.prev {
        left: 1rem;
      }

      &.next {
        right: 1rem;
      }
    }

    .carousel-indicators {
      position: absolute;
      bottom: 1rem;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 0.5rem;

      button {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        border: none;
        background: rgba(255, 255, 255, 0.5);
        cursor: pointer;
        padding: 0;

        &.active {
          background: white;
        }
      }
    }
  }
</style>