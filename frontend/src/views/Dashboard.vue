<template>
  <div class="dashboard">
    <el-row :gutter="16">
      <el-col :span="6" v-for="item in statCards" :key="item.label">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" :style="{ color: item.color }">{{ item.value }}</div>
          <div class="stat-label">{{ item.label }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="mt-16">
      <el-col :span="12">
        <el-card>
          <template #header>今日排课</template>
          <el-table :data="weeklySchedule" size="small">
            <el-table-column prop="course.name" label="课程" />
            <el-table-column prop="teacher.name" label="教师" width="100" />
            <el-table-column prop="classroom.name" label="教室" width="100" />
            <el-table-column label="时间" width="120">
              <template #default="{ row }">{{ row.start_time }} - {{ row.end_time }}</template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>最近上课记录</template>
          <el-table :data="recentLessons" size="small">
            <el-table-column prop="enrollment.student.name" label="学员" />
            <el-table-column prop="enrollment.course.name" label="课程" />
            <el-table-column prop="lesson_date" label="日期" width="110">
              <template #default="{ row }">{{ fmtDate(row.lesson_date) }}</template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="90">
              <template #default="{ row }">
                <el-tag :type="row.status === 'attended' ? 'success' : 'danger'" size="small">{{ row.status === 'attended' ? '出勤' : '缺勤' }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="mt-16">
      <el-col :span="12">
        <el-card>
          <template #header>待修乐器提醒</template>
          <el-table :data="lowStockInstruments" size="small">
            <el-table-column prop="name" label="乐器" />
            <el-table-column prop="brand" label="品牌" width="100" />
            <el-table-column prop="model" label="型号" width="120" />
            <el-table-column prop="status" label="状态" width="90">
              <template #default="{ row }">
                <el-tag type="danger" size="small">维修中</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>快捷入口</template>
          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/students')">新增学员</el-button>
            <el-button type="success" @click="$router.push('/enrollments')">报名登记</el-button>
            <el-button type="warning" @click="$router.push('/lesson-records')">记上课</el-button>
            <el-button type="info" @click="$router.push('/schedules')">排课表</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDashboard } from '../api/dashboard.js'

const statCards = ref([])
const weeklySchedule = ref([])
const recentLessons = ref([])
const lowStockInstruments = ref([])

function fmtDate(d) {
  if (!d) return '-'
  return d.split('T')[0]
}

onMounted(async () => {
  const data = await getDashboard()
  const s = data.stats
  statCards.value = [
    { label: '学员总数', value: s.total_students, color: '#409eff' },
    { label: '教师总数', value: s.total_teachers, color: '#67c23a' },
    { label: '课程总数', value: s.total_courses, color: '#e6a23c' },
    { label: '在报学员', value: s.active_enrollments, color: '#409eff' },
    { label: '今日课程', value: s.today_lessons, color: '#67c23a' },
    { label: '待考考级', value: s.pending_exams, color: '#f56c6c' },
    { label: '待修乐器', value: s.low_stock_instruments, color: '#909399' },
    { label: '本月营收', value: '¥' + (s.monthly_revenue || 0).toFixed(2), color: '#f56c6c' },
  ]
  weeklySchedule.value = data.weekly_schedule || []
  recentLessons.value = data.recent_lessons || []
  lowStockInstruments.value = data.low_stock_instruments || []
})
</script>

<style scoped>
.stat-card { text-align: center; }
.stat-value { font-size: 24px; font-weight: 700; }
.stat-label { font-size: 13px; color: #666; margin-top: 6px; }
.mt-16 { margin-top: 16px; }
.quick-actions { display: flex; gap: 12px; flex-wrap: wrap; }
</style>
