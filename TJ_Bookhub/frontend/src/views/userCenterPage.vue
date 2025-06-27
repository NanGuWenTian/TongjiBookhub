<template>
    <div class="main">
        <div class="personal-center-container">
            <div class="user-profile-card">
                <div class="left-section">
                <div class="avatar-container">
                    <img class="avatar" :src="user.avatarUrl" alt="用户头像" />
                </div>
                <div class="user-info">
                    <p><strong>昵称：</strong> {{ user.nickname }}</p>
                    <p><strong>邮箱：</strong> {{ user.email }}</p>
                    <p><strong>电话号码：</strong> {{ user.phone }}</p>
                    <p><strong>个性签名：</strong> {{ user.signature }}</p>
                </div>
                </div>
                <div class="right-section">
                  <div class="notification-bell">
                      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-bell" viewBox="0 0 16 16">
                      <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zM8 1.918l-.797.161A4.002 4.002 0 0 0 4 6c0 .628-.134 2.197-.459 3.742-.16.767-.376 1.566-.663 2.258h10.244c-.287-.692-.502-1.49-.663-2.258C12.134 8.197 12 6.628 12 6a4.002 4.002 0 0 0-3.203-3.92L8 1.918zM14.22 12c.223.447.481.801.78 1H1c.299-.199.557-.553.78-1C2.68 10.2 3 6.88 3 6c0-2.42 1.72-4.44 4.005-4.901a1 1 0 1 1 1.99 0A5.002 5.002 0 0 1 13 6c0 .88.32 4.2 1.22 6z"/>
                      </svg>
                  </div>
                  <a href="#" class="edit-profile-link" @click.prevent="openEditModal">修改个人信息 ></a>
                </div>
            </div>

            <div class="content-card">
                <div class="recently-viewed-section">
                    <div class="section-header">
                    <h3>最近看过</h3>
                    <div class="view-toggle-controls">
                        <span class="mode-status">当前模式: {{ currentModeText }}</span>
                        <button @click="toggleViewMode" class="toggle-button">
                        切换视图
                        </button>
                    </div>
                    </div>

                    <transition name="view-fade" mode="out-in">
                    <div v-if="!isDetailedView" class="books-container" key="card-view">
                        <div v-if="loading" class="loading-placeholder">加载中...</div>
                        <div v-else class="book-card" v-for="book in books" :key="book.id">
                        <img :src="book.cover" :alt="book.title" class="book-cover" />
                        <div class="book-info">
                            <p class="book-title">{{ book.title }}</p>
                            </div>
                        </div>
                    </div>

                    <div v-else class="details-list-container" key="list-view">
                        <div v-if="loading" class="loading-placeholder">加载中...</div>
                        <div v-else class="detail-item" v-for="book in books" :key="book.id">
                        <div class="detail-info-group">
                            <p class="detail-title">{{ book.title }}</p>
                            <p class="detail-author">作者: {{ book.author }}</p>
                        </div>
                        <div class="detail-date-group">
                            <p>借阅时间: {{ book.borrowDate }}</p>
                            <p>归还期限: {{ book.returnDate }}</p>
                        </div>
                        </div>
                    </div>
                    </transition>
                </div>

                <div class="my-comments-section">
                    <h3>我的评论</h3>
                    <div class="comments-container">
                    <div v-if="loading" class="loading-placeholder">加载中...</div>
                    <div v-else class="comment-item" v-for="comment in comments" :key="comment.id">
                        <p class="comment-content"><strong>评论{{ comment.id }}:</strong> {{ comment.content }}</p>
                        <div class="comment-meta">
                        <span>—— 评论于《{{ comment.bookTitle }}》</span>

                        <div class="comment-actions">
                            <span class="comment-date">{{ comment.date }}</span>
                            <button @click="editComment(comment.id)" class="action-button edit-button">修改</button>
                            <button @click="deleteComment(comment.id)" class="action-button delete-button">删除</button>
                        </div>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
        </div>

        <el-drawer
          v-model="editModalVisible"
          title="编辑个人信息"
          :before-close="handleClose"
        >
          <el-form :model="editForm" label-width="100px" ref="editFormRef">
            <el-form-item label="昵称:" prop="nickname" :rules="[{ required: true, message: '请输入昵称', trigger: 'blur' }]">
              <el-input v-model="editForm.nickname" maxlength="50" show-word-limit />
            </el-form-item>

            <el-form-item label="邮箱:" prop="email" :rules="[{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }]">
              <el-input v-model="editForm.email" />
            </el-form-item>

            <el-form-item label="电话号码:" prop="phone" :rules="[{ pattern: /^[0-9\-+]{0,20}$/, message: '电话号码格式不正确', trigger: 'blur' }]">
              <el-input v-model="editForm.phone" maxlength="20" />
            </el-form-item>

            <el-form-item label="上传头像">
              <el-upload
                  class="avatar-uploader"
                  :show-file-list="false"
                  :auto-upload="false"
                  :on-change="handleFileChange"
                >
                <img v-if="previewUrl" :src="previewUrl" class="avatar-preview" />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
              </el-upload>
            </el-form-item>


            <el-form-item label="个性签名:" prop="signature">
              <el-input
                type="textarea"
                v-model="editForm.signature"
                maxlength="255"
                show-word-limit
                :rows="5"
              />
            </el-form-item>
          </el-form>

          <template #footer>
            <el-button @click="editModalVisible = false">取消</el-button>
            <el-button type="primary" @click="submitEditForm">保存</el-button>
          </template>
        </el-drawer>
    </div>
