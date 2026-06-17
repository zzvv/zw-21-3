<template>
  <div>
    <div class="toolbar">
      <div class="date-selector">
        <el-button @click="prevDay" size="small"><el-icon><ArrowLeft /></el-icon></el-button>
        <el-date-picker v-model="selectedDate" type="date" value-format="YYYY-MM-DD" style="width: 180px" />
        <el-button @click="nextDay" size="small"><el-icon><ArrowRight /></el-icon></el-button>
        <el-button @click="today" size="small" type="primary">今天</el-button>
      </div>
      <div class="legend">
        <span class="legend-item"><span class="legend-dot available"></span>空闲</span>
        <span class="legend-item"><span class="legend-dot occupied"></span>已排课</span>
        <span class="legend-item"><span class="legend-dot maintenance"></span>维修中</span>
      </div>
    </div>

    <div class="board-header">
      <div class="time-column">时间</div>
      <div class="room-columns">
        <div v-for="room in data.classrooms" :key="room.id" class="room-header" :class="{ maintenance: room.status === 'maintenance' }">
          <div class="room-name">{{ room.name }}</div>
          <div class="room-info">{{ room.capacity }}人 / {{ room.piano_count }}台钢琴</div>
        </div>
      </div>
    </div>

    <div class="board-body">
      <div v-for="(slot, index) in timeSlots" :key="index" class="time-row">
        <div class="time-cell">{{ slot.start }}</div>
        <div class="room-cells">
          <div v-for="room in data.classrooms" :key="room.id" class="slot-cell" :class="getCellClass(room, room.slots[index])" @click="handleSlotClick(room, room.slots[index])">
            <div v-if="room.slots[index].occupied" class="occupied-content">
              <div class="course-name">{{ room.slots[index].schedule.course_name }}</div>
              <div class="teacher-name">{{ room.slots[index].schedule.teacher_name }}</div>
              <div class="time-range">{{ room.slots[index].schedule.start_time }}-{{ room.slots[index].schedule.end_time }}</div>
            </div>
            <div v-else-if="room.status === 'maintenance'" class="maintenance-content">
              <el-icon :size="20"><Wrench /></el-icon>
            </div>
            <div v-else class="available-content">
              <span>空闲</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="520px">
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
          <el-select v-model="form.classroom_id" style="width: 100%" :disabled="true">
            <el-option v-for="r in classrooms" :key="r.id" :label="r.name" :value="r.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="星期">
          <el-select v-model="form.weekday" style="width: 100%" :disabled="true">
            <el-option label="周一" :value="0" />
            <el-option label="周二" :value="1" />
            <el-option label="周三" :value="2" />
            <el-option label="周四" :value="3" />
            <el-option label="周五" :value="4" />
            <el-option label="周六" :value="5" />
            <el-option label="周日" :value="6" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间"><el-input v-model="form.start_time" :disabled="true" /></el-form-item>
        <el-form-item label="结束时间"><el-input v-model="form.end_time" :disabled="true" /></el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker v-model="form.start_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="form.end_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitSchedule">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { getClassroomBoard } from '../api/classroom.js'
import { createSchedule } from '../api/schedule.js'
import { listCourses } from '../api/course.js'
import { listTeachers } from '../api/teacher.js'
import { listClassrooms } from '../api/classroom.js'

const selectedDate = ref('')
const data = reactive({ date: '', weekday: 0, classrooms: [] })
const timeSlots = [
  { start: '08:00', end: '09:00' },
  { start: '09:00', end: '10:00' },
  { start: '10:00', end: '11:00' },
  { start: '11:00', end: '12:00' },
  { start: '13:00', end: '14:00' },
  { start: '14:00', end: '15:00' },
  { start: '15:00', end: '16:00' },
  { start: '16:00', end: '17:00' },
  { start: '17:00', end: '18:00' },
  { start: '18:00', end: '19:00' },
  { start: '19:00', end: '20:00' },
  { start: '20:00', end: '21:00' },
]

const dialogVisible = ref(false)
const dialogTitle = ref('')
const form = reactive({})
const courses = ref([])
const teachers = ref([])
const classrooms = ref([])

function getCellClass(room, slot) {
  if (room.status === 'maintenance') return 'maintenance'
  if (slot.occupied) return 'occupied'
  return 'available'
}

