<template>

  <div class="book-detail-container">
    <!-- 书籍基本信息区 -->
    <div class="book-info-section">
      <button class="back-button" @click="goBack" aria-label="返回上一页" v-html="backIconSvg"></button>
      <div class="left-section">
        <div class="book-cover-container">
          <img 
            v-if="book.cover_image" 
            :src="book.cover_image" 
            :alt="book.title"
            class="book-cover"
            @error="handleImageError"
          >
          <div v-else class="book-cover-placeholder">
            <span class="cover-text">{{ book.title?.substring(0, 2) || '无' }}</span>
          </div>
        </div>

        <div class="book-stats-vertical">
          <!-- 评分 -->
          <div class="stats-row">
            <template v-if="book.rating && book.rating > 0">
              <el-rate
                v-model="book.rating"
                disabled
                show-score
                text-color="#ff9900"
                score-template="{value} 分"
              />
            </template>
            <template v-else>
              <span class="label" style="padding-top: 5px; padding-bottom: 5px;">评分:</span>
              <span class="value">暂无评分</span>
            </template>
          </div>

          <!-- 借阅次数 -->
          <div class="stats-row" style="padding-top: 5px; padding-bottom: 5px;">
            <span class="label">
              累计借阅次数:
            </span>
            <span class="value">{{ book.borrow_counts }} 次</span>
          </div>

          <!-- 借书按钮 -->
          <div class="stats-row button-wrapper">
            <button 
              class="action-button"
              :class="{ 'return-button': isBorrowed }"
              @click="handleBookAction"
              :disabled="!isBorrowed && book.available_copies <= 0"
            >
              {{ isBorrowed ? '归还书籍' : book.available_copies > 0 ? '借阅此书' : '已借完' }}
            </button>
          </div>
        </div>
      </div>
      

      <div class="book-meta">
        <h1 class="book-title">{{ book.title }}</h1>
        <div class="meta-row">
          <span class="meta-label">作者:</span>
          <span class="meta-value">{{ book.author }}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">出版社:</span>
          <span class="meta-value">{{ book.publisher || '未知' }}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">出版日期:</span>
          <span class="meta-value">{{ formatDate(book.publish_date) }}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">ISBN:</span>
          <span class="meta-value">{{ book.isbn }}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">分类:</span>
          <span class="meta-value">{{ book.category || '未分类' }}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">库存状态:</span>
          <span class="meta-value availability" :class="{ 'available': book.available_copies > 0 }">
            {{ book.available_copies > 0 ? `可借 (剩余 ${book.available_copies} 本)` : '已借完' }}
          </span>
        </div>
        
        <div class="book-description">
          <h3 class="description-title">内容简介</h3>
          <p class="description-content">
            {{ isDescriptionExpanded ? fullDescription : shortDescription }}
          </p>

          <div class="toggle-button-wrapper" v-if="showToggleButton">
            <button class="toggle-button" @click="isDescriptionExpanded = !isDescriptionExpanded">
              {{ isDescriptionExpanded ? '收起' : '展开更多' }}
            </button>
          </div>
        </div>

      </div>
    </div>
    
    <!-- 评论区 -->
    <div class="book-comments-section">
      <div class="comments-header">
        <h2 class="section-title">💬 读者评论 ({{ totalComments }})</h2>
        <button class="add-comment-button" @click="showCommentModal = true">
          <span class="plus-icon">+</span> 添加评论
        </button>
      </div>
      
      <div v-if="comments.length > 0" class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-user">
            <div class="user-avatar">
              
            </div>
            <div class="user-info">
              <span class="user-name">用户{{ comment.user_id }}</span>
              <span class="comment-date">{{ formatDate(comment.created_time) }}</span>
            </div>
          </div>
          <div class="comment-content">
            <el-rate
              v-model="comment.rating"
              disabled
              show-score
              text-color="#ff9900"
              score-template="{value} 分"
            />
            <p class="comment-text">
              {{ comment.isExpanded || comment.content.length <= 150 
                  ? comment.content 
                  : comment.content.slice(0, 150) + '...' 
              }}
            </p>
            <div class="toggle-button-wrapper" v-if="comment.content.length > 150">
              <button class="toggle-button2" @click="comment.isExpanded = !comment.isExpanded">
                {{ comment.isExpanded ? '收起' : '展开' }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="no-comments">
        <p>暂无评论，快来发表第一条评论吧！</p>
      </div>
    </div>

    <div class="pagination pagination-center" >
      <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
      <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>

      <input type="number" v-model.number="jumpPage" min="1" :max="totalPages" placeholder="跳转页" style="width: 60px; margin-left: 10px;" />
      <button @click="goToPage(jumpPage)">跳转</button>
    </div>

    <!-- 借阅图书模态框 -->
    <div v-if="showBorrowModal" class="comment-modal">
      <div class="modal-content">
        <h3 class="modal-title">请选择借阅时间</h3>

        <el-form>
          <el-form-item label="借阅天数" style="padding-left: 3px">
            <el-select v-model="selectedDays" placeholder="请选择">
              <el-option v-for="day in [7, 14, 21, 28]" :key="day" :label="`${day} 天`" :value="day" />
            </el-select>
          </el-form-item>
        </el-form>

        <div class="modal-actions">
          <button class="cancel-button" @click="showBorrowModal = false">取消</button>
          <button class="submit-button" @click="confirmBorrow">确定借阅</button>
        </div>
      </div>
    </div>

    <div v-if="showReturnModal" class="comment-modal">
      <div class="modal-content">
        <h3 class="modal-title">确认归还图书</h3>
        <p style="margin-bottom: 20px; color: #5d4037;">{{ dueMessage }}</p>

        <div class="modal-actions">
          <button class="cancel-button" @click="showReturnModal = false">取消</button>
          <button class="submit-button" @click="confirmReturn">确认归还</button>
        </div>
      </div>
    </div>

    
    <!-- 添加评论模态框 -->
    <div v-if="showCommentModal" class="comment-modal">
      <div class="modal-content">
        <h3 class="modal-title">发表评论</h3>
        <div class="rating-section">
          <span>评分:</span>
           <el-rate v-model="newComment.rating" size="large" allow-half clearable
           :texts="['不及格', '及格', '中', '良', '优']"
            show-text
           />
        </div>
        <textarea 
          v-model="newComment.content" 
          class="comment-textarea" 
          placeholder="写下你的阅读感受..."
          rows="5"
        ></textarea>
        <div class="modal-actions">
          <button class="cancel-button" @click="showCommentModal = false">取消</button>
          <button class="submit-button" @click="submitComment">提交评论</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElNotification, ElSelect, ElOption, ElForm, ElFormItem } from 'element-plus'
