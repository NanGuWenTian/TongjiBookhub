<template>
  <div class="event-detail-page">
  <!-- <backgroundCartoon></backgroundCartoon> -->
    <!-- 活动信息模块 -->
    <div class="event-info-container">
      <div class="event-info">
        <img :src="event.image || 'https://picsum.photos/400/300'" alt="活动图片" class="event-image">
        <div class="info-right">
          <div class="brief-info">
            <h2 class="event-title">{{ event.title }}</h2>
            <p><strong>主办方:</strong> {{ event.organizer }}</p>
            <p><strong>主题:</strong> {{ event.theme }}</p>
            <p><strong>简介:</strong> {{ event.brief }}</p>
            <p><strong>地点:</strong> {{ event.location }}</p>
            <p><strong>开始时间:</strong> {{ formatDateTime(event.start_time) }}</p>
            <p><strong>结束时间:</strong> {{ formatDateTime(event.end_time) }}</p>
          </div>

          <!-- 这里的按钮尚未处理 -->
          <div class="operation">
            <button v-if="!hasParticipated && !isPastEvent" @click="participateEvent" class="btn-participate">
              点击参加
            </button>
            <button v-if="hasParticipated " @click="openFeedbackModal" class="btn-evaluate">
              点击评价
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 评论信息模块 -->
    <div class="comments-container">
      <h3 class="section-title">评论信息</h3>
      <div class="comment-list-wrapper">
          <div class="comment-list" v-if="comments.length > 0">
            <!-- <div class="comment-item" v-for="(comment,index) in comments" :key="index">
              <div class="comment-content">{{ comment.comment }}</div>
              <div class="comment-user">{{ comment.username }}</div>
            </div> -->
            <div 
                v-for="(item, idx) in comments" 
                :key="idx" 
                class="feedback-item"
              >
                <div class="user-avatar">
                  <span>{{ item.username.charAt(0) }}</span>
                </div>
                <div class="feedback-content">
                  <strong>{{ item.username }}：</strong>
                  <p>"{{ item.comment }}"</p>
                </div>
              </div>
          </div>
          <div class="no-comments" v-else>
            暂无评论
          </div>
      </div>
    </div>

    <!-- 相关活动推荐模块 -->
    <div class="related-events-container">
      <h3 class="section-title">相关活动推荐</h3>
      <div class="event-wall">
        <div class="event-card" v-for="relatedEvent in relatedEvents" :key="relatedEvent.id">
          <img :src="relatedEvent.image || 'https://picsum.photos/200/150'" alt="相关活动图片">
          <h4>{{ relatedEvent.title }}</h4>
          <p>时间: {{ formatDate(relatedEvent.start_time) }}</p>
          <button @click="navigateToEvent(relatedEvent.id)">查看详情</button>
        </div>
      </div>
    </div>

    <!-- 评论模态框 -->
    <div class="feedback-modal" v-if="isModalOpen">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ modalTitle }}</h2>
          <span class="close-btn" @click="closeFeedbackModal">&times;</span>
        </div>
        <textarea v-model="feedbackText" rows="5" placeholder="请输入您的评价..."></textarea>
        <button @click="submitFeedback" class="btn-submit">提交</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import {useRoute,useRouter} from 'vue-router'
import axios from 'axios';
// 解决组件复用
import { watch } from 'vue';
// 获取路由参数
const route = useRoute()
const router = useRouter()

const eventId = ref(route.params.id)

// 页面数据
const event = ref({})
const comments = ref([])
const relatedEvents = ref([])

// 状态管理
const hasParticipated = ref(false)
const isModalOpen = ref(false)
const modalTitle = ref('评价活动')
const feedbackText = ref('')

// 计算属性：判断活动是否已结束
const isPastEvent = computed(() => {
  if (!event.value.end_time) return false
  return new Date(event.value.end_time) < new Date()
})

// 获取活动详情
const loadEventDetails = async () => {
  try {
    const response = await axios.get('/api/events', {
      params: {
        id: eventId.value
      }
    });
    event.value = response.data.event_items[0]
    console.log('获取活动详情开始,当前活动编号为', eventId.value)
    console.log('获取活动详情成功,信息如下')
    console.log(event.value)
  } catch (error) {
    console.error('获取活动详情失败:', error)
  }
}

