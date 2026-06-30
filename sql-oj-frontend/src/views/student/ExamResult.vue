<template>
  <div class="exam-result-container">
    <div class="header">
      <h1>📊 考试结果</h1>
      <el-button @click="goToSubmissions">查看提交记录 →</el-button>
    </div>

    <div v-loading="loading" class="content">
      <!-- 总分 -->
      <el-card class="score-card">
        <div class="total-score">
          <span class="label">总分</span>
          <span class="value">{{ result.total_score || 0 }}</span>
          <span class="unit">分</span>
        </div>
        <div class="score-detail">
          <span>题目数：{{ result.question_count || 0 }}</span>
          <span>正确数：{{ result.correct_count || 0 }}</span>
        </div>
      </el-card>

      <!-- 每题详情 -->
      <el-card class="detail-card">
        <template #header>
          <span>📝 答题详情</span>
        </template>
        <el-table :data="result.details || []" stripe>
          <el-table-column prop="question_title" label="题目" min-width="150" />
          <el-table-column prop="score" label="得分" width="80" align="center">
            <template #default="{ row }">
              <span :class="{ 'correct': row.score > 0, 'wrong': row.score === 0 }">
                {{ row.score || 0 }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100" align="center">
            <template #default="{ row }">
              <el-tag :type="row.score > 0 ? 'success' : 'danger'" size="small">
                {{ row.score > 0 ? '正确' : '错误' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" align="center">
            <template #default="{ row }">
              <el-button type="primary" link @click="viewSubmission(row.submission_id)">查看SQL</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getExamResult } from '../../api/exams'

const route = useRoute()
const router = useRouter()
const examId = computed(() => Number(route.params.id))

const loading = ref(false)
const result = ref<any>({
  total_score: 0,
  question_count: 0,
  correct_count: 0,
  details: []
})

const loadResult = async () => {
  loading.value = true
  try {
    const res = await getExamResult(examId.value)
    result.value = res.data || {}
  } catch (error) {
    ElMessage.error('加载考试结果失败')
  } finally {
    loading.value = false
  }
}

const goToSubmissions = () => {
  router.push('/submissions')
}

const viewSubmission = (submissionId: number) => {
  if (submissionId) {
    router.push(`/submissions/${submissionId}`)
  }
}

onMounted(() => {
  loadResult()
})
</script>

<style scoped>
.exam-result-container {
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
.content {
  max-width: 800px;
  margin: 0 auto;
}
.score-card {
  margin-bottom: 20px;
  text-align: center;
}
.total-score .label {
  font-size: 16px;
  color: #909399;
}
.total-score .value {
  font-size: 48px;
  font-weight: 700;
  color: #409eff;
  margin: 0 8px;
}
.total-score .unit {
  font-size: 18px;
  color: #909399;
}
.score-detail {
  margin-top: 12px;
  display: flex;
  justify-content: center;
  gap: 30px;
  color: #606266;
}
.correct { color: #67c23a; font-weight: 600; }
.wrong { color: #f56c6c; font-weight: 600; }
</style>