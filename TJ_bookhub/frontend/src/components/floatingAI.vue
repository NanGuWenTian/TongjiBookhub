<template>
  <div
    class="floating-drawer"
    ref="box"
    :style="wrapperStyle"
    @mousedown="isExpanded && startDrag($event)"
    @touchstart="isExpanded && startDrag($event)"
  >
    <div class="icon-circle" @click="handleIconClick">
      <!-- <img :src="robot" alt="icon" /> -->
       <svg t="1751030026554" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="6691" width="128" height="128"><path d="M409.6 750.933l34.133 68.267H170.667v136.533h682.666V819.2H580.267l34.133-68.267h238.933A68.267 68.267 0 0 1 921.6 819.2v136.533A68.267 68.267 0 0 1 853.333 1024H170.667a68.267 68.267 0 0 1-68.267-68.267V819.2a68.267 68.267 0 0 1 68.267-68.267H409.6zM273.067 68.267h477.866a68.267 68.267 0 0 1 68.267 68.266V614.4a68.267 68.267 0 0 1-68.267 68.267H273.067A68.267 68.267 0 0 1 204.8 614.4V136.533a68.267 68.267 0 0 1 68.267-68.266z m0 68.266V614.4h477.866V136.533H273.067z m614.4 102.4a34.133 34.133 0 0 1 34.133 34.134v204.8a34.133 34.133 0 1 1-68.267 0v-204.8a34.133 34.133 0 0 1 34.134-34.134z m-750.934 0a34.133 34.133 0 0 1 34.134 34.134v204.8a34.133 34.133 0 0 1-68.267 0v-204.8a34.133 34.133 0 0 1 34.133-34.134zM989.867 307.2A34.133 34.133 0 0 1 1024 341.333V409.6a34.133 34.133 0 1 1-68.267 0v-68.267a34.133 34.133 0 0 1 34.134-34.133z m-955.734 0a34.133 34.133 0 0 1 34.134 34.133V409.6A34.133 34.133 0 0 1 0 409.6v-68.267A34.133 34.133 0 0 1 34.133 307.2z m341.334 102.4a51.2 51.2 0 1 0 0-102.4 51.2 51.2 0 0 0 0 102.4z m273.066 0a51.2 51.2 0 1 0 0-102.4 51.2 51.2 0 0 0 0 102.4zM512 0a34.133 34.133 0 0 1 34.133 34.133V102.4a34.133 34.133 0 0 1-68.266 0V34.133A34.133 34.133 0 0 1 512 0z m-68.267 614.4a34.133 34.133 0 0 1 34.134 34.133v136.534a34.133 34.133 0 1 1-68.267 0V648.533a34.133 34.133 0 0 1 34.133-34.133z m136.534 0a34.133 34.133 0 0 1 34.133 34.133v136.534a34.133 34.133 0 1 1-68.267 0V648.533a34.133 34.133 0 0 1 34.134-34.133z" fill="#ffffff" p-id="6692">        
       </path>
      </svg>
    </div>

    <!-- 展开后才显示文字 -->
    <div v-if="isExpanded" class="text-options">
      <span class="clickable" @click.stop="hideTony">隐藏</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onBeforeUnmount, nextTick } from 'vue'
import { useRouter } from 'vue-router'
// import robot from '@/assets/ai/robot.png'

const router = useRouter()

const box = ref(null)
const isExpanded = ref(false)
const dragging = ref(false)

const drawerWidth = ref(0)
const drawerHeight = ref(0)

const startX = ref(0)
const startY = ref(0)

const circleWidth = 60
const position = ref({ top: window.innerHeight * 0.75 - circleWidth / 2, left: window.innerWidth - circleWidth / 2 })

// 样式绑定
const wrapperStyle = computed(() => ({
  position: 'fixed',
  top: `${position.value.top}px`,
  left: `${position.value.left}px`,
  transition: dragging.value ? 'none' : 'left 0.3s ease',
  zIndex: 9999,
  cursor: isExpanded.value ? 'grab' : 'pointer',
}))

// // 初始设置：右边半隐藏（不可拖动）
const setInitialPosition = () => {
  const circleWidth = 60
  position.value.top = window.innerHeight * 0.75 - circleWidth / 2
  position.value.left = window.innerWidth - circleWidth / 2
}
const setPosition = ()=>{
  if (position.value.left > window.innerWidth /2 - circleWidth / 2)
  position.value.left = window.innerWidth - circleWidth / 2
  else
  position.value.left = 0 - circleWidth / 2
}

// 点击圆形 → 展开并允许拖动
const handleIconClick = () => {
  if (position.value.left >=0 && position.value.left < window.innerWidth - circleWidth / 2)
    {
      openTony();
    }
  else{
    if (!isExpanded.value) {
    expandDrawer()
    }
  }
}

// 展开滑出逻辑
const expandDrawer = () => {
  isExpanded.value = true
  nextTick(() => {
    drawerWidth.value = box.value.offsetWidth
    drawerHeight.value = box.value.offsetHeight
    if (position.value.left <0)
      position.value.left = 0
    else
      position.value.left = window.innerWidth - drawerWidth.value
  })
}

// 点击“打开Tony”跳转页面
const openTony = () => {
  console.log("点击跳转到人工智能页面");
  
  router.push('/ai-contact');
}

// 点击“隐藏Tony”恢复初始状态
const hideTony = () => {
  isExpanded.value = false
  dragging.value = false
  setTimeout(() => {
    setPosition()
  }, 100)
}

// 拖动逻辑
const startDrag = (e) => {
  const event = e.type.includes('touch') ? e.touches[0] : e
  dragging.value = true
  startX.value = event.clientX - position.value.left
  startY.value = event.clientY - position.value.top

  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
  document.addEventListener('touchmove', onDrag, { passive: false })
  document.addEventListener('touchend', stopDrag)
}

const onDrag = (e) => {
  const event = e.type.includes('touch') ? e.touches[0] : e
  e.preventDefault()
  const maxLeft = window.innerWidth - drawerWidth.value
  const maxTop = window.innerHeight - drawerHeight.value

  let newLeft = event.clientX - startX.value
  let newTop = event.clientY - startY.value

  position.value.left = Math.max(0, Math.min(newLeft, maxLeft))
  position.value.top = Math.max(0, Math.min(newTop, maxTop))
}

const stopDrag = () => {
  dragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('touchend', stopDrag)
}


onBeforeUnmount(() => {
  stopDrag()
  window.removeEventListener('resize', setInitialPosition)
})
</script>

<style scoped>
.floating-drawer {
  display: flex;
  flex-direction: column;
  align-items: center;
  user-select: none;
}

.icon-circle {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #60cfff, #4798ff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  overflow: hidden;
}

.icon-circle img {
  width: 80%;
  height: 80%;
}

.text-options {
  margin-top: -15px;
  background: linear-gradient(135deg, #60cfff, #4798ff);
  color: white;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 14px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  white-space: nowrap;
}
</style>