// 获取活动评论
const loadEventComments = async () => {
  try {
    const response = await axios.get(`/api/event_participation_record/get_feedback_by_event`,{
      params: {
        event_id: eventId.value
      }
    })
    comments.value = response.data.data
    console.log('获取活动评论成功,信息如下')
    console.log(comments.value)
  } catch (error) {
    console.error('获取活动评论失败:', error)
  }
}

// 检查用户参与状态
const checkUserParticipation = async () => {
  try {
    // const userResponse = await axios.get('/api/current_user')
    // const userId = userResponse.data.id
    const userId = 1 // 后期合并再改

    if (userId) {
      const response = await axios.get(`/api/event_participation_record/get_one_person_one_event_record`,{
        params: {
          user_id: userId,
          event_id: eventId.value
        }
      })
      hasParticipated.value = response.data.state == "success"
      console.log("获取用户参与状态成功，用户参与状态数据为");
      console.log(hasParticipated.value)

      // 如果用户已参与且有反馈，加载反馈内容
      if (hasParticipated.value && response.data.feedback) {
        feedbackText.value = response.data.feedback
        console.log("获取当前用户反馈成功，反馈内容为")
        console.log(feedbackText.value)
      }
    }
    console.log('用户是否已参与活动:', hasParticipated.value)
  } catch (error) {
    console.error('检查用户参与状态失败:', error)
  }
}

// 获取相关活动
const loadRelatedEvents = async () => {
  try{
    const response = await axios.get('/api/events/get_related_events', {
      params: {
        event_id: eventId.value
      }
    });
    relatedEvents.value = response.data.related_events;
    console.log("相关活动已加载完毕，信息如下");
    console.log(relatedEvents.value);
  }catch(error) {
    console.error('获取相关活动失败:', error)
  }
}

// 方法：格式化日期时间
const formatDateTime = (dateTime) => {
  console.log(dateTime)
  if (!dateTime) return ''
  return new Date(dateTime).toLocaleString()
}

// 方法：格式化日期
const formatDate = (dateTime) => {
  if (!dateTime) return ''
  return new Date(dateTime).toLocaleDateString()
}

// 方法：参加活动
const participateEvent = async () => {
  console.log("当前活动是否已过期", isPastEvent.value)
  console.log("当前新增请求为：", eventId.value)
  try {
    // 修改1：将params改为data，正确传递请求体
    await axios.post('/api/event_participation_record', {
      user_id: 1, // 实际应用中应从会话中获取用户ID
      event_id: eventId.value
    })
    hasParticipated.value = true
    alert('参加活动成功！')
  } catch (error) {
    console.error('参加活动失败:', error)
    alert('参加活动失败，请重试')
  }
}

// 方法：打开反馈模态框
const openFeedbackModal = () => {
  
  console.log("当前活动是否已过期",isPastEvent.value)

  modalTitle.value = hasParticipated.value && feedbackText.value ? '修改评论' : '添加评论'
  isModalOpen.value = true
}

// 方法：关闭反馈模态框
const closeFeedbackModal = () => {
  isModalOpen.value = false
}

// 方法：提交反馈
// const submitFeedback = ()=>{
//   console.log('提交反馈')
// }
const submitFeedback = async () => {
  if (!feedbackText.value.trim()) {
    alert('评论内容不能为空')
    return
  }

  try {
    // // 检查是更新还是创建评论
    // if (hasParticipated.value && feedbackText.value) {
    //   // 更新现有评论
    //   const participationRecords = await axios.get(
    //     `/api/event_participation_records?event_id=${eventId.value}&user_id=1` // 实际应用中应从会话中获取用户ID
    //   )

    //   if (participationRecords.data.length > 0) {
    //     const recordId = participationRecords.data[0].id
    //     await axios.put(`/api/event_participation_records/${recordId}`, {
    //       feedback: feedbackText.value
    //     })
    //   }
    // } else {
    //   // 创建新评论
    //   await axios.post('/api/event_participation_records', {
    //     event_id: eventId.value,
    //     user_id: 1, // 实际应用中应从会话中获取用户ID
    //     feedback: feedbackText.value
    //   })
    // }

    // 更新评论列表
    
    const response = await axios.put('/api/event_participation_record/add_or_modify_feedback', {
      user_id: 1, // 实际应用中应从会话中获取用户ID
      event_id: eventId.value,
      feedback: feedbackText.value
    });
    console.log("评论信息已插入成功！，返回为",response)
    loadEventComments()

    hasParticipated.value = true
    isModalOpen.value = false
    alert('评论提交成功！')
  } catch (error) {
    console.error('提交评论失败:', error)
    alert('提交评论失败，请重试')
  }
}

