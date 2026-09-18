<template>
  <main class="favorite-page">
    <header class="favorite-header">
      <button class="back" @click="router.back()"><van-icon name="arrow-left" /> 返回</button>
      <div><p>PERSONAL ARCHIVE</p><h1>我的收藏</h1></div>
      <button class="clear" :disabled="!favorites.length" @click="onClickClear"><van-icon name="delete-o" /> 清空</button>
    </header>
    <section class="favorite-hero"><span class="orb one"></span><span class="orb two"></span><p>BOOKMARKED STORIES</p><strong>{{ favorites.length }}</strong><em>篇已收藏资讯</em><small>你收藏的内容会保存在此设备，并优先展示最新加入的文章。</small></section>
    <section v-if="favorites.length" class="favorite-grid">
      <article v-for="(item, index) in favorites" :key="item.id" class="favorite-card" @click="goToNewsDetail(item)">
        <div class="cover"><img :src="item.image || picture(item.id)" :alt="translateTitle(item.title)" @error="imageError($event, item.id)" /><span>{{ String(index + 1).padStart(2, '0') }}</span></div>
        <div class="card-content"><p>{{ translateSource(item.author || item.source || '新闻资讯') }} · {{ item.publishTime || '实时更新' }}</p><h2>{{ translateTitle(item.title) }}</h2><small>收藏于 {{ item.favoriteTime || '刚刚' }}</small></div>
        <button class="remove" :aria-label="`删除收藏：${item.title}`" @click.stop="removeFavorite(item.id)"><van-icon name="cross" /></button>
      </article>
    </section>
    <section v-else class="empty-glass"><van-icon name="star-o" /><h2>还没有收藏</h2><p>发现值得回看的资讯后，点击文章中的“收藏”即可保存在这里。</p><button @click="router.push('/home')">去发现资讯</button></section>
  </main>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showDialog, showToast } from 'vant'
import { useFavoriteStore } from '../store/modules/favorite'
import { translateSource, translateTitle } from '../utils/newsTranslation'
const router = useRouter(); const favoriteStore = useFavoriteStore(); const favorites = computed(() => favoriteStore.getFavorites)
const picture = id => `https://picsum.photos/seed/nova-favorite-${encodeURIComponent(id)}/720/480`
const imageError = (event, id) => { event.target.src = picture(`${id}-alternate`) }
const goToNewsDetail = item => { if (item?.isLive) sessionStorage.setItem(`live-news:${item.id}`, JSON.stringify(item)); router.push(`/news/detail/${item.id}`) }
const removeFavorite = id => { favoriteStore.removeFavorite(id); favoriteStore.removeFavoriteApi(id).catch(() => {}); showToast({ message: '已移除收藏', position: 'bottom' }) }
const onClickClear = async () => { try { await showDialog({ title: '清空收藏', message: '确定清空全部收藏吗？', showCancelButton: true, className: 'archive-dialog' }); favoriteStore.clearFavorites(); favoriteStore.clearFavoritesApi().catch(() => {}); showToast({ message: '收藏已清空', position: 'bottom' }) } catch (_) {} }
onMounted(() => favoriteStore.loadFavorites())
</script>

<style scoped>
.favorite-page{min-height:100vh;padding:0 clamp(22px,7vw,132px) 76px;color:#edf3ff;background:radial-gradient(circle at 7% 14%,#164c65 0,transparent 32%),radial-gradient(circle at 95% 0,#6b43a4 0,transparent 37%),#090d1b}.favorite-header{height:92px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;border-bottom:1px solid rgba(255,255,255,.12)}.favorite-header h1{font-size:23px;margin:2px 0 0;text-align:center}.favorite-header p,.favorite-hero p{font-size:11px;color:#9ee9ff;letter-spacing:2px}.favorite-header p{text-align:center}.back,.clear{border:0;background:transparent;color:#d8e8fc;font-size:14px;justify-self:start}.clear{justify-self:end;color:#a9e8ff}.clear:disabled{opacity:.35}.favorite-hero{position:relative;overflow:hidden;margin:36px 0 26px;padding:31px 34px;border:1px solid rgba(193,221,255,.18);border-radius:25px;background:linear-gradient(120deg,rgba(19,49,72,.74),rgba(61,37,102,.62));box-shadow:inset 0 1px rgba(255,255,255,.12),0 18px 45px rgba(0,0,0,.2);backdrop-filter:blur(20px)}.favorite-hero>*:not(.orb){position:relative;z-index:1}.favorite-hero strong{display:inline-block;margin-top:6px;font-size:54px;line-height:1;color:#fff}.favorite-hero em{font-style:normal;margin-left:11px;color:#cad5ee}.favorite-hero small{display:block;margin-top:16px;color:#adbed6}.orb{position:absolute;border-radius:50%;filter:blur(3px);opacity:.45}.orb.one{width:180px;height:180px;right:9%;top:-98px;background:#95deff}.orb.two{width:125px;height:125px;right:0;bottom:-70px;background:#b68cff}.favorite-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}.favorite-card{position:relative;overflow:hidden;cursor:pointer;border:1px solid rgba(204,224,255,.16);border-radius:20px;background:rgba(255,255,255,.065);box-shadow:0 15px 32px rgba(0,0,0,.18);transition:transform .22s,border-color .22s;backdrop-filter:blur(14px)}.favorite-card:hover{transform:translateY(-5px);border-color:rgba(150,225,255,.5)}.cover{position:relative;height:160px;overflow:hidden}.cover img{width:100%;height:100%;display:block;object-fit:cover;transition:transform .35s}.favorite-card:hover img{transform:scale(1.05)}.cover:after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,transparent 48%,rgba(7,12,28,.68))}.cover span{position:absolute;z-index:1;top:12px;left:12px;border-radius:8px;padding:4px 7px;background:rgba(8,14,31,.62);font-size:11px;font-weight:800;letter-spacing:1px}.card-content{padding:17px}.card-content p{font-size:11px;color:#9de3f9}.card-content h2{min-height:52px;margin:7px 0 12px;font-size:17px;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.card-content small{color:#a6b3cc;font-size:11px}.remove{position:absolute;z-index:2;top:12px;right:12px;width:33px;height:33px;border:1px solid rgba(255,255,255,.35);border-radius:50%;color:#fff;background:rgba(15,19,38,.64);opacity:0;transition:opacity .2s,background .2s}.favorite-card:hover .remove,.remove:focus{opacity:1}.remove:hover{background:#ec466e}.empty-glass{max-width:560px;margin:84px auto;padding:54px 35px;text-align:center;border:1px solid rgba(189,219,255,.18);border-radius:25px;background:rgba(255,255,255,.055);backdrop-filter:blur(18px)}.empty-glass :deep(.van-icon){font-size:40px;color:#a88cff}.empty-glass h2{margin:14px 0 8px}.empty-glass p{color:#b0bed2;line-height:1.7}.empty-glass button{margin-top:22px;padding:10px 17px;border:0;border-radius:11px;color:#fff;background:linear-gradient(135deg,#4d99b5,#8154d7)}@media(max-width:600px){.favorite-page{padding:0 18px 76px}.favorite-header{height:76px}.favorite-header h1{font-size:19px}.favorite-hero{margin-top:22px;padding:25px}.favorite-hero strong{font-size:45px}.remove{opacity:1}.favorite-grid{grid-template-columns:1fr}.cover{height:180px}}
</style>
