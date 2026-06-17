<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">报名登记</el-button>
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 140px; margin-left: 12px;">
        <el-option label="进行中" value="active" />
        <el-option label="已完成" value="completed" />
        <el-option label="已取消" value="cancelled" />
      </el-select>
    </div>
    <el-table :data="filteredList" size="small" border>
      <el-table-column prop="student.name" label="学员" />
      <el-table-column prop="course.name" label="课程" />
      <el-table-column prop="schedule.teacher.name" label="教师" width="100" />
      <el-table-column prop="total_lessons" label="总课时" width="90" />
      <el-table-column prop="used_lessons" label="已用课时" width="90" />
      <el-table-column label="剩余" width="90">
        <template #default="{ row }">{{ row.total_lessons - row.used_lessons }}</template>
      </el-table-column>
      <el-table-column prop="amount" label="金额" width="100">
        <template #default="{ row }">¥{{ row.amount }}</template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button v-if="row.status === 'active'" size="small" text type="primary" @click="consume(row.id)">扣课</el-button>
          <el-button v-if="row.status === 'active'" size="small" text type="danger" @click="cancel(row.id)">取消</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="报名登记" width="480px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="学员">
          <el-select v-model="form.student_id" filterable style="width: 100%">
            <el-option v-for="s in students" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="课程">
          <el-select v-model="form.course_id" style="width: 100%">
            <el-option v-for="c in courses" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="排课时间">
          <el-select v-model="form.schedule_id" style="width: 100%">
            <el-option v-for="s in schedules" :key="s.id" :label="weekdayText(s.weekday) + ' ' + s.start_time + '-' + s.end_time + ' ' + s.teacher?.name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="总课时"><el-input v-model="form.total_lessons" type="number" /></el-form-item>
        <el-form-item label="金额"><el-input v-model="form.amount" type="number" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listEnrollments, createEnrollment, consumeLesson, cancelEnrollment } from '../api/enrollment.js'
import { listStudents } from '../api/student.js'
import { listCourses } from '../api/course.js'
import { listSchedules } from '../api/schedule.js'

const list = ref([])
const students = ref([])
const courses = ref([])
const schedules = ref([])
const filterStatus = ref('')
const dialogVisible = ref(false)
const form = ref({})

const filteredList = computed(() => {
  if (!filterStatus.value) return list.value
  return list.value.filter(e => e.status === filterStatus.value)
})

function weekdayText(w) {
  const map = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  return map[w] || w
}
function statusText(s) {
  const map = { active: '进行中', completed: '已完成', cancelled: '已取消' }
  return map[s] || s
}
function statusType(s) {
  const map = { active: 'primary', completed: 'success', cancelled: 'info' }
  return map[s] || 'info'
}

async function load() {
  list.value = await listEnrollments()
  students.value = await listStudents()
  courses.value = await listCourses()
  schedules.value = await listSchedules()
}

function openDialog() {
  form.value = { total_lessons: 12, amount: 0 }
  dialogVisible.value = true
}

async function submit() {
  await createEnrollment(form.value)
  dialogVisible.value = false
  await load()
}

async function consume(id) {
  await ElMessageBox.confirm('确认扣除一节课时？', '提示', { type: 'warning' })
  await consumeLesson(id)
  ElMessage.success('扣课成功')
  await load()
}

async function cancel(id) {
  await ElMessageBox.confirm('确认取消该报名？', '提示', { type: 'warning' })
  await cancelEnrollment(id)
  await load()
}

onMounted(load)
</script>

<style scoped>
.toolbar { margin-bottom: 12px; }
</style>
