<template>
  <div class="event-detail-page">
  <backgroundCartoon></backgroundCartoon>
    <!-- 活动信息模块 -->
    <div class="event-info-container">
      <div class="event-info">
        <img :src="event.image || 'https://picsum.photos/400/300'" alt="活动图片" class="event-image">
        <div class="info-right">
          <div class="brief-info">
            <h2 class="event-title">{{ event.title }}</h2>
            <p><strong>开始时间:</strong> {{ formatDateTime(event.start_time) }}</p>
            <p><strong>结束时间:</strong> {{ formatDateTime(event.end_time) }}</p>
            <p><strong>地点:</strong> {{ event.location }}</p>
            <p><strong>简介:</strong> {{ event.brief }}</p>
            <p><strong>主办方:</strong> {{ event.organizer }}</p>
            <p><strong>主题:</strong> {{ event.theme }}</p>
          </div>
          <div class="operation">
            <button v-if="!hasParticipated && !isPastEvent" @click="participateEvent" class="btn-participate">
              点击参加
            </button>
            <button v-if="hasParticipated && isPastEvent" @click="openFeedbackModal" class="btn-evaluate">
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
          <div class="comment-item" v-for="comment in comments" :key="comment.id">
            <div class="comment-content">{{ comment.feedback }}</div>
            <div class="comment-user">{{ comment.username }}</div>
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
        <span class="close-btn" @click="closeFeedbackModal">&times;</span>
        <h2>{{ modalTitle }}</h2>
        <textarea v-model="feedbackText" rows="5" placeholder="请输入您的评价..."></textarea>
        <button @click="submitFeedback" class="btn-submit">提交</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import backgroundCartoon from '@/components/backgroundCartoon.vue'
// import axios from 'axios'
// import { useRoute } from 'vue-router'

// 获取路由参数
// const route = useRoute()
// const eventId = ref(route.params.id)

// 状态管理
const event = ref({})
const comments = ref([])
const relatedEvents = ref([])
const hasParticipated = ref(false)
const isModalOpen = ref(false)
const modalTitle = ref('评价活动')
const feedbackText = ref('')

// 计算属性：判断活动是否已结束
const isPastEvent = computed(() => {
  if (!event.value.end_time) return false
  return new Date(event.value.end_time) < new Date()
})

// 生命周期钩子
onMounted(() => {
  // loadEventDetails()
  // loadEventComments()
  // checkUserParticipation()
  // loadRelatedEvents()

  // 捏造活动详情假数据
  event.value = {
    id: 1,
    title: '示例活动标题',
    start_time: '2024-01-01 10:00:00',
    end_time: '2024-01-01 12:00:00',
    location: '示例地点',
    brief: '这是一个示例活动的简介',
    organizer: '示例主办方',
    theme: '示例主题',
    image: 'https://picsum.photos/400/300',
    type_id: 1
  }

  // 捏造活动评论假数据
  comments.value = [
    {
      id: 1,
      feedback: '这是一条示例评论',
      username: '示例用户'
    }
  ]

  // 捏造用户参与状态假数据
  hasParticipated.value = false

  // 捏造相关活动假数据
  relatedEvents.value = [
    {
      id: 2,
      title: '相关活动1',
      start_time: '2024-01-02 10:00:00',
      image: 'https://picsum.photos/200/150'
    },
    {
      id: 3,
      title: '相关活动2',
      start_time: '2024-01-03 10:00:00',
      image: 'https://picsum.photos/200/150'
    }
  ]
})

// 获取活动详情
// const loadEventDetails = async () => {
//   try {
//     const response = await axios.get('/api/events', {
//       params: {
//         id: eventId.value
//       }
//     });
//     event.value = response.data.event_items
//     console.log('获取活动详情开始,当前活动编号为', eventId.value)
//     console.log('获取活动详情成功,信息如下')
//     console.log(event.value)
//   } catch (error) {
//     console.error('获取活动详情失败:', error)
//     handleApiError(error, '活动详情')
//   }
// }

