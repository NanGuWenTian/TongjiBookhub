<template>
  <div class="library-container">
    <div class="library-content">
      <div class="title-container">
        <h1 class="library-title">图书检索</h1>
      </div>
      <div class="search-container">
        <div class="search-box">
          <select v-model="searchType" class="search-type">
            <option value="title">书名</option>
            <option value="author">作者</option>
            <option value="isbn">ISBN</option>
            <option value="category">分类</option>
          </select>
          <input 
            v-model="searchQuery" 
            class="search-input" 
            :placeholder="`按${searchTypePlaceholder}搜索`"
            @keyup.enter="searchBooks"
          >
          <button class="search-button" @click="searchBooks">
            <el-icon class="search-icon"><Search /></el-icon>
          </button>
        </div>

        <div class="action-row">
          <div class="sort-container">
            <label for="sort-select" class="sort-label">排序方式:</label>
            <select 
              id="sort-select"
              v-model="sortOption" 
              class="sort-select"
              @change="sortBooks"
            >
              <option value="title_asc">书名 (A-Z)</option>
              <option value="title_desc">书名 (Z-A)</option>
              <option value="author_asc">作者 (A-Z)</option>
              <option value="author_desc">作者 (Z-A)</option>
              <option value="publish_date_desc">出版日期 (最新)</option>
              <option value="publish_date_asc">出版日期 (最旧)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 图书展示区域 -->
      <div class="books-container">
        <div v-if="loading" class="loading-animation">
          <div class="book-pulse"></div>
          <p>正在加载图书...</p>
        </div>
        
        <div v-if="!loading && books.length === 0" class="no-results">
          <div class="empty-shelf-animation">
            <div class="book-shimmer"></div>
            <div class="book-shimmer"></div>
            <div class="book-shimmer"></div>
          </div>
          <p>没有找到匹配的图书</p>
        </div>

        <transition-group name="book-list" tag="div" class="book-list-single">
          <div 
            v-for="(book, index) in displayBooks" 
            :key="book.id" 
            class="book-card-single"
            :style="{ 'transition-delay': `${index * 0.05}s` }"
          >
            <button class="look-button" @click="lookBook(book)">查看</button>
            <div class="book-cover-container">
              <div class="book-cover-placeholder" v-if="!book.cover_image">
                <span class="cover-text">{{ book.title.substring(0, 2) }}</span>
              </div>
              
              <img
                v-else
                :src="book.cover_image" 
                :alt="book.title"
                class="book-cover"
                @error="handleImageError"
              >

              <div class="availability-badge" :class="{ 'available': book.available_copies > 0 }">
                {{ book.available_copies > 0 ? '可借' : '已借完' }}
              </div>
            </div>
            <div class="book-details">
              <h3 class="book-title">{{ book.title }}</h3>
              <p class="book-author">作者: {{ book.author }}</p>
              <p class="book-isbn">ISBN: {{ book.isbn }}</p>
              <p class="book-category">分类: {{ book.category || '未分类' }}</p>
              <p class="book-publish-date">出版日期: {{ formatDate(book.publish_date) }}</p>
              <p class="book-description">{{ truncateDescription(book.description) }}</p>
            </div>
          </div>
        </transition-group>
      </div>

      <!-- 分页控件 -->
      <div v-if="books.length > 0" class="pagination" ref="paginationRef">
        <button 
          class="page-button" 
          :disabled="currentPage === 1" 
          @click="changePage(currentPage - 1)"
        >
          上一页
        </button>
        <span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
        <button 
          class="page-button" 
          :disabled="currentPage >= totalPages" 
          @click="changePage(currentPage + 1)"
        >
          下一页
        </button>
        <input 
          v-model.number="jumpPage"
          type="number"
          min="1"
          :max="totalPages"
          class="jump-input"
          placeholder="页码"
          @keyup.enter="jumpToPage"
        />
        <button 
          class="page-button" 
          @click="jumpToPage"
        >
          跳转
        </button>
      </div>   
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { getBooks } from '@/api/books'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

const router = useRouter()

const books = ref([])
const searchQuery = ref('')
const searchType = ref('title')
const loading = ref(false)
const currentPage = ref(1)
const itemsPerPage = 5
const totalItems = ref(0)
const sortOption = ref('title_asc')
const paginationRef = ref(null)
const jumpPage = ref(null)

const searchTypePlaceholder = computed(() => {
  const types = {
    title: '书名',
    author: '作者',
    isbn: 'ISBN',
    category: '分类'
  }
  return types[searchType.value]
})

