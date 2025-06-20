<template>
  <div class="book-detail-container">
    <!-- 书籍基本信息区 -->
    <div class="book-info-section">
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
            <span class="cover-text">{{ book.title.substring(0, 2) }}</span>
          </div>
        </div>
        <div class="left-row" >
          <span class="left-label">
            <i class="eye-icon">👁️</i> 累计借阅次数:
          </span>
          <span class="left-value">{{ book.borrow_counts }} 次</span>
        </div>
        <div class="button-container">
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
          <p class="description-content">{{ book.description || '暂无简介' }}</p>
        </div>
      </div>
    </div>
    
    <!-- 书籍目录区 -->
    <div class="book-catalog-section">
      <h2 class="section-title">📖 书籍目录</h2>
      <div v-if="catalog && catalog.length > 0" class="catalog-content">
        <div v-for="(chapter, index) in catalog" :key="index" class="chapter-item">
          <span class="chapter-index">第{{ index + 1 }}章</span>
          <span class="chapter-title">{{ chapter }}</span>
        </div>
      </div>
      <div v-else class="empty-catalog">
        <p>暂无目录信息</p>
      </div>
    </div>
    
    <!-- 评论区 -->
    <div class="book-comments-section">
      <div class="comments-header">
        <h2 class="section-title">💬 读者评论 ({{ comments.length }})</h2>
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
            <div class="comment-rating">
              <span 
                v-for="star in 5" 
                :key="star" 
                class="star"
                :class="{ 'filled': star <= comment.rating }"
              >★</span>
            </div>
            <p class="comment-text">{{ comment.content }}</p>
          </div>
        </div>
      </div>
      <div v-else class="no-comments">
        <p>暂无评论，快来发表第一条评论吧！</p>
      </div>
    </div>
    
    <!-- 添加评论模态框 -->
    <div v-if="showCommentModal" class="comment-modal">
      <div class="modal-content">
        <h3 class="modal-title">发表评论</h3>
        <div class="rating-section">
          <span>评分:</span>
          <div class="star-rating">
            <span 
              v-for="star in 5" 
              :key="star" 
              class="star"
              :class="{ 'filled': star <= newComment.rating }"
              @click="newComment.rating = star"
            >★</span>
          </div>
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

<script>
import { lookBook } from '@/api/books'
import { getComments } from '@/api/comments'

export default {
  data() {
    return {
      book: [],
      comments: [],
      isBorrowed: false,
      showCommentModal: false,
      newComment: {
        rating: 0,
        content: ''
      },
      catalog: [
        '框架设计概览',
        '响应式系统的作用与实现',
        '响应式系统的实现原理',
        '响应式系统的进阶用法',
        '非原始值的响应式方案',
        '原始值的响应式方案',
        '渲染器的设计',
        '挂载与更新',
        '简单diff算法'
      ]
    }
  },
  created() {
    this.loadBookData()
    this.loadComments()
    // this.checkBorrowStatus()
  },
  methods: {
    async loadBookData() {
      const bookId = this.$route.params.id
      try {
        const params = bookId
        const {data} = await lookBook(params)
        this.book = data
      } 
      catch (error) {
        console.error(error)
      }
    },
    async loadComments() {
      const bookId = this.$route.params.id
      try {
        const params = bookId
        const {data} = await getComments(params)
        this.comments = data
      } 
      catch (error) {
        console.error(error)
      }
    },
    async checkBorrowStatus() {
      // 这里应该是API调用检查当前用户是否已借阅该书
      // 模拟数据
      this.isBorrowed = false
    },
    handleBookAction() {
      if (this.isBorrowed) {
        this.returnBook()
      } else {
        this.borrowBook()
      }
    },
    async borrowBook() {
      try {
        // 调用借书API
        this.isBorrowed = true
        this.book.available_copies -= 1
        alert('借阅成功！')
      } catch (error) {
        console.error('借书失败:', error)
      }
    },
    async returnBook() {
      try {
        // 调用还书API
        this.isBorrowed = false
        this.book.available_copies += 1
        alert('归还成功！')
      } catch (error) {
        console.error('还书失败:', error)
      }
    },
    async submitComment() {
      if (this.newComment.rating === 0) {
        alert('请选择评分')
        return
      }
      if (!this.newComment.content.trim()) {
        alert('请输入评论内容')
        return
      }
      
      try {
        // 调用提交评论API
        this.comments.unshift({
          id: Date.now(),
          user_name: '当前用户',
          content: this.newComment.content,
          rating: this.newComment.rating,
          created_at: new Date().toISOString()
        })
        this.showCommentModal = false
        this.newComment = { rating: 0, content: '' }
      } catch (error) {
        console.error('提交评论失败:', error)
      }
    },
    handleImageError(event) {
      event.target.src = ''
      event.target.style.display = 'none'
      event.target.parentElement.querySelector('.book-cover-placeholder').style.display = 'flex'
    },
    formatDate(dateString) {
      if (!dateString) 
        return '未知'
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' })
    }
  }
}
</script>

<style scoped>
.book-detail-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  color: #333;
  background-color: #f9f5f0;
  min-height: 100vh;
}

/* 书籍信息区样式 */
.book-info-section {
  display: flex;
  gap: 30px;
  margin-bottom: 40px;
  background-color: #fff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.book-cover-container {
  flex: 0 0 240px;
  height: 320px;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: relative;
}

