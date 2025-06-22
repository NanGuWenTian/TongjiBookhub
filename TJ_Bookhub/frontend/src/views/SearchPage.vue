<template>
  <div class="library-container">
    <!-- 主内容区 -->
    <div class="library-content">
      <!-- 顶部标题和搜索栏 -->
      <div class="library-header">
        <div class="title-container">
          <h1 class="library-title">📚 图书检索</h1>
          <p class="library-subtitle">畅游知识海洋</p>
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
              <span class="search-icon">🔍</span>
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
                <option value="publish_date_desc">出版日期 (最新)</option>
                <option value="publish_date_asc">出版日期 (最旧)</option>
              </select>
            </div>
            
            <button 
              v-if="isAdmin" 
              class="add-book-button" 
              @click="showAddBookModal = true"
            >
              <span class="plus-icon">+</span> 添加图书
            </button>
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
            v-for="(book, index) in paginatedBooks" 
            :key="book.id" 
            class="book-card-single"
            :style="{ 'transition-delay': `${index * 0.05}s` }"
          >
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
              <p class="book-copies">库存: {{ book.available_copies }} / {{ book.total_copies }}</p>
              <p class="book-description">{{ book.description || '暂无简介' }}</p>
              <div class="book-actions">
                <button class="look-button" @click="lookBook(book)">查看</button>
                <div v-if="isAdmin" class="admin-actions">
                  <button class="edit-button" @click="editBook(book)">编辑</button>
                  <button class="delete-button" @click="deleteBook(book.id)">删除</button>
                </div>
              </div>
            </div>
          </div>
        </transition-group>
      </div>

      <!-- 分页控件 -->
      <!-- <div v-if="books.length > 0" class="pagination">
        <button 
          class="page-button" 
          :disabled="currentPage === 1" 
          @click="changePage(currentPage - 1)"
        >
          &lt; 上一页
        </button>
        <span 
          v-for="page in visiblePages" 
          :key="page"
          class="page-number"
          :class="{ 'active': page === currentPage }"
          @click="changePage(page)"
        >
          {{ page }}
        </span>
        <button 
          class="page-button" 
          :disabled="currentPage >= totalPages" 
          @click="changePage(currentPage + 1)"
        >
          下一页 &gt;
        </button>
      </div> -->
      <div v-if="books.length > 0" class="pagination">
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
      </div>

      <!-- 添加/编辑图书模态框 -->
      <BookModal 
        v-if="showAddBookModal || showEditBookModal"
        :book="currentBook"
        :isEdit="showEditBookModal"
        @close="closeModal"
        @save="saveBook"
      />
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import BookModal from '@/components/BookModal.vue'
import { fetchBooks, addBook, updateBook, deleteBook } from '@/api/books'