function truncateDescription(desc) {
  if (!desc) return '暂无简介'
  return desc.length > 100 ? desc.slice(0, 100) + '...' : desc
}

function formatDate(dateString) {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit'
  })
}

const sortedBooks = computed(() => {
  return [...books.value].sort((a, b) => {
    switch (sortOption.value) {
      case 'title_asc': return a.title.localeCompare(b.title)
      case 'title_desc': return b.title.localeCompare(a.title)
      case 'author_asc': return a.author.localeCompare(b.author)
      case 'author_desc': return b.author.localeCompare(a.author)
      case 'publish_date_desc': return new Date(b.publish_date) - new Date(a.publish_date)
      case 'publish_date_asc': return new Date(a.publish_date) - new Date(b.publish_date)
      default: return 0
    }
  })
})

const displayBooks = computed(() => {
  return sortedBooks.value.slice(0, itemsPerPage)
})

async function loadBooks() {
  loading.value = true
  const params = {
    [searchType.value]: searchQuery.value,
    page: currentPage.value,
    limit: itemsPerPage
  }

  const result = await getBooks(params)

  loading.value = false
  if (result.code !== 200) {
    ElMessage.error(result.msg || '载入失败');
    return;
  }
  else {
    books.value = result.data
    totalItems.value = result.total
  }
}

function searchBooks() {
  currentPage.value = 1
  loadBooks()
}

function sortBooks() {
  currentPage.value = 1
  loadBooks()
}

function lookBook(book) {
  router.push({ name: 'bookDetailedPage', params: { id: book.id } })
}

const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage))

function changePage(page) {
  if (page >= 1 && page <= totalPages.value && page !== currentPage.value) {
    currentPage.value = page
    loadBooks()
    nextTick(() => {
      setTimeout(() => {
        paginationRef.value?.scrollIntoView({
          behavior: 'smooth',
          block: 'end'
        })
      }, 500)
    })
  }
}

function jumpToPage() {
  if (
    Number.isInteger(jumpPage.value) &&
    jumpPage.value >= 1 &&
    jumpPage.value <= totalPages.value
  ) {
    changePage(jumpPage.value)
  } else {
    ElMessage.warning(`请输入 1 到 ${totalPages.value} 的有效页码`)
  }
}

onMounted(() => {
  loadBooks()
})
</script>

<style scoped>
/* 基础样式 */
.library-container {
  font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  width: 80%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  color:#2c3e50;
  background-color: #f5f9ff;
  min-height: 100vh;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(74, 137, 220, 0.1);
}

.library-content {
  width: 100%;
}

/* 顶部标题和搜索栏 */
.title-container {
  text-align: center;
  margin-bottom: 20px;
}

.library-title {
  margin: 50px 0px;
  font-size: 2.6rem;
  background: linear-gradient(135deg, #4a89dc 0%, #3b7dd8 100%);
  background-clip: text; 
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 2px;
  font-weight: 600;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}

/* 搜索框样式 */
.search-container {
  margin-bottom: 0px;
}

.search-box {
  display: flex;
  background: white;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  border: 1px solid #e0e6ed;
}

.search-type {
  padding: 10px 12px;
  border: none;
  background: #e6f0fd;
  font-size: 14px;
  cursor: pointer;
  outline: none;
  min-width: 90px;
  color: #2c3e50;
  border-right: 1px solid #d4e1f8;
  font-weight: 500;
}

.search-input {
  flex: 1;
  padding: 10px 15px;
  border: none;
  font-size: 15px;
  outline: none;
  background: #fff;
  color: #3c4858;
}

.search-input::placeholder {
  color: #b8c2cc;
}

.search-button {
  padding: 0 20px;
  border: none;
  background: #4a89dc;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.search-button:hover {
  background: #3b7dd8;
}

.search-icon {
  font-size: 18px;
}

/* 操作行样式 */
.action-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
}

.sort-container {
  display: flex;
  align-items: center;
  margin-top: 5px;
}

.sort-label {
  margin-left: 18px;
  margin-right: 13px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.9);
}

.sort-select {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #e0e6ed;
  background: #fff;
  font-size: 14px;
  cursor: pointer;
  outline: none;
  min-width: 160px;
  color: #3c4858;
  transition: all 0.3s ease;
}

.sort-select:hover {
  border-color: #c4d5f1;
}

/* 图书列表样式 */
.books-container {
  margin-top: 15px;
}

