import Vue from 'vue'
import VueRouter from 'vue-router'
import SearchPage from '../views/SearchPage.vue'
import BookDetailedPage from '@/views/BookDetailedPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'SearchPage',
    component: SearchPage
  },
  {
    path: '/book/:id',
    name: 'BookDetail',
    component: BookDetailedPage
  },
  {
    path:'/analysis',
    name:'bookAnalysis',
    component:()=>import('../views/bookAnalysis.vue')
  },
  {
    path:'/event',
    name:'eventRecommend',
    component:()=>import('../views/eventRecommend.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router