// 获取活动评论
// const loadEventComments = async () => {
//   try {
//     const response = await axios.get(`/api/event_participation_feedback/get_feedback_by_event?event_id=${eventId.value}`)
//     comments.value = response.data.data
//     console.log('获取活动评论成功,信息如下')
//     console.log(comments.value)
//   } catch (error) {
//     console.error('获取活动评论失败:', error)
//     handleApiError(error, '活动评论')
//   }
// }

// 检查用户参与状态
// const checkUserParticipation = async () => {
//   try {
//     // const userResponse = await axios.get('/api/current_user')
//     // const userId = userResponse.data.id
//     const userId = 1 // 后期合并再改

//     if (userId) {
//       const response = await axios.get(
//         `/api/event_participation_records/get_one_person_one_event_record?event_id=${eventId.value}&user_id=${userId}`
//       )
//       hasParticipated.value = response.data.state == "success"

//       // 如果用户已参与且有反馈，加载反馈内容
//       if (hasParticipated.value && response.data.feedback) {
//         feedbackText.value = response.data.feedback
//       }
//     }
//     console.log('用户是否已参与活动:', hasParticipated.value)
//   } catch (error) {
//     console.error('检查用户参与状态失败:', error)
//     handleApiError(error, '用户参与状态')
//   }
// }

// 获取相关活动
// const loadRelatedEvents = async () => {
//   try {
//     // 确保活动详情已加载完成
//     if (!event.value || !event.value.type_id) {
//       console.log('活动详情未加载完成，无法获取相关活动')
//       return
//     }

//     const response = await axios.get(`/api/events?type_id=${event.value.type_id}`)
//     relatedEvents.value = response.data
//     console.log('获取相关活动成功,信息如下')
//     console.log(relatedEvents.value)
//   } catch (error) {
//     console.error('获取相关活动失败:', error)
//     handleApiError(error, '相关活动')
//   }
// }

// 统一处理API错误
// const handleApiError = (error, dataType) => {
//   let message = `加载${dataType}失败`
//   if (error.response) {
//     message += `: ${error.response.status} ${error.response.statusText}`
//   }
//   alert(message + '，请重试')
// }

// 方法：格式化日期时间
const formatDateTime = (dateTime) => {
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
  try {
    // await axios.post('/api/event_participation_records', {
    //   event_id: eventId.value,
    //   user_id: 1 // 实际应用中应从会话中获取用户ID
    // })
    hasParticipated.value = true
    alert('参加活动成功！')
  } catch (error) {
    console.error('参加活动失败:', error)
    alert('参加活动失败，请重试')
  }
}

// 方法：打开反馈模态框
const openFeedbackModal = () => {
  modalTitle.value = hasParticipated.value && feedbackText.value ? '修改评论' : '添加评论'
  isModalOpen.value = true
}

// 方法：关闭反馈模态框
const closeFeedbackModal = () => {
  isModalOpen.value = false
}

// 方法：提交反馈
const submitFeedback = async () => {
  if (!feedbackText.value.trim()) {
    alert('评论内容不能为空')
    return
  }

  try {
    // 检查是更新还是创建评论
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
    // const commentsResponse = await axios.get(`/api/event_participation_feedback/get_feedback_by_event?event_id=${eventId.value}`)
    // comments.value = commentsResponse.data.data

    hasParticipated.value = true
    isModalOpen.value = false
    alert('评论提交成功！')
  } catch (error) {
    console.error('提交评论失败:', error)
    alert('提交评论失败，请重试')
  }
}

// 方法：导航到其他活动
const navigateToEvent = (id) => {
  window.location.href = `/event/detail?id=${id}`
}
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
      height: 800px;
      overflow-y: auto;
      border: 1px solid #eee;
      border-radius: 4px;
      padding: 10px;

      .comment-item {
        display: flex;
        justify-content: space-between;
        padding: 10px;
        border-bottom: 1px solid #eee;

        .comment-content {
          flex: 1;
          margin-right: 20px;
        }

        .comment-user {
          min-width: 100px;
          text-align: right;
          color: #666;
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

      .close-btn {
        float: right;
        font-size: 24px;
        cursor: pointer;
      }

      h2 {
        margin-top: 0;
      }

      textarea {
        width: 100%;
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