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
                  <div class="logout-button" @click="handleLogout" style="cursor: pointer;">
                     <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                      <polyline points="16 17 21 12 16 7"></polyline>
                      <line x1="21" y1="12" x2="9" y2="12"></line>
                    </svg>
                  </div>
                  <a href="#" class="edit-profile-link" @click.prevent="openEditModal">修改个人信息 ></a>
                </div>
            </div>

            <div class="content-card">
                <div class="recently-viewed-section">
                    <div class="section-header">
                    <h3>{{ currentModeTitle }}</h3>
                    <div class="view-toggle-controls">
                        <span class="mode-status">当前模式: {{ currentModeText }}</span>
                        <button @click="toggleViewMode" class="toggle-button">
                        切换视图
                        </button>
                    </div>
                    </div>

                    <transition name="view-fade" mode="out-in">
                      <div v-if="!isDetailedView" class="books-container" key="card-view">
                        <div v-if="loadingrecords" class="loading-placeholder">加载中...</div>

                        <template v-else>
                          <div v-if="books.length === 0" class="no-books-message">
                            我扑在书上就像饥饿的人扑在面包上！你也应该饿了，快去扑到书上吧！
                          </div>
                          <div v-else class="book-card" v-for="book in books" :key="book.id">
                            <img :src="book.cover" :alt="book.title" class="book-cover" />
                            <div class="book-info">
                              <p class="book-title">{{ book.title }}</p>
                            </div>
                          </div>
                        </template>
                      </div>

                      <div v-else class="details-list-container" key="list-view">
                          <div v-if="loadingrecords" class="loading-placeholder">加载中...</div>
                          <template v-else>
                            <div v-if="books.length === 0" class="no-books-message">
                              您还没有任何借阅记录，快去借书吧！
                            </div>
                            <div v-else class="detail-item" v-for="book in books" :key="book.id" :class="statusClass(book.status)">
                              <div class="detail-info-group">
                                <p class="detail-title">{{ book.title }}</p>
                                <p class="detail-author">作者: {{ book.author }}</p>
                              </div>
                              
                              <div class="detail-action-group" v-if="book.status === 'borrowed'">
                                <el-button type="primary" size="small" plain @click="returnBook(book.bookId)">归还</el-button>
                              </div>

                              <div class="detail-action-group" v-if="book.status === 'overdued'">
                                <el-button type="warning" size="small" plain @click="returnBook(book.bookId)">归还</el-button>
                              </div>

                              <div class="detail-date-group fixed-width">
                                <p>借阅时间: {{ formatDateTime(book.borrowDate) }}</p>
                                <p v-if="book.status === 'finished'">归还时间: {{ formatDateTime(book.returnDate) }}</p>
                                <p v-else>到期时间: {{ formatDateTime(book.dueDate) }}</p>
                              </div>
                            </div>
                          </template>
                      </div>
                    
                    </transition>
                </div>

                <div class="my-comments-section">
                    <h3>我的评论</h3>
                    <div class="comments-container">
                    <div v-if="loading" class="loading-placeholder">加载中...</div>
                    <div v-else class="comment-item" v-for="(comment, index) in comments" :key="comment.id">
                        <p class="comment-content"><strong>评论{{ index + 1 }}:</strong> {{ comment.content }}</p>
                        <div class="comment-meta">
                          <div class="left-side">
                            <span>—— 评论于《{{ comment.bookTitle }}》</span>
                            <el-rate
                              v-model="comment.rating"
                              disabled
                              show-score
                              text-color="#ff9900"
                              score-template="{value} 分"
                            />
                          </div>

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

        <el-dialog v-model="editCommentDialogVisible" title="修改评论" width="500px">
          <el-form :model="editCommentForm" label-width="40px">
            <el-form-item label="评分">
              <el-rate v-model="editCommentForm.rating" allow-half clearable
              :texts="['不及格', '及格', '中', '良', '优']"
                show-text
              />
            </el-form-item>
            <el-form-item label="内容">
              <el-input
                type="textarea"
                v-model="editCommentForm.content"
                :rows="5"
                maxlength="500"
                show-word-limit
              />
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="editCommentDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitEditedComment">保存</el-button>
          </template>
        </el-dialog>

    </div>
</template>


<script setup> 
import { ref, onMounted, computed} from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getUserInfo, uploadAvatar, updateUserInfo } from '@/api/user';
import { getBorrowRecords } from '@/api/borrow_records';
import { getUserComments, updateComment, cutComment } from '@/api/comments';
import loadingAvatar from '@/assets/avatar/loading.png'
import undefinedAvatar from '@/assets/avatar/undefined.png'

const router = useRouter()
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

