<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">新增学员</el-button>
      <el-input v-model="search" placeholder="搜索姓名/电话" clearable style="width: 220px; margin-left: 12px;" @keyup.enter="load" />
      <el-select v-model="filterLevel" placeholder="级别筛选" clearable style="width: 140px; margin-left: 12px;">
        <el-option label="初级" value="beginner" />
        <el-option label="中级" value="intermediate" />
        <el-option label="高级" value="advanced" />
      </el-select>
    </div>
    <el-table :data="filteredList" size="small" border>
      <el-table-column prop="name" label="姓名" width="100" />
      <el-table-column prop="phone" label="电话" width="130" />
      <el-table-column prop="parent_name" label="家长姓名" width="100" />
      <el-table-column prop="parent_phone" label="家长电话" width="130" />
      <el-table-column prop="birthday" label="生日" width="110">
        <template #default="{ row }">{{ fmtDate(row.birthday) }}</template>
      </el-table-column>
      <el-table-column prop="level" label="级别" width="90">
        <template #default="{ row }">
          <el-tag :type="levelType(row.level)" size="small">{{ levelText(row.level) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" />
      <el-table-column label="操作" width="140">
        <template #default="{ row }">
          <el-button size="small" text @click="openDialog(row)">编辑</el-button>
          <el-button size="small" text type="danger" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑学员' : '新增学员'" width="520px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="家长姓名"><el-input v-model="form.parent_name" /></el-form-item>
        <el-form-item label="家长电话"><el-input v-model="form.parent_phone" /></el-form-item>
        <el-form-item label="生日">
          <el-date-picker v-model="form.birthday" type="date" value-format="YYYY-MM-DDTHH:mm:ss" style="width: 100%" />
        </el-form-item>
        <el-form-item label="级别">
          <el-select v-model="form.level" style="width: 100%">
            <el-option label="初级" value="beginner" />
            <el-option label="中级" value="intermediate" />
            <el-option label="高级" value="advanced" />
          </el-select>
        </el-form-item>
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
import { listStudents, createStudent, updateStudent, deleteStudent } from '../api/student.js'

const list = ref([])
const search = ref('')
const filterLevel = ref('')
const dialogVisible = ref(false)
const form = ref({})

const filteredList = computed(() => {
  let res = list.value
  if (filterLevel.value) res = res.filter(s => s.level === filterLevel.value)
  return res
})

function levelText(l) {
  const map = { beginner: '初级', intermediate: '中级', advanced: '高级' }
  return map[l] || l
}
function levelType(l) {
  const map = { beginner: 'info', intermediate: 'warning', advanced: 'success' }
  return map[l] || 'info'
}
function fmtDate(d) {
  if (!d) return '-'
  return d.split('T')[0]
}

async function load() {
  list.value = await listStudents({ q: search.value })
}

function openDialog(row = null) {
  form.value = row ? { ...row } : { level: 'beginner' }
  dialogVisible.value = true
}

async function submit() {
  const data = { ...form.value }
  if (data.id) {
    await updateStudent(data.id, data)
  } else {
    await createStudent(data)
  }
  dialogVisible.value = false
  await load()
}

async function remove(id) {
  await ElMessageBox.confirm('确认删除该学员？', '提示', { type: 'warning' })
  await deleteStudent(id)
  await load()
}

onMounted(load)
</script>

<style scoped>
.toolbar { margin-bottom: 12px; }
</style>
