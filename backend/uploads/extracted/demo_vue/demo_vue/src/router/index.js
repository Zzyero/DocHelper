import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/studio',
    name: 'Studio',
    component: () => import('../views/Studio.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 