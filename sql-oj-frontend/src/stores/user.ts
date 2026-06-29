import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '../types/api'
import { login as loginApi, getCurrentUser } from '../api/auth'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))

  // 登录
  const login = async (username: string, password: string) => {
    const res = await loginApi({ username, password })
    token.value = res.data.access
    localStorage.setItem('access_token', res.data.access)
    await fetchUser()
    return res
  }

  // 获取当前用户信息
  const fetchUser = async () => {
    const res = await getCurrentUser()
    user.value = res.data
    localStorage.setItem('user', JSON.stringify(res.data))
  }

  // 登出
  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  // 从本地恢复用户信息
  const restoreUser = () => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      user.value = JSON.parse(storedUser)
    }
  }
  // 在 return 里添加
const isTeacher = computed(() => user.value?.user_type === 'teacher')
const isStudent = computed(() => user.value?.user_type === 'student')

return { user, token, isTeacher, isStudent, login, fetchUser, logout, restoreUser }

})