.book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.book-cover:hover {
  transform: scale(1.02);
}

.book-cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #d7ccc8 0%, #bcaaa4 100%);
}

.cover-text {
  font-size: 3rem;
  color: #fff;
  font-weight: bold;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
}

.left-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding: 12px 12px;
  background-color: #ffffff;
  border-radius: 6px;
  font-size: 15px;
}

.left-label {
  font-weight: 600;
  color: #3e2723;
  display: flex;
  align-items: center;
  gap: 6px;
}

.eye-icon {
  font-size: 16px;
  color: #8d6e63;
}

.left-value {
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 4px;
}

.book-meta {
  flex: 1;
}

.book-title {
  margin: 0 0 15px 0;
  font-size: 1.8rem;
  color: #3e2723;
  font-weight: 600;
}

.meta-row {
  display: flex;
  margin-bottom: 8px;
  font-size: 15px;
}

.meta-label {
  font-weight: 600;
  color: #5d4037;
  min-width: 80px;
}

.meta-value {
  color: #4e342e;
}

.availability {
  font-weight: 600;
}

.availability.available {
  color: #2e7d32;
}

.availability:not(.available) {
  color: #c62828;
}

.book-description {
  margin: 20px 0;
  padding: 15px;
  background-color: #f5f1e8;
  border-radius: 6px;
}

.description-title {
  margin: 0 0 10px 0;
  font-size: 1.2rem;
  color: #5d4037;
}

.description-content {
  margin: 0;
  line-height: 1.8;
  color: #4e342e;
}

.button-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;      /* 垂直居中（可选） */
  margin-top: 20px;         /* 可根据需要调整间距 */
}

.action-button {
  padding: 12px 24px;
  background-color: #5d4037;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 15px;
}

.action-button:hover:not(:disabled) {
  background-color: #3e2723;
  transform: translateY(-2px);
}

.action-button:disabled {
  background-color: #a1887f;
  cursor: not-allowed;
}

.return-button {
  background-color: #2e7d32;
}

.return-button:hover:not(:disabled) {
  background-color: #1b5e20;
}

/* 书籍目录区样式 */
.book-catalog-section {
  background-color: #fff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 40px;
}

.section-title {
  margin: 0 0 20px 0;
  font-size: 1.5rem;
  color: #3e2723;
  position: relative;
  padding-bottom: 10px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background-color: #8d6e63;
}

.catalog-content {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.chapter-item {
  padding: 12px 15px;
  background-color: #f5f1e8;
  border-radius: 4px;
  display: flex;
  align-items: center;
  transition: all 0.2s ease;
}

.chapter-item:hover {
  background-color: #efebe9;
  transform: translateX(5px);
}

.chapter-index {
  font-weight: 600;
  color: #5d4037;
  margin-right: 10px;
}

.chapter-title {
  color: #4e342e;
}

.empty-catalog {
  text-align: center;
  padding: 30px;
  color: #5d4037;
}

/* 评论区样式 */
.book-comments-section {
  background-color: #fff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-comment-button {
  padding: 8px 16px;
  background-color: #8d6e63;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.add-comment-button:hover {
  background-color: #6d4c41;
}

.plus-icon {
  margin-right: 5px;
  font-size: 16px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  display: flex;
  gap: 15px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 6px;
}

.comment-user {
  flex: 0 0 120px;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #8d6e63;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 8px;
}

.user-name {
  display: block;
  font-weight: 600;
  color: #3e2723;
}

.comment-date {
  font-size: 12px;
  color: #8d6e63;
}

.comment-content {
  flex: 1;
}

.comment-rating {
  margin-bottom: 8px;
}

.star {
  color: #bcaaa4;
  font-size: 18px;
  margin-right: 2px;
}

.star.filled {
  color: #ffc107;
}

.comment-text {
  margin: 0;
  line-height: 1.6;
  color: #4e342e;
}

.no-comments {
  text-align: center;
  padding: 30px;
  color: #5d4037;
}

/* 评论模态框样式 */
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
  padding: 25px;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-title {
  margin: 0 0 20px 0;
  font-size: 1.3rem;
  color: #3e2723;
}

.rating-section {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.rating-section span {
  margin-right: 10px;
  color: #5d4037;
}

.star-rating {
  display: flex;
}

.star-rating .star {
  cursor: pointer;
  font-size: 24px;
  transition: all 0.2s;
}

.star-rating .star:hover {
  transform: scale(1.2);
}

.comment-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #d7ccc8;
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
  margin-bottom: 20px;
  resize: vertical;
  min-height: 100px;
}

.comment-textarea:focus {
  outline: none;
  border-color: #8d6e63;
  box-shadow: 0 0 0 2px rgba(141, 110, 99, 0.2);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.cancel-button {
  padding: 8px 16px;
  background-color: #efebe9;
  color: #5d4037;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-button:hover {
  background-color: #d7ccc8;
}

.submit-button {
  padding: 8px 16px;
  background-color: #5d4037;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.submit-button:hover {
  background-color: #3e2723;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .book-info-section {
    flex-direction: column;
  }
  
  .book-cover-container {
    flex: 0 0 auto;
    height: auto;
    aspect-ratio: 2/3;
  }
  
  .catalog-content {
    grid-template-columns: 1fr;
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
}
</style>