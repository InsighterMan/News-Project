<template>
  <van-tabbar v-model="active" route>
    <van-tabbar-item to="/home" icon="home-o">{{ $t('nav.home') }}</van-tabbar-item>
    <van-tabbar-item to="/aichat" icon="chat-o">{{ $t('nav.aiChat') }}</van-tabbar-item>
    <van-tabbar-item to="/my" icon="user-o">{{ $t('nav.my') }}</van-tabbar-item>
  </van-tabbar>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const active = ref(0)

// 根据当前路由路径设置激活的标签
const setActiveTab = () => {
  const path = route.path
  if (path.includes('/home')) {
    active.value = 0
  } else if (path.includes('/aichat')) {
    active.value = 1
  } else if (path.includes('/my')) {
    active.value = 2
  }
}

// 初始化时设置激活标签
setActiveTab()
</script>

<style scoped>
:deep(.van-tabbar){height:64px;background:rgba(10,12,24,.96);border-top:1px solid rgba(255,255,255,.08);box-shadow:0 -12px 30px rgba(0,0,0,.18)}
:deep(.van-tabbar-item){background:transparent;color:#9298b3}:deep(.van-tabbar-item--active){background:transparent;color:#a78bfa}
</style>
