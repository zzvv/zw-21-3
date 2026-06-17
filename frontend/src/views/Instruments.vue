<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">新增乐器</el-button>
      <el-select v-model="filterStatus" placeholder="状态筛选" clearable style="width: 140px; margin-left: 12px;">
        <el-option label="可用" value="available" />
        <el-option label="使用中" value="in_use" />
        <el-option label="维修中" value="maintenance" />
        <el-option label="报废" value="retired" />
      </el-select>
    </div>
    <el-table :data="filteredList" size="small" border>
      <el-table-column prop="name" label="名称" width="140" />
      <el-table-column prop="brand" label="品牌" width="120" />
      <el-table-column prop="model" label="型号" width="120" />
      <el-table-column prop="serial_no" label="序列号" width="140" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="purchase_date" label="购买日期" width="110">
        <template #default="{ row }">{{ fmtDate(row.purchase_date) }}</template>
      </el-table-column>
      <el-table-column prop="price" label="价格" width="100">
        <template #default="{ row }">¥{{ row.price }}</template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" text @click="openDialog(row)">编辑</el-button>
          <el-button size="small" text @click="setStatus(row)">状态</el-button>
          <el-button size="small" text type="danger" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑乐器' : '新增乐器'" width="520px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="品牌"><el-input v-model="form.brand" /></el-form-item>
        <el-form-item label="型号"><el-input v-model="form.model" /></el-form-item>
        <el-form-item label="序列号"><el-input v-model="form.serial_no" /></el-form-item>
        <el-form-item label="购买日期">
          <el-date-picker v-model="form.purchase_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="价格"><el-input-number v-model="form.price" :min="0" :precision="2" style="width: 100%" /></el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="可用" value="available" />
            <el-option label="使用中" value="in_use" />
            <el-option label="维修中" value="maintenance" />
            <el-option label="报废" value="retired" />
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
import { listInstruments, createInstrument, updateInstrument, updateInstrumentStatus, deleteInstrument } from '../api/instrument.js'

const list = ref([])
const filterStatus = ref('')
const dialogVisible = ref(false)
const form = ref({})

const filteredList = computed(() => {
  if (!filterStatus.value) return list.value
  return list.value.filter(i => i.status === filterStatus.value)
})

function statusText(s) {
  const map = { available: '可用', in_use: '使用中', maintenance: '维修中', retired: '报废' }
  return map[s] || s
}
function statusType(s) {
  const map = { available: 'success', in_use: 'primary', maintenance: 'warning', retired: 'info' }
  return map[s] || 'info'
}
function fmtDate(d) {
  if (!d) return '-'
  return d.split('T')[0]
}

async function load() {
  list.value = await listInstruments()
}

function openDialog(row = null) {
  form.value = row ? { ...row } : { status: 'available', price: 0 }
  dialogVisible.value = true
}

async function submit() {
  const data = { ...form.value }
  if (data.id) {
    await updateInstrument(data.id, data)
  } else {
    await createInstrument(data)
  }
  dialogVisible.value = false
  await load()
}

async function setStatus(row) {
  const { value } = await ElMessageBox.prompt('请输入新状态（available/in_use/maintenance/retired）', '更新状态', {
    inputValue: row.status,
    confirmButtonText: '确定',
    cancelButtonText: '取消',
  }).catch(() => ({}))
  if (!value) return
  await updateInstrumentStatus(row.id, value)
  await load()
}

async function remove(id) {
  await ElMessageBox.confirm('确认删除该乐器？', '提示', { type: 'warning' })
  await deleteInstrument(id)
  await load()
}

onMounted(load)
</script>

<style scoped>
.toolbar { margin-bottom: 12px; }
</style>
