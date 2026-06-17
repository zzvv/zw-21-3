<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">新增教室</el-button>
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 140px; margin-left: 12px;">
        <el-option label="空闲" value="available" />
        <el-option label="使用中" value="in_use" />
        <el-option label="维修中" value="maintenance" />
      </el-select>
    </div>
    <el-table :data="filteredList" size="small" border>
      <el-table-column prop="name" label="教室名称" width="150" />
      <el-table-column prop="capacity" label="容纳人数" width="90" />
      <el-table-column prop="piano_count" label="钢琴数量" width="90" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
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

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑教室' : '新增教室'" width="480px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="教室名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="容纳人数"><el-input v-model="form.capacity" type="number" /></el-form-item>
        <el-form-item label="钢琴数量"><el-input v-model="form.piano_count" type="number" /></el-form-item>
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
import { listClassrooms, createClassroom, updateClassroom, deleteClassroom } from '../api/classroom.js'

const list = ref([])
const filterStatus = ref('')
const dialogVisible = ref(false)
const form = ref({})

const filteredList = computed(() => {
  if (!filterStatus.value) return list.value
  return list.value.filter(c => c.status === filterStatus.value)
})

function statusText(s) {
  const map = { available: '空闲', in_use: '使用中', maintenance: '维修中' }
  return map[s] || s
}
function statusType(s) {
  const map = { available: 'success', in_use: 'warning', maintenance: 'danger' }
  return map[s] || 'info'
}

async function load() {
  list.value = await listClassrooms()
}

function openDialog(row = null) {
  form.value = row ? { ...row } : { capacity: 4, piano_count: 1 }
  dialogVisible.value = true
}

async function submit() {
  const data = { ...form.value }
  if (data.id) {
    await updateClassroom(data.id, data)
  } else {
    await createClassroom(data)
  }
  dialogVisible.value = false
  await load()
}

async function remove(id) {
  await ElMessageBox.confirm('确认删除该教室？', '提示', { type: 'warning' })
  await deleteClassroom(id)
  await load()
}

onMounted(load)
</script>

<style scoped>
.toolbar { margin-bottom: 12px; }
</style>
