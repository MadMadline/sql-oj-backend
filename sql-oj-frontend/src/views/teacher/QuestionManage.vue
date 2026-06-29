<template>
  <div class="manage-container">
    <div class="header">
      <h1>📝 题目管理</h1>
      <div class="actions">
        <el-button type="primary" @click="goToCreate">+ 创建题目</el-button>
        <el-button type="danger" @click="handleLogout">退出</el-button>
      </div>
    </div>

    <el-table :data="questions" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <!-- ✅ 显示题目名称，如果没有则截取描述 -->
      <el-table-column prop="title" label="题目名称" min-width="200">
        <template #default="{ row }">
          <span>{{ row.title || truncateDescription(row.description) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="difficulty" label="难度" width="100">
        <template #default="{ row }">
          <el-tag :type="difficultyTag(row.difficulty)">
            {{ difficultyText(row.difficulty) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="{ row }">
          <el-button type="info" link @click="viewDetail(row.id)">查看</el-button>
          <el-button type="primary" link @click="goToEdit(row.id)">编辑</el-button>
          <el-button type="danger" link @click="handleDelete(row.id)">删除</el-button>
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
import { getQuestions, deleteQuestion } from '../../api/questions'

const router = useRouter()
const userStore = useUserStore()

const questions = ref<any[]>([])
const loading = ref(false)

// ✅ 截取描述作为备选显示
const truncateDescription = (desc: string) => {
  if (!desc) return '未命名题目'
  return desc.length > 30 ? desc.substring(0, 30) + '...' : desc
}

const difficultyTag = (diff: string) => {
  if (diff === 'easy') return 'success'
  if (diff === 'medium') return 'warning'
  return 'danger'
}

const difficultyText = (diff: string) => {
  if (diff === 'easy') return '简单'
  if (diff === 'medium') return '中等'
  return '困难'
}

const loadQuestions = async () => {
  loading.value = true
  try {
    const res = await getQuestions()
    questions.value = res.data.results || res.data || []
  } catch (error) {
    ElMessage.error('加载题目失败')
  } finally {
    loading.value = false
  }
}

const goToCreate = () => {
  router.push('/teacher/questions/create')
}

const goToEdit = (id: number) => {
  router.push(`/teacher/questions/create?id=${id}`)
}

const viewDetail = (id: number) => {
  router.push(`/teacher/questions/${id}`)
}

const handleDelete = (id: number) => {
  ElMessageBox.confirm('确定要删除这道题吗？删除后不可恢复', '提示', {
    confirmButtonText: '确定删除',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteQuestion(id)
      ElMessage.success('删除成功 ✅')
      await loadQuestions()
    } catch (error) {
      ElMessage.error('删除失败，请重试')
    }
  }).catch(() => {
    // 用户取消，不做任何事
  })
}

// ✅ 退出登录增加确认弹窗
const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  }).catch(() => {
    // 用户取消，不做任何事
  })
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.manage-container {
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

.actions {
  display: flex;
  gap: 12px;
}

/* ✅ 表格样式优化 */
.manage-container :deep(.el-table) {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
</style>