import { getBookDetails, getBookStatus, getBookBorrowed, getBookFinished } from '@/api/books'
import { getComments, addComment } from '@/api/comments'

const route = useRoute()
const router = useRouter()

// 图书相关常量
const book = ref({})
const isBorrowed = ref(false)
const showCommentModal = ref(false)
const isDescriptionExpanded = ref(false)
const showToggleButton = ref(false)
const MAX_LENGTH = 240
const fullDescription = ref('')
const shortDescription = ref('')
const showBorrowModal = ref(false)
const selectedDays = ref(14)
const showReturnModal = ref(false)
const dueDate = ref(new Date())
const dueMessage = ref('')
// 评论相关常量
const comments = ref([])
const newComment = ref({ rating: 0, content: '' })
const currentPage = ref(1)
const pageSize = 5
const totalComments = ref(0)
const totalPages = computed(() => Math.ceil(totalComments.value / pageSize))
const jumpPage = ref(currentPage.value)


onMounted(() => {
  loadBookData()
  checkBookStatus()
  loadComments()
})

async function loadBookData() {
  const bookId = route.params.id
  const result = await getBookDetails(bookId)
  
  if (result.code !== 200) {
    ElMessage.error(result.msg || '载入当前图书失败');
    return;
  }
  else {
    book.value = result.data
    if (book.value.rating) {
      book.value.rating = parseFloat(book.value.rating.toFixed(1))
    }
    fullDescription.value = book.value.description || '暂无简介'
    if (fullDescription.value.length > MAX_LENGTH) {
      showToggleButton.value = true
      shortDescription.value = fullDescription.value.slice(0, MAX_LENGTH) + '...'
    }
    else {
    shortDescription.value = fullDescription.value
    showToggleButton.value = false
    }
  }
}

