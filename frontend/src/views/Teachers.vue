<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">新增教师</el-button>
      <el-select v-model="filterInstrument" placeholder="乐器筛选" clearable style="width: 140px; margin-left: 12px;">
        <el-option label="钢琴" value="钢琴" />
        <el-option label="小提琴" value="小提琴" />
        <el-option label="吉他" value="吉他" />
        <el-option label="古筝" value="古筝" />
      </el-select>
    </div>
    <el-table :data="filteredList" size="small" border>
      <el-table-column prop="name" label="姓名" width="100" />
      <el-table-column prop="phone" label="电话" width="130" />
      <el-table-column prop="instrument" label="擅长乐器" width="100" />
      <el-table-column prop="level" label="级别" width="100">
        <template #default="{ row }">{{ levelText(row.level) }}</template>
      </el-table-column>
      <el-table-column prop="hire_date" label="入职日期" width="110">
        <template #default="{ row }">{{ fmtDate(row.hire_date) }}</template>
      </el-table-column>
      <el-table-column prop="bio" label="简介" />
      <el-table-column label="操作" width="140">
        <template #default="{ row }">
          <el-button size="small" text @click="openDialog(row)">编辑</el-button>
          <el-button size="small" text type="danger" @click="remove(row.id)">禁用</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑教师' : '新增教师'" width="520px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="擅长乐器"><el-input v-model="form.instrument" /></el-form-item>
        <el-form-item label="级别">
          <el-select v-model="form.level" style="width: 100%">
            <el-option label="初级" value="junior" />
            <el-option label="中级" value="intermediate" />
            <el-option label="高级" value="senior" />
          </el-select>
        </el-form-item>
        <el-form-item label="入职日期">
          <el-date-picker v-model="form.hire_date" type="date" value-format="YYYY-MM-DDTHH:mm:ss" style="width: 100%" />
        </el-form-item>
        <el-form-item label="简介"><el-input v-model="form.bio" type="textarea" :rows="3" /></el-form-item>
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
import { listTeachers, createTeacher, updateTeacher, deleteTeacher } from '../api/teacher.js'

const list = ref([])
const filterInstrument = ref('')
const dialogVisible = ref(false)
const form = ref({})

const filteredList = computed(() => {
  if (!filterInstrument.value) return list.value
  return list.value.filter(t => t.instrument === filterInstrument.value)
})

function levelText(l) {
  const map = { junior: '初级', intermediate: '中级', senior: '高级' }
  return map[l] || l
}
function fmtDate(d) {
  if (!d) return '-'
  return d.split('T')[0]
}

async function load() {
  list.value = await listTeachers()
}

function openDialog(row = null) {
  form.value = row ? { ...row } : { level: 'intermediate' }
  dialogVisible.value = true
}

async function submit() {
  const data = { ...form.value }
  if (data.id) {
    await updateTeacher(data.id, data)
  } else {
    await createTeacher(data)
  }
  dialogVisible.value = false
  await load()
}

async function remove(id) {
  await ElMessageBox.confirm('确认禁用该教师？', '提示', { type: 'warning' })
  await deleteTeacher(id)
  await load()
}

onMounted(load)
</script>

<style scoped>
.toolbar { margin-bottom: 12px; }
</style>
