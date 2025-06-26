<template>
  <div class="table-page">
    <div class="page-header">
      <h2>图书表</h2>
      
      <div @click="openCreateModal" class="add-button">
        <svg t="1750696376433" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5987" width="20" height="20">
          <path d="M631.466667 392.533333V0h-238.933334v392.533333H0v238.933334h392.533333V1024h238.933334v-392.533333h392.533333v-238.933334z" fill="#ffffff" p-id="5988">     
          </path>
        </svg>
         <div class="add-button-text">新增</div>
      </div>
    </div>
    
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>序号</th>
            <th>书名</th>
            <th>作者</th>
            <th>ISBN</th>
            <th>出版社</th>
            <th>出版日期</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.id" class="table-row">
            <td>{{ book.id }}</td>
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.isbn }}</td>
            <td>{{ book.publisher }}</td>
            <td>{{ formatDateTime(book.publish_date) }}</td>
            <td class="actions">
              <button @click="openEditModal(book)" class="action-button edit">
                <i class="fas fa-edit"></i> 编辑
              </button>
              <button @click="deleteBook(book.id)" class="action-button delete">
                <i class="fas fa-trash"></i> 删除
              </button>
            </td>
          </tr>
          <tr v-if="books.length === 0" class="empty-row">
            <td colspan="8">暂无图书数据</td>
          </tr>
        </tbody>
      </table>
    </div>
    

    <!-- 分页 -->
    <div class="pagination" v-if="totalPages > 1">
      <button @click="goToPage(1)" :disabled="currentPage === 1" class="page-button">
        首页
      </button>
      
      <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1" class="page-button">
        <svg t="1750706333034" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="33610" width="20" height="20">
          <path d="M368.98014982 512l396.79044788 396.79044789a62.33660968 62.33660968 0 1 1-88.18963346 88.18963346L236.69569962 556.03191401a62.33660968 62.33660968 0 0 1 0-88.06382802L677.64386696 27.01991865a62.33660968 62.33660968 0 1 1 88.063828 88.18963346L369.04305256 512z" p-id="33611">
          </path>
        </svg>
      </button>
      
      <!-- 页码按钮区域 -->
      <div class="page-numbers">
        <!-- 显示页码或省略号 -->
        <div v-for="(item, index) in displayPages" :key="index">
          <button v-if="item !== '...'" 
                  @click="goToPage(item)" 
                  :class="{'page-button active': item === currentPage}"
                  class="page-button">
            {{ item }}
          </button>
          <span v-else class="ellipsis">...</span>
        </div>
      </div>
      
      <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages" class="page-button">
        <svg t="1750706415014" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="33768" width="20" height="20">
          <path d="M648.41999999 512l-378.48-378.48a59.46 59.46 0 1 1 84.12-84.12L774.59999999 470a59.46 59.46 0 0 1 0 84L353.99999999 974.6a59.46 59.46 0 1 1-83.99999999-84.11999999L648.36 512z" p-id="33769"></path>
        </svg>
      </button>
      
      <button @click="goToPage(totalPages)" :disabled="currentPage === totalPages" class="page-button">
        尾页
      </button>
    </div>
    
    <!-- 模态表单 -->
    <!-- :show="showModal" -->
    <formModal
      v-if ="showModal"
      :formTitle="isEdit ? '编辑图书' : '新增图书'"
      :submitText="isEdit ? '更新' : '创建'"
      :formFields="bookFormFields"
      :initialData="formData"
      :isEdit="isEdit"
      :recordId="currentRecordId"
      @submit="handleFormSubmit"
      @close="closeModal"
      />
  </div>
</template>

<script setup>
import { ref,  onMounted, onUnmounted, computed } from 'vue';
import formModal from '@/components/formModal.vue';
import axios from 'axios';

// const router = useRouter();
const showModal = ref(false);
const isEdit = ref(false);
const currentRecordId = ref(null);
const books = ref([]);
const currentPage = ref(1);
const perPage = ref(10);
const totalItems = ref(0);
const totalPages = ref(1);
const loading = ref(false);

// const dataFinished = ref(false);

// 表单数据和验证
const formData = ref({
  title: '',
  category_id: '',
  author: '',
  isbn: '',
  publisher: '',
  publish_date: '',
  total_copies: '',
  description: '',
  cover_image: ''
});

