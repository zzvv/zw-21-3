<template>
  <div>
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">新增课程</el-button>
      <el-select v-model="filterInstrument" placeholder="乐器筛选" clearable style="width: 140px; margin-left: 12px;">
        <el-option label="钢琴" value="钢琴" />
        <el-option label="小提琴" value="小提琴" />
        <el-option label="吉他" value="吉他" />
        <el-option label="古筝" value="古筝" />
      </el-select>
    </div>
    <el-table :data="filteredList" size="small" border>
      <el-table-column prop="name" label="课程名称" />
      <el-table-column prop="instrument" label="乐器" width="100" />
      <el-table-column prop="duration_minutes" label="时长(分)" width="90" />
      <el-table-column prop="price" label="单价" width="100">
        <template #default="{ row }">¥{{ row.price }}</template>
      </el-table-column>
      <el-table-column prop="max_students" label="最大人数" width="90" />
      <el-table-column prop="teacher.name" label="任课教师" width="100" />
      <el-table-column prop="description" label="描述" />
      <el-table-column label="操作" width="140">
        <template #default="{ row }">
          <el-button size="small" text @click="openDialog(row)">编辑</el-button>
          <el-button size="small" text type="danger" @click="remove(row.id)">禁用</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑课程' : '新增课程'" width="520px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="课程名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="乐器"><el-input v-model="form.instrument" /></el-form-item>
        <el-form-item label="时长(分钟)"><el-input v-model="form.duration_minutes" type="number" /></el-form-item>
        <el-form-item label="单价"><el-input v-model="form.price" type="number" /></el-form-item>
        <el-form-item label="最大人数"><el-input v-model="form.max_students" type="number" /></el-form-item>
        <el-form-item label="任课教师">
          <el-select v-model="form.teacher_id" style="width: 100%">
            <el-option v-for="t in teachers" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" :rows="2" /></el-form-item>
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
import { listCourses, createCourse, updateCourse, deleteCourse } from '../api/course.js'
import { listTeachers } from '../api/teacher.js'

const list = ref([])
const teachers = ref([])
const filterInstrument = ref('')
const dialogVisible = ref(false)
const form = ref({})

const filteredList = computed(() => {
  if (!filterInstrument.value) return list.value
  return list.value.filter(c => c.instrument === filterInstrument.value)
})

async function load() {
  list.value = await listCourses()
  teachers.value = await listTeachers()
}

function openDialog(row = null) {
  form.value = row ? { ...row } : { duration_minutes: 45, price: 0, max_students: 1 }
  dialogVisible.value = true
}

async function submit() {
  const data = { ...form.value }
  if (data.id) {
    await updateCourse(data.id, data)
  } else {
    await createCourse(data)
  }
  dialogVisible.value = false
  await load()
}

async function remove(id) {
  await ElMessageBox.confirm('确认禁用该课程？', '提示', { type: 'warning' })
  await deleteCourse(id)
  await load()
}

onMounted(load)
</script>

<style scoped>
.toolbar { margin-bottom: 12px; }
</style>
