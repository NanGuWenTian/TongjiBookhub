<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-container">
      <div class="modal-header">
        <h2>{{ isEdit ? '编辑图书' : '添加新图书' }}</h2>
        <button class="close-btn" @click="close">&times;</button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="submit">
          <div class="form-group">
            <label for="title">书名</label>
            <input 
              id="title" 
              v-model="formData.title" 
              type="text" 
              required
              placeholder="输入书名"
            >
          </div>
          
          <div class="form-group">
            <label for="author">作者</label>
            <input 
              id="author" 
              v-model="formData.author" 
              type="text" 
              required
              placeholder="输入作者"
            >
          </div>
          
          <div class="form-group">
            <label for="isbn">ISBN</label>
            <input 
              id="isbn" 
              v-model="formData.isbn" 
              type="text" 
              required
              placeholder="输入ISBN"
            >
          </div>
          
          <div class="form-group">
            <label for="publisher">出版社</label>
            <input 
              id="publisher" 
              v-model="formData.publisher" 
              type="text" 
              placeholder="输入出版社"
            >
          </div>
          
          <div class="form-group">
            <label for="publish_date">出版日期</label>
            <input 
              id="publish_date" 
              v-model="formData.publish_date" 
              type="date" 
            >
          </div>
          
          <div class="form-group">
            <label for="total_copies">总数量</label>
            <input 
              id="total_copies" 
              v-model.number="formData.total_copies" 
              type="number" 
              min="1"
              required
            >
          </div>
          
          <div class="form-group">
            <label for="available_copies">可借数量</label>
            <input 
              id="available_copies" 
              v-model.number="formData.available_copies" 
              type="number" 
              min="0"
              required
            >
          </div>
          
          <div class="form-group">
            <label for="category">分类</label>
            <select id="category" v-model="formData.category">
              <option value="">选择分类</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="description">描述</label>
            <textarea 
              id="description" 
              v-model="formData.description" 
              rows="3"
              placeholder="输入图书描述"
            ></textarea>
          </div>
          
          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="close">取消</button>
            <button type="submit" class="submit-btn">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BookModal',
  props: {
    book: {
      type: Object,
      default: null
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      formData: {
        title: '',
        author: '',
        isbn: '',
        publisher: '',
        publish_date: '',
        total_copies: 1,
        available_copies: 1,
        category: '',
        description: ''
      },
      categories: ['文学', '科技', '历史', '艺术', '教育', '小说', '传记', '其他']
    }
  },
  watch: {
    book: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.formData = { ...newVal }
          // 确保数字类型的值正确
          this.formData.total_copies = Number(newVal.total_copies) || 1
          this.formData.available_copies = Number(newVal.available_copies) || 1
        }
      }
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    submit() {
      // 深拷贝表单数据以避免直接修改props
      const bookData = JSON.parse(JSON.stringify(this.formData))
      
      // 转换日期格式
      if (bookData.publish_date === '') {
        delete bookData.publish_date
      }
      
      // 确保可用数量不大于总数量
      if (bookData.available_copies > bookData.total_copies) {
        alert('可借数量不能大于总数量')
        return
      }
      
      this.$emit('save', bookData)
    }
  }
}
</script>

<style>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.cancel-btn,
.submit-btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.cancel-btn {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  color: #333;
}

.submit-btn {
  background-color: #42b983;
  border: 1px solid #42b983;
  color: white;
}

.submit-btn:hover {
  background-color: #3aa876;
}

@media (max-width: 480px) {
  .modal-container {
    width: 95%;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .cancel-btn,
  .submit-btn {
    width: 100%;
  }
}
</style>