import { createRouter, createWebHistory } from 'vue-router'
// import SearchPage from '../views/SearchPage.vue'
import welcomePage from '../views/welcomePage.vue'
import indexPage from '../views/indexPage.vue'
import BookDetailedPage from '@/views/BookDetailedPage.vue'

const routes = [
  {
    path: '/',
    name: 'welcomePage',
    component: welcomePage
  },
  {
    path: '/index',
    name: 'indexPage',
    component: indexPage
  },
  {
    path: '/book/:id',
    name: 'BookDetail',
    component: BookDetailedPage
  },
  {
    path: '/analysis',
    name: 'bookAnalysis',
    component: () => import('../views/bookAnalysis.vue')
  },
  {
    path: '/event',
    name: 'eventRecommend',
    component: () => import('../views/eventRecommend.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
