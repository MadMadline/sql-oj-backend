<template>
  <div class="question-list-container">
    <div class="header">
      <h1>📚 SQL 题库</h1>
      <div class="user-info">
        <span>欢迎，{{ userStore.user?.username }}</span>
        <el-button type="primary" link @click="goToProfile">👤 个人中心</el-button>
        <el-button type="primary" link @click="goToExams">📋 考试</el-button>
        <el-button type="primary" link @click="goToSubmissions">📝 我的提交</el-button>
        <el-button type="danger" size="small" @click="handleLogout">退出</el-button>
      </div>
    </div>

    <el-table :data="questions" v-loading="loading" stripe>
      <el-table-column prop="id" label="题号" width="80" />
      <el-table-column prop="title" label="题目名称" min-width="200">
        <template #default="{ row }">
          <span>{{ row.title || truncateDescription(row.description) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="difficulty" label="难度" width="100">
        <template #default="{ row }">
          <el-tag :type="difficultyTagType(row.difficulty)">
            {{ difficultyText(row.difficulty) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="goToDetail(row.id)">
            开始答题
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        @current-change="loadQuestions"
        layout="prev, pager, next"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '../../stores/user'
import { getQuestions } from '../../api/questions'

const router = useRouter()
const userStore = useUserStore()

const questions = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const truncateDescription = (desc: string) => {
  if (!desc) return '未命名题目'
  if (desc.length > 30) return desc.substring(0, 30) + '...'
  return desc
}

const difficultyTagType = (difficulty: string) => {
  switch (difficulty) {
    case 'easy': return 'success'
    case 'medium': return 'warning'
    case 'hard': return 'danger'
    default: return 'info'
  }
}

const difficultyText = (difficulty: string) => {
  switch (difficulty) {
    case 'easy': return '简单'
    case 'medium': return '中等'
    case 'hard': return '困难'
    default: return difficulty
  }
}

const loadQuestions = async () => {
  loading.value = true
  try {
    const res = await getQuestions({ page: currentPage.value })
    questions.value = res.data.results || []
    total.value = res.data.count || 0
  } catch (error) {
    ElMessage.error('加载题目列表失败')
  } finally {
    loading.value = false
  }
}

const goToProfile = () => {
  router.push('/profile')
}

const goToExams = () => {
  router.push('/exams')
}

const goToDetail = (id: number) => {
  router.push(`/questions/${id}`)
}

const goToSubmissions = () => {
  router.push('/submissions')
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  }).catch(() => {})
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.question-list-container {
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f7fa;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background: white;
  padding: 16px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
.header h1 {
  margin: 0;
  font-size: 22px;
  color: #2d3748;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>