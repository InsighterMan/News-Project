<template>
  <div class="app" @click.capture="guardGuestAction">
    <router-view v-slot="{ Component }">
      <template v-if="$route.meta.keepAlive">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </template>
      <template v-else>
        <component :is="Component" />
      </template>
    </router-view>
    <div v-if="guestAuthVisible" class="auth-mask"><section class="auth-card"><van-icon name="lock"/><h2>请登录后使用</h2><p>登录后即可点赞、收藏新闻并同步保存记录。</p><div><button @click="$router.push('/login')">去登录</button><button class="secondary" @click="$router.push('/register')">去注册</button></div><a @click="guestAuthVisible=false">暂不登录</a></section></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from './store/user'
import { useI18n } from 'vue-i18n'
const guestAuthVisible = ref(false)
const userStore = useUserStore()
const { locale } = useI18n()
const isEnglish = computed(() => locale.value === 'en-US')
const guardGuestAction = (event) => {
  if (userStore.getLoginStatus) return
  const button = event.target.closest('button')
  if (!button) return
  const text = button.innerText || ''
  if (/点赞|收藏|Like|Save/.test(text)) {
    event.preventDefault()
    event.stopPropagation()
    guestAuthVisible.value = true
  }
}
const englishText = {
  '此刻，正在发生':'Happening Now','百度新闻 · 实时聚合':'Live news aggregation','实时资讯流':'Live News Feed','头条':'Headlines','社会':'Society','国内':'China','国际':'World','娱乐':'Entertainment','体育':'Sports','科技':'Technology','财经':'Business','为你精选':'Selected for You','更新于':'Updated','正在连接资讯源':'Connecting to news sources','加载中...':'Loading...','加载中…':'Loading...','刷新':'Refresh','搜索':'Search','取消':'Cancel','返回':'Back','返回资讯流':'Back to Feed','点赞':'Like','已赞':'Liked','收藏':'Save','已收藏':'Saved','相关推荐':'Related Stories','新闻来源与完整报道':'Source & full report','我的':'My','未登录':'Not Signed In','我的点赞':'My Likes','我的收藏':'My Favorites','浏览历史':'Reading History','设置':'Settings','退出登录':'Log Out','个人信息':'Profile','头像':'Avatar','用户名':'Username','账号ID':'Account ID','个人简介':'Bio','修改密码':'Change Password','当前密码:':'Current password:','新密码:':'New password:','确认密码:':'Confirm password:','确认':'Confirm','用户登录':'Sign In','用户注册':'Create Account','密码':'Password','确认密码':'Confirm Password','请输入用户名':'Enter username','请输入密码':'Enter password','请再次输入密码':'Re-enter password','登录':'Sign In','注册':'Create Account','已有账号？':'Already have an account?','去登录':'Sign In','去注册':'Create Account','语言设置':'Language','主题定制':'Theme','个性化':'Personalization','选择语言':'Select Language','选择主题':'Select Theme','简体中文':'Simplified Chinese','紫曜玻璃':'Violet Glass','深海玻璃':'Ocean Glass','琥珀玻璃':'Amber Glass','森屿玻璃':'Forest Glass','新闻资讯':'News','实时更新':'Updated live','刚刚更新':'Just updated','阅读':'views','条浏览记录':'reading records','条点赞记录':'liked records','还没有浏览记录':'No reading history yet','还没有收藏':'No saved stories yet','还没有点赞记录':'No liked stories yet','去看新闻':'Browse news','去发现资讯':'Discover news','去点赞新闻':'Like news','清空':'Clear','删除':'Delete','暂不登录':'Not now','请登录后使用':'Sign in to continue'
}
englishText['实时聚合'] = 'Live Aggregation'
const translateVisibleText = () => {
  if (!isEnglish.value) return
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT)
  const nodes = []; let node
  while ((node = walker.nextNode())) nodes.push(node)
  nodes.forEach(textNode => {
    const raw = textNode.nodeValue; const trimmed = raw.trim()
    if (!trimmed || !/[\u4e00-\u9fff]/.test(trimmed)) return
    const translated = englishText[trimmed] || Object.entries(englishText).reduce((value,[zh,en]) => value.replaceAll(zh,en), trimmed)
    if (translated !== trimmed) textNode.nodeValue = raw.replace(trimmed, translated)
  })
}
onMounted(() => { const observer = new MutationObserver(() => queueMicrotask(translateVisibleText)); observer.observe(document.body,{childList:true,subtree:true,characterData:true}); translateVisibleText() })
watch(isEnglish, () => queueMicrotask(translateVisibleText))
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-size: 16px;
  background-color: var(--theme-bg, #090b16);
  color: var(--theme-text, #eef2ff);
  height: 100%;
  width: 100%;
}

.app {
  width: 100%;
  min-height: 100vh;
}

.van-dialog, .van-popup { background:linear-gradient(135deg,color-mix(in srgb,var(--theme-accent,#875ce5) 22%,#101524),rgba(18,22,45,.94)) !important; color:var(--theme-text,#f2f3ff) !important; border:1px solid rgba(220,230,255,.18); box-shadow:0 24px 70px rgba(0,0,0,.45); backdrop-filter:blur(24px); }
.van-dialog__header, .van-dialog__message, .van-dialog__confirm, .van-dialog__cancel { color:var(--theme-text,#f2f3ff) !important; }
.van-dialog__footer,.van-dialog__footer .van-button{background:rgba(8,12,28,.72) !important;border-color:rgba(220,230,255,.13) !important}.van-dialog__footer:after{border-color:rgba(220,230,255,.13)!important}
.settings-sheet{min-height:270px;padding-bottom:12px}.settings-sheet .popup-title{color:var(--theme-text);font-size:17px}.settings-sheet .van-cell-group,.settings-sheet .van-cell{background:transparent !important;color:var(--theme-text)!important}.settings-sheet .van-cell__title{color:var(--theme-text)!important}.settings-sheet .van-button{background:linear-gradient(135deg,var(--theme-accent),var(--secondary-color))!important;border:0!important}
.van-tabbar { background:rgba(9,13,29,.88) !important; border-top:1px solid rgba(255,255,255,.12) !important; backdrop-filter:blur(18px); }
.van-tabbar-item, .van-tabbar-item--active { background:transparent !important; color:#afa6d8 !important; }
.van-tabbar-item--active { color:#a98cff !important; }
.auth-mask{position:fixed;inset:0;z-index:1200;display:grid;place-items:center;background:rgba(3,7,18,.6);backdrop-filter:blur(8px)}.auth-card{width:min(430px,calc(100vw - 40px));padding:35px 28px;border:1px solid rgba(220,230,255,.24);border-radius:26px;text-align:center;background:linear-gradient(135deg,color-mix(in srgb,var(--theme-accent) 28%,#151b36),rgba(12,17,38,.96));box-shadow:0 24px 70px rgba(0,0,0,.45)}.auth-card>.van-icon{font-size:34px;color:var(--theme-accent)}.auth-card h2{margin:14px 0 8px}.auth-card p{color:#c6cce1;line-height:1.65}.auth-card div{display:flex;gap:12px;margin-top:24px}.auth-card button{flex:1;border:0;border-radius:13px;padding:12px;color:#fff;background:linear-gradient(135deg,var(--theme-accent),var(--secondary-color));font:inherit}.auth-card .secondary{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2)}.auth-card a{display:inline-block;margin-top:18px;color:#c8cfe4;font-size:13px;cursor:pointer}

/* Theme contract: pages which were originally designed with fixed purple/blue values. */
html[data-theme] .home-shell,html[data-theme] .search-page,html[data-theme] .detail,html[data-theme] .history-page,html[data-theme] .favorite-page,html[data-theme] .profile-page{background:radial-gradient(circle at 92% 0,color-mix(in srgb,var(--theme-accent) 46%,transparent),transparent 40%),radial-gradient(circle at 6% 20%,color-mix(in srgb,var(--secondary-color) 38%,transparent),transparent 42%),var(--theme-bg)!important;color:var(--theme-text)!important}
html[data-theme] .home-shell .hero{background:radial-gradient(circle at 86% 0%,color-mix(in srgb,var(--theme-accent) 72%,transparent),transparent 34%),radial-gradient(circle at 15% 95%,color-mix(in srgb,var(--secondary-color) 65%,transparent),transparent 45%),color-mix(in srgb,var(--theme-bg) 74%,#111829)!important}html[data-theme] .home-shell .category-scroller button.active,html[data-theme] .home-shell .search-box button,html[data-theme] .search-page form button,html[data-theme] .history-empty button,html[data-theme] .empty-glass button{background:linear-gradient(135deg,var(--primary-color),var(--theme-accent))!important;box-shadow:0 6px 18px color-mix(in srgb,var(--theme-accent) 28%,transparent)!important}html[data-theme] .home-shell .category-scroller button{background:color-mix(in srgb,var(--theme-bg) 62%,#222a42)!important;color:var(--theme-text)!important}
html[data-theme] .profile-page .van-nav-bar,html[data-theme] .profile-page .van-cell-group,html[data-theme] .profile-page .van-cell{color:var(--theme-text)!important}html[data-theme] .profile-page .van-nav-bar__title,html[data-theme] .profile-page .van-cell__title,html[data-theme] .profile-page .van-cell__value,html[data-theme] .profile-page .van-cell__right-icon{color:var(--theme-text)!important}html[data-theme] .profile-page .van-cell-group{background:linear-gradient(135deg,rgba(255,255,255,.1),color-mix(in srgb,var(--theme-accent) 34%,rgba(10,16,35,.7)))!important;border-color:color-mix(in srgb,var(--theme-accent) 45%,rgba(220,230,255,.22))!important}html[data-theme] .profile-page .van-dialog.password-dialog,html[data-theme] .profile-page .van-dialog.bio-dialog{background:linear-gradient(145deg,color-mix(in srgb,var(--theme-accent) 30%,#11172c),rgba(10,15,34,.96))!important}html[data-theme] .profile-page .profile-dialog-input:focus{border-color:var(--theme-accent)!important;box-shadow:0 0 0 3px color-mix(in srgb,var(--theme-accent) 22%,transparent)!important}
html[data-theme] .van-dialog.password-dialog,html[data-theme] .van-dialog.bio-dialog{background:linear-gradient(145deg,color-mix(in srgb,var(--theme-accent) 38%,#11172c),color-mix(in srgb,var(--secondary-color) 35%,#0b1023))!important;border-color:color-mix(in srgb,var(--theme-accent) 48%,rgba(210,225,255,.24))!important}html[data-theme] .van-dialog.password-dialog .van-dialog__confirm,html[data-theme] .van-dialog.bio-dialog .van-dialog__confirm{color:var(--theme-accent)!important}html[data-theme] .van-dialog.password-dialog .profile-dialog-input,html[data-theme] .van-dialog.bio-dialog .profile-dialog-input{border-color:color-mix(in srgb,var(--theme-accent) 42%,rgba(200,220,255,.25))!important}

/* 移动端适配 */
@media (min-width: 900px) {
  .app { min-width: 100%; }
}
</style>
