<template>
  <div id="app">
    <navBar v-if="showNavBar" />
    <router-view/>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import navBar from './components/navBar.vue'

const route = useRoute()

const hideNavBarRoutes = ['/', '/admin']

const showNavBar = computed(() => {
  return !hideNavBarRoutes.includes(route.path)
})
</script>

<style>
body {
  margin: 0;
}
</style>
