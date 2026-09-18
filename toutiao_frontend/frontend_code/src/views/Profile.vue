<template>
  <div class="profile-page">
    <van-nav-bar
      title="个人信息"
      left-arrow
      @click-left="$router.back()"
      fixed
    />
    
    <div class="profile-container">
      <van-cell-group inset class="avatar-group">
        <van-cell title="头像" center is-link @click="avatarInput?.click()">
          <template #right-icon>
            <van-image
              round
              width="60"
              height="60"
              :src="avatarUrl"
            />
          </template>
        </van-cell>
      </van-cell-group>
      
      <van-cell-group inset class="info-group">
        <van-cell title="用户名" :value="userInfo.username || 'admin'" />
        <van-cell title="账号ID" :value="`ID: ${accountId}`" />
        <van-cell title="个人简介" :value="userBio || '暂无简介'" is-link @click="showBioDialog" />
      </van-cell-group>
      
      <van-cell-group inset class="security-group">
        <van-cell title="修改密码" is-link @click="showPasswordConfirm" />
      </van-cell-group>
    </div>
    <input ref="avatarInput" class="avatar-input" type="file" accept="image/*" @change="changeAvatar" />
  </div>
</template>

<script setup>
import { ref, computed, h, onMounted } from 'vue';
import { useUserStore } from '../store/user';
import { showDialog, showToast, showLoadingToast, showSuccessToast, showFailToast } from 'vant';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { apiConfig } from '../config/api';

const router = useRouter();
const userStore = useUserStore();
const avatarInput = ref(null);
const defaultAvatar = 'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg';
const userInfo = computed(() => userStore.userInfo);
const avatarUrl = computed(() => localStorage.getItem('profile-avatar') || userInfo.value?.avatar || defaultAvatar);
const createAccountId = () => {
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const digits = '0123456789';
  const all = letters + digits;
  const value = [
    letters[Math.floor(Math.random() * letters.length)],
    digits[Math.floor(Math.random() * digits.length)],
    ...Array.from({ length: 3 }, () => all[Math.floor(Math.random() * all.length)])
  ];
  return `news-${value.sort(() => Math.random() - 0.5).join('')}`;
};
const accountId = computed(() => {
  const identity = userInfo.value?.id || userInfo.value?.username || userStore.token || 'local-user';
  const key = `profile-account-id:${identity}`;
  let value = localStorage.getItem(key);
  if (!/^news-[A-Z0-9]{5}$/.test(value || '')) {
    value = createAccountId();
    localStorage.setItem(key, value);
  }
  return value;
});

const changeAvatar = (event) => {
  const file = event.target.files?.[0];
  if (!file) return;
  if (file.size > 1024 * 1024) { showToast('头像请小于 1MB'); return; }
  const reader = new FileReader();
  reader.onload = () => {
    // Images encoded as base64 are longer than the current database column.
    // Persist locally so avatar changes always work; a URL-based avatar can
    // still be synced by the account API later.
    localStorage.setItem('profile-avatar', reader.result);
    if (userStore.userInfo) userStore.userInfo.avatar = reader.result;
    showSuccessToast('头像已保存到本机');
  };
  reader.readAsDataURL(file);
};

// 初始化用户状态
onMounted(async () => {
  // 如果用户未登录，跳转到登录页面
  if (!userStore.getLoginStatus) {
    router.push('/login');
    return;
  }
  
  // 获取用户信息
  try {
    // 显示加载提示
    const loadingInstance = showLoadingToast({
      message: '加载中...',
      forbidClick: true,
      duration: 0
    });
    
    // console.log('获取用户信息，当前token:', userStore.token);
    
    // 使用新的 getUserInfoDetail 方法
    const result = await userStore.getUserInfoDetail();
    
    // 手动关闭加载提示
    loadingInstance.close();
    
    if (result.success) {
      console.log('获取用户信息成功:', userStore.userInfo);
      // 显示成功提示
      // showSuccessToast('获取用户信息成功');
    } else {
      console.error('获取用户信息失败:', result.message);
      showFailToast(result.message || '获取用户信息失败');
    }
  } catch (error) {
    console.error('获取用户信息请求失败:', error);
    // 确保关闭加载提示
    showToast.clear();
    showToast.fail('获取用户信息失败');
  }
});

