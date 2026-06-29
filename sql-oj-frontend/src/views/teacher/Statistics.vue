<template>
  <div class="statistics">
    <h1>📊 统计分析</h1>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>📈 题目通过率</span>
          </template>
          <div ref="questionChart" style="height: 350px"></div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card>
          <template #header>
            <span>🏆 学生通过率排名</span>
          </template>
          <el-table :data="studentRanking" stripe v-loading="rankingLoading">
            <el-table-column prop="rank" label="排名" width="70">
              <template #default="{ $index }">
                <span :class="{ 'top-rank': $index < 3 }">{{ $index + 1 }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="username" label="学生" />
            <el-table-column prop="pass_rate" label="通过率" width="120">
              <template #default="{ row }">
                <el-progress :percentage="row.pass_rate" :stroke-width="8" />
              </template>
            </el-table-column>
            <el-table-column prop="solved_count" label="通过数" width="80" />
            <el-table-column prop="total_submissions" label="提交次数" width="80" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>📋 整体数据概览</span>
          </template>
          <div class="overview-stats">
            <div class="stat-card">
              <div class="stat-value">{{ overview.total_questions || 0 }}</div>
              <div class="stat-label">题目总数</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ overview.total_submissions || 0 }}</div>
              <div class="stat-label">总提交次数</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ overview.total_users || 0 }}</div>
              <div class="stat-label">注册用户</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ avgPassRate }}%</div>
              <div class="stat-label">平均通过率</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import * as echarts from 'echarts'
import { getQuestionStats, getStudentStats, getOverview } from '../../api/stats'

const rankingLoading = ref(false)
const studentRanking = ref<any[]>([])
const questionStats = ref<any[]>([])
const overview = ref<any>({})

const avgPassRate = computed(() => {
  if (questionStats.value.length === 0) return 0
  const sum = questionStats.value.reduce((acc, q) => acc + (q.pass_rate || 0), 0)
  return Math.round(sum / questionStats.value.length)
})

// 加载题目通过率数据
const loadQuestionStats = async () => {
  try {
    const res = await getQuestionStats()
    questionStats.value = res.data.results || res.data || []
    renderChart()
  } catch (error) {
    console.error('加载题目统计失败', error)
  }
}

// 加载学生排名
const loadStudentStats = async () => {
  rankingLoading.value = true
  try {
    const res = await getStudentStats()
    studentRanking.value = res.data.results || res.data || []
  } catch (error) {
    console.error('加载学生排名失败', error)
  } finally {
    rankingLoading.value = false
  }
}

// 加载概览数据
const loadOverview = async () => {
  try {
    const res = await getOverview()
    overview.value = res.data || {}
  } catch (error) {
    console.error('加载概览数据失败', error)
  }
}

// 渲染图表
const renderChart = () => {
  const chartDom = document.getElementById('questionChart')
  if (!chartDom || questionStats.value.length === 0) return

  const chart = echarts.init(chartDom)
  chart.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: questionStats.value.map(q => q.question_title || `题目${q.question_id}`), axisLabel: { rotate: 30 } },
    yAxis: { type: 'value', name: '通过率 (%)', max: 100 },
    series: [{
      name: '通过率',
      type: 'bar',
      data: questionStats.value.map(q => q.pass_rate || 0),
      itemStyle: {
        borderRadius: [4, 4, 0, 0],
        color: (params: any) => {
          const value = params.value
          if (value >= 80) return '#67c23a'
          if (value >= 60) return '#409eff'
          return '#e6a23c'
        }
      },
      label: { show: true, position: 'top', formatter: '{c}%' }
    }]
  })

  window.addEventListener('resize', () => chart.resize())
}

onMounted(() => {
  loadQuestionStats()
  loadStudentStats()
  loadOverview()
})
</script>

<style scoped>
.statistics {
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f7fa;
}
.overview-stats {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}
.stat-card {
  flex: 1;
  min-width: 150px;
  padding: 20px;
  text-align: center;
  background-color: #f5f7fa;
  border-radius: 8px;
}
.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
}
.stat-label {
  margin-top: 8px;
  color: #909399;
}
.top-rank {
  font-weight: bold;
  color: #e6a23c;
}
</style>