// 方法：导航到其他活动
const navigateToEvent = (id)=>{
  router.push({ name: 'eventDetail', params: { id } })
}

watch(() => route.params.id, (newId) => {
  eventId.value = newId
  loadEventDetails()
  loadEventComments()
  loadRelatedEvents()
  checkUserParticipation()
});

// 生命周期钩子
onMounted(() => {
  console.log('活动详情页面加载开始,当前活动编号为', eventId.value)
  loadEventDetails()
  loadEventComments()
  loadRelatedEvents()
  checkUserParticipation()
})
</script>

<style lang="scss" scoped>
.event-detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;

  .event-info-container {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;

    .event-info {
      display: flex;
      gap: 20px;

      .event-image {
        width: 300px;
        height: auto;
        border-radius: 4px;
      }

      .info-right {
        flex: 1;

        .brief-info {
          margin-bottom: 20px;

          .event-title {
            margin-top: 0;
            color: #333;
          }

          p {
            margin: 8px 0;
            color: #666;
          }
        }

        .operation {
          button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;

            &:hover {
              background-color: #45a049;
            }
          }
        }
      }
    }
  }

  .comments-container {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;

    .section-title {
      margin-top: 0;
      color: #333;
    }

    .comment-list-wrapper {
      // height: px;
      overflow-y: auto;
      border: 1px solid #eee;
      border-radius: 4px;
      padding: 10px;

      .comment-list{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1rem;
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
        }
      }

      .no-comments {
        text-align: center;
        padding: 20px;
        color: #999;
      }
    }
  }

  .related-events-container {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;

    .section-title {
      margin-top: 0;
      color: #333;
    }

    .event-wall {
      display: flex;
      overflow-x: auto;
      gap: 15px;
      padding-bottom: 10px;

      .event-card {
        min-width: 200px;
        border: 1px solid #eee;
        border-radius: 4px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

        img {
          width: 100%;
          height: 120px;
          object-fit: cover;
          border-radius: 4px;
          margin-bottom: 10px;
        }

        h4 {
          margin: 0;
          font-size: 16px;
          color: #333;
        }

        p {
          margin: 8px 0;
          font-size: 14px;
          color: #666;
        }

        button {
          width: 100%;
          padding: 8px;
          background-color: #2196F3;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;

          &:hover {
            background-color: #0b7dda;
          }
        }
      }
    }
  }

  .feedback-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;

    .modal-content {
      background-color: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
      width: 90%;
      max-width: 500px;
      display: flex;
      flex-direction: column;
      align-items: center;

      .modal-header {
        display: flex;
        justify-content: center; // 让子元素水平居中
        align-items: center; // 让子元素垂直居中
        width: 100%;
        position: relative;
        margin-bottom: 15px;

        h2 {
          font-size: large;
          margin: 0; // 去除默认的外边距
        }

        .close-btn {
          position: absolute; // 使用绝对定位
          right: 10px; // 距离右侧 10px
          top: 50%; // 垂直居中
          transform: translateY(-50%); // 微调垂直位置
          font-size: 24px;
          cursor: pointer;
        }
      }

      textarea {
        width: 90%;
        padding: 10px;
        margin-bottom: 15px;
        border: 1px solid #ddd;
        border-radius: 4px;
        resize: none;
      }

      .btn-submit {
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;

        &:hover {
          background-color: #45a049;
        }
      }
    }
  }
}
</style>