import { defineStore } from 'pinia';

export const useThemeStore = defineStore('theme', {
  state: () => ({
    currentTheme: localStorage.getItem('theme') || 'violet',
    themes: {
      violet:{name:'紫曜玻璃',backgroundColor:'#0a0d1c',textColor:'#eef2ff',primaryColor:'#a281ff',secondaryColor:'#5b3ca8',accent:'#875ce5'},
      ocean:{name:'深海玻璃',backgroundColor:'#07151d',textColor:'#e9fbff',primaryColor:'#68d7f2',secondaryColor:'#17647b',accent:'#2190b3'},
      amber:{name:'琥珀玻璃',backgroundColor:'#191009',textColor:'#fff4e8',primaryColor:'#ffc06a',secondaryColor:'#9b4c23',accent:'#db7b34'},
      forest:{name:'森屿玻璃',backgroundColor:'#091710',textColor:'#ecfff3',primaryColor:'#8ce0a7',secondaryColor:'#256447',accent:'#40975e'}
    }
  }),
  
  getters: {
    getCurrentTheme: (state) => state.currentTheme,
    getThemeConfig: (state) => state.themes[state.currentTheme],
    getAllThemes: (state) => Object.keys(state.themes).map(key => ({
      id: key,
      name: state.themes[key].name,
      primaryColor: state.themes[key].primaryColor
    }))
  },
  
  actions: {
    setTheme(themeName) {
      if (this.themes[themeName]) {
        this.currentTheme = themeName;
        localStorage.setItem('theme', themeName);
        this.applyTheme();
      }
    },
    
    applyTheme() {
      // 兼容旧版本保存的 light/dark 等主题名，避免 CSS 变量未定义而退回白屏。
      if (!this.themes[this.currentTheme]) {
        this.currentTheme = 'violet';
        localStorage.setItem('theme', this.currentTheme);
      }
      const theme = this.themes[this.currentTheme];
      document.documentElement.style.setProperty('--background-color', theme.backgroundColor);
      document.documentElement.style.setProperty('--text-color', theme.textColor);
      document.documentElement.style.setProperty('--primary-color', theme.primaryColor);
      document.documentElement.style.setProperty('--secondary-color', theme.secondaryColor);
      document.documentElement.style.setProperty('--theme-accent', theme.accent);
      document.documentElement.style.setProperty('--theme-bg', theme.backgroundColor);
      document.documentElement.dataset.theme = this.currentTheme;
    },
    
    initTheme() {
      this.applyTheme();
    }
  }
});
