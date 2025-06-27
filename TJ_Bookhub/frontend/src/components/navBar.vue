<template>
  <div class="container-fluid">
    <div class="row">
      <div class="mode-switcher">
        <a style="background: #49AFD0;" href="/index" title="TJBookhub 书" class="header-main-nav-link">
          <span class="hidden-xs">TJBookhub Home</span>
        </a>
      </div>

      <div class="clear"></div>

      <div class="navigation-block theme-switcher-block">
        <div class="navigation-element navigation-theme-switcher">
          <div class="navigation-icon theme-icons">
            <el-icon
              class="theme-icon"
              :class="{ 'active-theme': currentTheme === 'light' }"
              @click="switchTheme('light')"
              title="浅色模式"
            >
              <Sunny />
            </el-icon>
            <el-icon
              class="theme-icon"
              :class="{ 'active-theme': currentTheme === 'dark' }"
              @click="switchTheme('dark')"
              title="深色模式"
            >
              <Moon />
            </el-icon>
          </div>
        </div>
      </div>

      <div class="navigation-block notification-block">
        <section class="navigation-element navigation-notifications" style="position: relative;">
          <div class="navigation-icon" @click="toggleReminderPanel">
            <el-icon><Bell /></el-icon>
            <div class="badge" v-if="hasUnread"></div>
          </div>
          <div class="notifications-board" v-show="showReminderPanel" ref="reminderRef">
            <div class="notifications-board__title">提醒</div>
            <div class="reminder-columns">
              <div class="reminder-column">
                <h4>未读提醒</h4>
                <div v-if="unreadReminders.length === 0" class="empty">暂无未读提醒</div>
                <div v-for="reminder in unreadReminders" :key="reminder.id" class="reminder-item unread">
                  <p class="reminder-content">{{ reminder.content }}</p>
                  <div class="reminder-header">
                    <span class="reminder-time">{{ reminder.created_time }}</span>
                  </div>
                  <el-button type="primary" size="small" @click="handleMarkAsRead(reminder.id)">标记为已读</el-button>
                </div>
              </div>

              <div class="reminder-column">
                <h4>已读提醒</h4>
                <div v-if="readReminders.length === 0" class="empty">暂无已读提醒</div>
                <div v-for="reminder in readReminders" :key="reminder.id" class="reminder-item read">
                  <p class="reminder-content">{{ reminder.content }}</p>
                  <div class="reminder-header">
                    <span class="reminder-time">{{ reminder.created_time }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <div class="navigation-block user-block">
        <el-popover
          placement="bottom-start"
          width="220"
          trigger="hover"
          popper-class="user-popover"
        >
          <template #reference>
            <div class="profile-header__avatar" style="cursor: pointer;">
              <img
                v-if="userInfo.avatar"
                :src="userInfo.avatar"
                alt="用户头像"
                class="avatar-img"
              />
              <div v-else class="profile-header__avatar-letter">U</div>
            </div>
          </template>

          <div class="user-info-card">
            <img :src="userInfo.avatar" alt="头像" class="user-info-card__avatar" />
            <div class="user-info-card__name">{{ userInfo.username }}</div>
            <div class="user-info-card__email">{{ userInfo.email }}</div>
          </div>
        </el-popover>
      </div>

      <div class="navigation-block menu-block">
        <section class="navigation-element navigation-menu-element">
          <div class="navigation-icon" @click="openNavigationMenu" ref="menuButtonRef">
            <el-icon><Menu /></el-icon>
          </div>

          <!-- 菜单面板 -->
          <transition name="fade">
            <div class="navbar-menu" v-show="isMenuOpen" ref="menuRef">
              <div class="navbar-menu__item" @click="router.push('/search')">
                <el-icon><Search /></el-icon>
                <span>书籍搜索</span>
              </div>
              <div class="navbar-menu__item" @click="router.push('/analysis')">
                <el-icon><DataAnalysis /></el-icon>
                <span>阅读数据</span>
              </div>
              <div class="navbar-menu__item" @click="router.push('/event')">
                <el-icon><Star /></el-icon>
                <span>精彩活动</span>
              </div>
              <div class="navbar-menu__item" @click="router.push('/userCenter')">
                <el-icon><User /></el-icon>
                <span>个人中心</span>
              </div>
            </div>
          </transition>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElNotification } from 'element-plus'
import { Bell, Sunny, Moon, Menu, Search, User, Star, DataAnalysis } from '@element-plus/icons-vue'
import { getUserInfoBrief } from '../api/user'
import { getReminders, markReminderAsRead } from '@/api/reminders'
import eventBus from '@/utils/eventBus'

