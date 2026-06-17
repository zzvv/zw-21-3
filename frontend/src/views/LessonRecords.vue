<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">记上课</el-button>
    </div>
    <el-table :data="list" size="small" border>
      <el-table-column prop="enrollment.student.name" label="学员" />
      <el-table-column prop="enrollment.course.name" label="课程" />
      <el-table-column prop="lesson_date" label="上课日期" width="110">
        <template #default="{ row }">{{ fmtDate(row.lesson_date) }}</template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.status === 'attended' ? 'success' : 'danger'" size="small">{{ row.status === 'attended' ? '出勤' : '缺勤' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="content" label="上课内容" />
      <el-table-column prop="homework" label="作业" />
      <el-table-column label="操作" width="140">
        <template #default="{ row }">
          <el-button size="small" text @click="openDialog(row)">编辑</el-button>
          <el-button size="small" text type="danger" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑上课记录' : '记上课'" width="480px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="报名记录">
          <el-select v-model="form.enrollment_id" filterable style="width: 100%">
            <el-option v-for="e in activeEnrollments" :key="e.id" :label="e.student?.name + ' - ' + e.course?.name" :value="e.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="上课日期">
          <el-date-picker v-model="form.lesson_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="出勤" value="attended" />
            <el-option label="缺勤" value="absent" />
          </el-select>
        </el-form-item>
        <el-form-item label="上课内容"><el-input v-model="form.content" type="textarea" :rows="2" /></el-form-item>
        <el-form-item label="作业"><el-input v-model="form.homework" type="textarea" :rows="2" /></el-form-item>
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
import { listLessonRecords, createLessonRecord, updateLessonRecord, deleteLessonRecord } from '../api/lessonRecord.js'
import { listEnrollments } from '../api/enrollment.js'

const list = ref([])
const enrollments = ref([])
const dialogVisible = ref(false)
const form = ref({})

const activeEnrollments = computed(() => {
  return enrollments.value.filter(e => e.status === 'active')
})

function fmtDate(d) {
  if (!d) return '-'
  return d.split('T')[0]
}

async function load() {
  list.value = await listLessonRecords()
  enrollments.value = await listEnrollments()
}

function openDialog(row = null) {
  form.value = row ? { ...row } : { status: 'attended' }
  dialogVisible.value = true
}

async function submit() {
  const data = { ...form.value }
  if (data.id) {
    await updateLessonRecord(data.id, data)
  } else {
    await createLessonRecord(data)
  }
  dialogVisible.value = false
  await load()
}

async function remove(id) {
  await ElMessageBox.confirm('确认删除该记录？', '提示', { type: 'warning' })
  await deleteLessonRecord(id)
  await load()
}

onMounted(load)
</script>

<style scoped>
.toolbar { margin-bottom: 12px; }
</style>
