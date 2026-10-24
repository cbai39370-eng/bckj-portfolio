/**
 * 完整国际化多语言翻译引擎 (i18n Engine for Wodniack Portfolio)
 */
import Emitter from './Emitter';
import { getDailyMotto, type DailyMotto } from '../data/daily-mottos';

export type Lang = 'en' | 'zh';

export const translations = {
  en: {
    // Top Nav
    navMystery: 'Mystery',
    navGems: 'Web Gems',
    navTools: 'Geek Tools',
    navAbout: 'About BC',
    navWork: 'Work',
    navContact: 'Contact',
    location: 'Narrative Detective Studio // Creative Hub',
    availPrefix: 'Open for Playtest & Collaborations →',
    hireMe: 'Contact BC',
    langToggle: 'ZH',

    // Hero
    heroCreative: 'Creative',
    heroDeveloper: 'Developer',
    heroSlogan: '“Good morning, and in case I don\'t see ya, good afternoon, good evening, and good night!”',
    heroSloganEn: 'Motto by Truman Burbank // Dedicated to curious minds',
    heroSubtitle: 'Indie Murder Mystery DevLog · Daily Radar · Web Gems · Geek Toolbox',
    heroDoThings: ['G', 'O', 'O', 'D', '·', 'N', 'I', 'G', 'H', 'T'],
    heroAuthor: ['B', 'C', '·', 'S', 'T', 'U', 'D', 'I', 'O'],

    // About
    aboutTitle: 'About BC',
    aboutP1: 'Curiosity and obsessive dedication to craft are the truest foundations of any narrative architect and creative engineer. The hunger to construct interlocking storylines, airtight clue chains, and resonant digital experiences—that is what makes building an indie narrative game so exhilarating.',
    aboutP2: 'A compelling murder mystery needs no combat combos or physics hit-pause; its soul lies in airtight locked-room logic, subtle psychological tension, and that breathless moment when all clues converge into undeniable truth. Tuning every testimony paradox and evidence tree is my daily ritual.',
    aboutP3: 'Beyond narrative game dev, this site serves as my personal digital nexus: scanning daily global trend radars, dissecting ethereal creative web gems, and curating local-first geek productivity utilities.',
    aboutP4: 'In the famous words of The Truman Show: "Good morning, and in case I don\'t see ya, good afternoon, good evening, and good night!" May every visitor finding their way here discover a spark of inspiration or the pure joy of deduction.',
    aboutP5: 'Open for narrative playtesting, creative collaborations, and technical exchanges. Stay sharp, stay honest, and keep building things with a soul.',
    awardsTitle: 'Milestones & Archive',

    // Awards / Spatial Portals
    awardBadgeDev: '[ INDIE DEV // DEV 82% ]',
    awardTextDev: '2025 Detective Mystery: "The 7th Clockstop" · Closed Beta',
    awardSubDev: 'Act IV Locked-Room Mechanics & Paradox Verification · Enter Chamber ➔',
    awardCounterRadar: '(Daily Trends Radar)',
    awardSubRadar: 'Tech · Detective Logic · Curiosity Radar ➔',
    awardBadgeGems: '[ WEB GEMS ]',
    awardTextGems: 'Creative Web Vault',
    awardSubGems: 'Curating Awwwards-Level Digital Artifacts & Interaction Shaders ➔',
    awardCounterSuggest: '(Case Co-Dev)',
    awardSubSuggest: 'Critiques & Plot Brainstorms ➔',
    awardBadgeToolbox: '[ GEEK SUITE ]',
    awardTextToolbox: 'Geek Utility Armory',
    awardSubToolbox: 'Private Cloud Storage · Pragmatic Open-Source Productivity Arsenal ➔ Open Vault',

    // Mobile drawer & Header extras
    portalDev: '01 · Mystery Dev',
    portalRadar: '02 · Daily Radar',
    portalGems: '03 · Web Gems',
    portalSuggest: '04 · Case Co-Dev',
    portalToolbox: '05 · Geek Tools',
    portalActionLabel: 'DIMENSIONAL PORTALS // JUMP',
    portalClose: 'Return to Reality',

    // Work
    workTitle: 'Selected Work & DevLog',
    workScrollHint: 'Explore Narrative Engines, Clue Trees & Creative Tech',

    // My Way
    myWayTitle: 'Journey',
    myWayIntro: 'Milestones, Workspaces, and Creative Artifacts',

    // CTA
    ctaButton: 'GO',
    ctaHeading: "Let's Talk",
    ctaContact: 'hello@wodniack.dev',

    // Palette dock & Nav
    paletteTitle: 'COLOR PALETTES // THEMES',
    dockTitle: 'PALETTE SELECTOR // COLOR SCHEME',
    dockHint: 'Click to switch site theme',
    dockButton: 'Palettes',
  },

  zh: {
    // Top Nav
    paletteTitle: '配色方案 // 主题调色板',
    navMystery: '剧本推理',
    navGems: '神仙网站',
    navTools: '极客工具',
    navAbout: '关于 BC',
    navWork: '精选作品',
    navContact: '联系合作',
    location: '剧本杀独立研发 // 灵感枢纽',
    availPrefix: '新剧本试玩 · 交流合作 →',
    hireMe: '联系制作人 BC',
    langToggle: 'EN',

    // Hero
    heroCreative: '独立制作',
    heroDeveloper: '叙事推理',
    heroSlogan: '“早上好，以防再也见不到你，祝你下午好，晚上好，晚安！”',
    heroSloganEn: '— 楚门的世界 // 献给所有心怀好奇的探索者',
    heroSubtitle: '剧本杀独立研发手札 · 每日热点雷达 · 神仙网站探索 · 极客软件箱',
    heroDoThings: ['早', '上', '好', '祝', '你', '晚', '安'],
    heroAuthor: ['B', 'C', '·', '独', '立', '工', '坊'],

    // About
    aboutTitle: '关于制作人工坊',
    aboutP1: '好奇心与纯粹的探索欲，是独立游戏人与创意工程师最宝贵的基石。对故事逻辑如何精密咬合、嫌疑人物证链如何天衣无缝、数字交互如何打动人心——这正是创造属于自己的沉浸式剧本杀世界最令人着迷之处。',
    aboutP2: '我深信，优秀的剧本杀游戏不需要眼花缭乱的物理打击感，而是需要直击心灵的伏笔编织、严密的密室诡计与让人拍案叫绝的反转推导。在真机上反复校验每一段不在场证明、测试每一次搜证微反馈，这是我日常研发中最享受的时光。',
    aboutP3: '除独立游戏研发外，这里也是我的个人数字中枢：每日扫描全球科技热点雷达、解构神仙级创意网站的前端动效、精选本地离线优先的极客工具箱。将琐碎的技术沉淀为优雅的艺术，是我恒久的追求。',
    aboutP4: '正如《楚门的世界》那句著名的问候：“早上好，以防再也见不到你，祝你下午好，晚上好，晚安！”愿每一个踏入这里的旅人，都能在此捕获一丝灵感的火花或推理的纯粹乐趣。',
    aboutP5: '工坊始终开放跨界合作、剧本试玩交流与灵感碰撞。保持敏锐，保持真诚，在充满变数的数字宇宙中，坚持做纯粹有价值的创造。',
    awardsTitle: '研发里程碑 & 探索印记',

    // Awards / Spatial Portals
    awardBadgeDev: '[ 独立研发进程 // DEV 82% ]',
    awardTextDev: '2025 本格推理新作《第七次停钟》· 封闭验证中',
    awardSubDev: '第四幕密室机械构型与不在场证明闭环推演 · 点击时空穿梭 ➔',
    awardCounterRadar: '(今日热点雷达)',
    awardSubRadar: '科技 · 剧情推理 · 奇闻观察 ➔',
    awardBadgeGems: '[ WEB GEMS ]',
    awardTextGems: '神仙网站探索',
    awardSubGems: '挖掘全球惊艳交互与数字宝藏 ➔',
    awardCounterSuggest: '(案卷建议)',
    awardSubSuggest: '剧本挑刺 & 脑洞 ➔',
    awardBadgeToolbox: '[ GEEK SUITE ]',
    awardTextToolbox: '极客实用工具箱',
    awardSubToolbox: '私有高速云盘 · 实用开源生产力装备 ➔ 点击开启军火库',

    // Mobile drawer & Header extras
    portalDev: '01 · 研发机密',
    portalRadar: '02 · 今日雷达',
    portalGems: '03 · 神仙网站',
    portalSuggest: '04 · 案卷建议',
    portalToolbox: '05 · 极客工具',
    portalActionLabel: 'DIMENSIONAL PORTALS // 时空快捷舱',
    portalClose: '返回现实维度',

    // Work
    workTitle: '精选研发与作品',
    workScrollHint: '横向检视剧本杀推理引擎、物证链图谱与灵感库',

    // My Way
    myWayTitle: '探索轨迹',
    myWayIntro: '代码长征 · 工位变迁与独立创作者的里程碑记忆',

    // CTA
    ctaButton: '出发',
    ctaHeading: '灵感碰撞',
    ctaContact: 'hello@wodniack.dev',

    // Palette dock
    dockTitle: 'PALETTE SELECTOR // 调色板',
    dockHint: '点击实时切换整站色彩',
    dockButton: '一键调色',
  },
};

