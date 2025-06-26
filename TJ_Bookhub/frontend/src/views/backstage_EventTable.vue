<template>
  <div class="table-page">
    <div class="page-header">
      <h2>活动表</h2>
      
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
            <th>标题</th>
            <th>类型</th>
            <th>开始时间</th>
            <th>结束时间</th>
            <th>地点</th>
            <th>参与人数</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="event in events" :key="event.id" class="table-row">
            <td>{{ event.id }}</td>
            <td>{{ event.title }}</td>
            <td>{{ event.category ? event.category.name : '无' }}</td>
            <td>{{ formatDateTime(event.start_time) }}</td>
            <td>{{ formatDateTime(event.end_time) }}</td>
            <td>{{ event.location }}</td>
            <td>{{ event.participate_counts }}</td>
            <td class="actions">
              <button @click="openEditModal(event)" class="action-button edit">
                <i class="fas fa-edit"></i> 编辑
              </button>
              <button @click="deleteEvent(event.id)" class="action-button delete">
                <i class="fas fa-trash"></i> 删除
              </button>
            </td>
          </tr>
          <tr v-if="events.length === 0" class="empty-row">
            <td colspan="8">暂无活动数据</td>
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
      :formTitle="isEdit ? '编辑活动' : '新增活动'"
      :submitText="isEdit ? '更新' : '创建'"
      :formFields="eventFormFields"
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
const events = ref([]);
const currentPage = ref(1);
const perPage = ref(10);
const totalItems = ref(0);
const totalPages = ref(1);
const loading = ref(false);

// const dataFinished = ref(false);

// 表单数据和验证
const formData = ref({
  title: '',
  type_id: '',
  image: '',
  start_time: '',
  end_time: '',
  location: '',
  brief: '',
  organizer: '',
  theme: '',
  is_featured: false
});

// 表单字段定义
const eventFormFields = [
  {
    name: 'title',
    label: '活动标题',
    type: 'text',
    placeholder: '输入活动标题',
    required: true
  },
  {
    name: 'type_id',
    label: '活动类型',
    type: 'select',
    required: true,
    options: []
  },
  {
    name: 'image',
    label: '图片地址',
    type: 'text',
    placeholder: '输入图片URL'
  },
  {
    name: 'start_time',
    label: '开始时间',
    type: 'date',
    required: true
  },
  {
    name: 'end_time',
    label: '结束时间',
    type: 'date',
    required: true
  },
  {
    name: 'location',
    label: '活动地点',
    type: 'text',
    placeholder: '输入活动地点'
  },
  {
    name: 'brief',
    label: '活动简介',
    type: 'textarea',
    placeholder: '输入活动简介',
    rows: 3
  },
  {
    name: 'organizer',
    label: '主办方',
    type: 'text',
    placeholder: '输入主办方'
  },
  {
    name: 'theme',
    label: '活动主题',
    type: 'text',
    placeholder: '输入活动主题'
  },
  {
    name: 'is_featured',
    label: '是否精选',
    type: 'select',
    options: [
      { value: true, label: '是' },
      { value: false, label: '否' }
    ]
  }
];

// 加载活动类型选项
const fetchEventCategories = async () => {
  try {
    const response = await axios.get('/api/event_category');
    eventFormFields[1].options = response.data.map(category => ({
      value: category.id,
      label: category.name
    }));
  } catch (error) {
    console.error('获取活动类型失败:', error);
  }
};

// 加载活动数据
const fetchEventsData = async (page = 1) => {
  loading.value = true;
  try {
    const response = await axios.get('/api/events', {
      params: {
        page,
        per_page: perPage.value
      }
    });
    events.value = response.data.event_items;
    totalItems.value = response.data.total;
    totalPages.value = response.data.pages;
    currentPage.value = page;
  } catch (error) {
    console.error('获取活动数据失败:', error);
  } finally {
    loading.value = false;
  }
};

// 格式化日期时间
const formatDateTime = (dateTime) => {
  if (!dateTime) return '-';
  const date = new Date(dateTime);
  return date.toLocaleString();
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
const openEditModal = (event) => {


  isEdit.value = true;

  currentRecordId.value = event.id;
  populateFormData(event);

  console.log("数据填充完毕，formData:", formData);
  showModal.value = true;
  
};

// 重置表单数据
const resetFormData = () => {
  formData.value.title = '';
  formData.value.type_id = '';
  formData.value.image = '';
  formData.value.start_time = '';
  formData.value.end_time = '';
  formData.value.location = '';
  formData.value.brief = '';
  formData.value.organizer = '';
  formData.value.theme = '';
  formData.value.is_featured = '';
};

// 填充表单数据
const populateFormData = (event) => {
  // console.log("填充表单数据");

  // console.log("活动标题",event.title);
  formData.value.title = event.title;
  // console.log("活动类型",event.category.id);
  formData.value.type_id = event.category.id;
  // console.log("活动图片",event.image)
  formData.value.image = event.image;
  // console.log("活动开始时间",event.start_time);
  formData.value.start_time = event.start_time ;
  // console.log("活动结束时间",event.end_time);
  formData.value.end_time = event.end_time ;
  // console.log("活动地点",event.location);
  formData.value.location = event.location;
  // console.log("活动简要描述",event.brief);
  formData.value.brief = event.brief;
  // console.log("活动组织者",event.organizer);
  formData.value.organizer = event.organizer;
  // console.log("活动主题",event.theme);
  formData.value.theme = event.theme;
  // console.log("活动是否精选",event.is_featured);
  formData.value.is_featured = event.is_featured;

  // dataFinished.value = true;
};

// 处理表单提交
const handleFormSubmit = async (payload) => {
  try {
    let response;
    if (payload.isEdit) {
      response = await axios.put(`/api/events/${payload.recordId}`, payload.data);
      console.log('更新活动成功:', response.data);
    } else {
      response = await axios.post('/api/events', payload.data);
      console.log('创建活动成功:', response.data);
    }
    showModal.value = false;
    fetchEventsData(currentPage.value);
  } catch (error) {
    console.error('表单提交失败:', error);
  }
};

// 删除活动
const deleteEvent = async (id) => {
  if (confirm('确定要删除这个活动吗？')) {
    try {
      await axios.delete(`/api/events/${id}`);
      console.log('删除活动成功');
      fetchEventsData(currentPage.value);
    } catch (error) {
      console.error('删除活动失败:', error);
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
    fetchEventsData(page);
  }
};


// 生命周期钩子
onMounted(() => {
  fetchEventCategories();
  fetchEventsData();
  currentPage.value = 1;
});

onUnmounted(() => {
  // 清理操作
});
</script>

<!-- <style scoped>
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
      text-align: left;
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
</style> -->

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