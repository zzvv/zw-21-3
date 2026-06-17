<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">新增用户</el-button>
    </div>
    <el-table :data="list" size="small" border>
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="real_name" label="姓名" width="120" />
      <el-table-column prop="phone" label="电话" width="130" />
      <el-table-column prop="role" label="角色" width="100">
        <template #default="{ row }">
          <el-tag :type="roleType(row.role)" size="small">{{ roleText(row.role) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">{{ row.is_active ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="160">
        <template #default="{ row }">{{ fmtDate(row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button size="small" text type="danger" @click="remove(row.id)">禁用</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="新增用户" width="480px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="用户名"><el-input v-model="form.username" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="form.password" type="password" show-password /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.real_name" /></el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role" style="width: 100%">
            <el-option label="管理员" value="admin" />
            <el-option label="经理" value="manager" />
            <el-option label="教师" value="teacher" />
          </el-select>
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
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listUsers, createUser, deleteUser } from '../api/user.js'

const list = ref([])
const dialogVisible = ref(false)
const form = ref({})

function roleText(r) {
  const map = { admin: '管理员', manager: '经理', teacher: '教师' }
  return map[r] || r
}
function roleType(r) {
  const map = { admin: 'danger', manager: 'warning', teacher: 'success' }
  return map[r] || 'info'
}
function fmtDate(d) {
  if (!d) return '-'
  return d.split('T').join(' ')
}

async function load() {
  list.value = await listUsers()
}

function openDialog() {
  form.value = { role: 'teacher' }
  dialogVisible.value = true
}

async function submit() {
  await createUser(form.value)
  dialogVisible.value = false
  await load()
}

async function remove(id) {
  await ElMessageBox.confirm('确认禁用该用户？', '提示', { type: 'warning' })
  await deleteUser(id)
  await load()
}

onMounted(load)
</script>

<style scoped>
.toolbar { margin-bottom: 12px; }
</style>