async function checkBookStatus() {
  const bookId = route.params.id
  const result = await getBookStatus(bookId)
  if (result.code !== 200) {
    ElMessage.error(result.msg || '检查书本状态失败');
    return;
  }
  else {
    isBorrowed.value = result.data.is_borrowed
    dueDate.value = result.data.due_date ? new Date(result.data.due_date) : null
  }

}

function checkReturnStatus() {
  const now = new Date()
  const diffMs = dueDate.value.getTime() - now.getTime()
  const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24))

  if (diffMs >= 0) {
    dueMessage.value = `您的图书还有不到 ${diffDays} 天到期，确认归还？`
  } else {
    const overdueDays = -diffDays + 1
    dueMessage.value = `您的图书已经逾期近 ${overdueDays} 天，请尽快归还！`
  }
}

async function loadComments() {
  const bookId = route.params.id
  const params = {
    page: currentPage.value,
    limit: pageSize
  }
  const result = await getComments(bookId, params)
  if (result.code !== 200) {
    ElMessage.error(result.msg || '载入评论失败');
    return;
  }
  else {
    totalComments.value = result.data.total
    comments.value = result.data.comments.map(comment => ({
      ...comment,
      isExpanded: false
    }))
  }
}

function handleBookAction() {
  if (isBorrowed.value) {
    checkReturnStatus()
    showReturnModal.value = true
  } else {
    showBorrowModal.value = true
  }
}

async function confirmBorrow() {
  const result = await getBookBorrowed(book.value.id, selectedDays.value)
  if (result.code !== 200) {
    ElNotification.error(result.msg || '借阅书籍失败!');
    return;
  } else {
    showBorrowModal.value = false
    isBorrowed.value = true
    book.value.available_copies -= 1
    book.value.borrow_counts += 1
    ElNotification.success(result.msg || '借阅成功！');
  }
}

async function confirmReturn() {
  const result = await getBookFinished(book.value.id)
  if (result.code !== 200) {
    ElNotification.error(result.msg || '归还书籍失败!');
    return;
  } else {
    showReturnModal.value = false
    isBorrowed.value = false
    book.value.available_copies += 1
    ElNotification.success(result.msg || '归还成功！');
  }
}


async function submitComment() {
  if (newComment.value.rating === 0) {
    ElMessage.warning('图书不易，请至少给0.5分吧！');
    return
  }
  if (!newComment.value.content.trim()) {
    ElMessage.warning('您好像忘记输入评论内容啦！');
    return
  }

  const bookId = route.params.id
  const result = await addComment(bookId, newComment.value)
  if (result.code === 200) {
    showCommentModal.value = false
    ElNotification.success(result.msg || '评论成功！');
    book.value.rating = result.data.rating.toFixed(1);
    newComment.value = { rating: 0, content: '' }
    loadComments()
  } else {
    ElNotification.error(result.msg || '评论失败！');
  }
}

function handleImageError(event) {
  event.target.src = ''
  event.target.style.display = 'none'
  event.target.parentElement.querySelector('.book-cover-placeholder').style.display = 'flex'
}

function formatDate(dateString) {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit'
  })
}

function goToPage(page) {
  if (page < 1 || page > totalPages.value) {
    ElMessage.warning(`请输入 1 到 ${totalPages.value} 的有效页码`)
    return
  }
  loadComments(page)
}

function goBack() {
  router.back()
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value-=1
    loadComments()
  }
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value += 1
    loadComments()
  }
}

watch(currentPage, (newPage) => {
  jumpPage.value = newPage
})

const backIconSvg = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16">
  <path d="M15 8a.5.5 0 0 0-.5-.5H2.707l5.147-5.146a.5.5 0 1 0-.708-.708l-6 6a.5.5 0 0 0 0 .708l6 6a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z"/>
