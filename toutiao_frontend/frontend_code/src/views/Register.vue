<template>
  <div class="register-page">
    <van-nav-bar
      title="用户注册"
      left-arrow
      @click-left="onClickLeft"
      fixed
    />
    
    <div class="register-container">
      <div class="register-logo">
        <van-image
          width="80"
          height="80"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
          round
        />
        <h2>新闻资讯</h2>
      </div>
      
      <van-form @submit="onSubmit" class="register-form">
        <van-cell-group inset>
          <van-field
            v-model="username"
            name="username"
            label="用户名"
            placeholder="请输入用户名"
            :rules="[{ required: true, message: '请填写用户名' }]"
          />
          <van-field
            v-model="password"
            type="password"
            name="password"
            label="密码"
            placeholder="请输入密码"
            :rules="[{ required: true, message: '请填写密码' }]"
          />
          <van-field
            v-model="confirmPassword"
            type="password"
            name="confirmPassword"
            label="确认密码"
            placeholder="请再次输入密码"
            :rules="[
              { required: true, message: '请确认密码' },
              { validator: validatePassword, message: '两次密码不一致' }
            ]"
          />
        </van-cell-group>
        
        <div class="submit-btn">
          <van-button round block type="primary" native-type="submit" size="large">
            注册
          </van-button>
        </div>
        
        <div class="login-link">
          已有账号？<span @click="goToLogin">去登录</span>
        </div>
      </van-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';
import { useUserStore } from '../store/user';

const router = useRouter();
const userStore = useUserStore();

const username = ref('');
const password = ref('');
const confirmPassword = ref('');

// 验证两次密码是否一致
const validatePassword = () => {
  return password.value === confirmPassword.value;
};

const onSubmit = async () => {
  // 显示加载提示
  showToast({
    type: 'loading',
    message: '注册中...',
    forbidClick: true,
    duration: 0
  });
  
  try {
    // 调用API注册
    const result = await userStore.register({
      username: username.value,
      password: password.value
    });
    
    if (result.success) {
      showToast({
        type: 'success',
        message: result.message
      });
      
      router.push('/');
    } else {
      showToast({
        type: 'fail',
        message: result.message
      });
    }
  } catch (error) {
    showToast({
      type: 'fail',
      message: '注册失败，请稍后再试'
    });
  }
};

const onClickLeft = () => {
  router.back();
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  color: var(--text-color, #eef2ff);
  background: radial-gradient(circle at 88% 5%, color-mix(in srgb, var(--theme-accent, #875ce5) 82%, transparent), transparent 34%), var(--theme-bg, #0a0d1c);
}

.register-container {
  padding-top: 56px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.register-logo {
  margin: 40px 0;
  text-align: center;
}

.register-logo h2 {
  margin-top: 16px;
  color: var(--text-color, #eef2ff);
  font-size: 22px;
}

.register-form {
  width: 100%;
  padding: 0 16px;
}

.submit-btn {
  margin: 24px 16px;
}

.login-link {
  text-align: center;
  margin-top: 16px;
  color: rgba(230, 237, 255, .72);
  font-size: 14px;
}

.login-link span {
  color: var(--primary-color, #a281ff);
  cursor: pointer;
}

:deep(.van-nav-bar), :deep(.van-cell-group), :deep(.van-cell) { background: rgba(255,255,255,.07) !important; color: var(--text-color,#eef2ff) !important; }
:deep(.van-nav-bar) { border-bottom: 1px solid rgba(220,230,255,.14); backdrop-filter: blur(18px); }
:deep(.van-nav-bar__title), :deep(.van-nav-bar__arrow), :deep(.van-field__label), :deep(.van-field__control) { color: var(--text-color,#eef2ff) !important; }
:deep(.van-cell-group) { border: 1px solid rgba(220,230,255,.18) !important; border-radius: 18px; overflow: hidden; backdrop-filter: blur(18px); box-shadow: 0 18px 48px rgba(0,0,0,.16); }
:deep(.van-cell:after) { border-color: rgba(220,230,255,.14); }
:deep(.van-button--primary) { border: 0; background: linear-gradient(135deg, var(--primary-color,#a281ff), var(--theme-accent,#875ce5)); box-shadow: 0 14px 30px color-mix(in srgb,var(--theme-accent,#875ce5) 32%,transparent); }
</style>