async function load() {
  if (!selectedDate.value) {
    const today = new Date()
    selectedDate.value = today.toISOString().split('T')[0]
  }
  data.classrooms = []
  const result = await getClassroomBoard({ date: selectedDate.value })
  Object.assign(data, result)
  courses.value = await listCourses()
  teachers.value = await listTeachers()
  classrooms.value = await listClassrooms()
}

function prevDay() {
  const d = new Date(selectedDate.value)
  d.setDate(d.getDate() - 1)
  selectedDate.value = d.toISOString().split('T')[0]
}

function nextDay() {
  const d = new Date(selectedDate.value)
  d.setDate(d.getDate() + 1)
  selectedDate.value = d.toISOString().split('T')[0]
}

function today() {
  const today = new Date()
  selectedDate.value = today.toISOString().split('T')[0]
}

function handleSlotClick(room, slot) {
  if (room.status === 'maintenance') {
    ElMessage.warning('该教室正在维修中，暂不可用')
    return
  }
  if (slot.occupied) {
    ElMessage.info(`课程：${slot.schedule.course_name}\n教师：${slot.schedule.teacher_name}\n时间：${slot.schedule.start_time}-${slot.schedule.end_time}`)
    return
  }
  dialogTitle.value = `新增排课 - ${room.name} ${slot.time}`
  Object.assign(form, {
    course_id: '',
    teacher_id: '',
    classroom_id: room.id,
    weekday: data.weekday,
    start_time: slot.start_time,
    end_time: slot.end_time,
    start_date: selectedDate.value,
    end_date: '',
  })
  dialogVisible.value = true
}

async function submitSchedule() {
  if (!form.course_id || !form.teacher_id) {
    ElMessage.warning('请选择课程和教师')
    return
  }
  await createSchedule(form)
  dialogVisible.value = false
  ElMessage.success('排课成功')
  await load()
}

watch(selectedDate, load)
onMounted(load)
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.date-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend {
  display: flex;
  gap: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #666;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-dot.available { background: #f0f9eb; border: 1px solid #b7eb8f; }
.legend-dot.occupied { background: #fff7e6; border: 1px solid #ffd591; }
.legend-dot.maintenance { background: #fff2f0; border: 1px solid #ffccc7; }

.board-header {
  display: flex;
  background: #fff;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.time-column {
  width: 70px;
  padding: 12px 8px;
  text-align: center;
  font-weight: 600;
  color: #333;
  background: #f5f7fa;
  border-right: 1px solid #e4e7ed;
}

.room-columns {
  flex: 1;
  display: flex;
}

.room-header {
  flex: 1;
  padding: 12px 8px;
  text-align: center;
  border-right: 1px solid #e4e7ed;
}

.room-header:last-child { border-right: none; }
.room-header.maintenance { background: #fff2f0; }

.room-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.room-info {
  font-size: 12px;
  color: #999;
}

.board-body {
  background: #fff;
  border-radius: 0 0 8px 8px;
  border-top: none;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  overflow: hidden;
}

.time-row {
  display: flex;
  border-bottom: 1px solid #f0f0f0;
}

.time-row:last-child { border-bottom: none; }

.time-cell {
  width: 70px;
  padding: 12px 8px;
  text-align: center;
  font-size: 13px;
  color: #666;
  background: #fafafa;
  border-right: 1px solid #e4e7ed;
}

.room-cells {
  flex: 1;
  display: flex;
}

.slot-cell {
  flex: 1;
  padding: 8px;
  min-height: 80px;
  border-right: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.2s;
}

.slot-cell:last-child { border-right: none; }

.slot-cell.available:hover {
  background: #f6ffed;
}

.slot-cell.occupied:hover {
  background: #fffbe6;
}

.slot-cell.maintenance {
  background: #fff2f0;
  cursor: not-allowed;
}

.occupied-content {
  padding: 6px;
  background: #fff7e6;
  border-radius: 4px;
  border: 1px solid #ffd591;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.course-name {
  font-size: 13px;
  font-weight: 600;
  color: #d46b08;
  margin-bottom: 2px;
}

.teacher-name {
  font-size: 12px;
  color: #8c8c8c;
  margin-bottom: 2px;
}

.time-range {
  font-size: 11px;
  color: #bfbfbf;
}

.available-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #999;
}

.maintenance-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ff4d4f;
}
</style>