</template>


<script setup> 
import { ref, onMounted, computed } from 'vue';
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getUserInfo, uploadAvatar, updateUserInfo } from '@/api/user';
import loadingAvatar from '@/assets/avatar/loading.png'
import undefinedAvatar from '@/assets/avatar/undefined.png'

const editModalVisible = ref(false)
const user = ref({
  email: '加载中...',
  nickname: '加载中...',
  phone: '加载中...',
  signature: '加载中...',
  avatarUrl: loadingAvatar
});
const editForm = ref({
  nickname: '',
  email: '',
  phone: '',
  avatar: '',
  signature: ''
})
const editFormRef = ref(null)
const previewUrl = ref('')
const newAvatarFile = ref(null)
const newAvatarUrl = ref('')

const handleFileChange = (file) => {
  previewUrl.value = ''
  newAvatarFile.value = null
  const isJpgOrPng = file.raw.type === 'image/jpeg' || file.raw.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJpgOrPng) {
    ElMessage.error('头像必须是 JPG/PNG 格式!')
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
  }
  
  if (!isJpgOrPng || !isLt2M) {
    return
  }
  
  newAvatarFile.value = file.raw
  const reader = new FileReader()
  reader.readAsDataURL(file.raw)
  reader.onload = (e) => {
    previewUrl.value = e.target.result
  }
}

function openEditModal() {
  editModalVisible.value = true
}

function handleClose(done) {
  done()
}

async function submitEditForm() {
  const valid = await editFormRef.value.validate()
  if (!valid) {
    ElMessage.error('请检查输入项')
    return
  }

  newAvatarUrl.value = null
  if (newAvatarFile.value) {
    const result = await uploadAvatar(newAvatarFile.value)
    console.log(result)
    if (result.code !== 200) {
      ElMessage.error(result.msg || '上传头像失败')
    }
    else {
      newAvatarUrl.value= result.url
    }
  }

  const result = await updateUserInfo({
    nickname: editForm.value.nickname,
    avatar: newAvatarUrl.value,
    phone: editForm.value.phone,
    email: editForm.value.email,
    bio: editForm.value.signature,
  })

  if (result.code !== 200) {
    ElMessage.error(result.msg || '修改用户信息失败')
  }
  else {
    ElMessage.success('修改用户信息成功')
    fetchUserProfile();
  }
  editModalVisible.value = false
}


