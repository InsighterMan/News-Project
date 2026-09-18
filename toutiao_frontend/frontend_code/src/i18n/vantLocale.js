import { Locale } from 'vant'
import zhCN from 'vant/es/locale/lang/zh-CN.mjs'
import enUS from 'vant/es/locale/lang/en-US.mjs'

// Vant dialogs, toasts and action sheets keep their own locale. Keep it in
// lockstep with vue-i18n so a Chinese interface never exposes English actions.
export const syncVantLocale = (locale) => {
  const language = locale === 'en-US' ? 'en-US' : 'zh-CN'
  Locale.use(language, language === 'en-US' ? enUS : zhCN)
}
