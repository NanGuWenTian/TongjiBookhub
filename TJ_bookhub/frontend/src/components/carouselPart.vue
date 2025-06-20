<template>
  <div class="carousel">
    <div class="carousel-inner" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
      <div 
        v-for="item in events" 
        :key="item.id" 
        class="carousel-item"
        @click="handleClick(item.id)"
      >
        <img :src="item.url" :alt="item.title" class="carousel-image">
        <!-- <div class="carousel-caption">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <div class="event-meta">
            <span class="date">{{ item.date }}</span>
            <span class="location">{{ item.location }}</span>
          </div>
        </div> -->
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
        v-for="item in events" 
        :key="item.id" 
        :class="{ active: currentIndex === item.id-1 }"
        @click="goTo(item.id - 1)"
      ></button>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
  // const props = defineProps({
  //   events: {
  //     type: Array,
  //     default: () => [
  //       {
  //         id: 1,
  //         title: '默认活动1',
  //         url: 'https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_1.jpg',
  //         date: '2023-01-01',
  //         location: '图书馆大厅',
  //         description: '默认活动描述1'
  //       },
  //       {
  //         id: 2,
  //         title: '默认活动2',
  //         url: 'https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_2.jpg',
  //         date: '2023-01-02',
  //         location: '体育馆',
  //         description: '默认活动描述2'
  //       },
  //       {
  //         id: 3,
  //         title: '默认活动3',
  //         url: 'https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_3.jpg',
  //         date: '2023-01-03',
  //         location: '学生活动中心',
  //         description: '默认活动描述3'
  //       }
  //     ]
  //   }
  // });

  const events = ref([
  {
          id: 1,
          title: '默认活动1',
          url: 'https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_12.jpg',
          date: '2023-01-01',
          location: '图书馆大厅',
          description: '默认活动描述1'
        },
        {
          id: 2,
          title: '默认活动2',
          url: 'https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_13.jpg',
          date: '2023-01-02',
          location: '体育馆',
          description: '默认活动描述2'
        },
        {
          id: 3,
          title: '默认活动3',
          url: 'https://mp-db1971d7-59f6-422b-8fad-4b97767e2fbd.cdn.bspapp.com/staticEvent/event_3.jpg',
          date: '2023-01-03',
          location: '学生活动中心',
          description: '默认活动描述3'
        }
  ])
  const handleClick = (event_id)=>{
    console.log("您已点击活动卡片");
    console.log(event_id);
  }

  const currentIndex = ref(0);
  // let autoPlayInterval;

  const next = () => {
    currentIndex.value = (currentIndex.value + 1) % events.value.length;
  };

  const prev = () => {
    currentIndex.value = (currentIndex.value - 1 + events.value.length) % events.value.length;
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
          filter: brightness(0.7);
        }

        .carousel-caption {
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          padding: 2rem;
          color: white;
          // background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);

          h3 {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
          }

          p {
            margin-bottom: 1rem;
          }

          .event-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.9rem;
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