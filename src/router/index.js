import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Upload from '../views/Upload.vue'
import Generate from '../views/Generate.vue'
import Templates from '../views/Templates.vue'
import History from '../views/History.vue'
import Settings from '../views/Settings.vue'
import AIChat from '../views/AIChat.vue'

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: {
      title: '首页'
    }
  },
  {
    path: '/upload',
    name: 'Upload',
    component: Upload,
    meta: {
      title: '文件上传'
    }
  },
  {
    path: '/generate',
    name: 'Generate',
    component: Generate,
    meta: {
      title: '报告生成'
    }
  },
  {
    path: '/templates',
    name: 'Templates',
    component: Templates,
    meta: {
      title: '模板库'
    }
  },
  {
    path: '/history',
    name: 'History',
    component: History,
    meta: {
      title: '历史记录'
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: {
      title: '设置'
    }
  },
  {
    path: '/ai-chat',
    name: 'AIChat',
    component: AIChat,
    meta: {
      title: 'AI对话'
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - DocHelper`
  }
  next()
})

export default router