// 表单字段定义
const bookFormFields = [
  {
    name: 'title',
    label: '图书标题',
    type: 'text',
    placeholder: '输入图书标题',
    required: true
  },
  {
    name: 'category_id',
    label: '图书类型',
    type: 'select',
    required: true,
    options: []
  },
  {
    name: 'author',
    label: '作者',
    type: 'text',
    placeholder: '输入作者'
  },
  {
    name: 'isbn',
    label: 'ISBN',
    type: 'text',
    placeholder: '输入ISBN'
  },
  {
    name: 'publisher',
    label: '出版社',
    type: 'text',
    placeholder: '输入出版社'
  },
  {
    name: 'publish_date',
    label: '出版日期',
    type: 'date',
    required: true
  },
  {
    name: 'total_copies',
    label: '可用馆藏数',
    type: 'number',
    placeholder: '输入可用馆藏数',
    required: true
  },
  {
    name: 'description',
    label: '图书简介',
    type: 'textarea',
    placeholder: '输入图书简介',
    rows: 3
  },
  {
    name: 'cover_image',
    label: '封面地址',
    type: 'text',
    placeholder: '输入封面URL'
  }
];

// 加载图书类型选项
const fetchBookCategories = async () => {
  try {
    const response = await axios.get('/api/book_category');
    bookFormFields[1].options = response.data.map(category => ({
      value: category.id,
      label: category.name
    }));
  } catch (error) {
    console.error('获取图书类型失败:', error);
  }
};

// 加载图书数据
const fetchBooksData = async (page = 1) => {
  loading.value = true;
  try {
    const response = await axios.get('/api/books/admin', {
      params: {
        page,
        per_page: perPage.value
      }
    });
    books.value = response.data.book_items;
    totalItems.value = response.data.total;
    totalPages.value = response.data.pages;
    currentPage.value = page;
  } catch (error) {
    console.error('获取图书数据失败:', error);
  } finally {
    loading.value = false;
  }
};

// 格式化日期时间
function formatDateTime(dateString) {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit'
  })
}

// 打开创建模态框
const openCreateModal = () => {
  isEdit.value = false;
  currentRecordId.value = null;
  resetFormData();
  showModal.value = true;
  console.log('您点击了创建按钮，现在正在打开模态表单');
};

// 打开编辑模态框
const openEditModal = (book) => {


  isEdit.value = true;

  currentRecordId.value = book.id;
  populateFormData(book);

  console.log("数据填充完毕，formData:", formData);
  showModal.value = true;
  
};

// 重置表单数据
const resetFormData = () => {
  formData.value.title = '';
  formData.value.category_id = '';
  formData.value.author= '';
  formData.value.isbn = '';
  formData.value.publisher = '';
  formData.value.publish_date = '';
  formData.value.total_copies = '';
  formData.value.description = '';
  formData.value.cover_image = '';
};

// 填充表单数据
const populateFormData = (book) => {
  formData.value.title = book.title;
  formData.value.category_id = book.category;
  formData.value.author = book.author;
  formData.value.isbn = book.isbn;
  formData.value.publisher = book.publisher;
  formData.value.publish_date = book.publish_date;
  console.log("publish_date:", book.publish_date);
  formData.value.total_copies = book.total_copies;
  formData.value.description = book.description;
  formData.value.cover_image = book.cover_image;
};

// 处理表单提交
const handleFormSubmit = async (payload) => {
  try {
    let response;
    if (payload.isEdit) {
      response = await axios.put(`/api/books/admin/${payload.recordId}`, payload.data);
      console.log('更新图书成功:', response.data);
    } else {
      response = await axios.post('/api/books/admin', payload.data);
      console.log('创建图书成功:', response.data);
    }
    showModal.value = false;
    fetchBooksData(currentPage.value);
  } catch (error) {
    console.error('表单提交失败:', error);
  }
};

// 删除图书
const deleteBook = async (id) => {
  if (confirm('确定要删除这个图书吗？')) {
    try {
      await axios.delete(`/api/books/admin/${id}`);
      console.log('删除图书成功');
      fetchBooksData(currentPage.value);
    } catch (error) {
      console.error('删除图书失败:', error);
    }
  }
};

//关闭模态框
const closeModal = () => {
  showModal.value = false;
  resetFormData();
  // dataFinished.value = false; 
}