</svg>
`
</script>

<style scoped>
.book-detail-container {
  max-width: 1000px;
  width: 90%;
  margin: 0 auto;
  padding: 20px;
  color: #2c3e50;
  background-color: #f5f9ff;
  min-height: 100vh;
  font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* 书籍信息区样式 */
.back-button {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: rgba(74, 137, 220, 0.1);
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  color: #4a89dc;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.back-button:hover {
  background-color: rgba(74, 137, 220, 0.2);
  transform: translateX(-2px);
}

.book-info-section {
  position: relative;
  display: flex;
  gap: 30px;
  margin-bottom: 40px;
  background-color: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(74, 137, 220, 0.1);
  border: 1px solid #e6f0fd;
}

.book-cover-container {
  flex: 0 0 240px;
  height: 320px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 6px 18px rgba(74, 137, 220, 0.15);
  position: relative;
  background: linear-gradient(135deg, #e6f0fd 0%, #d4e1f8 100%);
}

.book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.book-cover:hover {
  transform: scale(1.03);
}

.book-cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e6f0fd 0%, #d4e1f8 100%);
}

.cover-text {
  font-size: 3rem;
  color: #4a89dc;
  font-weight: bold;
  opacity: 0.8;
}

.book-meta {
  flex: 1;
}

.book-title {
  margin: 0 0 15px 0;
  font-size: 1.8rem;
  color: #2c3e50;
  font-weight: 600;
  line-height: 1.3;
}

.meta-row {
  display: flex;
  margin-bottom: 10px;
  font-size: 15px;
  line-height: 1.6;
}

.meta-label {
  font-weight: 600;
  color: #4a89dc;
  min-width: 80px;
}

.meta-value {
  color: #5d6d7e;
}

.availability {
  font-weight: 600;
}

.availability.available {
  color: #48cfad;
}

.availability:not(.available) {
  color: #ff5e57;
}

.book-description {
  margin: 25px 0;
  padding: 20px;
  background-color: #f5f9ff;
  border-radius: 8px;
  border-left: 4px solid #4a89dc;
}

.description-title {
  margin: 0 0 15px 0;
  font-size: 1.2rem;
  color: #4a89dc;
  font-weight: 600;
}

.description-content {
  margin: 0;
  line-height: 1.8;
  color: #5d6d7e;
}

.action-button {
  padding: 12px 24px;
  background-color: #4a89dc;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 15px;
  box-shadow: 0 2px 8px rgba(74, 137, 220, 0.3);
}

.action-button:hover:not(:disabled) {
  background-color: #3b7dd8;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 137, 220, 0.4);
}

.action-button:disabled {
  background-color: #b8c2cc;
  cursor: not-allowed;
}

.return-button {
  background-color: #48cfad;
  box-shadow: 0 2px 8px rgba(72, 207, 173, 0.3);
}

.return-button:hover:not(:disabled) {
  background-color: #37bc9b;
  box-shadow: 0 4px 12px rgba(72, 207, 173, 0.4);
}

/* 评论区样式 */
.book-comments-section {
  background-color: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(74, 137, 220, 0.1);
  border: 1px solid #e6f0fd;
}

.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e6f0fd;
}

.section-title {
  margin: 0;
  font-size: 1.4rem;
  color: #2c3e50;
  font-weight: 600;
}

.add-comment-button {
  padding: 10px 20px;
  background-color: #4a89dc;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(74, 137, 220, 0.3);
}

.add-comment-button:hover {
  background-color: #3b7dd8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(74, 137, 220, 0.4);
}

.plus-icon {
  margin-right: 6px;
  font-size: 16px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  background-color: #f5f9ff;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid #e6f0fd;
}

.comment-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 137, 220, 0.1);
}

.comment-user {
  flex: 0 0 120px;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #4a89dc;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}

.user-name {
  display: block;
  font-weight: 600;
  color: #2c3e50;
}

.comment-date {
  font-size: 12px;
  color: #8ba3c7;
}

.comment-content {
  flex: 1;
}

.comment-text {
  margin: 10px 0 0;
  line-height: 1.6;
  color: #5d6d7e;
}

.no-comments {
  text-align: center;
  padding: 40px;
  color: #8ba3c7;
  font-size: 15px;
}

/* 模态框样式 */
.comment-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 12px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 8px 30px rgba(74, 137, 220, 0.2);
  border: 1px solid #e6f0fd;
}

.modal-title {
  margin: 0 0 20px 0;
  font-size: 1.3rem;
  color: #2c3e50;
  font-weight: 600;
}

.rating-section {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.rating-section span {
  margin-right: 15px;
  color: #4a89dc;
  font-weight: 500;
}

.comment-textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #e6f0fd;
  border-radius: 8px;
  font-family: inherit;
  font-size: 14px;
  margin-bottom: 20px;
  resize: vertical;
  min-height: 120px;
  box-sizing: border-box;
  transition: all 0.3s ease;
  color: #5d6d7e;
}

.comment-textarea:focus {
  outline: none;
  border-color: #4a89dc;
  box-shadow: 0 0 0 3px rgba(74, 137, 220, 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

.cancel-button {
  padding: 10px 20px;
  background-color: #f5f9ff;
  color: #4a89dc;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.cancel-button:hover {
  background-color: #e6f0fd;
  color: #3b7dd8;
}

.submit-button {
  padding: 10px 20px;
  background-color: #4a89dc;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(74, 137, 220, 0.3);
}

.submit-button:hover {
  background-color: #3b7dd8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(74, 137, 220, 0.4);
}

/* 图书统计信息 */
.book-stats-vertical {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 25px;
  padding: 20px;
  border-radius: 8px;
  background-color: #f5f9ff;
  border: 1px solid #e6f0fd;
}

.stats-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  background-color: #fff;
  padding: 0px 16px;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(74, 137, 220, 0.05);
  border: 1px solid #e6f0fd;
}

.label {
  color: #4a89dc;
  font-weight: 500;
}

.value {
  color: #5d6d7e;
}

.button-wrapper {
  justify-content: center;
  background: transparent;
  box-shadow: none;
  border: none;
  padding: 0;
}

.button-wrapper .action-button {
  width: 100%;
  max-width: 220px;
}

.toggle-button-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.toggle-button {
  background: none;
  border: none;
  color: #4a89dc;
  font-weight: 500;
  cursor: pointer;
  font-size: 14px;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.toggle-button:hover {
  color: #3b7dd8;
  background-color: rgba(74, 137, 220, 0.1);
}

.toggle-button2 {
  background: none;
  border: none;
  color: #8ba3c7;
  font-size: 13px;
  padding: 4px 8px;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.toggle-button2:hover {
  color: #4a89dc;
  background-color: rgba(74, 137, 220, 0.1);
}

/* 分页样式 */
.pagination {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 30px;
  justify-content: center;
  flex-wrap: wrap;
}

.pagination button {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background-color: #4a89dc;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  box-shadow: 0 2px 6px rgba(74, 137, 220, 0.2);
}

.pagination button:hover:not(:disabled) {
  background-color: #3b7dd8;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(74, 137, 220, 0.3);
}

.pagination button:disabled {
  background-color: #b8c2cc;
  cursor: not-allowed;
  box-shadow: none;
}

.pagination input {
  width: 60px;
  padding: 8px;
  border: 1px solid #e6f0fd;
  border-radius: 6px;
  font-size: 14px;
  text-align: center;
  transition: all 0.3s ease;
}

.pagination input:focus {
  outline: none;
  border-color: #4a89dc;
  box-shadow: 0 0 0 2px rgba(74, 137, 220, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .book-info-section {
    flex-direction: column;
    padding: 20px;
  }
  
  .book-cover-container {
    flex: 0 0 auto;
    height: auto;
    aspect-ratio: 2/3;
    margin-bottom: 20px;
  }
  
  .book-stats-vertical {
    margin-top: 15px;
  }
  
  .comments-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .comment-item {
    flex-direction: column;
  }
  
  .comment-user {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    gap: 15px;
  }
  
  .user-info {
    display: flex;
    flex-direction: column;
  }
  
  .pagination {
    gap: 8px;
  }
  
  .pagination button, 
  .pagination input {
    padding: 6px 12px;
  font-size: 13px;
  }
}
</style>