// --- API 接口预留 ---
const fetchUserProfile = async () => {
  const result  = await getUserInfo();
  if (result.code !== 200) {
    ElMessage.error(result.msg || '加载失败');
    return;
  }
  if (!result.data.nickname) {
    user.value.nickname = '未命名用户'
  }
  else {
    user.value.nickname = result.data.nickname
    editForm.value.nickname = user.value.nickname
  }

  if (!result.data.avatar) {
    user.value.avatarUrl = undefinedAvatar
  }
  else {
    user.value.avatarUrl = result.data.avatar + '?t=' + Date.now()
  }

  if (!result.data.phone) {
    user.value.phone = '未绑定手机号'
  }
  else {
    user.value.phone = result.data.phone
    editForm.value.phone = user.value.phone
  }

  if (!result.data.bio) {
    user.value.signature = '这个人很懒，什么都没写。'
  }
  else {
    user.value.signature = result.data.bio
    editForm.value.signature = user.value.signature
  }

  user.value.email = result.data.email
  editForm.value.email = user.value.email
};

const isDetailedView = ref(false);
const books = ref([]);
// const loading = ref(true);

const currentModeText = computed(() => isDetailedView.value ? '详细模式' : '默认模式');

const toggleViewMode = () => {
  isDetailedView.value = !isDetailedView.value;
};
const fetchRecentlyViewed = async () => {
  loading.value = true;
    books.value = [
      { id: 1, title: '三体', author: '刘慈欣', cover: '', borrowDate: '2025-06-10', returnDate: '2025-07-10' },
      { id: 2, title: '人类简史', author: '尤瓦尔·赫拉利', cover: '', borrowDate: '2025-06-08', returnDate: '2025-07-08' },
      { id: 3, title: '原则', author: '瑞·达利欧', cover: '', borrowDate: '2025-06-05', returnDate: '2025-07-05' },
      { id: 4, title: '深度工作', author: '卡尔·纽波特', cover: '', borrowDate: '2025-06-01', returnDate: '2025-07-01' },
      { id: 5, title: '百年孤独', author: '加西亚·马尔克斯', cover: '', borrowDate: '2025-05-28', returnDate: '2025-06-28' },
      { id: 6, title: '活着', author: '余华', cover: '', borrowDate: '2025-05-25', returnDate: '2025-06-25' },
    ];
    loading.value = false;
};

const comments = ref([]);
const loading = ref(true);

// --- API 接口预留 ---
const fetchMyComments = async () => {
  loading.value = true;

  comments.value = [
    { id: 1, content: '这本书的宇宙观设定真是太宏伟了，读起来让人心潮澎湃，强烈推荐！', bookTitle: '三体', date: '2025-06-15' },
    { id: 2, content: '从一个新的角度审视了人类的发展史，很多观点都非常有启发性。', bookTitle: '人类简史', date: '2025-06-10' },
    { id: 3, content: '不仅仅是投资原则，更是为人处世的哲学。看完之后对工作和生活都有了新的思考。', bookTitle: '原则', date: '2025-05-28' },
    { id: 4, content: '在信息爆炸的时代，深度工作的能力显得尤为重要。这本书提供了切实可行的方法。', bookTitle: '深度工作', date: '2025-05-12' },
    { id: 5, content: '魔幻现实主义的巅峰之作，家族百年的兴衰荣辱让人唏嘘不已。', bookTitle: '百年孤独', date: '2025-04-20' },
  ];
  loading.value = false;

};

// 2. 新增：修改评论的函数 (接口预留)
const editComment = (id) => {
  // 将来这里会调用API，或者弹出一个编辑框
  console.log(`准备修改ID为 ${id} 的评论。`);
  const commentToEdit = comments.value.find(c => c.id === id);
  alert(`正在修改评论：\n"${commentToEdit.content}"`);
};