class I18nManager {
  currentLang: Lang = 'zh';
  mottoOffset: number = 0;

  constructor() {
    // 初始化语言偏好，默认优先中文
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('site-language') as Lang;
      if (saved === 'zh' || saved === 'en') {
        this.currentLang = saved;
      } else {
        this.currentLang = 'zh';
        localStorage.setItem('site-language', 'zh');
      }

      this.mottoOffset = parseInt(localStorage.getItem('motto-offset') || '0', 10);
    }
  }

  getTodayMotto(): DailyMotto {
    return getDailyMotto(this.mottoOffset);
  }

  nextMotto() {
    this.mottoOffset++;
    if (typeof window !== 'undefined') {
      localStorage.setItem('motto-offset', String(this.mottoOffset));
      this.updateDOM();
      Emitter.emit('mottochange', this.getTodayMotto());
    }
  }

  getLang(): Lang {
    return this.currentLang;
  }

  setLang(lang: Lang) {
    this.currentLang = lang;
    if (typeof window !== 'undefined') {
      localStorage.setItem('site-language', lang);
      document.documentElement.setAttribute('lang', lang);

      if (lang === 'zh') {
        document.documentElement.classList.add('is-lang-zh');
      } else {
        document.documentElement.classList.remove('is-lang-zh');
      }

      this.updateDOM();
      Emitter.emit('langchange', lang);
    }
  }

  toggle() {
    this.setLang(this.currentLang === 'en' ? 'zh' : 'en');
  }

  updateDOM() {
    const isZh = this.currentLang === 'zh';
    const t = translations[this.currentLang];
    const today = this.getTodayMotto();

    // 更新所有带有 data-i18n 属性的节点
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n') as keyof typeof t;

      // 联动特判：关于页面的第四段（aboutP4）自动根据今日电影名台词动态深度融合
      if (key === 'aboutP4') {
        el.textContent = isZh ? today.aboutZh : today.aboutEn;
        return;
      }

      if (key && t[key] !== undefined) {
        if (Array.isArray(t[key])) {
          // 数组型字符串保持原样或拼接
          el.textContent = (t[key] as string[]).join(' ');
        } else {
          el.innerHTML = t[key] as string;
        }
      }
    });

    // 动态同步顶部电影标语横幅（Hero Motto Banner）
    document.querySelectorAll('.js-slogan-badge').forEach((el) => {
      el.textContent = today.badge;
    });
    document.querySelectorAll('.js-slogan-zh').forEach((el) => {
      el.textContent = today.quoteZh;
    });
    document.querySelectorAll('.js-slogan-en').forEach((el) => {
      el.textContent = today.quoteEn;
    });

    // 更新双态语言按钮状态
    document.querySelectorAll('.js-lang-opt-zh').forEach((el) => {
      el.classList.toggle('is-active', isZh);
    });
    document.querySelectorAll('.js-lang-opt-en').forEach((el) => {
      el.classList.toggle('is-active', !isZh);
    });

    // 兼容单文本按钮
    document.querySelectorAll('.js-lang-text').forEach((el) => {
      el.textContent = isZh ? '中' : 'EN';
    });

    // 更新按钮 title 提示
    document.querySelectorAll('.js-lang').forEach((el) => {
      el.setAttribute(
        'title',
        isZh
          ? '当前：中文 (点击切换为英文 / Switch to EN)'
          : 'Current: English (点击切换为中文 / Switch to ZH)'
      );
    });
  }
}

export const i18n = new I18nManager();