const userBio = computed(() => userStore.userInfo?.bio || '暂无简介');

const showPasswordConfirm = () => {
  // 使用ref创建响应式变量
  const oldPassword = ref('');
  const newPassword = ref('');
  const confirmPassword = ref('');
  
  showDialog({
    title: '修改密码',
    showCancelButton: true,
    className: 'password-dialog',
    message: h('div', { style: 'text-align: left; padding: 10px 0;' }, [
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, '当前密码：'),
        h('input', {
          type: 'password',
          value: oldPassword.value,
          onInput: (e) => { oldPassword.value = e.target.value },
          class: 'profile-dialog-input',
          style: 'width: 100%; box-sizing: border-box;'
        })
      ]),
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, '新密码：'),
        h('input', {
          type: 'password',
          value: newPassword.value,
          onInput: (e) => { newPassword.value = e.target.value },
          class: 'profile-dialog-input',
          style: 'width: 100%; box-sizing: border-box;'
        })
      ]),
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, '确认密码：'),
        h('input', {
          type: 'password',
          value: confirmPassword.value,
          onInput: (e) => { confirmPassword.value = e.target.value },
          class: 'profile-dialog-input',
          style: 'width: 100%; box-sizing: border-box;'
        })
      ])
    ]),
  }).then(async () => {
    // 点击确认按钮
    if (!oldPassword.value) {
      showToast('请输入当前密码');
      return;
    }
    
    if (!newPassword.value) {
      showToast('请输入新密码');
      return;
    }
    
    if (newPassword.value !== confirmPassword.value) {
      showToast('两次密码输入不一致');
      return;
    }
    
    try {
      // 显示加载提示
      const loadingInstance = showLoadingToast({
        message: '修改中...',
        forbidClick: true,
        duration: 0
      });
      
      // 调用API更新密码
      const result = await userStore.updatePassword(oldPassword.value, newPassword.value);
      
      // 关闭加载提示
      loadingInstance.close();
      
      if (result && result.success) {
        showSuccessToast('密码修改成功');
      } else {
        showFailToast((result && result.message) || '密码修改失败');
      }
    } catch (error) {
      console.error('修改密码失败:', error);
      showToast.clear();
      showToast.fail('密码修改失败');
    }
  }).catch(() => {
    // 点击取消按钮
  });
};

const showBioDialog = () => {
  // 使用ref创建响应式变量
  const newBioValue = ref(userBio.value);
  
  showDialog({
    title: '修改个人简介',
    showCancelButton: true,
    confirmButtonText: '确认',
    className: 'bio-dialog',
    message: h('div', { style: 'text-align: left; padding: 10px 0;' }, [
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, '个人简介：'),
        h('textarea', {
          value: newBioValue.value,
          onInput: (e) => { newBioValue.value = e.target.value },
          class: 'profile-dialog-input profile-dialog-textarea',
          style: 'width: 100%; box-sizing: border-box;'
        })
      ])
    ])
  }).then(async () => {
    // 点击确认按钮
    try {
      // 显示加载提示
      const loadingInstance = showLoadingToast({
        message: '保存中...',
        forbidClick: true,
        duration: 0
      });
      
      console.log('更新个人简介:', newBioValue.value);
      
      // 调用API更新个人简介
      const result = await userStore.updateUserBio(newBioValue.value);
      
      // 关闭加载提示
      loadingInstance.close();
      
      if (result && result.success) {
        showSuccessToast('个人简介修改成功');
      } else {
        showFailToast((result && result.message) || '个人简介修改失败');
      }
    } catch (error) {
      console.error('更新个人简介失败:', error);
      showToast.clear();
      showToast.fail('个人简介修改失败');
    }
  }).catch(() => {
    // 点击取消按钮
  });
};
</script>

