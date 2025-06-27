<template>
  <div class="carousel">
    <div class="carousel-inner" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
      <div 
        v-for="(item) in events" 
        :key="item.id" 
        class="carousel-item"
        @click="handleClick(item.id)"
      >
        <img :src="item.image" :alt="item.title" class="carousel-image">
        <div class="carousel-caption">
          <h3>{{ item.title }}</h3>
          <p>{{ item.brief }}</p>
          <div class="event-meta">
            <span>{{ formatDateTime(item.start_time) }} - {{ formatDateTime(item.end_time) }}</span>
            <span>{{ item.location }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <button class="carousel-control prev" @click="prev">
       <svg t="1750576636973" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5415" width="25" height="25">
        <path d="M298.456371 578.74104299L298.456371 678.80714199 398.519398 678.807142 398.519398 778.864947 498.583347 778.864947 498.583347 878.923878 598.647398 878.923878 598.647398 978.983731 798.780518 978.98373099 798.780518 878.923878 698.710426 878.923878 698.710426 778.864947 598.647398 778.864947 598.647398 678.807142 498.583347 678.807142 498.583347 578.741043 398.519398 578.741043 398.519398 478.68631 498.583347 478.68631 498.583347 378.620211 598.647398 378.620211 598.647398 278.562406 698.710426 278.562406 698.710426 178.502451 798.780518 178.502451 798.780518 78.443622 598.647398 78.443622 598.647398 178.502451 498.583347 178.502451 498.583347 278.562406 398.519398 278.562406 398.519398 378.620211 298.456371 378.620211 298.456371 478.68631 198.38423 478.68631 198.38423 578.74104299Z" p-id="5416">
        </path>
      </svg>
    </button>
    <button class="carousel-control next" @click="next">
       <svg t="1750576683348" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5573" width="25" height="25">
        <path d="M725.543629 445.258957 725.543629 345.192858 625.480602 345.192858 625.480602 245.135053 525.416653 245.135053 525.416653 145.076122 425.352602 145.076122 425.352602 45.016269 225.219482 45.016269 225.219482 145.076122 325.289574 145.076122 325.289574 245.135053 425.352602 245.135053 425.352602 345.192858 525.416653 345.192858 525.416653 445.258957 625.480602 445.258957 625.480602 545.31369 525.416653 545.31369 525.416653 645.379789 425.352602 645.379789 425.352602 745.437594 325.289574 745.437594 325.289574 845.497549 225.219482 845.497549 225.219482 945.556378 425.352602 945.556378 425.352602 845.497549 525.416653 845.497549 525.416653 745.437594 625.480602 745.437594 625.480602 645.379789 725.543629 645.379789 725.543629 545.31369 825.61577 545.31369 825.61577 445.258957Z" fill="#2c2c2c" p-id="5574">
       </path>
      </svg>
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
  import { ref, onMounted, toRefs} from 'vue';
  import {useRouter} from 'vue-router';
  const router = useRouter();
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

  // 这里是之前遇到的bug2：子组件中的对象，只有改成ref类，才能再刷新后重新获得数据！
  const props = defineProps({
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
  const {events} = toRefs(props);
  const handleClick = (event_id) => {
    // console.log("您已点击活动卡片");
    // console.log("当前活动卡片id");
    // console.log(event_id);
    // console.log("活动信息为");
    // console.log(events.value);

    // console.log("活动总数为");
    // console.log(events.value.length);
    // // console.log("之后会跳转到活动详情页面","活动id为",event_id)
    // console.log("您已点击活动卡片-组件内部");
    // console.log("活动id为",event_id)
    router.push({ name: 'eventDetail', params: { id: event_id } })
  }

  // 这里是活动数组中的下标
  const currentIndex = ref(0);

  const next = () => {
    currentIndex.value = (currentIndex.value +1) % events.value.length;
  };

  const prev = () => {
    currentIndex.value = (currentIndex.value -1 + events.value.length) % events.value.length;
  };

  const goTo = (index) => {
    currentIndex.value = index;
  };

  // 如果需要自动播放，可以取消下面的注释
  // const startAutoPlay = () => {
  //   autoPlayInterval = setInterval(next, 5000);
  // };

  onMounted(() => {
    console.log("组件接收到的信息是");
    console.log(events.value);
  });

</script>
<style scoped lang="scss">
  .carousel {
    position: relative;
    width: 100%;
    height: 450px;
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