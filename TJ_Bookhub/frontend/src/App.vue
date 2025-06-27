<template>
  <div id="app">
    <backgroundCartoon v-if="!shouldHideNavbar" />
    <navBar v-if="!shouldHideNavbar" />
    <floatingAI v-if="!shouldHideNavbar" />

    <router-view/>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router'; // 引入路由钩子
import navBar from './components/navBar.vue';
import backgroundCartoon from '@/components/backgroundCartoon';
import floatingAI from '@/components/floatingAI';

const route = useRoute(); // 获取当前路由实例

const adminPrefix = '/admin'; // 定义管理员路径前缀

// 计算属性：根据当前路径动态判断是否隐藏导航栏
const shouldHideNavbar = computed(() => {
  const pathname = route.path;
  // 检查是否是根路径或是否以/admin开头
  return pathname === '/' || pathname.startsWith(adminPrefix) || pathname == '/ai-contact';
});
</script>

<style>
body {
  margin: 0;
}
</style>