.loading-animation {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.book-pulse {
  width: 60px;
  height: 90px;
  background: #e6f0fd;
  border-radius: 4px;
  animation: pulse 1.5s infinite ease-in-out;
  margin-bottom: 20px;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; transform: scale(0.98); }
  50% { opacity: 1; transform: scale(1.02); }
}

.no-results {
  text-align: center;
  padding: 40px 0;
  color: #4a89dc;
}

.empty-shelf-animation {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 25px;
  height: 100px;
  align-items: flex-end;
}

.book-shimmer {
  width: 60px;
  height: 80px;
  background: linear-gradient(90deg, #e6f0fd 25%, #d4e1f8 50%, #e6f0fd 75%);
  background-size: 200% 100%;
  border-radius: 4px;
  animation: shimmer 2s infinite linear;
}

.book-shimmer:nth-child(1) {
  height: 90px;
  animation-delay: 0.1s;
}
.book-shimmer:nth-child(2) {
  height: 70px;
  animation-delay: 0.3s;
}
.book-shimmer:nth-child(3) {
  height: 80px;
  animation-delay: 0.2s;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* 单列图书卡片样式 */
.book-list-single {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.book-card-single {
  display: flex;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  height: 240px;
  border-left: 4px solid #4a89dc;
  position: relative;
}

.book-card-single:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.book-cover-container {
  position: relative;
  flex: 0 0 160px;
  min-height: 220px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f9ff;
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
  font-size: 2rem;
  color: #4a89dc;
  font-weight: bold;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
}

.book-cover {
  width: 95%;
  height: 95%;
  object-fit: cover;
  object-position: center;
  border: 1px solid #e0e6ed;
  border-radius: 2px;
}

.availability-badge {
  position: absolute;
  top: 10px;
  right: 5px;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  color: white;
  background: #ff5e57;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.availability-badge.available {
  background: #48cfad;
}

.book-details {
  flex: 1;
  padding: 15px 20px;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.book-title {
  margin: 0 0 8px 0;
  font-size: 1.4rem;
  color: #2c3e50;
  border-bottom: 1px solid #e0e6ed;
  padding-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 600;
}

.book-author, .book-isbn, .book-category, .book-publish-date, .book-copies {
  margin: 4px 0;
  font-size: 15px;
  color: #5d6d7e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-description {
  margin: 8px 0;
  font-size: 15px;
  color: #5d6d7e;
  line-height: 1.5;
  flex-grow: 1;
  white-space: normal;        
  overflow-wrap: break-word;  
}

.look-button {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 10;
  padding: 6px 16px;         
  font-size: 15px;            
  border-radius: 6px;        
  background-color: #4a89dc;
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  font-weight: 500;
}

.look-button:hover {
  background-color: #3b7dd8;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 30px 0 10px;
  gap: 8px;
}

.page-button {
  padding: 8px 16px;
  background: #4a89dc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
}

.page-button:hover:not(:disabled) {
  background: #3b7dd8;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.page-button:disabled {
  background: #b8c2cc;
  cursor: not-allowed;
  transform: none;
}

.page-info {
  margin: 0 10px;
  color: #5d6d7e;
  font-size: 14px;
}

.jump-input {
  width: 60px;
  padding: 8px;
  border: 1px solid #e0e6ed;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  text-align: center;
  color: #3c4858;
  transition: all 0.3s ease;
}

.jump-input:focus {
  border-color: #4a89dc;
  box-shadow: 0 0 0 2px rgba(74, 137, 220, 0.2);
}

/* 过渡动画 */
.book-list-enter-active {
  transition: all 0.4s ease;
}
.book-list-leave-active {
  transition: all 0.2s ease;
}
.book-list-enter, .book-list-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
.book-list-move {
  transition: transform 0.4s;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .library-container {
    padding: 15px;
    max-width: 95%;
  }
  
  .library-header {
    padding: 20px;
  }
  
  .book-card-single {
    flex-direction: column;
    height: auto;
  }
  
  .book-cover-container {
    flex: 0 0 200px;
  }
  
  .action-row {
    flex-direction: column;
    gap: 10px;
  }
  
  .sort-container {
    width: 100%;
  }
  
  .sort-select {
    width: 100%;
  }
  
  .search-box {
    flex-direction: column;
  }
  
  .search-type, .search-input, .search-button {
    width: 100%;
  }
  
  .search-type {
    border-right: none;
    border-bottom: 1px solid #d4e1f8;
  }
  
  .pagination {
    flex-wrap: wrap;
  }
}
</style>