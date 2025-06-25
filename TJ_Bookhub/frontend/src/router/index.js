import { createRouter, createWebHistory } from 'vue-router'
import welcomePage from '../views/welcomePage.vue'
import indexPage from '../views/indexPage.vue'
import searchPage from '../views/searchPage.vue'
import bookDetailedPage from '../views/bookDetailedPage.vue'

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
    path: '/search',
    name: 'searchPage',
    component: searchPage
  },
  {
    path: '/book/:id',
    name: 'bookDetailedPage',
    component: bookDetailedPage
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