// 3. 新增：删除评论的函数
const deleteComment = (id) => {
  console.log(`准备删除ID为 ${id} 的评论。`);
  // 实际操作前给用户一个确认提示
  if (confirm('你确定要删除这条评论吗？')) {
    // 从前端列表中移除该评论，实现立即刷新
    comments.value = comments.value.filter(comment => comment.id !== id);
    // 在实际应用中，这里还需要向后端发送一个删除请求
    // fetch(`/api/comments/${id}`, { method: 'DELETE' });
    console.log(`ID为 ${id} 的评论已从界面移除。`);
  }
};

// onMounted 是一个生命周期钩子，在组件挂载到 DOM 后执行
onMounted(() => {
    fetchUserProfile();
    fetchRecentlyViewed();
    fetchMyComments();
});
</script>


<style lang="scss" scoped>
.main {
    margin: 0;
    font-family: 'Noto Sans SC', sans-serif;
    background: linear-gradient(135deg, #e6f7ff 0%, #b3e0ff 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: 20px;
    box-sizing: border-box;
}

.personal-center-container {
    display: flex;
    flex-direction: column;
    gap: 30px;
    margin: 0 auto;
    width: 90%;
    max-width: 1200px;  
    padding: 20px;
}

.content-card {
  background-color: #ffffff;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  overflow: hidden; /* 确保子元素的圆角生效 */
  transition: all 0.3s ease-in-out;
}

.content-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
}

.user-profile-card {
  background-color: #ffffff;
  border-radius: 20px;
  padding: 30px 40px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease-in-out;
}

.user-profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
}

.left-section {
  display: flex;
  align-items: center;
  gap: 30px;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 3px solid #b3e0ff;
  object-fit: cover;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.avatar-text {
  font-size: 14px;
  color: #555;
  font-weight: 500;
}

.user-info {
  font-size: 16px;
  color: #333;
  text-align: left;
}

.user-info p {
  margin: 8px 0;
}

.user-info strong {
  color: #0056b3;
  margin-right: 8px;
}

.right-section {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-between;
  height: 100%;
}

.notification-bell {
  color: #6c757d;
  cursor: pointer;
  transition: color 0.3s ease;
  margin-bottom: 50px; /* 增加与下方链接的距离 */
}

.notification-bell:hover {
  color: #007bff;
}

.edit-profile-link {
  font-size: 16px;
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.edit-profile-link:hover {
  color: #0056b3;
  text-decoration: underline;
}

.recently-viewed-section {
  padding: 20px 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h3 {
  font-size: 22px;
  color: #333;
  margin: 0;
  font-weight: 500;
  border-left: 5px solid #85c1e9;
  padding-left: 15px;
}

.view-toggle-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.mode-status {
  font-size: 14px;
  color: #6c757d;
  background-color: #f8f9fa;
  padding: 5px 10px;
  border-radius: 15px;
  border: 1px solid #dee2e6;
}

.toggle-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 123, 255, 0.2);
}

.toggle-button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 123, 255, 0.3);
}

/* --- 卡片视图样式 --- */
.books-container {
  display: flex;
  gap: 25px;
  overflow-x: auto;
  padding-bottom: 20px;
}
.book-card {
  flex: 0 0 140px;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  padding: 15px;
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}
.book-card:hover {
  transform: translateY(-8px) scale(1.05);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}
