<template>
  <div class="profile-container">
    <div class="header">
      <h1>👤 个人中心</h1>
      <el-button @click="goBack">← 返回</el-button>
    </div>

    <div class="profile-content">
      <!-- 左侧：用户信息卡片 -->
      <el-card class="info-card">
        <template #header>
          <span>📋 个人信息</span>
        </template>
        <div class="avatar-section">
          <el-avatar :size="80" :src="userAvatar">
            {{ userStore.user?.username?.charAt(0)?.toUpperCase() }}
          </el-avatar>
          <div class="user-badge">
            <el-tag :type="userStore.user?.user_type === 'teacher' ? 'warning' : 'success'">
              {{ userStore.user?.user_type === 'teacher' ? '教师' : '学生' }}
            </el-tag>
          </div>
        </div>

        <el-form :model="profileForm" label-width="80px" class="profile-form">
          <el-form-item label="用户名">
            <el-input v-model="profileForm.username" disabled />
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="profileForm.email" placeholder="请输入邮箱" />
          </el-form-item>
          <el-form-item label="身份">
            <el-input :value="userStore.user?.user_type === 'teacher' ? '教师' : '学生'" disabled />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="updateProfile" :loading="updating">
              保存修改
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 右侧：统计数据 -->
      <el-card class="stats-card">
        <template #header>
          <span>📊 个人数据</span>
        </template>

        <div class="stats-grid">
          <!-- 学生统计 -->
          <template v-if="!isTeacher">
            <div class="stat-item">
              <div class="stat-value">{{ stats.total_submissions || 0 }}</div>
              <div class="stat-label">总提交次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.pass_rate != null ? (stats.pass_rate * 100).toFixed(0) : 0 }}%</div>
              <div class="stat-label">通过率</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.passed_questions || 0 }}</div>
              <div class="stat-label">通过题目数</div>
            </div>
          </template>

          <!-- 教师统计 -->
          <template v-if="isTeacher">
            <div class="stat-item">
              <div class="stat-value">{{ stats.questions_created || 0 }}</div>
              <div class="stat-label">创建题目数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ stats.exams_created || 0 }}</div>
              <div class="stat-label">创建考试数</div>
            </div>
          </template>
        </div>

        <!-- 最近提交记录（仅学生可见） -->
        <div v-if="!isTeacher" class="recent-submissions">
          <h4>📝 最近提交</h4>
          <el-table :data="recentSubmissions" v-loading="submissionsLoading" size="small">
            <el-table-column prop="question" label="题目ID" width="70" />
            <el-table-column prop="execution_status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="statusTagType(row.execution_status)" size="small">
                  {{ row.execution_status || 'PENDING' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="score" label="得分" width="60" />
            <el-table-column prop="submission_time" label="提交时间" width="160">
              <template #default="{ row }">
                {{ row.submission_time || row.created_at || '-' }}
              </template>
            </el-table-column>
          </el-table>
          <div v-if="recentSubmissions.length === 0" class="empty-hint">
            暂无提交记录
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'
import { updateUser, getUserStats, getRecentSubmissions } from '../api/users'

const router = useRouter()
const userStore = useUserStore()

const isTeacher = computed(() => userStore.user?.user_type === 'teacher')

const profileForm = ref({
  username: userStore.user?.username || '',
  email: userStore.user?.email || ''
})

// ✅ 使用后端实际返回的字段名
const stats = ref({
  total_submissions: 0,
  pass_rate: 0,
  passed_questions: 0,
  questions_created: 0,
  exams_created: 0
})

const recentSubmissions = ref<any[]>([])
const updating = ref(false)
const submissionsLoading = ref(false)

const userAvatar = computed(() => {
  return userStore.user?.avatar || ''
})

// ✅ 加载统计数据，直接映射后端字段
const loadStats = async () => {
  try {
    const res = await getUserStats()
    const data = res.data || {}
    stats.value = {
      total_submissions: data.total_submissions || 0,
      pass_rate: data.pass_rate || 0,
      passed_questions: data.passed_questions || 0,
      questions_created: data.questions_created || 0,
      exams_created: data.exams_created || 0
    }
  } catch (error) {
    console.log('📊 统计数据接口暂不可用（后端未实现）')
  }
}

const loadRecentSubmissions = async () => {
  submissionsLoading.value = true
  try {
    const res = await getRecentSubmissions()
    const data = res.data.results || res.data || []
    recentSubmissions.value = data.slice(0, 5)
  } catch (error) {
    console.log('📝 最近提交接口暂不可用（后端未实现）')
    recentSubmissions.value = []
  } finally {
    submissionsLoading.value = false
  }
}

const updateProfile = async () => {
  if (!profileForm.value.email) {
    ElMessage.warning('请输入邮箱')
    return
  }

  updating.value = true
  try {
    await updateUser({ email: profileForm.value.email })
    await userStore.fetchUser()
    ElMessage.success('个人信息已更新 ✅')
  } catch (error: any) {
    const msg = error.response?.data?.error || '更新失败，请重试'
    ElMessage.error(msg)
  } finally {
    updating.value = false
  }
}

const goBack = () => {
  if (isTeacher.value) {
    router.push('/teacher')
  } else {
    router.push('/questions')
  }
}

const statusTagType = (status: string) => {
  switch (status) {
    case 'ACCEPTED': return 'success'
    case 'WRONG_ANSWER': return 'danger'
    case 'TIMEOUT': return 'warning'
    default: return 'info'
  }
}

onMounted(() => {
  loadStats()
  loadRecentSubmissions()
})
</script>

<style scoped>
.profile-container {
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

.profile-content {
  display: flex;
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
.info-card {
  flex: 1;
}
.stats-card {
  flex: 2;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}
.user-badge {
  margin-top: 10px;
}

.profile-form {
  margin-top: 10px;
}
.profile-form .el-form-item {
  margin-bottom: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}
.stat-item {
  text-align: center;
  padding: 12px;
  background-color: #f7fafc;
  border-radius: 8px;
}
.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #409eff;
}
.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

.recent-submissions {
  margin-top: 10px;
}
.recent-submissions h4 {
  margin: 0 0 12px 0;
  color: #2d3748;
}
.empty-hint {
  text-align: center;
  color: #c0c4cc;
  padding: 20px 0;
}
</style>