export default {
  components: { BookModal },
  data() {
    return {
      books: [],
      searchQuery: '',
      searchType: 'title',
      selectedCategory: '',
      categories: ['文学', '科技', '历史', '艺术', '小说', '传记', '计算机', '心理学'],
      showAddBookModal: false,
      showEditBookModal: false,
      currentBook: null,
      loading: false,
      currentPage: 1,
      itemsPerPage: 5, // 每页显示5本书
      totalItems: 0,
      sortOption: 'title_asc'
    }
  },
  computed: {
    ...mapState(['user']),
    isAdmin() {
      return true
      // return this.user && this.user.is_admin
    },
    searchTypePlaceholder() {
      const types = {
        title: '书名',
        author: '作者',
        isbn: 'ISBN',
        category: '分类'
      }
      return types[this.searchType] || '书名'
    },
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage)
    },
    sortedBooks() {
      return [...this.books].sort((a, b) => {
        switch(this.sortOption) {
          case 'title_asc': return a.title.localeCompare(b.title)
          case 'title_desc': return b.title.localeCompare(a.title)
          case 'author_asc': return a.author.localeCompare(b.author)
          case 'publish_date_desc': return new Date(b.publish_date) - new Date(a.publish_date)
          case 'publish_date_asc': return new Date(a.publish_date) - new Date(b.publish_date)
          default: return 0
        }
      })
    },
    paginatedBooks() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.sortedBooks.slice(start, end)
    },
    visiblePages() {
      const pages = []
      const range = 2
      let start = Math.max(1, this.currentPage - range)
      let end = Math.min(this.totalPages, this.currentPage + range)
      
      if (start > 1) pages.push(1)
      if (start > 2) pages.push('...')
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      
      if (end < this.totalPages - 1) pages.push('...')
      if (end < this.totalPages) pages.push(this.totalPages)
      
      return pages
    }
  },
  created() {
    this.loadBooks()
  },
  methods: {
    async loadBooks() {
      this.loading = true
      try {
        const params = {
          [this.searchType]: this.searchQuery,
          category: this.selectedCategory,
          page: this.currentPage,
          limit: this.itemsPerPage
        }
        const { data } = await fetchBooks(params)
        this.books = data
        this.totalItems = data.length
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    searchBooks() {
      this.currentPage = 1
      this.loadBooks()
    },
    sortBooks() {
      this.currentPage = 1
    },
    editBook(book) {
      this.currentBook = { ...book }
      this.showEditBookModal = true
    },
    async deleteBook(id) {
      if (confirm('确定要删除这本书吗？')) {
        try {
          await deleteBook(id)
          this.loadBooks()
        } catch (error) {
          console.error(error)
        }
      }
    },
    lookBook(book) {
      this.$router.push({
        name: 'BookDetail',
        params: { id: book.id }
      });
    },
    closeModal() {
      this.showAddBookModal = false
      this.showEditBookModal = false
      this.currentBook = null
    },
    async saveBook(bookData) {
      try {
        if (bookData.id) {
          await updateBook(bookData.id, bookData)
        } else {
          await addBook(bookData)
        }
        this.closeModal()
        this.loadBooks()
      } catch (error) {
        console.error(error)
      }
    },
    handleImageError(event) {
      event.target.src = ''
    },
    formatDate(dateString) {
      if (!dateString) return '未知'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
        this.currentPage = page
        this.loadBooks()
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }
  }
}
</script>

<style scoped>
/* 基础样式 */
.library-container {
  font-family: 'Noto Serif SC', 'SimSun', serif;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  color: #333;
  background-color: #f5f1e8;
  min-height: 100vh;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}

.library-content {
  width: 100%;
}

/* 顶部标题和搜索栏 */
.library-header {
  background-color: #5d4037;
  padding: 20px 25px;
  border-radius: 5px;
  margin-bottom: 25px;
  color: #fff;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16);
}

.title-container {
  text-align: center;
  margin-bottom: 20px;
}

.library-title {
  margin: 0;
  font-size: 2rem;
  color: #fff;
  letter-spacing: 1px;
}

.library-subtitle {
  margin: 5px 0 0;
  font-size: 0.9rem;
  color: #d7ccc8;
  font-style: italic;
}

/* 搜索框样式 */
.search-container {
  margin-bottom: 15px;
}

.search-box {
  display: flex;
  background: white;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
}

.search-type {
  padding: 10px 12px;
  border: none;
  background: #d7ccc8;
  font-size: 14px;
  cursor: pointer;
  outline: none;
  min-width: 90px;
  color: #3e2723;
  border-right: 1px solid #bcaaa4;
}

.search-input {
  flex: 1;
  padding: 10px 15px;
  border: none;
  font-size: 15px;
  outline: none;
  background: #fff;
}

.search-button {
  padding: 0 18px;
  border: none;
  background: #8d6e63;
  color: white;
  cursor: pointer;
  transition: background 0.3s;
}

.search-button:hover {
  background: #6d4c41;
}

.search-icon {
  font-size: 16px;
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
}

.sort-label {
  margin-right: 8px;
  font-size: 14px;
  color: #efebe9;
}

.sort-select {
  padding: 8px 12px;
  border-radius: 4px;
  border: none;
  background: #fff;
  font-size: 14px;
  cursor: pointer;
  outline: none;
  min-width: 160px;
  color: #3e2723;
}

.add-book-button {
  padding: 8px 16px;
  background: #a1887f;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.add-book-button:hover {
  background: #8d6e63;
  transform: translateY(-1px);
}

.plus-icon {
  margin-right: 5px;
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
  background: #d7ccc8;
  border-radius: 3px;
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
  color: #5d4037;
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
  background: linear-gradient(90deg, #efebe9 25%, #d7ccc8 50%, #efebe9 75%);
  background-size: 200% 100%;
  border-radius: 3px;
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
  border-radius: 5px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  height: 320px;
  border-left: 4px solid #8d6e63;
  position: relative;
}

.book-card-single:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.book-cover-container {
  position: relative;
  flex: 0 0 160px;
  min-height: 220px;
  background: #efebe9;
  overflow: hidden;
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
  font-size: 2rem;
  color: #fff;
  font-weight: bold;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
}

.book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.3s ease;
}

.book-card-single:hover .book-cover {
  transform: scale(1.05);
}

.availability-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  color: white;
  background: #d32f2f;
}

.availability-badge.available {
  background: #388e3c;
}

.book-details {
  flex: 1;
  padding: 15px;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.book-title {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
  color: #3e2723;
  border-bottom: 1px solid #d7ccc8;
  padding-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-author, .book-isbn, .book-category, .book-publish-date, .book-copies {
  margin: 3px 0;
  font-size: 14px;
  color: #5d4037;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-description {
  margin: 10px 0;
  font-size: 13px;
  color: #4e342e;
  line-height: 1.5;
  flex-grow: 1;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
}

.book-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.look-button {
  padding: 8px 16px;
  background: #5d4037;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 14px;
}

.look-button:hover:not(:disabled) {
  background: #3e2723;
}

.look-button:disabled {
  background: #a1887f;
  cursor: not-allowed;
}

.admin-actions {
  display: flex;
  gap: 6px;
}

.edit-button, .delete-button {
  padding: 8px 12px;
  border: none;
  border-radius: 3px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-button {
  background: #8d6e63;
  color: white;
}

.edit-button:hover {
  background: #6d4c41;
}

.delete-button {
  background: #5d4037;
  color: white;
}

.delete-button:hover {
  background: #3e2723;
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
  padding: 8px 12px;
  background: #8d6e63;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 14px;
}

.page-button:hover:not(:disabled) {
  background: #6d4c41;
}

.page-button:disabled {
  background: #bcaaa4;
  cursor: not-allowed;
}

.page-number {
  padding: 6px 12px;
  cursor: pointer;
  border-radius: 3px;
  font-size: 14px;
  color: #5d4037;
}

.page-number:hover:not(.active) {
  background: #d7ccc8;
}

.page-number.active {
  background: #5d4037;
  color: white;
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
    padding: 10px;
  }
  
  .library-header {
    padding: 15px;
  }
  
  .book-card-single {
    flex-direction: column;
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
  
  .add-book-button {
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
    border-bottom: 1px solid #bcaaa4;
  }
}
</style>