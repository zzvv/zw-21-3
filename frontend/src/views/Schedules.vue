<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">新增排课</el-button>
      <el-select v-model="filterWeekday" placeholder="星期筛选" clearable style="width: 140px; margin-left: 12px;">
        <el-option label="周一" :value="0" />
        <el-option label="周二" :value="1" />
        <el-option label="周三" :value="2" />
        <el-option label="周四" :value="3" />
        <el-option label="周五" :value="4" />
        <el-option label="周六" :value="5" />
        <el-option label="周日" :value="6" />
      </el-select>
    </div>
    <el-table :data="filteredList" size="small" border>
      <el-table-column prop="course.name" label="课程" />
      <el-table-column prop="teacher.name" label="教师" width="100" />
      <el-table-column prop="classroom.name" label="教室" width="100" />
      <el-table-column prop="weekday" label="星期" width="80">
        <template #default="{ row }">{{ weekdayText(row.weekday) }}</template>
      </el-table-column>
      <el-table-column label="时间" width="120">
        <template #default="{ row }">{{ row.start_time }} - {{ row.end_time }}</template>
      </el-table-column>
      <el-table-column prop="start_date" label="开始日期" width="110">
        <template #default="{ row }">{{ fmtDate(row.start_date) }}</template>
      </el-table-column>
      <el-table-column prop="end_date" label="结束日期" width="110">
        <template #default="{ row }">{{ fmtDate(row.end_date) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="140">
        <template #default="{ row }">
          <el-button size="small" text @click="openDialog(row)">编辑</el-button>
          <el-button size="small" text type="danger" @click="remove(row.id)">禁用</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑排课' : '新增排课'" width="520px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="课程">
          <el-select v-model="form.course_id" style="width: 100%">
            <el-option v-for="c in courses" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="教师">
          <el-select v-model="form.teacher_id" style="width: 100%">
            <el-option v-for="t in teachers" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="教室">
          <el-select v-model="form.classroom_id" style="width: 100%">
            <el-option v-for="r in classrooms" :key="r.id" :label="r.name" :value="r.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="星期">
          <el-select v-model="form.weekday" style="width: 100%">
            <el-option label="周一" :value="0" />
            <el-option label="周二" :value="1" />
            <el-option label="周三" :value="2" />
            <el-option label="周四" :value="3" />
            <el-option label="周五" :value="4" />
            <el-option label="周六" :value="5" />
            <el-option label="周日" :value="6" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间"><el-input v-model="form.start_time" placeholder="09:00" /></el-form-item>
        <el-form-item label="结束时间"><el-input v-model="form.end_time" placeholder="10:00" /></el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker v-model="form.start_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="form.end_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
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
import { listSchedules, createSchedule, updateSchedule, deleteSchedule } from '../api/schedule.js'
import { listCourses } from '../api/course.js'
import { listTeachers } from '../api/teacher.js'
import { listClassrooms } from '../api/classroom.js'

const list = ref([])
const courses = ref([])
const teachers = ref([])
const classrooms = ref([])
const filterWeekday = ref('')
const dialogVisible = ref(false)
const form = ref({})

const filteredList = computed(() => {
  if (filterWeekday.value === '') return list.value
  return list.value.filter(s => s.weekday === filterWeekday.value)
})

function weekdayText(w) {
  const map = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  return map[w] || w
}
function fmtDate(d) {
  if (!d) return '-'
  return d.split('T')[0]
}

async function load() {
  list.value = await listSchedules()
  courses.value = await listCourses()
  teachers.value = await listTeachers()
  classrooms.value = await listClassrooms()
}

function openDialog(row = null) {
  form.value = row ? { ...row } : { weekday: 5 }
  dialogVisible.value = true
}

async function submit() {
  const data = { ...form.value }
  if (data.id) {
    await updateSchedule(data.id, data)
  } else {
    await createSchedule(data)
  }
  dialogVisible.value = false
  await load()
}

async function remove(id) {
  await ElMessageBox.confirm('确认禁用该排课？', '提示', { type: 'warning' })
  await deleteSchedule(id)
  await load()
}

onMounted(load)
</script>

<style scoped>
.toolbar { margin-bottom: 12px; }
</style>
