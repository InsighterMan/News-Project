<template>
  <div class="my-container">
    <van-nav-bar :title="$t('my.title')" />
    <div class="user-info" @click="goToProfile" v-if="isLogin">
      <div class="avatar">
        <van-image
          round
          width="80"
          height="80"
          :src="avatarUrl"
        />
      </div>
      <div class="info">
        <div class="username">{{ isLogin ? userInfo.username : $t('my.notLoggedIn') }}</div>
        <div class="desc" v-if="isLogin">{{ userBio || $t('profile.bio') }}</div>
      </div>
      <van-icon name="arrow" class="arrow-icon" />
    </div>
    <div class="user-info guest-info" v-else>
      <div class="avatar">
        <van-image
          round
          width="80"
          height="80"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
        />
      </div>
      <div class="info">
        <p class="eyebrow">NEWS ACCOUNT</p>
        <div class="username">{{ $t('my.notLoggedIn') }}</div>
        <div class="desc">登录后同步收藏、点赞和浏览足迹</div>
        <div class="guest-actions"><button @click="goToLogin">{{ $t('my.goToLogin') }}</button><button class="outline" @click="goToRegister">{{ $t('my.goToRegister') }}</button></div>
      </div>
    </div>

    <div class="menu-list">
      <van-cell-group inset>
        <van-cell :title="$t('my.myLikes')" is-link @click="goToLikes" />
        <van-cell :title="$t('my.myFavorite')" is-link @click="goToFavorite" />
        <van-cell :title="$t('my.browsingHistory')" is-link @click="goToHistory" />
        <van-cell :title="$t('my.settings')" is-link @click="goToSettings" />
        <van-cell v-if="isLogin" :title="$t('my.logout')" @click="handleLogout" />
      </van-cell-group>
    </div>
    <tab-bar />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '../store/user';
import { useRouter } from 'vue-router';
import { computed, ref } from 'vue';
import { showDialog, showToast } from 'vant';
import TabBar from '../components/TabBar.vue';
import { useI18n } from 'vue-i18n';

const userStore = useUserStore();
const router = useRouter();
const { t } = useI18n();

// 从store获取用户信息和登录状态
const userInfo = computed(() => userStore.userInfo);
const isLogin = computed(() => userStore.getLoginStatus);
const userBio = computed(() => userStore.getUserBio || t('profile.bio'));
const defaultAvatar = 'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg';
const avatarUrl = computed(() => localStorage.getItem('profile-avatar') || userInfo.value?.avatar || defaultAvatar);

// 跳转到登录页
const goToLogin = () => {
  router.push('/login');
};

// 跳转到注册页
const goToRegister = () => {
  router.push('/register');
};

// 跳转到个人信息页
const goToProfile = () => {
  if (isLogin.value) {
    router.push('/profile');
  }
};

// 跳转到浏览历史页面
const goToHistory = () => {
  if (isLogin.value) {
    router.push('/history');
  } else {
    showToast(t('common.login'));
    router.push('/login');
  }
};

// 跳转到我的收藏页面
const goToFavorite = () => {
  if (isLogin.value) {
    router.push('/favorite');
  } else {
    showToast(t('common.login'));
    router.push('/login');
  }
};

// 跳转到设置页面
const goToSettings = () => {
  router.push('/settings');
};
const goToLikes = () => router.push('/likes');

// 退出登录
const handleLogout = () => {
  showDialog({
    title: t('common.confirm'),
    message: t('my.logout') + '?',
    showCancelButton: true,
  }).then((action) => {
    if (action === 'confirm') {
      userStore.logout();
      router.push('/login');
    }
  });
};

// 获取用户信息
onMounted(async () => {
  try {
    await userStore.getUserInfoDetail();
  } catch (error) {
    console.error('获取用户信息失败:', error);
  }
});
</script>

<style scoped>
.my-container {
  padding-top: 46px;
  padding-bottom: 50px;
  background: radial-gradient(circle at 90% 0, color-mix(in srgb,var(--theme-accent) 42%,transparent), transparent 45%), radial-gradient(circle at 5% 70%, color-mix(in srgb,var(--secondary-color) 35%,transparent), transparent 50%), var(--theme-bg);
  color: var(--theme-text);
  min-height: 100vh;
  box-sizing: border-box;
}

.van-nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
}

.user-info {
  display: flex;
  align-items: center;
  padding: 28px 26px;
  background: linear-gradient(125deg, rgba(255,255,255,.08), color-mix(in srgb,var(--theme-accent) 62%,#12172b));
  color: #fff;
  border-radius: 22px;
  margin: 24px auto;
  max-width: 980px;
  position: relative;
}

.arrow-icon {
  position: absolute;
  right: 16px;
  color: #969799;
}

.avatar {
  margin-right: 16px;
}

.info {
  flex: 1;
}

.username {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 4px;
}

.desc {
  font-size: 14px;
  color: #d4cff4;
}

.guest-info{min-height:172px;background:linear-gradient(125deg,rgba(255,255,255,.1),color-mix(in srgb,var(--theme-accent) 55%,#17213b));border:1px solid rgba(225,235,255,.22);box-shadow:0 22px 55px rgba(0,0,0,.25);overflow:hidden}.guest-info:after{content:'';position:absolute;width:190px;height:190px;right:-55px;top:-70px;border-radius:50%;background:color-mix(in srgb,var(--theme-accent) 42%,transparent);filter:blur(18px)}.guest-info .avatar,.guest-info .info{position:relative;z-index:1}.guest-info .avatar :deep(img){border:2px solid rgba(255,255,255,.55);box-shadow:0 10px 26px rgba(0,0,0,.25)}.eyebrow{font-size:10px;letter-spacing:1.8px;color:#d5d4ff;margin-bottom:7px}.guest-info .username{font-size:24px}.guest-info .desc{margin-top:3px;color:rgba(244,246,255,.78)}.guest-actions{display:flex;gap:10px;margin-top:16px}.guest-actions button{border:0;border-radius:11px;padding:9px 16px;color:#fff;background:linear-gradient(135deg,var(--primary-color),var(--theme-accent));font:inherit;font-size:13px;cursor:pointer;box-shadow:0 8px 20px color-mix(in srgb,var(--theme-accent) 32%,transparent)}.guest-actions .outline{background:rgba(8,13,31,.2);border:1px solid rgba(255,255,255,.35);box-shadow:none}

.menu-list {
  margin: 0 auto;
  max-width: 980px;
}
:deep(.van-nav-bar),:deep(.van-cell-group),:deep(.van-cell){background:transparent;color:#eef0ff}:deep(.van-nav-bar__title),:deep(.van-cell__title),:deep(.van-cell__value),:deep(.van-cell__right-icon){color:#eef0ff}:deep(.van-cell-group){border:1px solid rgba(255,255,255,.1);border-radius:20px;overflow:hidden;background:rgba(255,255,255,.05);backdrop-filter:blur(18px)}:deep(.van-cell){padding:18px;border-bottom:1px solid rgba(255,255,255,.08)}:deep(.van-cell:after){display:none}
</style>