.book-cover {
  width: 100px;
  height: 140px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 12px;
}
.book-info {
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.book-info p { margin: 2px 0; }
.book-title {
  font-size: 15px;
  font-weight: 500;
  white-space: normal;
  overflow: visible;
  text-overflow: unset;
  color: #34495e; 
}
.book-author { font-size: 13px; color: #7f8c8d; }

/* --- 详细列表视图样式 --- */
.details-list-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 275px;
  overflow-y: auto;
  padding-right: 10px;
  padding-bottom: 5px;
}
.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 10px;
  border-left: 5px solid transparent;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  flex-shrink: 0;
}
.detail-item:hover {
  transform: translateX(5px);
  border-left-color: #007bff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* 新增的样式规则，确保左对齐 */
.detail-info-group {
  text-align: left;
}

.detail-item p {
  margin: 4px 0;
  font-size: 14px;
  color: #6c757d;
}
.detail-title {
  font-size: 16px;
  font-weight: 500;
  color: #343a40 !important;
}
.detail-author {
  font-size: 14px !important;
  color: #495057 !important;
}
.detail-date-group {
  text-align: right;
  flex-shrink: 0;
  padding-left: 20px;
}

.loading-placeholder {
  width: 100%;
  text-align: center;
  color: #777;
  padding: 100px 0;
}

/* --- Transition 动画 (无变化) --- */
.view-fade-enter-active,
.view-fade-leave-active {
  transition: all 0.4s ease;
}
.view-fade-enter-from,
.view-fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.my-comments-section {
  padding: 20px 30px;
  border-top: 1px solid #e0e0e0;
}

h3 {
  font-size: 22px;
  color: #333;
  margin-top: 10px;
  margin-bottom: 20px;
  font-weight: 500;
  border-left: 5px solid #85c1e9;
  padding-left: 15px;
}

.comments-container {
  height: 300px;
  overflow-y: auto;
  padding-right: 15px;
}

.comment-item {
  border-bottom: 1px dashed #ccc;
  padding: 15px 5px;
  transition: background-color 0.3s;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-item:hover {
    background-color: #f8fcff;
    border-radius: 8px;
}

.comment-content {
  font-size: 16px;
  color: #34495e;
  line-height: 1.6;
  margin: 0 0 10px 0;
}

.comment-content strong {
  color: #2980b9;
}

/* 修改: 让元信息容器垂直居中对齐内部元素 */
.comment-meta {
  font-size: 14px;
  color: #7f8c8d;
  display: flex;
  justify-content: space-between;
  align-items: center; /* 垂直居中 */
}

/* 新增: 操作按钮的容器 */
.comment-actions {
  display: flex;
  align-items: center;
  gap: 15px; /* 设置元素之间的间距 */
}

.comment-date {
  font-style: italic;
  color: #95a5a6; /* 让日期颜色稍浅一些 */
}

/* 新增: 操作按钮的通用样式 */
.action-button {
  background-color: transparent;
  border: 1px solid #dcdcdc;
  border-radius: 5px;
  padding: 4px 10px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

/* 新增: 修改按钮的特定样式 */
.edit-button {
  color: #3498db;
  border-color: #aed6f1;
}

.edit-button:hover {
  background-color: #eaf5fc;
  border-color: #3498db;
}

/* 新增: 删除按钮的特定样式 */
.delete-button {
  color: #e74c3c;
  border-color: #f5b7b1;
}

.delete-button:hover {
  background-color: #fdedec;
  border-color: #e74c3c;
}

.loading-placeholder {
  width: 100%;
  text-align: center;
  color: #777;
  padding: 100px 0;
}

.avatar-uploader {
  :deep() {
    .avatar {
      width: 178px;
      height: 178px;
      display: block;
    }
    .el-upload {
      border: 1px dashed var(--el-border-color);
      border-radius: 6px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      transition: var(--el-transition-duration-fast);
    }
    .el-upload:hover {
      border-color: var(--el-color-primary);
    }
    .el-icon.avatar-uploader-icon {
      font-size: 28px;
      color: #8c939d;
      width: 178px;
      height: 178px;
      text-align: center;
    }
    .avatar-preview {
      width: 100%;
      max-width: 178px;
      height: auto;
      max-height: 178px;
      object-fit: cover;
      // border-radius: 50%;
      border: 1px solid #ccc;
    }
  }
}

</style>