const router = useRouter()

const currentTheme = ref('light')
const isMenuOpen = ref(false)
const menuRef = ref(null)
const menuButtonRef = ref(null)
const userInfo = ref({
  username: '',
  email: '',
  avatar: ''
})

const openNavigationMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const handleClickOutside = (event) => {
  // 检查点击目标是否在菜单或菜单按钮之外
  if (menuRef.value && menuButtonRef.value) {
    const isClickInside = menuRef.value.contains(event.target) || 
                          menuButtonRef.value.contains(event.target);
    if (!isClickInside) {
      isMenuOpen.value = false;
    }
  }
}

const switchTheme = (mode) => {
  const html = document.documentElement
  if (mode === 'dark') {
    html.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    html.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
  currentTheme.value = mode
}

const fetchUserProfile = async () => {
  const result  = await getUserInfoBrief();
  if (result.code !== 200) {
    ElMessage.error(result.msg || '加载失败');
    return;
  }
  userInfo.value.avatar = result.data.avatar + '?t=' + Date.now();
  userInfo.value.username = result.data.username;
  userInfo.value.email = result.data.email;
}

// const reminders = ref([])
const readReminders = ref([])
const unreadReminders = ref([])
const showReminderPanel = ref(false)
const hasUnread = ref(false)

const toggleReminderPanel = () => {
  console.log(showReminderPanel.value)
  showReminderPanel.value = !showReminderPanel.value
}

const fetchReminders = async () => {
  const result = await getReminders()
  if (result.code === 200) {
    unreadReminders.value = result.data.filter(item => !item.is_read)
    readReminders.value = result.data.filter(item => item.is_read)
    hasUnread.value = unreadReminders.value.length > 0
  }
  else{
    ElMessage.error(result.msg || '提醒获取失败');
  }
}

const handleMarkAsRead = async (id) => {
  const res = await markReminderAsRead(id)
  if (res.code === 200) {
    const index = unreadReminders.value.findIndex(r => r.id === id)
    if (index !== -1) {
      const read = unreadReminders.value.splice(index, 1)[0]
      read.is_read = true
      readReminders.value.unshift(read)
    }
    hasUnread.value = unreadReminders.value.length > 0
    ElNotification.success({
      title: '成功',
      message: '已标记为已读',
      position: 'top-left'
    })
  }
  else{
    ElMessage.error(res.msg || '标记已读失败');
  }
}

onMounted(() => {
  fetchUserProfile();
  fetchReminders()
  eventBus.on('updated', () => {
    fetchUserProfile()
  })

  const saved = localStorage.getItem('theme')
  if (saved === 'dark') {
    document.documentElement.classList.add('dark')
  }
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  eventBus.off('avatar-updated')
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.container-fluid {
  padding: 0 15px;
  margin: 0 auto;
  top: 0;
  z-index: 100;
  position: sticky;
  background-color: var(--my-bg-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-end;
  gap: 16px;
  padding: 8px 0;
}

.mode-switcher {
  display: flex;
  align-items: center;
  margin-right: auto;
}

.mode-switcher a {
  padding: 8px 16px;
  color: var(--my-button-text-color);
  background-color: var(--my-button-bg-color);
  border-radius: 5px;
  font-weight: bold;
  text-decoration: none;
  transition: background 0.3s;
  font-size: 14px;
}
.mode-switcher a:hover {
  background-color: var(--my-button-hover-color);
}

.clear {
  flex-grow: 1;
}

/* 通用导航模块间距和效果 */
.navigation-block {
  padding: 4px 10px;
  border-radius: 6px;
  transition: all 0.2s ease;
  margin: 0 6px;
}
.navigation-block:hover {
  background-color: var(--my-hover-bg);
}

.navigation-element {
  position: relative;
}

/* 图标容器统一样式 */
.navigation-icon {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--my-icon-color);
  transition: color 0.2s;
  font-size: 22px;
}
.navigation-icon:hover {
  color: var(--my-icon-hover-color);
}

/* 主题切换图标 */
.theme-icons {
  display: flex;
  align-items: center;
  gap: 12px;
}
.theme-icon {
  width: 36px;
  height: 36px;
  background-color: var(--my-theme-icon-bg);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  color: var(--my-icon-color);
  font-size: 18px;
}
.theme-icon:hover {
  background-color: var(--my-theme-icon-hover-bg);
  transform: scale(1.05);
  color: var(--my-icon-hover-color);
}
.theme-icon.active-theme {
  background-color: var(--my-icon-active-bg);
  color: var(--my-active-text-color);
}
.theme-icon svg {
  font-size: 18px;
}


.badge {
  position: absolute;
  top: 4px;
  right: 4px;
  background-color: #f56c6c;
  border-radius: 50%;
  width: 8px;
  height: 8px;
  border: 2px solid #fff;
}


.notifications-board {
  position: absolute;
  right: 0;
  top: 100%;
  width: 500px;
  max-height: 300px;
  background: var(--my-bg-color);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 10px;
  z-index: 1000;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.notifications-board__title {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 10px;
  text-align: center;
}

.reminder-columns {
  display: flex;
  gap: 10px;
  justify-content: space-between;
}

.reminder-column {
  flex: 1;
  overflow-y: auto;
  max-height: 220px;
  padding-right: 6px;
}

.reminder-column h4 {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 6px;
  text-align: center;
  color: var(--my-text-color);
  border-bottom: 1px solid #ccc;
  padding-bottom: 4px;
}

.reminder-item {
  background-color: #f5f7fa;
  border-radius: 6px;
  padding: 10px;
  border-bottom: 1px solid #e4e4e4;
  margin-bottom: 8px;
  word-break: break-word;
  transition: background 0.3s;
}

.reminder-item.unread {
  background-color: #fff7e6;
}

.reminder-item.read {
  background-color: #f0f0f0;
}

.reminder-content {
  font-size: 13px;
  margin-bottom: 6px;
  color: #333;
}

.reminder-header {
  display: flex;
  justify-content: flex-end;
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.empty {
  font-size: 13px;
  color: #999;
  text-align: center;
  margin-top: 10px;
}


.notification-block .navigation-icon,
.menu-block .navigation-icon {
  font-size: 24px;
  padding: 8px 10px;
}


.profile-header__avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--my-button-bg-color);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border: 2px solid #4dabf7;
  box-shadow: 0 0 5px rgba(77, 171, 247, 0.5);
}
.profile-header__avatar-letter {
  color: white;
  font-weight: bold;
  font-size: 18px;
  border: 2px solid #4dabf7;
  box-shadow: 0 0 5px rgba(77, 171, 247, 0.5);
}
.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 菜单下拉弹窗 */
.navbar-menu {
  position: absolute;
  right: 0;
  top: 120%;
  width: 150px;
  background-color: var(--my-bg-color);
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  padding: 10px 0;
  z-index: 999;
  display: flex;
  flex-direction: column;
}

.navbar-menu__item {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  color: var(--my-text-color);
  cursor: pointer;
  transition: background-color 0.2s ease;
  font-size: 14px;
}
.navbar-menu__item:hover {
  background-color: var(--my-hover-bg);
  color: var(--my-icon-hover-color);
}
.navbar-menu__item el-icon,
.navbar-menu__item .el-icon {
  margin-right: 8px;
  font-size: 16px;
}

/* 动画过渡 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

/* 响应式样式 */
@media (max-width: 768px) {
  .row {
    flex-direction: column;
    align-items: flex-start;
  }

  .mode-switcher,
  .navigation-block {
    margin: 8px 0;
  }

  .navbar-menu {
    width: 100%;
  }
}

.user-info-card {
  text-align: center;
}

.user-info-card__avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 8px;
}

.user-info-card__name {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 4px;
}

.user-info-card__email {
  font-size: 14px;
  color: #666;
  word-break: break-word;
}

:deep(.user-popover) {
  padding: 12px;
  border-radius: 10px;
}
</style>

<style>
/* 默认主题变量 */
:root {
  --my-bg-color: #ffffff;
  --my-text-color: #303133;

  --my-button-bg-color: #49AFD0;
  --my-button-hover-color: #3a9cb8;
  --my-button-text-color: #fff;

  --my-icon-color: #606266;
  --my-icon-hover-color: #409EFF;

  --my-theme-icon-bg: #f4f4f5;
  --my-theme-icon-hover-bg: #e0e0e0;
  --my-icon-active-bg: #409EFF;
  --my-active-text-color: #ffffff;

  --my-hover-bg: rgba(0, 0, 0, 0.05);
}

/* 黑暗模式变量 */
.dark {
  --my-bg-color: #696969;
  --my-text-color: #eeeeee;

  --my-button-bg-color: #5c9bad;
  --my-button-hover-color: #417d8d;
  --my-button-text-color: #fff;

  --my-icon-color: #d3d3d3;
  --my-icon-hover-color: #66b1ff;

  --my-theme-icon-bg: #333;
  --my-theme-icon-hover-bg: #444;
  --my-icon-active-bg: #66b1ff;
  --my-active-text-color: #ffffff;

  --my-hover-bg: rgba(255, 255, 255, 0.05);
}
</style>
