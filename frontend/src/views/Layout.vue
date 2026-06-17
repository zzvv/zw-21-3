<template>
  <el-container class="layout">
    <el-aside width="210px" class="aside">
      <div class="logo">
        <el-icon :size="22"><Headset /></el-icon>
        <span>琴行教务系统</span>
      </div>
      <el-menu :default-active="route.path" router class="menu" background-color="#1a1a2e" text-color="#b0b0c0" active-text-color="#409eff">
        <el-menu-item index="/dashboard"><el-icon><Odometer /></el-icon><span>数据看板</span></el-menu-item>
        <el-menu-item index="/teachers"><el-icon><User /></el-icon><span>教师管理</span></el-menu-item>
        <el-menu-item index="/students"><el-icon><UserFilled /></el-icon><span>学员管理</span></el-menu-item>
        <el-menu-item index="/courses"><el-icon><Reading /></el-icon><span>课程管理</span></el-menu-item>
        <el-menu-item index="/classrooms"><el-icon><OfficeBuilding /></el-icon><span>教室管理</span></el-menu-item>
        <el-menu-item index="/classroom-board"><el-icon><Grid /></el-icon><span>教室看板</span></el-menu-item>
        <el-menu-item index="/schedules"><el-icon><Calendar /></el-icon><span>排课管理</span></el-menu-item>
        <el-menu-item index="/enrollments"><el-icon><Tickets /></el-icon><span>报名管理</span></el-menu-item>
        <el-menu-item index="/lesson-records"><el-icon><Document /></el-icon><span>上课记录</span></el-menu-item>
        <el-menu-item index="/exams"><el-icon><Medal /></el-icon><span>考级管理</span></el-menu-item>
        <el-menu-item index="/instruments"><el-icon><Headset /></el-icon><span>乐器管理</span></el-menu-item>
        <el-menu-item index="/users" v-if="userStore.isAdmin"><el-icon><Setting /></el-icon><span>用户管理</span></el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span class="header-title">{{ pageTitle }}</span>
        <div class="header-right">
          <el-tag v-if="userStore.userInfo" size="small" effect="plain">{{ userStore.userInfo.real_name || userStore.userInfo.username }}</el-tag>
          <el-button size="small" @click="logout" text><el-icon><SwitchButton /></el-icon> 退出</el-button>
        </div>
      </el-header>
      <el-main class="main"><router-view /></el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user.js'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const pageTitle = computed(() => {
  const map = {
    '/dashboard': '数据看板',
    '/teachers': '教师管理',
    '/students': '学员管理',
    '/courses': '课程管理',
    '/classrooms': '教室管理',
    '/classroom-board': '教室占用看板',
    '/schedules': '排课管理',
    '/enrollments': '报名管理',
    '/lesson-records': '上课记录',
    '/exams': '考级管理',
    '/instruments': '乐器管理',
    '/users': '用户管理',
  }
  return map[route.path] || '琴行教务系统'
})

function logout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout { height: 100vh; background: #f5f7fa; }
.aside { background: #1a1a2e; }
.logo { height: 56px; display: flex; align-items: center; gap: 10px; padding: 0 18px; color: #fff; font-size: 16px; font-weight: 600; border-bottom: 1px solid #2d2d44; }
.menu { border-right: none; }
.header { display: flex; align-items: center; justify-content: space-between; background: #fff; border-bottom: 1px solid #e4e7ed; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.header-title { font-size: 16px; font-weight: 600; color: #333; }
.header-right { display: flex; align-items: center; gap: 12px; }
.main { padding: 20px; overflow: auto; }
</style>