<style>
.avatar-input { display: none; }
.profile-page{min-height:100vh;background:radial-gradient(circle at 90% 0,#533a97,transparent 45%),#0a0c18;color:#f0f1fb;padding-top:46px}.profile-container{max-width:1100px;margin:0 auto;padding:32px}.profile-page .van-nav-bar,.profile-page .van-cell-group,.profile-page .van-cell{background:transparent!important;color:#eef0ff!important}.profile-page .van-nav-bar__title,.profile-page .van-cell__title,.profile-page .van-cell__value,.profile-page .van-cell__right-icon{color:#eef0ff!important}.profile-page .van-cell-group{border:1px solid rgba(184,216,255,.18)!important;border-radius:18px!important;overflow:hidden;background:linear-gradient(135deg,rgba(33,53,84,.64),rgba(61,39,105,.54))!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.1),0 14px 30px rgba(0,0,0,.16)!important;backdrop-filter:blur(18px)}.profile-page .van-cell{padding:18px!important}.profile-page .van-cell:after{border-color:rgba(255,255,255,.1)!important}
.profile-page {
  background: radial-gradient(circle at 90% 0,#533a97,transparent 45%),#0a0c18;
}

.profile-container {
  padding: 32px;
}

.avatar-group,
.info-group,
.security-group {
  margin-top: 16px;
}

.password-dialog .van-dialog__content {
  padding: 20px;
}

.password-form .form-item {
  margin-bottom: 15px;
  text-align: left;
}

.password-form .form-item span {
  display: block;
  margin-bottom: 5px;
  text-align: left;
}

.van-dialog.password-dialog,.van-dialog.bio-dialog{width:min(92vw,440px)!important;color:#edf5ff!important;border:1px solid rgba(173,213,255,.25)!important;border-radius:24px!important;background:linear-gradient(145deg,rgba(24,42,70,.96),rgba(38,29,75,.96))!important;box-shadow:0 24px 70px rgba(0,0,0,.52),inset 0 1px 0 rgba(255,255,255,.12)!important;backdrop-filter:blur(24px)}.password-dialog .van-dialog__header,.bio-dialog .van-dialog__header{padding-top:25px;color:#f5f8ff!important;font-size:20px;font-weight:750}.password-dialog .van-dialog__content,.bio-dialog .van-dialog__content{padding:22px 28px!important;color:#dce9fb!important}.password-dialog .van-dialog__message,.bio-dialog .van-dialog__message{color:#dce9fb!important;font-size:15px;line-height:1.65;text-align:left!important}.password-dialog .van-dialog__footer,.bio-dialog .van-dialog__footer,.password-dialog .van-button,.bio-dialog .van-button{background:rgba(11,20,40,.9)!important;border:0!important}.password-dialog .van-dialog__footer,.bio-dialog .van-dialog__footer{border-top:1px solid rgba(255,255,255,.1)!important}.password-dialog .van-dialog__cancel,.bio-dialog .van-dialog__cancel{color:#bfcae0!important}.password-dialog .van-dialog__confirm,.bio-dialog .van-dialog__confirm{color:#9ee8ff!important;font-weight:700}.password-dialog .van-hairline--left:after,.bio-dialog .van-hairline--left:after{border-color:rgba(255,255,255,.1)!important}.profile-dialog-input{display:block;width:100%;margin-top:7px;padding:11px 12px;border:1px solid rgba(177,215,255,.25)!important;border-radius:12px!important;outline:0;color:#f1f7ff!important;background:rgba(7,16,32,.62)!important;box-shadow:inset 0 1px 5px rgba(0,0,0,.18)}.profile-dialog-input:focus{border-color:#84dcff!important;box-shadow:0 0 0 3px rgba(87,196,255,.14)}.profile-dialog-textarea{min-height:116px;resize:vertical}.van-overlay{background:rgba(3,7,18,.68)!important;backdrop-filter:blur(7px)}
</style>
