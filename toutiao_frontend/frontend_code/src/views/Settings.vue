<template>
  <div class="settings-container">
    <van-nav-bar
      :title="$t('settings.title')"
      left-arrow
      @click-left="onClickLeft"
    />
    
    <div class="settings-list">
      <van-cell-group inset :title="$t('settings.personalization')">
        <van-cell :title="$t('settings.themeCustomization')" is-link @click="showThemePopup = true" />
        <van-cell :title="$t('settings.languageSettings')" is-link @click="showLanguagePopup = true" />
      </van-cell-group>
      
    </div>
    
    <!-- 主题选择弹出层 -->
    <van-popup
      v-model:show="showThemePopup"
      class="settings-sheet"
      position="bottom"
      round
      :style="{ height: '40%' }"
    >
      <div class="popup-title">{{ $t('settings.selectTheme') }}</div>
      <div class="theme-list">
        <div 
          v-for="theme in themeList" 
          :key="theme.id" 
          class="theme-item"
          :class="{ active: currentTheme === theme.id }"
          @click="changeTheme(theme.id)"
        >
          <div class="theme-color" :style="{ backgroundColor: theme.primaryColor }"></div>
          <div class="theme-name">{{ theme.name }}</div>
        </div>
      </div>
    </van-popup>
    
    <!-- 语言选择弹出层 -->
    <van-popup
      v-model:show="showLanguagePopup"
      class="settings-sheet"
      position="bottom"
      round
      :style="{ height: '40%' }"
    >
      <div class="popup-title">{{ $t('settings.selectLanguage') }}</div>
      <van-radio-group v-model="currentLanguage">
        <van-cell-group inset>
          <van-cell 
            v-for="lang in languageOptions" 
            :key="lang.value" 
            :title="lang.label" 
            clickable 
            @click="currentLanguage = lang.value"
            :class="{ 'language-active': currentLanguage === lang.value }"
          >
            <template #right-icon>
              <van-icon v-if="currentLanguage === lang.value" name="success" class="language-check" />
            </template>
          </van-cell>
        </van-cell-group>
      </van-radio-group>
      <div class="popup-footer">
        <van-button type="primary" block @click="changeLanguage">{{ $t('common.confirm') }}</van-button>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';
import { useThemeStore } from '../store/theme';
import { useI18n } from 'vue-i18n';
import { useLanguageStore } from '../store/language';
import { syncVantLocale } from '../i18n/vantLocale';

const router = useRouter();
const themeStore = useThemeStore();
const languageStore = useLanguageStore();
const { t, locale } = useI18n();

// 返回上一页
const onClickLeft = () => {
  router.back();
};

// 主题相关
const showThemePopup = ref(false);
const themeList = computed(() => themeStore.getAllThemes);
const currentTheme = computed(() => themeStore.getCurrentTheme);

// 切换主题
const changeTheme = (themeId) => {
  themeStore.setTheme(themeId);
  showToast(t('settings.themeChanged'));
  showThemePopup.value = false;
};

// 语言相关
const showLanguagePopup = ref(false);
const currentLanguage = ref(languageStore.getCurrentLanguage);
const languageOptions = [
  { label: '简体中文', value: 'zh-CN' },
  { label: 'English', value: 'en-US' }
];

// 切换语言
const changeLanguage = () => {
  languageStore.setLanguage(currentLanguage.value);
  locale.value = currentLanguage.value;
  syncVantLocale(currentLanguage.value);
  showLanguagePopup.value = false;
  showToast(t('settings.languageChanged'));
};
</script>

<style scoped>
.settings-container {
  min-height: 100vh;
  background: radial-gradient(circle at 90% 0,color-mix(in srgb,var(--theme-accent) 42%,transparent),transparent 40%),var(--theme-bg);
  color: var(--theme-text);
  padding-top: 46px;
  padding-bottom: 20px;
}

.settings-list {
  max-width: 1000px;
  margin: 30px auto;
}

.popup-title {
  text-align: center;
  padding: 16px;
  font-size: 16px;
  font-weight: bold;
  border-bottom: 1px solid rgba(220,230,255,.16);
}

.theme-list {
  display: flex;
  flex-wrap: wrap;
  padding: 16px;
}

.theme-item {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 16px;
  cursor: pointer;
}

.theme-color {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-bottom: 8px;
  border: 2px solid transparent;
}

.theme-item.active .theme-color {
  border-color: var(--theme-text);
}

.theme-name {
  font-size: 12px;
}

.popup-footer {
  padding: 16px;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
}

.language-active {
  background-color: rgba(255,255,255,.12);
}
.language-check { color: var(--theme-accent); font-size: 20px; font-weight: 800; }
:deep(.van-nav-bar),:deep(.van-cell-group),:deep(.van-cell){background:transparent;color:var(--theme-text)}:deep(.van-nav-bar__title),:deep(.van-cell__title),:deep(.van-cell__right-icon),:deep(.van-cell-group__title){color:var(--theme-text)}:deep(.van-cell-group){border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.06);border-radius:18px;overflow:hidden;backdrop-filter:blur(16px)}:deep(.van-cell:after){border-color:rgba(255,255,255,.1)}
</style>
