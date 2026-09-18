<template>
  <main class="ai-shell">
    <header><div class="orb">✦</div><div><b>AI ASSISTANT</b><small><i /> {{ english ? 'Local DeepSeek conversation' : '本地 DeepSeek 对话模式' }}</small></div></header>
    <section class="intro"><p>{{ english ? 'Your news companion' : '你的新闻使用助手' }}</p><h1>{{ english ? 'What would you like to know?' : '有什么想了解的？' }}</h1><div class="chips"><button v-for="q in suggestions" :key="q" @click="ask(q)">{{ q }}</button></div></section>
    <section ref="box" class="messages"><div v-for="(m, i) in messages" :key="i" :class="['message', m.role]"><div class="bubble">{{ m.content }}</div></div></section>
    <form class="composer" @submit.prevent="send"><textarea v-model="input" :disabled="loading" :placeholder="english ? 'Ask a question, Enter to send' : '输入问题，Enter 发送'" @keydown.enter.exact.prevent="send" /><button :disabled="!input.trim() || loading"><van-loading v-if="loading" size="16" /><van-icon v-else name="arrow-up" /></button></form>
    <div v-if="showAuth" class="auth-mask"><section class="auth-card"><van-icon name="lock" /><h2>{{ english ? 'Sign in to use AI' : '请登录后使用' }}</h2><p>{{ english ? 'AI conversation is available after you sign in.' : '登录后即可继续使用 AI 问答服务。' }}</p><div><button @click="$router.push('/login')">{{ english ? 'Go to Login' : '去登录' }}</button><button class="secondary" @click="$router.push('/register')">{{ english ? 'Go to Register' : '去注册' }}</button></div><a @click="showAuth = false">{{ english ? 'Not now' : '暂不登录' }}</a></section></div>
    <tab-bar />
  </main>
</template>

<script setup>
import { computed, nextTick, ref } from 'vue'
import axios from 'axios'
import { useUserStore } from '../store/user'
import { aiChatConfig } from '../config/api'
import TabBar from '../components/TabBar.vue'

const user = useUserStore()
const english = computed(() => localStorage.getItem('language') === 'en-US')
const showAuth = ref(false)
const input = ref('')
const box = ref(null)
const loading = ref(false)
const messages = ref([{ role: 'assistant', content: english.value
  ? 'Hello, I am your AI assistant. I can help you search, save, like news, or update your profile.'
  : '您好，我是您的AI助理。可以问我如何搜索、收藏、点赞新闻或修改个人资料。' }])
const suggestions = computed(() => english.value
  ? ['How do I search news?', 'How do I save an article?', 'How do I change my avatar?']
  : ['如何搜索新闻？', '怎么收藏文章？', '如何修改头像？'])

const scrollToLatest = async () => {
  await nextTick()
  if (box.value) box.value.scrollTop = box.value.scrollHeight
}

const send = async () => {
  if (!user.getLoginStatus) { showAuth.value = true; return }
  const question = input.value.trim()
  if (!question || loading.value) return

  const userMessage = { role: 'user', content: question }
  messages.value.push(userMessage)
  const context = messages.value.slice(-12).map(({ role, content }) => ({ role, content }))
  const pendingMessage = { role: 'assistant', content: english.value ? 'Thinking…' : '正在思考…' }
  messages.value.push(pendingMessage)
  input.value = ''
  loading.value = true
  await scrollToLatest()

  try {
    const response = await axios.post(aiChatConfig.apiEndpoint, {
      messages: context,
      language: english.value ? 'en-US' : 'zh-CN'
    }, { headers: { Authorization: user.getToken } })
    const content = response.data?.data?.content
    pendingMessage.content = content || (english.value ? 'The local AI service returned no answer. Please try again.' : '本地 AI 服务没有返回回答，请重试。')
  } catch (error) {
    const status = error.response?.status
    const detail = error.response?.data?.detail || error.response?.data?.message
    if (status === 401) {
      user.logout()
      showAuth.value = true
      pendingMessage.content = english.value
        ? 'Your sign-in has expired. Please sign in again to use AI chat.'
        : '登录状态已失效，请重新登录后使用 AI 问答。'
    } else pendingMessage.content = detail || (english.value
      ? 'Unable to reach the local AI service. Please make sure Ollama is running.'
      : '暂时无法连接本地 AI 服务，请确认 Ollama 正在运行。')
  } finally {
    loading.value = false
    await scrollToLatest()
  }
}

const ask = question => {
  if (!user.getLoginStatus) { showAuth.value = true; return }
  input.value = question
  send()
}
</script>

<style>
.ai-shell{min-height:100vh;background:radial-gradient(circle at 92% 0,color-mix(in srgb,var(--theme-accent) 48%,transparent),transparent 38%),var(--theme-bg);color:var(--theme-text);padding:28px clamp(20px,7vw,140px) 96px}.ai-shell header{display:flex;align-items:center;gap:10px}.orb{display:grid;place-items:center;width:42px;height:42px;border-radius:15px;background:linear-gradient(135deg,var(--theme-accent),var(--secondary-color));font-size:20px}.ai-shell b{display:block;letter-spacing:1px}.ai-shell small{color:#aeb3ce;font-size:11px}.ai-shell small i{display:inline-block;width:6px;height:6px;border-radius:50%;background:#78f5c1}.intro{padding:70px 0 30px}.intro p{color:var(--theme-accent);margin:0}.intro h1{font-size:clamp(32px,4vw,54px);margin:12px 0 24px}.chips{display:flex;gap:10px}.chips button{border:1px solid rgba(210,220,255,.2);background:rgba(255,255,255,.07);color:var(--theme-text);border-radius:22px;padding:10px 15px}.messages{height:35vh;overflow:auto;padding:10px 0}.message{display:flex;margin:14px 0}.message.user{justify-content:flex-end}.bubble{max-width:70%;padding:14px 18px;border-radius:17px 17px 17px 4px;background:rgba(255,255,255,.09);line-height:1.6;white-space:pre-wrap}.user .bubble{background:var(--theme-accent);border-radius:17px 17px 4px 17px}.composer{display:flex;gap:10px;border:1px solid rgba(210,220,255,.2);background:rgba(255,255,255,.07);border-radius:18px;padding:10px 12px}.composer textarea{flex:1;border:0;background:transparent;outline:0;color:#fff;resize:none;font:inherit}.composer button{border:0;border-radius:13px;background:var(--theme-accent);color:#fff;width:40px}.composer button:disabled{opacity:.55}
</style>