import eventBus from '@/utils/eventBus'
async function submitEditForm() {
  try {
    await editFormRef.value.validate()
  } catch (error) {
    ElNotification.error({message: '请检查输入项', position: 'top-left'})
    return
  }

  newAvatarUrl.value = null
  if (newAvatarFile.value) {
    const result = await uploadAvatar(newAvatarFile.value)
    if (result.code !== 200) {
      ElNotification.error({message: result.msg || '上传头像失败', position: 'top-left'})
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
    ElNotification.error({ message: result.msg || '修改用户信息失败', position: 'top-left' })
  }
  else {
    ElNotification.success({ message: '修改用户信息成功', position: 'top-left' })
    fetchUserProfile();
  }
  editModalVisible.value = false
  eventBus.emit('updated')
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
const loadingrecords = ref(false);
const currentModeText = computed(() => isDetailedView.value ? '详细模式' : '默认模式');
const currentModeTitle = computed(() => isDetailedView.value ? '借阅记录' : '最近看过');
const statusClass = (status) => {
  switch(status) {
    case 'finished':
      return 'status-finished'
    case 'overdued':
      return 'status-overdued'
    case 'borrowed':
      return 'status-borrowed'
    default:
      return ''
  }
}

const formatDateTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
};


function returnBook (bookId) {
  ElMessage.success('点击归还书籍以归还！')
  router.push(`/book/${bookId}`)
}

const toggleViewMode = () => {
  isDetailedView.value = !isDetailedView.value;
  localStorage.setItem('viewMode', isDetailedView.value ? 'detailed' : 'simple');
};

// --- API 接口预留 ---
const fetchRecentlyViewed = async () => {
    loadingrecords.value = true;
    const result = await getBorrowRecords();
    if (result.code !== 200) {
      ElMessage.error(result.msg || '加载失败');
      return;
    }
    loadingrecords.value = false;
    books.value = result.data;
};

const comments = ref([]);
const loading = ref(true);

// --- API 接口预留 ---
const fetchMyComments = async () => {
  loading.value = true;
  const result = await getUserComments();
  if (result.code !== 200) {
    ElMessage.error(result.msg || '加载失败');
    return;
  }
  comments.value = result.data;
  loading.value = false;
};


const editCommentDialogVisible = ref(false);
const editCommentForm = ref({
  id: null,
  content: '',
  rating: 0,
});

const editComment = (id) => {
  const comment = comments.value.find(c => c.id === id);
  if (!comment) return;

  editCommentForm.value = {
    id: comment.id,
    content: comment.content,
    rating: comment.rating
  };
  editCommentDialogVisible.value = true;
};

const submitEditedComment = async () => {
  if (editCommentForm.value.rating === 0) {
    ElNotification.error({ message: '写书不易，至少给个0.5分吧老大！', position: 'top-left' });
    return
  }
  if (editCommentForm.value.content.length === 0) {
    ElNotification.error({ message: '请输入评论内容！', position: 'top-left' });
    return
  }

  const result = await updateComment(editCommentForm.value.id, {
    content: editCommentForm.value.content,
    rating: editCommentForm.value.rating
  });

  if (result.code === 200) {
    ElNotification.success({ message: '评论已更新', position: 'top-left' });
    editCommentDialogVisible.value = false;
    fetchMyComments();
  } else {
    ElNotification.error({ message: '更新评论失败', position: 'top-left' });
  }
};

const deleteComment = async (id) => {
  try {
    await ElMessageBox.confirm('你确定要删除这条评论吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    });

    const result = await cutComment(id);
    if (result.code === 200) {
      ElNotification.success({ message: '删除成功', position: 'top-left' });
      fetchMyComments();
    } else {
      ElNotification.error({ message: result.msg || '删除失败', position: 'top-left' });
    }
  } catch {
    ElMessage.info('取消删除');
  }
};

onMounted(() => {
  const saved = localStorage.getItem('viewMode');
  if (saved === 'detailed') {
    isDetailedView.value = true;
  }
  else {
    isDetailedView.value = false;
  }
  fetchUserProfile();
  fetchRecentlyViewed();
  fetchMyComments();
});

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('theme')
    ElMessage.success('已退出登录')
    router.push('/')
  }).catch(() => {
    ElMessage.info('已取消退出')
  })
}
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

.logout-button {
  color: #6c757d;
  cursor: pointer;
  transition: color 0.3s ease;
  margin-bottom: 50px; /* 增加与下方链接的距离 */
}

.logout-button:hover {
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
.no-books-message {
  margin: 0 auto;
  text-align: center;
  padding: 60px 20px;
  font-size: 20px;
  color: #7d29dc;
}

.books-container {
  display: flex;
  gap: 25px;
  overflow-x: auto;
  padding-bottom: 20px;
  padding-top: 15px;
  padding-left: 5px;
  padding-right: 5px;
}
.book-card {
  flex: 0 0 140px;
  background-color: #fff;
  border: 1px solid rgba(0, 0, 0, 0.1);
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
  border-color: rgba(0, 123, 255, 0.3); 
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
}
.detail-item:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.detail-date-group.fixed-width {
  width: 200px;
  font-size: 14px;
  color: #555;
  margin-right: 20px;
}

/* 新增的样式规则，确保左对齐 */
.detail-info-group {
  text-align: left;
  flex: 1;
  min-width: 200px;
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

.detail-item {
  border-left-width: 5px;
  border-left-style: solid;
}

.status-finished {
  background-color: #e8f5e9;
  border-left-color: #4caf50;
}
.status-overdued {
  background-color: #fdecea;
  border-left-color: #f44336;
}
.status-borrowed {
  background-color: #e3f2fd;
  border-left-color: #2196f3;
}

.status-finished:hover {
  background-color: #c8e6c9;
}
.status-overdued:hover {
  background-color: #f8d7da;
}
.status-borrowed:hover {
  background-color: #bbdefb;
}

.detail-action-group {
  margin-left: auto;
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

  .left-side{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }
}


.comment-actions {
  display: flex;
  align-items: center;
  gap: 15px; 
}

.comment-date {
  font-style: italic;
  color: #95a5a6;
}

.action-button {
  background-color: transparent;
  border: 1px solid #dcdcdc;
  border-radius: 5px;
  padding: 4px 10px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.edit-button {
  color: #3498db;
  border-color: #aed6f1;
}

.edit-button:hover {
  background-color: #eaf5fc;
  border-color: #3498db;
}

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