<template>
  <div class="login-wrap">
    <div class="login-box">
      <h2 class="title">琴行教务管理系统</h2>
      <p class="subtitle">Music School Management System</p>
      <el-form :model="form" :rules="rules" ref="formRef" @keyup.enter="login">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" :prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" :prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width: 100%" size="large" @click="login" :loading="loading">登录</el-button>
        </el-form-item>
      </el-form>
      <p class="hint">默认账号：admin / 123456</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user.js'
import request from '../api/request.js'

const router = useRouter()
const store = useUserStore()
const formRef = ref()
const loading = ref(false)
const form = reactive({ username: '', password: '' })

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function login() {
  await formRef.value.validate()
  loading.value = true
  try {
    const data = await request.post('/auth/login', new URLSearchParams({ username: form.username, password: form.password }), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
    store.setToken(data.access_token)
    const me = await request.get('/auth/me')
    store.setUser(me)
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap { height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
.login-box { width: 380px; padding: 40px; background: #fff; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
.title { font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 4px; color: #1a1a2e; }
.subtitle { text-align: center; color: #999; font-size: 12px; margin-bottom: 24px; }
.hint { text-align: center; color: #bbb; font-size: 12px; margin-top: 12px; }
</style>
