const titleMap = {
  '习近平就发展先进制造业作出重要指示':'Xi Jinping Issues Important Instructions on Advanced Manufacturing',
  '习言道｜持续做大做强先进制造业':"Xi's Words | Continue Building a Strong Advanced Manufacturing Sector",
  '【向新之翼】习言道｜总书记引领科技强国路':'Wings of Innovation | Xi Leads the Drive for a Technology Powerhouse',
  '学习进行时丨让新兴技术照亮共同繁荣之路':'Study in Progress | Emerging Technology Lights the Way to Shared Prosperity',
  '我国成功发射天仪51、52星':'China Successfully Launches Tianyi-51 and Tianyi-52 Satellites',
  '平陆运河正式通航 航拍视角看运河雄姿':'Pinglu Canal Opens to Navigation: An Aerial View',
  '（爱知·名古屋亚运会）“亚运村邮轮”静待各国运动员':'Aichi–Nagoya Asian Games: The Athletes’ Village Cruise Awaits Delegations',
  '世界跨度最大公铁两用大桥上演“空中牵索”':'World’s Longest-Span Road-Rail Bridge Performs Aerial Cable Installation',
  '国新办就“十五五”时期加快推动广播电视和网络视听高质量发展有关情况举行新闻发布会':'State Council Briefing on High-Quality Broadcasting and Online Audiovisual Development in the 15th Five-Year Plan',
  '一家三代人接力治沙 守护种下的绿洲':'Three Generations Fight Desertification to Protect a Growing Oasis',
  '100秒直击岛内舆论：台湾只有一条路，统一是“必答题”':'100-Second Brief: Public Opinion on Taiwan Says Reunification Is Inevitable',
  '习近平致信祝贺吉林大学建校80周年':'Xi Sends Congratulatory Letter for Jilin University’s 80th Anniversary',
  '北京香山论坛有多“香”？看看各国嘉宾怎么说':'What International Guests Say About the Beijing Xiangshan Forum',
  '第23届中国—东盟博览会开幕 新成员东帝汶首次亮相':'23rd China–ASEAN Expo Opens; Timor-Leste Makes Its Debut',
  '推广一体化电视、严禁AI魔改……这场发布会信息量很大':'Integrated TV and Rules Against AI Alterations: Key Briefing Takeaways',
  '中国代表团亮相爱知·名古屋亚运会欢迎仪式':'Chinese Delegation Appears at Aichi–Nagoya Asian Games Welcome Ceremony',
  '平陆运河通航：中国西南出海格局迎来历史性重塑':'Pinglu Canal Opens, Reshaping Southwest China’s Access to the Sea',
  '2026年国家网络安全宣传周“电信日”主题活动举行':'2026 National Cybersecurity Awareness Week Telecom Day Event Held',
  '长征胜利90周年丨':'90th Anniversary of the Long March Victory',
  '红色遗址交织乡村新貌引八方来客':'Historic Red Sites and Rural Renewal Draw Visitors from Afar',
  '商务部：中美经贸团队正就降税等议题保持密切交流':'Ministry of Commerce: China and US Trade Teams Remain in Close Contact on Tariff Reductions',
  '要把战场延伸至太空？美高官称需为月球周边作战做准备':'US Official Says Forces Must Prepare for Operations Near the Moon',
  '把战场延伸至太空？美高官称需为月球周边作战准备':'US Official Says Forces Must Prepare for Operations Near the Moon',
  '日本首相高市早苗改组内阁 日本维新会成员首次入阁':'Japan’s PM Sanae Takaichi Reshuffles Cabinet; Ishin Members Join for First Time',
  '沙特拦截弹储备告急求助多国，“美方库存已大幅减少”':'Saudi Arabia Seeks Help as Interceptor Stocks Run Low, Report Says',
  '重大转变！冯德莱恩力推加拿大成为欧盟首个"准成员国"':'Major Shift: Von der Leyen Pushes Canada as EU’s First “Associate Member”'
}
const descriptionMap = {
  '实时新闻报道，点击查看详情。':'Live news coverage. Open the article for details.',
  '中新网实时报道，点击进入项目内详情后可查看摘要与原文来源。':'Live coverage from China News Service. Open the article for a summary and original source.',
  '这是一则来自公开新闻来源的实时资讯。':'This is a live update from a public news source.',
  '围绕本条资讯的相关信息正在持续更新。项目展示标题、来源与摘要，并提供原始新闻来源以供核验。':'Related information is being updated continuously. This page provides the headline, source and summary for reference.',
  '请以新闻原始发布方的后续报道为准。':'Please refer to follow-up coverage from the original publisher.'
}
export const isEnglish = () => localStorage.getItem('language') === 'en-US'
export const translateTitle = (value) => isEnglish() ? (titleMap[value] || value) : value
export const translateDescription = (value) => isEnglish() ? (descriptionMap[value] || value) : value
export const translateSource = (value) => isEnglish() && (!value || value === '新闻资讯' || value === '中国新闻网') ? 'China News Service' : value
