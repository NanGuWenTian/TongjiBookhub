import { createRouter, createWebHistory } from 'vue-router'
import welcomePage from '../views/welcomePage.vue'
import indexPage from '../views/indexPage.vue'
import searchPage from '../views/searchPage.vue'
import bookDetailedPage from '../views/bookDetailedPage.vue'
import bookAnalysis from '../views/bookAnalysis.vue'
import eventRecommend from '../views/eventRecommend.vue'
import eventDetail from '../views/eventDetail.vue'
import userCenterPage from '../views/userCenterPage.vue'
import adminBackage from '../views/adminBackage.vue'
import backstage_EventTable from '../views/backstage_EventTable.vue'
import backstage_EventCategoryTable from '../views/backstage_EventCategoryTable.vue'
import backstage_EventParticipationRecordTable from '../views/backstage_EventParticipationRecordTable.vue'
import backstage_UserTable from '../views/backstage_UserTable.vue'
import backstage_BookTable from '../views/backstage_BookTable.vue'
import backstage_BookCategoryTable from '../views/backstage_BookCategoryTable.vue'
import aiContact from '@/views/aiContact.vue'




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
    component: bookAnalysis
  },
  {
    path: '/event',
    name: 'eventRecommend',
    component: eventRecommend
  },
  {
    path: '/event/detail/:id',
    name: 'eventDetail',
    component: eventDetail
  },
  {
    path: '/userCenter',
    name: 'userCenterPage',
    component: userCenterPage
  },
  {
    path:'/admin',
    name:'admin',
    component:adminBackage,
    children:[
      {
        path:'event-table',
        name:'eventTable',
        component:backstage_EventTable
      },
      {
        path:'event-category-table',
        name:'eventCategoryTable',
        component:backstage_EventCategoryTable
      },
      {
        path:'event-participation-record-table',
        name:'eventParticipationRecordTable',
        component:backstage_EventParticipationRecordTable
      },
      {
        path:'user-table',
        name:'userTable',
        component:backstage_UserTable
      },
      {
        path:'book-table',
        name:'bookTable',
        component:backstage_BookTable
      },
      {
        path:'book-category-table',
        name:'bookCategoryTable',
        component:backstage_BookCategoryTable
      }
    ]
  },
  {
    path:'/ai-contact',
    name:'aiContact',
    component:aiContact
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
