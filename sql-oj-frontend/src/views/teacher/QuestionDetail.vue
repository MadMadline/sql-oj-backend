<template>
  <div class="teacher-question-detail">
    <div class="header">
      <el-button @click="goBack">← 返回题目管理</el-button>
      <h1>📝 题目详情（教师视图）</h1>
    </div>

    <div v-loading="loading" class="content">
      <el-card class="question-info">
        <template #header>
          <div class="card-header">
            <span class="question-title">{{ question.title || '未命名题目' }}</span>
            <el-tag :type="difficultyTagType(question.difficulty)">
              {{ difficultyText(question.difficulty) }}
            </el-tag>
          </div>
        </template>

        <!-- ✅ 教师视图：渲染 Markdown -->
        <div class="section">
          <h3>📖 题目描述</h3>
          <div class="markdown-body" v-html="renderedDescription"></div>
        </div>

        <!-- 建表语句（教师可见） -->
        <div v-if="question.create_table_sql" class="section">
          <h3>📊 建表语句</h3>
          <pre class="sql-block">{{ question.create_table_sql }}</pre>
        </div>

        <!-- 样例输入/输出 -->
        <div class="sample-row">
          <div class="sample-item">
            <h3>📥 样例输入</h3>
            <div class="markdown-body sample-content" v-html="renderedSampleInput"></div>
          </div>
          <div class="sample-item">
            <h3>📤 样例输出</h3>
            <div class="markdown-body sample-content" v-html="renderedSampleOutput"></div>
          </div>
        </div>

        <!-- 教师可见：参考答案 -->
        <div class="section answer-section">
          <h3>🔑 参考答案</h3>
          <div v-if="question.answers && question.answers.length > 0">
            <div v-for="(ans, idx) in question.answers" :key="idx" class="answer-item">
              <span class="answer-label">答案 {{ idx + 1 }}：</span>
              <pre class="answer-sql">{{ ans.correct_sql }}</pre>
            </div>
          </div>
          <div v-else class="no-answer">
            <span style="color: #909399;">暂未设置参考答案</span>
          </div>
        </div>

        <!-- 教师可见：测试用例 -->
        <div class="section test-cases-section">
          <h3>🧪 测试用例</h3>
          <div v-if="question.test_cases && question.test_cases.length > 0">
            <div v-for="(tc, idx) in question.test_cases" :key="idx" class="test-case-item">
              <span class="test-case-label">用例 {{ idx + 1 }}</span>
              <div class="test-case-row">
                <div>
                  <span class="label">测试输入：</span>
                  <pre>{{ tc.test_input || '（空）' }}</pre>
                </div>
                <div>
                  <span class="label">预期输出：</span>
                  <pre>{{ tc.expected_output || '（空）' }}</pre>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="no-answer">
            <span style="color: #909399;">暂未设置测试用例</span>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { marked } from 'marked'
import { getQuestionDetail } from '../../api/questions'

const route = useRoute()
const router = useRouter()
const questionId = computed(() => Number(route.params.id))

const loading = ref(false)
const question = ref<any>({})

// ✅ 配置 marked 渲染选项
marked.setOptions({
  breaks: true,
  gfm: true,
  tables: true
})

const renderMarkdown = (text: string) => {
  if (!text) return ''
  return marked.parse(text)
}

const renderedDescription = computed(() => {
  return renderMarkdown(question.value.description || '暂无描述')
})

const renderedSampleInput = computed(() => {
  return renderMarkdown(question.value.sample_input || '无')
})

const renderedSampleOutput = computed(() => {
  return renderMarkdown(question.value.sample_output || '无')
})

const loadQuestion = async () => {
  loading.value = true
  try {
    const res = await getQuestionDetail(questionId.value)
    question.value = res.data || {}
  } catch (error) {
    ElMessage.error('加载题目失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/teacher/questions')
}

const difficultyTagType = (diff: string) => {
  switch (diff) {
    case 'easy': return 'success'
    case 'medium': return 'warning'
    case 'hard': return 'danger'
    default: return 'info'
  }
}

const difficultyText = (diff: string) => {
  switch (diff) {
    case 'easy': return '简单'
    case 'medium': return '中等'
    case 'hard': return '困难'
    default: return diff || '未知'
  }
}

onMounted(() => {
  loadQuestion()
})
</script>

<style scoped>
.teacher-question-detail {
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
.header h1 {
  margin: 0;
  font-size: 20px;
  color: #2d3748;
}
.content {
  max-width: 1000px;
  margin: 0 auto;
}
.question-info {
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.question-title {
  font-size: 18px;
  font-weight: 600;
  color: #2d3748;
}

.section {
  margin-top: 16px;
}
.section h3 {
  font-size: 15px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 8px;
}

/* ✅ Markdown 样式 */
.markdown-body {
  background-color: #f7fafc;
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #409eff;
  line-height: 1.8;
  font-size: 15px;
  color: #2d3748;
  overflow-x: auto;
}
.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  font-size: 16px;
  font-weight: 600;
  margin: 12px 0 8px;
}
.markdown-body :deep(p) {
  margin: 8px 0;
}
.markdown-body :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 12px 0;
  font-size: 14px;
}
.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid #d1d5db;
  padding: 8px 12px;
  text-align: left;
}
.markdown-body :deep(th) {
  background-color: #e5e7eb;
  font-weight: 600;
}
.markdown-body :deep(code) {
  background-color: #e5e7eb;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
}
.markdown-body :deep(pre) {
  background-color: #1e293b;
  color: #e2e8f0;
  padding: 12px 16px;
  border-radius: 8px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 13px;
}
.markdown-body :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

.sample-content {
  background-color: #f7fafc;
  border-left-color: #e6a23c;
}

.sample-row {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}
.sample-item {
  flex: 1;
}
.sample-item h3 {
  font-size: 14px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 6px;
}

.sql-block,
.answer-sql {
  background-color: #1e293b;
  color: #e2e8f0;
  padding: 12px 16px;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  border: none;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
  overflow-x: auto;
}

.answer-section {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}
.answer-item {
  margin-bottom: 8px;
}
.answer-label {
  font-weight: 500;
  color: #2d3748;
  display: block;
  margin-bottom: 4px;
}

.test-cases-section {
  margin-top: 16px;
}
.test-case-item {
  background-color: #f7fafc;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  border: 1px solid #e2e8f0;
}
.test-case-label {
  font-weight: 600;
  color: #2d3748;
  display: block;
  margin-bottom: 6px;
}
.test-case-row {
  display: flex;
  gap: 16px;
}
.test-case-row > div {
  flex: 1;
}
.test-case-row .label {
  font-size: 13px;
  color: #606266;
}
.test-case-row pre {
  background-color: white;
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
  margin: 4px 0 0;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  white-space: pre-wrap;
  word-break: break-all;
}
.no-answer {
  padding: 12px;
  background-color: #f7fafc;
  border-radius: 8px;
}
</style>