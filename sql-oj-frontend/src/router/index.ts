import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/',
      redirect: '/questions'
    },
    // ========== 学生端页面（无布局）==========
    {
      path: '/questions',
      name: 'QuestionList',
      component: () => import('../views/student/QuestionList.vue'),
      meta: { requiresAuth: true, allowedRoles: ['student', 'teacher'] }
    },
    {
      path: '/questions/:id',
      name: 'QuestionDetail',
      component: () => import('../views/student/QuestionDetail.vue'),
      meta: { requiresAuth: true, allowedRoles: ['student', 'teacher'] }
    },
    {
      path: '/exams',
      name: 'ExamList',
      component: () => import('../views/student/ExamList.vue'),
      meta: { requiresAuth: true, allowedRoles: ['student', 'teacher'] }
    },
    {
      path: '/submissions',
      name: 'MySubmissions',
      component: () => import('../views/student/MySubmissions.vue'),
      meta: { requiresAuth: true, allowedRoles: ['student', 'teacher'] }
    },
    // 在学生端路由中添加
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('../views/Profile.vue'),
      meta: { requiresAuth: true, allowedRoles: ['student', 'teacher'] }
    },
    {
      path: '/exam/:id',
      name: 'ExamPanel',
      component: () => import('../views/student/ExamPanel.vue'),
      meta: { requiresAuth: true, allowedRoles: ['student'] }
    },
    // ========== 教师端页面（使用 Layout）==========
    {
      path: '/teacher',
      component: () => import('../views/teacher/Layout.vue'),
      meta: { requiresAuth: true, allowedRoles: ['teacher'] },
      children: [
        {
          path: 'questions',
          name: 'TeacherQuestionList',
          component: () => import('../views/teacher/QuestionManage.vue')
        },
        {
          path: 'questions/:id',
          name: 'TeacherQuestionDetail',
          component: () => import('../views/teacher/QuestionDetail.vue')
        },
        {
          path: 'questions/create',
          name: 'CreateQuestion',
          component: () => import('../views/teacher/CreateQuestion.vue')
        },
        {
          path: 'exams',
          name: 'ExamManage',
          component: () => import('../views/teacher/ExamManage.vue')
        },
        {
          path: 'stats',
          name: 'Statistics',
          component: () => import('../views/teacher/Statistics.vue')
        },
        {
          path: '',
          redirect: '/teacher/questions'
        }
      ]
    }
  ]
})

// 路由守卫：检查登录 + 角色权限
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null

  // 需要登录但没 token
  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }

  // 检查角色权限
  if (to.meta.allowedRoles && user) {
    if (!to.meta.allowedRoles.includes(user.user_type)) {
      // 无权限，根据身份跳转到对应首页
      if (user.user_type === 'teacher') {
        next('/teacher')
      } else {
        next('/questions')
      }
      return
    }
  }

  next()
})

export default router