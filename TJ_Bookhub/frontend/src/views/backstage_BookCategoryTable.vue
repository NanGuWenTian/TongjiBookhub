<template>
  <div class="table-page">
    <div class="page-header">
      <h2>书籍种类表</h2>
      
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
            <th>名称</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="category in categories" :key="category.id" class="table-row">
            <td>{{ category.id }}</td>
            <td>{{ category.name }}</td>
            <td class="actions">
              <button @click="openEditModal(category)" class="action-button edit">
                <i class="fas fa-edit"></i> 编辑
              </button>
              <button @click="deleteCategory(category.id)" class="action-button delete">
                <i class="fas fa-trash"></i> 删除
              </button>
            </td>
          </tr>
          <tr v-if="categories.length === 0" class="empty-row">
            <td colspan="3">暂无书籍种类数据</td>
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
      :formTitle="isEdit ? '编辑书籍种类' : '新增书籍种类'"
      :submitText="isEdit ? '更新' : '创建'"
      :formFields="categoryFormFields"
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

const showModal = ref(false);
const isEdit = ref(false);
const currentRecordId = ref(null);
const categories = ref([]);
const currentPage = ref(1);
const perPage = ref(10);
const totalItems = ref(0);
const totalPages = ref(1);
const loading = ref(false);

// 表单数据和验证
const formData = ref({
  name: ''
});

// 表单字段定义
const categoryFormFields = [
  {
    name: 'name',
    label: '书籍种类名称',
    type: 'text',
    placeholder: '输入书籍种类名称',
    required: true
  }
];

// 加载书籍种类数据
const fetchCategoriesData = async (page = 1) => {
  loading.value = true;
  try {
    const response = await axios.get('/api/book_category', {
      params: {
        page,
        per_page: perPage.value
      }
    });
    categories.value = response.data;
    totalItems.value = response.data.length;
    totalPages.value = Math.ceil(totalItems.value / perPage.value);
    currentPage.value = page;
  } catch (error) {
    console.error('获取书籍种类数据失败:', error);
  } finally {
    loading.value = false;
  }
};

// 打开创建模态框
const openCreateModal = () => {
  isEdit.value = false;
  currentRecordId.value = null;
  resetFormData();
  showModal.value = true;
  console.log('您点击了创建按钮，现在正在打开模态表单');
};

// 打开编辑模态框
const openEditModal = (category) => {
  isEdit.value = true;
  currentRecordId.value = category.id;
  populateFormData(category);
  console.log("数据填充完毕，formData:", formData);
  showModal.value = true;
};

// 重置表单数据
const resetFormData = () => {
  formData.value.name = '';
};

// 填充表单数据
const populateFormData = (category) => {
  formData.value.name = category.name;
};

// 处理表单提交
const handleFormSubmit = async (payload) => {
  try {
    let response;
    if (payload.isEdit) {
      response = await axios.put(`/api/book_category/${payload.recordId}`, payload.data);
      console.log('更新书籍种类成功:', response.data);
    } else {
      response = await axios.post('/api/book_category', payload.data);
      console.log('创建书籍种类成功:', response.data);
    }
    showModal.value = false;
    fetchCategoriesData(currentPage.value);
  } catch (error) {
    console.error('表单提交失败:', error);
  }
};

// 删除书籍种类
const deleteCategory = async (id) => {
  if (confirm('确定要删除这个书籍种类吗？')) {
    try {
      await axios.delete(`/api/book_category/${id}`);
      console.log('删除书籍种类成功');
      fetchCategoriesData(currentPage.value);
    } catch (error) {
      console.error('删除书籍种类失败:', error);
    }
  }
};

//关闭模态框
const closeModal = () => {
  showModal.value = false;
  resetFormData();
};

// 分页相关
const displayPages = computed(() => {
  const pages = [];
  
  // 页数少于5时显示全部页码
  if (totalPages.value <= 5) {
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i);
    }
  }
  else{
    // 页数超过5时的显示逻辑
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
  }
  return pages;
});

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    fetchCategoriesData(page);
  }
};

// 生命周期钩子
onMounted(() => {
  fetchCategoriesData();
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

    th, td {
      padding: 12px 15px;
      text-align: center;
      border-bottom: 1px solid #eee;
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
    justify-content: center;
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