<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">新增考级</el-button>
      <el-select v-model="filterStudent" placeholder="学员筛选" clearable filterable style="width: 180px; margin-left: 12px;">
        <el-option v-for="s in students" :key="s.id" :label="s.name" :value="s.id" />
      </el-select>
    </div>
    <el-table :data="filteredList" size="small" border>
      <el-table-column prop="student.name" label="学员" width="100" />
      <el-table-column prop="exam_name" label="考级名称" width="160" />
      <el-table-column prop="instrument" label="乐器" width="100" />
      <el-table-column prop="level" label="级别" width="100" />
      <el-table-column prop="exam_date" label="考试日期" width="110">
        <template #default="{ row }">{{ fmtDate(row.exam_date) }}</template>
      </el-table-column>
      <el-table-column prop="result" label="结果" width="90">
        <template #default="{ row }">
          <el-tag :type="resultType(row.result)" size="small">{{ resultText(row.result) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="score" label="成绩" width="90" />
      <el-table-column prop="certificate_no" label="证书编号" width="140" />
      <el-table-column prop="remark" label="备注" />
      <el-table-column label="操作" width="140">
        <template #default="{ row }">
          <el-button size="small" text @click="openDialog(row)">编辑</el-button>
          <el-button size="small" text type="danger" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑考级' : '新增考级'" width="520px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="学员">
          <el-select v-model="form.student_id" filterable style="width: 100%">
            <el-option v-for="s in students" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="考级名称"><el-input v-model="form.exam_name" /></el-form-item>
        <el-form-item label="乐器"><el-input v-model="form.instrument" /></el-form-item>
        <el-form-item label="级别"><el-input v-model="form.level" /></el-form-item>
        <el-form-item label="考试日期">
          <el-date-picker v-model="form.exam_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="结果">
          <el-select v-model="form.result" style="width: 100%">
            <el-option label="通过" value="passed" />
            <el-option label="未通过" value="failed" />
            <el-option label="待定" value="pending" />
          </el-select>
        </el-form-item>
        <el-form-item label="成绩"><el-input v-model="form.score" /></el-form-item>
        <el-form-item label="证书编号"><el-input v-model="form.certificate_no" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" type="textarea" :rows="2" /></el-form-item>
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
import { listExams, createExam, updateExam, deleteExam } from '../api/exam.js'
import { listStudents } from '../api/student.js'

const list = ref([])
const students = ref([])
const filterStudent = ref('')
const dialogVisible = ref(false)
const form = ref({})

const filteredList = computed(() => {
  if (!filterStudent.value) return list.value
  return list.value.filter(e => e.student_id === filterStudent.value)
})

function resultText(r) {
  const map = { passed: '通过', failed: '未通过', pending: '待定' }
  return map[r] || r
}
function resultType(r) {
  const map = { passed: 'success', failed: 'danger', pending: 'info' }
  return map[r] || 'info'
}
function fmtDate(d) {
  if (!d) return '-'
  return d.split('T')[0]
}

async function load() {
  list.value = await listExams()
  students.value = await listStudents()
}

function openDialog(row = null) {
  form.value = row ? { ...row } : { result: 'pending' }
  dialogVisible.value = true
}

async function submit() {
  const data = { ...form.value }
  if (data.id) {
    await updateExam(data.id, data)
  } else {
    await createExam(data)
  }
  dialogVisible.value = false
  await load()
}

async function remove(id) {
  await ElMessageBox.confirm('确认删除该考级记录？', '提示', { type: 'warning' })
  await deleteExam(id)
  await load()
}

onMounted(load)
</script>

<style scoped>
.toolbar { margin-bottom: 12px; }
</style>
