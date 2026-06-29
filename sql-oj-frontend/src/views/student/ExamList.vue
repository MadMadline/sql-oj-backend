<template>
  <div class="exam-list-container">
    <div class="header">
      <h1>📋 我的考试</h1>
      <div class="user-info">
        <span>欢迎，{{ userStore.user?.username }}</span>
        <el-button type="primary" link @click="goToQuestions">← 返回题库</el-button>
        <el-button type="danger" size="small" @click="handleLogout">退出</el-button>
      </div>
    </div>

    <!-- ✅ 增加空状态提示 -->
    <div v-if="!loading && exams.length === 0" class="empty-state">
      <el-empty description="暂无考试安排" />
    </div>

    <el-table v-else :data="exams" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="考试名称" min-width="150" />
      <el-table-column prop="start_time" label="开始时间" width="180" />
      <el-table-column prop="end_time" label="结束时间" width="180" />
      <el-table-column prop="total_score" label="总分" width="80" />
      <el-table-column label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="getExamStatus(row).type">
            {{ getExamStatus(row).text }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            @click="enterExam(row.id)"
            :disabled="getExamStatus(row).disabled"
          >
            {{ getExamStatus(row).buttonText }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '../../stores/user'
import { getExams } from '../../api/exams'

const router = useRouter()
const userStore = useUserStore()

const exams = ref<any[]>([])
const loading = ref(false)

const getExamStatus = (exam: any) => {
  const now = new Date()
  const start = new Date(exam.start_time)
  const end = new Date(exam.end_time)

  if (now < start) {
    return { text: '未开始', type: 'info', disabled: true, buttonText: '未开始' }
  } else if (now > end) {
    return { text: '已结束', type: 'danger', disabled: true, buttonText: '已结束' }
  } else {
    return { text: '进行中', type: 'success', disabled: false, buttonText: '进入考试' }
  }
}

// ✅ 修改：加载考试时，如果后端支持按学生过滤，带上 user_id
const loadExams = async () => {
  loading.value = true
  try {
    // 如果后端支持按学生过滤，可以加上 params
    // const res = await getExams({ user_id: userStore.user?.id })
    const res = await getExams()
    exams.value = res.data.results || res.data || []
  } catch (error) {
    ElMessage.error('加载考试列表失败')
  } finally {
    loading.value = false
  }
}

const enterExam = (examId: number) => {
  router.push(`/exam/${examId}`)
}

const goToQuestions = () => {
  router.push('/questions')
}

const handleLogout = () => {
  ElMessageBox.confirm('确定退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出')
  })
}

onMounted(() => {
  loadExams()
})
</script>

<style scoped>
.exam-list-container {
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f7fa;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}
.empty-state {
  margin-top: 60px;
}
</style>