// 分页相关
const displayPages = computed(() => {
  const pages = [];
  
  // 页数少于5时显示全部页码
  if (totalPages.value <= 5) {
    console.log("当前页面总数小于5为",totalPages.value);
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i);
    }
    console.log("当前处于上半区，页面计算完毕，一共有：",pages);
    // return pages;
  }
  else{
    // 页数超过5时的显示逻辑
    // const current = currentPage.value;
    pages.push(1); // 始终显示第一页
    
    // 计算中间页码范围
    let start = Math.max(2, currentPage.value - 2);
    let end = Math.min(totalPages.value - 1, start + 3); // 中间显示5个页码
    
    // 处理边界情况
    if (start > 2) pages.push('...'); // 前面有省略号
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    if (end < totalPages.value - 1) pages.push('...'); // 后面有省略号
    
    pages.push(totalPages.value); // 始终显示最后一页
    
    // 后面页数超过五，还需要回来验证
    console.log("当前处于下半区，页面计算完毕，一共有：",pages);
  }
  return pages;
});


const goToPage = (page) => {
  // 这里仍然有bug-已解决
  // print( Object.prototype.toString.call(page) );
  // console.log("当前去往页面",page);
  // console.log("当前页面总数",totalPages.value);
  // console.log("当前页面有",displayPages.value);
  if (page >= 1 && page <= totalPages.value) {
    fetchBooksData(page);
  }
};


// 生命周期钩子
onMounted(() => {
  fetchBookCategories();
  fetchBooksData();
  currentPage.value = 1;
});

onUnmounted(() => {
  // 清理操作
});
</script>

<style scoped>
.table-page {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      margin: 0;
      font-size: 24px;
    }

    .add-button {
      background-color: #2ecc71;
      color: white;
      border: none;
      border-radius: 4px;
      padding: 8px 15px;
      cursor: pointer;
      display: flex;
      align-items: center;
      font-weight: 500;
  
      svg {
        margin-right: 5px;
      }
      .add-button-text {
        display: block;
      }
    }
  }


  .table-container {
    overflow-x: auto;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }

  .data-table {
    width: 100%;
    border-collapse: collapse;

    /* 修改表头和表项的样式 */
    th, td {
      padding: 12px 15px;
      text-align: center; /* 水平居中 */
      border-bottom: 1px solid #eee;
      vertical-align: middle; /* 垂直居中 */
    }

    th {
      background-color: #f5f5f5;
      font-weight: 600;
    }
  }

  .table-row {
    &:hover {
      background-color: #f9f9f9;
    }
  }

  .empty-row {
    color: #7f8c8d;
    text-align: center;
  }

  .actions {
    display: flex;
    gap: 5px;
    justify-content: center; /* 让操作按钮水平居中 */
  }

  .action-button {
    background: none;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    display: flex;
    align-items: center;
  }

  .edit {
    background-color: #3498db;
    color: white;
  }

  .delete {
    background-color: #e74c3c;
    color: white;
  }

  .pagination {
    display: flex;
    justify-content: right;
    align-items: center;
    margin-top: 20px;
    padding: 10px 0;
    .page-numbers {
      display: flex;
      align-items: center;
      margin: 0 10px;
    }
    .page-button {
      /* 原有样式保留 */
      
      min-width: 30px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #f5f5f5;
      border: 1px solid #ddd;
      border-radius: 4px;
      padding: 8px 12px;
      cursor: pointer;
      margin: 0 5px;
      transition: background-color 0.3s;

      &:hover:not(:disabled) {
        background-color: #e9e9e9;
      }

      &.active {
        background-color: #3498db;
        color: white;
        border-color: #3498db;
      }

      &:disabled {
        cursor: not-allowed;
        opacity: 0.5;
      }
    }
    .ellipsis {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 30px;
      color: #999;
      font-size: 16px;
    }
    .page-button {
      background-color: #f5f5f5;
      border: 1px solid #ddd;
      border-radius: 4px;
      padding: 8px 12px;
      cursor: pointer;
      margin: 0 5px;
      transition: background-color 0.3s;

      &:hover:not(:disabled) {
        background-color: #e9e9e9;
      }

      &.active {
        background-color: #3498db;
        color: white;
        border-color: #3498db;
      }

      &:disabled {
        cursor: not-allowed;
        opacity: 0.5;
      }
    }

    .page-info {
      margin-left: 10px;
      font-size: 14px;
      color: #7f8c8d;
    }
  }
}
</style> 