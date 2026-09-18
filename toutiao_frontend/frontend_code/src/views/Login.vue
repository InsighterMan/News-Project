<template>
  <div class="login-page">
    <van-nav-bar
      title="用户登录"
      left-arrow
      @click-left="onClickLeft"
      fixed
    />
    
    <div class="login-container">
      <div class="login-logo">
        <van-image
          width="80"
          height="80"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
          round
        />
        <h2>新闻资讯</h2>
      </div>
      
      <van-form @submit="onSubmit" class="login-form">
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
        </van-cell-group>
        
        <div class="submit-btn">
          <van-button round block type="primary" native-type="submit" size="large">
            登录
          </van-button>
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

const onSubmit = async (values) => {
  // 显示加载提示
  showToast({
    type: 'loading',
    message: '登录中...',
    forbidClick: true,
    duration: 0
  });
  
  try {
    // 调用API登录
    const result = await userStore.login({
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
      message: '登录失败，请稍后再试'
    });
  }
};

const onClickLeft = () => {
  router.back();
};
</script>

<style scoped>
.login-page{min-height:100vh;background:radial-gradient(circle at 88% 5%,var(--theme-accent,#875ce5),transparent 34%),var(--theme-bg,#0a0d1c);color:var(--text-color,#eef2ff)}

.login-container {
  padding-top: 56px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-logo {
  margin: 40px 0;
  text-align: center;
}

.login-logo h2 {
  margin-top: 16px;
  color: var(--text-color,#eef2ff);
  font-size: 22px;
}

.login-form {
  width: 100%;
  padding: 0 16px;
}
:deep(.van-nav-bar),:deep(.van-cell-group),:deep(.van-cell){background:rgba(255,255,255,.07)!important;color:var(--text-color,#eef2ff)!important}:deep(.van-nav-bar__title),:deep(.van-field__label),:deep(.van-field__control){color:var(--text-color,#eef2ff)!important}:deep(.van-cell-group){border:1px solid rgba(255,255,255,.16)!important;border-radius:18px;backdrop-filter:blur(18px)}:deep(.van-button--primary){border:0;background:linear-gradient(135deg,var(--primary-color,#a281ff),var(--theme-accent,#875ce5))}

.submit-btn {
  margin: 24px 16px;
}

.login-tips {
  text-align: center;
  color: #969799;
  font-size: 14px;
  margin-top: 16px;
}

.login-tips p {
  margin: 8px 0;
}
</style>
