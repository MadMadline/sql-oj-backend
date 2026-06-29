<template>
  <div class="submissions-container">
    <div class="header">
      <el-button @click="goBack">← 返回</el-button>
      <h1>📝 我的提交记录</h1>
    </div>

    <el-table :data="submissions" v-loading="loading" stripe>
      <el-table-column prop="id" label="提交ID" width="80" />
      <el-table-column prop="question" label="题目ID" width="80" />
      <el-table-column prop="submitted_sql" label="提交的SQL" min-width="250">
        <template #default="{ row }">
          <div class="sql-preview">{{ truncateSQL(row.submitted_sql) }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="execution_status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.execution_status)">
            {{ row.execution_status || 'PENDING' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="score" label="得分" width="80" />
      <!-- ✅ 新增：提交时间列 -->
      <el-table-column prop="created_at" label="提交时间" width="180" />
      <!-- ✅ 新增：查看详情操作 -->
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button type="primary" link @click="viewDetail(row)">查看详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        @current-change="loadSubmissions"
        layout="prev, pager, next"
      />
    </div>

    <!-- ✅ 详情弹窗 -->
    <el-dialog v-model="detailVisible" title="提交详情" width="700px">
      <div class="detail-item">
        <strong>提交 ID：</strong>{{ currentDetail.id }}
      </div>
      <div class="detail-item">
        <strong>题目 ID：</strong>{{ currentDetail.question }}
      </div>
      <div class="detail-item">
        <strong>提交的 SQL：</strong>
        <pre class="sql-detail">{{ currentDetail.submitted_sql || '（空）' }}</pre>
      </div>
      <div class="detail-item">
        <strong>判题状态：</strong>
        <el-tag :type="statusTagType(currentDetail.execution_status)">
          {{ currentDetail.execution_status || 'PENDING' }}
        </el-tag>
      </div>
      <div class="detail-item">
        <strong>得分：</strong>{{ currentDetail.score ?? 0 }}
      </div>
      <div class="detail-item" v-if="currentDetail.details">
        <strong>详细结果：</strong>
        <pre class="sql-detail">{{ JSON.stringify(currentDetail.details, null, 2) }}</pre>
      </div>
      <div class="detail-item" v-if="currentDetail.created_at">
        <strong>提交时间：</strong>{{ currentDetail.created_at }}
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getSubmissions } from '../../api/submissions'

const router = useRouter()

const submissions = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// ✅ 详情弹窗相关
const detailVisible = ref(false)
const currentDetail = ref<any>({})

const truncateSQL = (sql: string) => {
  if (!sql) return ''
  if (sql.length > 80) return sql.substring(0, 80) + '...'
  return sql
}

const statusTagType = (status: string) => {
  switch (status) {
    case 'ACCEPTED': return 'success'
    case 'WRONG_ANSWER': return 'danger'
    case 'TIMEOUT': return 'warning'
    default: return 'info'
  }
}

const loadSubmissions = async () => {
  loading.value = true
  try {
    const res = await getSubmissions({ page: currentPage.value })
    submissions.value = res.data.results || []
    total.value = res.data.count || 0
  } catch (error) {
    ElMessage.error('加载提交记录失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/questions')
}

// ✅ 查看详情
const viewDetail = (row: any) => {
  currentDetail.value = row
  detailVisible.value = true
}

onMounted(() => {
  loadSubmissions()
})
</script>

<style scoped>
.submissions-container {
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f7fa;
}
.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  background: white;
  padding: 16px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
.sql-preview {
  font-family: monospace;
  font-size: 12px;
  color: #606266;
}
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* ✅ 详情弹窗样式 */
.detail-item {
  margin-bottom: 12px;
}
.sql-detail {
  background-color: #f5f7fa;
  padding: 12px 16px;
  border-radius: 6px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  white-space: pre-wrap;
  word-break: break-all;
  border: 1px solid #e4e7ed;
  margin: 4px 0 0 0;
  max-height: 200px;
  overflow-y: auto;
}
</style>