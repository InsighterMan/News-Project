import { defineStore } from 'pinia'
import axios from 'axios'
import { apiConfig } from '../../config/api'

const client = axios.create({ baseURL: apiConfig.baseURL, timeout: 12000 })

// A feed can be assembled from more than one public source.  Never render the
// same headline twice merely because upstream sources assigned it different IDs.
const titleKey = (item) => String(item?.title || '')
  .replace(/[【】\[\]（）()“”‘’·|｜—–\-\s]/g, '')
  .toLocaleLowerCase()

const uniqueNews = (items = []) => {
  const seen = new Set()
  return items.filter((item) => {
    const key = titleKey(item)
    if (!key || seen.has(key)) return false
    seen.add(key)
    return true
  })
}

export const useNewsStore = defineStore('news', {
  state: () => ({ newsList: [], newsDetail: {}, categories: [], currentCategory: 1, loading: false, refreshing: false, finished: false, categoriesLoading: false, liveMode: true, lastUpdated: null, trending: [] }),
  actions: {
    async getCategories() {
      if (this.categoriesLoading || this.categories.length) return
      this.categoriesLoading = true
      try { const { data } = await client.get('/api/news/categories'); this.categories = data.code === 200 ? data.data : [] }
      catch { this.categories = ['头条', '社会', '国内', '国际', '娱乐', '体育', '科技', '财经'].map((name, index) => ({ id: index + 1, name })) }
      finally { this.categoriesLoading = false }
    },
    async getTrending() { try { this.trending = (await client.get('/api/live/trending')).data.data || [] } catch { this.trending = [] } },
    async getNewsList(isRefresh = false) {
      if (this.loading && !isRefresh) return
      if (isRefresh) { this.newsList = []; this.finished = false; this.refreshing = true }
      this.loading = true
      try {
        const category = this.categories.find(item => item.id === this.currentCategory)?.name || '头条'
        const params = this.liveMode ? { category, limit: 24 } : { categoryId: this.currentCategory, page: isRefresh ? 1 : Math.ceil(this.newsList.length / 10) + 1, pageSize: 10 }
        const { data } = await client.get(this.liveMode ? '/api/live/news' : '/api/news/list', { params })
        const list = data?.data?.list || []
        if (this.liveMode && list.length === 0) {
          const fallback = await client.get('/api/news/list', { params: { categoryId: this.currentCategory, page: 1, pageSize: 24 } })
          this.newsList = uniqueNews(fallback.data?.data?.list || [])
        } else this.newsList = uniqueNews(this.liveMode || isRefresh ? list : [...this.newsList, ...list])
        sessionStorage.setItem('latest-news', JSON.stringify(this.newsList))
        this.finished = this.liveMode || !data?.data?.hasMore || list.length < (params.pageSize || 24); this.lastUpdated = new Date()
      } catch (error) {
        console.error('获取新闻列表失败:', error)
        // Baidu may temporarily challenge automated requests. Keep the app
        // usable by falling back to the project's verified local news cache.
        if (this.liveMode) {
          try {
            const { data } = await client.get('/api/news/list', { params: { categoryId: this.currentCategory, page: 1, pageSize: 24 } })
            this.newsList = uniqueNews(data?.data?.list || [])
            this.finished = true; this.lastUpdated = new Date()
          } catch (fallbackError) { console.error('本地新闻回退失败:', fallbackError) }
        }
      }
      finally { this.loading = false; this.refreshing = false }
    },
    async searchLive(keyword) {
      this.loading = true
      const cached = JSON.parse(sessionStorage.getItem('latest-news') || '[]')
      try {
        const { data } = await client.get('/api/live/news', { params: { keyword, limit: 24 } })
        const result = uniqueNews(data?.data?.list || [])
        // Search results must never silently become the entire homepage feed.
        // If a source times out, only use locally cached items that actually match.
        this.newsList = result.length ? result : uniqueNews(cached.filter(item => item.title?.includes(keyword) || item.description?.includes(keyword)))
        sessionStorage.setItem('latest-search', JSON.stringify(this.newsList))
      } catch (error) {
        console.error('搜索新闻失败:', error)
        this.newsList = uniqueNews(cached.filter(item => item.title?.includes(keyword) || item.description?.includes(keyword)))
      } finally {
        this.finished = true; this.lastUpdated = new Date(); this.loading = false
      }
    },
    changeCategory(categoryId) { if (this.currentCategory === categoryId && this.newsList.length) return; this.currentCategory = categoryId; this.getNewsList(true) },
    setLiveMode(enabled) { this.liveMode = enabled; this.getNewsList(true) },
    async getNewsDetail(id) { try { const { data } = await client.get('/api/news/detail', { params: { id } }); if (data.code === 200) this.newsDetail = data.data } catch (error) { console.error('获取新闻详情失败:', error) } },
    async getLiveDetail(id) {
      try {
        const { data } = await client.get('/api/live/news', { params: { category: '头条', limit: 50 } })
        const liveItems = uniqueNews(data?.data?.list || [])
        // A direct detail-page visit still needs context for its recommendation cards.
        this.newsList = liveItems
        sessionStorage.setItem('latest-news', JSON.stringify(liveItems))
        const found = liveItems.find(item => item.id === id)
        if (found) this.newsDetail = found
        return found
      } catch (error) {
        console.error('获取实时新闻详情失败:', error)
        return null
      }
    },
    getCategoryName(categoryId) { return this.categories.find(item => item.id === categoryId)?.name || '新闻' }
  }
})
