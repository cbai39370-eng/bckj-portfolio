#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BC Studio - 时空舱自动化情报与开源矿藏中枢
- 抓取信源：GitHub Trending/Search (影音播放器/音视频源/开源神兵)、HackerNews 科技热榜、V2EX 开发者生态、全球前沿创意网站
- 智能轮转与归档：
  * 今日雷达：FIFO 维持最新 15 条
  * 开源装备：当期精选 30 款（个人云盘置顶），超量自动存入【历史卷宗】永久可查
  * 神仙网站：动态推荐 20 款，超量归档
- 创新分类系统：智子推演、天籁之源、极影魔方、视觉力场等工坊专属极客代号
- 目标文件：src/data/spatial-chambers.json
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JSON_PATH = os.path.join(WORKSPACE_DIR, 'src', 'data', 'spatial-chambers.json')

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 BC-Intel-Bot/2.0'

# ==========================================
# 创新分类系统定义 (BC 极客工坊暗号)
# ==========================================
RADAR_CATEGORIES = [
    {"id": "all", "label": "全境侦测", "en": "ALL RADAR"},
    {"id": "ai", "label": "智子推演", "en": "AI & PARADOX"},
    {"id": "global", "label": "寰宇前沿", "en": "GLOBAL TECH"},
    {"id": "domestic", "label": "极客生态", "en": "DOMESTIC DEV"},
    {"id": "observatory", "label": "视界暗线", "en": "OBSERVATORY"}
]

TOOLBOX_CATEGORIES = [
    {"id": "all", "label": "全库装备", "en": "ALL ARSENAL"},
    {"id": "audio", "label": "天籁之源", "en": "AUDIO & SOURCE"},
    {"id": "video", "label": "极影魔方", "en": "VIDEO & STREAM"},
    {"id": "local", "label": "离线神兵", "en": "LOCAL FIRST"},
    {"id": "geek", "label": "逆向兵刃", "en": "GEEK TOOLS"}
]

GEMS_CATEGORIES = [
    {"id": "all", "label": "全境矿脉", "en": "ALL GEMS"},
    {"id": "shader", "label": "视觉力场", "en": "SHADER & 3D"},
    {"id": "typo", "label": "瑞士排版", "en": "TYPO & GRID"},
    {"id": "kinetic", "label": "奇趣交互", "en": "KINETIC UX"},
    {"id": "studio", "label": "灵感矿脉", "en": "STUDIO VAULT"}
]


def http_get_json(url, timeout=10, headers=None):
    """通用的 JSON HTTP GET 请求助手"""
    req_headers = {'User-Agent': USER_AGENT, 'Accept': 'application/json'}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read().decode('utf-8', errors='ignore')
            return json.loads(data)
    except Exception as e:
        print(f"[WARN] HTTP GET 失败 ({url}): {e}")
        return None


def fetch_hacker_news(limit=6):
    """获取 HackerNews Top 科技头条"""
    print("[1/4] 正在拉取全球前沿科技情报 (HackerNews)...")
    top_ids = http_get_json('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=8)
    if not top_ids:
        return []
    
    news_items = []
    for sid in top_ids[:limit]:
        item = http_get_json(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json', timeout=5)
        if item and 'title' in item:
            news_items.append({
                'title': item.get('title'),
                'url': item.get('url') or f"https://news.ycombinator.com/item?id={sid}",
                'score': item.get('score', 0),
                'by': item.get('by', 'anon'),
                'source': 'HackerNews'
            })
    return news_items


def fetch_v2ex_hot(limit=6):
    """获取国内开发者热议话题 (V2EX Hot)"""
    print("[2/4] 正在拉取国内极客热议话题 (V2EX)...")
    topics = http_get_json('https://www.v2ex.com/api/topics/hot.json', timeout=8)
    if not topics:
        return []
    
    domestic_items = []
    for t in topics[:limit]:
        domestic_items.append({
            'title': t.get('title', ''),
            'url': t.get('url') or f"https://www.v2ex.com/t/{t.get('id')}",
            'replies': t.get('replies', 0),
            'node': (t.get('node') or {}).get('title', '开发者论坛'),
            'source': 'V2EX'
        })
    return domestic_items


def fetch_github_tools():
    """扫描 GitHub 上的开源影音播放器、音频源、视频源与极客神兵"""
    print("[3/4] 正在探测 GitHub 顶级开源神兵 (Music/Video Players & Sources)...")
    live_tools = []
    try:
        gh_headers = {'User-Agent': USER_AGENT}
        gh_token = os.environ.get('GITHUB_TOKEN')
        if gh_token:
            gh_headers['Authorization'] = f'Bearer {gh_token}'
        
        # 搜索热门音频与播放器
        search_url = 'https://api.github.com/search/repositories?q=topic:music-player+sort:stars&per_page=6'
        data = http_get_json(search_url, timeout=6, headers=gh_headers)
        if data and 'items' in data:
            for item in data['items'][:4]:
                stars_k = f"{round(item.get('stargazers_count', 0) / 1000, 1)}k★"
                name_clean = item.get('name')
                desc = item.get('description') or '精选开源播放器客户端'
                live_tools.append({
                    "name": f"{name_clean} // 跨平台音乐流媒体客户端",
                    "desc": desc,
                    "badge": f"GITHUB · {stars_k}",
                    "categoryId": "audio",
                    "url": item.get('html_url'),
                    "launchText": "探查源码 ➔",
                    "stars": stars_k
                })
    except Exception as e:
        print(f"[INFO] GitHub 在线探测日志: {e}")

    return live_tools


# ==========================================
# 标杆高分开源装备库与神仙网站种子库
# ==========================================
BENCHMARK_TOOLBOX_SEED = [
    # 1. 音频与音源 (Audio & Source)
    {
        "name": "MusicFree // 插件化多音源桌面音乐播放器",
        "desc": "基于插件化架构的跨平台音乐神器。本身不集成任何音源，用户可通过自定义 JS 脚本插件自由接入全网无损音频与歌单，纯净无广告。",
        "badge": "MULTI-SOURCE · 16.8k★",
        "categoryId": "audio",
        "url": "https://github.com/maotoumao/MusicFree",
        "launchText": "探查源码 ➔",
        "platform": "WIN · MAC · ANDROID"
    },
    {
        "name": "Spotube // 纯净跨平台流媒体音乐客户端",
        "desc": "利用 Spotify API 抓取元数据并由 YouTube / Piped 提供无损无广告音频流，完全开源轻量，内存占用不足官方十分之一。",
        "badge": "CROSS-PLATFORM · 33.2k★",
        "categoryId": "audio",
        "url": "https://github.com/KRTirtho/spotube",
        "launchText": "探查源码 ➔",
        "platform": "WIN · MAC · LINUX"
    },
    {
        "name": "lx-music-desktop // 经典多源无损音乐桌面端",
        "desc": "基于 Electron 与 Vue 打造的开源音频流客户端。支持各大平台歌曲搜索、歌词逐字同步与自定义音源解析脚本。",
        "badge": "GITHUB · 54.7k★",
        "categoryId": "audio",
        "url": "https://github.com/lyswhut/lx-music-desktop",
        "launchText": "探查源码 ➔",
        "platform": "WIN · MAC · LINUX"
    },
    {
        "name": "YesPlayMusic // 高颜值网易云第三方桌面客户端",
        "desc": "极具现代苹果设计美学的第三方音乐客户端。支持 UnblockNeteaseMusic 自动音源替换、Touch Bar 快捷控制与暗黑模式。",
        "badge": "DESIGN AWARD · 31.5k★",
        "categoryId": "audio",
        "url": "https://github.com/qier222/YesPlayMusic",
        "launchText": "探查源码 ➔",
        "platform": "WIN · MAC · WEB"
    },
    {
        "name": "Listen1 // 全网音乐多合一聚合搜索播放器",
        "desc": "打破曲库壁垒，聚合各大平台曲库。一个搜索框搞定全网找歌与歌单导入，本地安全离线运行。",
        "badge": "AGGREGATION · 14.1k★",
        "categoryId": "audio",
        "url": "https://github.com/listen1/listen1_desktop",
        "launchText": "探查源码 ➔",
        "platform": "CHROME · DESKTOP"
    },

    # 2. 视频与流媒体源 (Video & Stream)
    {
        "name": "IINA // macOS 现代极简视频播放器天花板",
        "desc": "基于 mpv 内核深度定制的现代化开源播放器。完美契合 macOS 设计哲学，支持画中画、外挂字幕实时搜索、HDR 与任意流媒体协议解码。",
        "badge": "MACOS ELITE · 38.5k★",
        "categoryId": "video",
        "url": "https://github.com/iina/iina",
        "launchText": "探查源码 ➔",
        "platform": "MACOS"
    },
    {
        "name": "LosslessCut // 无损音视频极速裁剪拼接神兵",
        "desc": "基于 FFmpeg 打造的零编解码极速剪刀。无需二次渲染，光速粗剪 4K 巨型视频无画质损耗，极客工作流必备生产力。",
        "badge": "LOSSLESS · 22.4k★",
        "categoryId": "video",
        "url": "https://github.com/mifi/lossless-cut",
        "launchText": "探查源码 ➔",
        "platform": "CROSS-PLATFORM"
    },
    {
        "name": "MediaGo // 跨平台网页流媒体嗅探与下载器",
        "desc": "支持 m3u8 / MPD 自动解密与多线程合并抓取，内置极简浏览器自动嗅探网页视频源，快速保存公开高清素材。",
        "badge": "SNIFFER · 6.8k★",
        "categoryId": "video",
        "url": "https://github.com/bistutu/MediaGo",
        "launchText": "探查源码 ➔",
        "platform": "WIN · MAC · LINUX"
    },
    {
        "name": "mpv.net // 现代化极客硬核视频渲染播放器",
        "desc": "基于 libmpv 架构的高性能视频播放器，具备完备的 GPU 着色器扩展与高画质升采样算法支持。",
        "badge": "HIGH-PERF · 4.9k★",
        "categoryId": "video",
        "url": "https://github.com/mpvnet-player/mpv.net",
        "launchText": "探查源码 ➔",
        "platform": "WINDOWS"
    },
    {
        "name": "BBDown // 命令行高画质流媒体解构下载器",
        "desc": "多线程分块下载、杜比视界与真彩画质解析、多音轨分离抓取的硬核轻量级媒体终端工具。",
        "badge": "CLI POWER · 12.3k★",
        "categoryId": "video",
        "url": "https://github.com/nilaoda/BBDown",
        "launchText": "探查源码 ➔",
        "platform": "ALL TERMINALS"
    },

    # 3. 离线神兵 (Local First)
    {
        "name": "DevToys // 瑞士军刀开发者离线工具箱",
        "desc": "纯本地离线运行的开发利器，涵盖 JSON/YAML 校验、JWT 解码、正则表达式演算、Hash 验算与色彩转换。",
        "badge": "OFFLINE · 25.1k★",
        "categoryId": "local",
        "url": "https://github.com/DevToys-app/DevToys",
        "launchText": "探查源码 ➔",
        "platform": "WIN · MAC · LINUX"
    },
    {
        "name": "LocalSend // 局域网跨端无损极速传输协议",
        "desc": "无需连接互联网、纯局域网点对点互传文件神器。完全开源，秒杀 AirDrop 并通吃 iOS、Android、Windows、Mac。",
        "badge": "P2P SHARE · 49.8k★",
        "categoryId": "local",
        "url": "https://github.com/localsend/localsend",
        "launchText": "探查源码 ➔",
        "platform": "ALL PLATFORMS"
    },
    {
        "name": "Flameshot // 现代化硬核极简截图标注工具",
        "desc": "支持像素级拾色、模糊马赛克、序号标注、多显示器协同与命令行截图自动化，完全本地隐私无后台。",
        "badge": "PRODUCTIVITY · 24.6k★",
        "categoryId": "local",
        "url": "https://github.com/flameshot-org/flameshot",
        "launchText": "探查源码 ➔",
        "platform": "CROSS-PLATFORM"
    },

    # 4. 逆向兵刃 (Geek Arsenal)
    {
        "name": "HTTP Toolkit // 现代化抓包嗅探与网络重构台",
        "desc": "一键拦截、检查并重写 HTTP(S) 网络请求。精准调试 API 接口、解密 App 请求协议与流量分析。",
        "badge": "TRAFFIC · 9.8k★",
        "categoryId": "geek",
        "url": "https://github.com/httptoolkit/httptoolkit",
        "launchText": "探查源码 ➔",
        "platform": "WIN · MAC · LINUX"
    },
    {
        "name": "CyberChef // 极客密码学与数据转换瑞士军刀",
        "desc": "被称为网络安全界的厨师机。纯本地浏览器运行的加密解密、编码转换、反混淆与特征分析超级工作台。",
        "badge": "SWISS ARMY · 30.2k★",
        "categoryId": "geek",
        "url": "https://github.com/gchq/CyberChef",
        "launchText": "探查源码 ➔",
        "platform": "BROWSER / OFFLINE"
    }
]

BENCHMARK_GEMS_SEED = [
    # 1. 视觉力场 (Shader & 3D)
    {
        "url": "https://wodniack.dev",
        "badge": "WEBBY MASTER",
        "badgeClass": "is-webby",
        "rank": "№ 01 · MASTERPIECE",
        "title": "Antoine Wodniack Portfolio",
        "domain": "wodniack.dev ↗",
        "categoryId": "shader",
        "desc": "瑞士平面网格设计、极限排版美学与 Matter.js 刚体物理交互的教科书级天花板典范。",
        "techTags": ["MATTER.JS", "CANVAS 2D", "LENIS SMOOTH", "SWISS TYPO"],
        "footLabel": "INTERACTIVE ARCHIVE",
        "linkText": "VISIT ARCHIVE // 打开灵感 ↳"
    },
    {
        "url": "https://bruno-simon.com",
        "badge": "3D EXPERIMENTAL",
        "badgeClass": "is-codepen",
        "rank": "№ 02 · THREE.JS CAR",
        "title": "Bruno Simon 3D Interactive World",
        "domain": "bruno-simon.com ↗",
        "categoryId": "shader",
        "desc": "在网页中开着越野车漫游探索的 WebGL 3D 物理交互神作，Three.js 交互叙事里程碑。",
        "techTags": ["THREE.JS", "CANNON.JS", "GLSL", "PHYSICS 3D"],
        "footLabel": "CREATIVE WORLD",
        "linkText": "ENTER WORLD // 启动漫游 ↳"
    },
    {
        "url": "https://www.shadertoy.com",
        "badge": "MATH & ART",
        "badgeClass": "is-webby",
        "rank": "№ 03 · PIXEL MAGIC",
        "title": "Shadertoy // 光线步进算法艺术殿堂",
        "domain": "shadertoy.com ↗",
        "categoryId": "shader",
        "desc": "仅用纯数学公式与像素着色器（Fragment Shader）渲染出逼真黑洞、云海与机械奇迹的代码圣殿。",
        "techTags": ["RAYMARCHING", "GLSL SHADER", "PURE MATH", "GPU POWER"],
        "footLabel": "ALGORITHM VAULT",
        "linkText": "DECODE SHADER // 破译算力 ↳"
    },

    # 2. 瑞士排版 (Typo & Grid)
    {
        "url": "https://www.swissted.com",
        "badge": "VINTAGE PUNK",
        "badgeClass": "is-webby",
        "rank": "№ 04 · SWISS POSTER",
        "title": "Swissted // 国际主义平面设计海报展",
        "domain": "swissted.com ↗",
        "categoryId": "typo",
        "desc": "将经典朋克摇滚海报用严谨的瑞士国际字体排版风格进行重构，黑白线框与红黑撞色的教科书。",
        "techTags": ["INTERNATIONAL TYPO", "HELVETICA", "GRID SYSTEM", "BRUTALISM"],
        "footLabel": "TYPO MASTER",
        "linkText": "EXPLORE POSTER // 探查海报 ↳"
    },
    {
        "url": "https://www.curated.design",
        "badge": "CURATION GOLD",
        "badgeClass": "is-codepen",
        "rank": "№ 05 · GRID CATALOG",
        "title": "Curated Design // 极简网格灵感图谱",
        "domain": "curated.design ↗",
        "categoryId": "typo",
        "desc": "按版式网格、衬线排版、动效曲线严苛分类的全球数字设计索引库，寻找神仙审美的必看矿脉。",
        "techTags": ["GRID CATALOG", "MICRO-INTERACTIONS", "EDITORIAL", "CURATION"],
        "footLabel": "INSPIRATION HUB",
        "linkText": "SEARCH CATALOG // 查阅图谱 ↳"
    },

    # 3. 奇趣交互 (Kinetic UX)
    {
        "url": "https://linear.app",
        "badge": "CRAFT CELEBRITY",
        "badgeClass": "is-webby",
        "rank": "№ 06 · KINETIC CRAFT",
        "title": "Linear // 极致微交互与暗黑质感巅峰",
        "domain": "linear.app ↗",
        "categoryId": "kinetic",
        "desc": "被全网前端与产品设计师奉为神作的软件官网。光影渐变漫反射、精密快捷键交互与极致帧率体验。",
        "techTags": ["KEYBOARD FIRST", "DARK MODE LUXURY", "GLOW SHADER", "REACT SMOOTH"],
        "footLabel": "CRAFT EXCELLENCE",
        "linkText": "STUDY CRAFT // 研读微动效 ↳"
    },
    {
        "url": "https://codepen.io/wodniack",
        "badge": "CODEPEN LAB",
        "badgeClass": "is-codepen",
        "rank": "№ 07 · SHADER & MATH",
        "title": "Wodniack Creative Lab",
        "domain": "codepen.io/wodniack ↗",
        "categoryId": "kinetic",
        "desc": "Wormhole 虫洞穿梭、SVG 几何极速透视与 Canvas 极坐标光速星流特效的官方开源实验场。",
        "techTags": ["HYPERSPACE WARP", "SVG MESH", "POLAR SHADER", "OPEN SOURCE"],
        "footLabel": "CREATIVE SOURCE",
        "linkText": "EXPLORE PEN // 探查源码 ↳"
    },

    # 4. 灵感矿脉 (Studio Vault)
    {
        "url": "https://rauno.me/craft",
        "badge": "INDIE ENGINEER",
        "badgeClass": "is-webby",
        "rank": "№ 08 · DESIGN ENGINEERING",
        "title": "Rauno Craft // 交互工程手记",
        "domain": "rauno.me/craft ↗",
        "categoryId": "studio",
        "desc": "Vercel 设计工程副总监的个人实验手札。解构磁吸光标、弹簧物理阻尼与流体界面计算模型。",
        "techTags": ["SPRING PHYSICS", "MAGNETIC CURSOR", "MICRO-CRAFT", "INTERACTION"],
        "footLabel": "ENGINEERING NOTES",
        "linkText": "READ CRAFT // 研读手札 ↳"
    }
]


def call_llm_intelligence(hn_news, v2_news, gh_tools):
    """调用 AI 大模型（DeepSeek / Gemini / OpenAI 格式）重塑全方位时空舱数据"""
    api_key = os.environ.get('AI_API_KEY') or os.environ.get('DEEPSEEK_API_KEY') or os.environ.get('GEMINI_API_KEY') or os.environ.get('OPENAI_API_KEY')
    base_url = os.environ.get('AI_BASE_URL', 'https://api.deepseek.com/v1').rstrip('/')
    model_name = os.environ.get('AI_MODEL', 'deepseek-chat')

    if not api_key:
        print("[INFO] 未检测到 AI_API_KEY，自动启用内置极客智能模板引擎。")
        return None

    print(f"[AI] 正在接入 AI 大模型 ({model_name} @ {base_url}) 生成每日专属分类情报...")

    prompt = f"""
你现在是 BC Studio (独立游戏研发工坊 & 极客灵感数字枢纽) 的首席技术情报官。
请根据以下今日抓取的原始互联网动态与开源项目，提炼出【今日热点雷达】和【开源影音装备】，并严格分配指定分类 ID：

【雷达可用分类 categoryId】：
- "ai": 智子推演 (大模型破局、AI 推理、本格逻辑)
- "global": 寰宇前沿 (HackerNews、海外前沿架构、硬件突破)
- "domestic": 极客生态 (国内独立开发、程序员思潮、生产力)
- "observatory": 视界暗线 (互联网奇闻、未解谜团、网络考古)

【装备可用分类 categoryId】：
- "audio": 天籁之源 (开源桌面音乐播放器、无损音频源、插件解码)
- "video": 极影魔方 (极客视频播放器、流媒体嗅探器、IPTV源、LosslessCut)
- "local": 离线神兵 (纯本地离线生产力工具、DevToys、Markdown)
- "geek": 逆向兵刃 (抓包嗅探、数据转换、解密工具)

【原始科技资讯】：
HackerNews: {json.dumps(hn_news[:4], ensure_ascii=False)}
V2EX: {json.dumps(v2_news[:4], ensure_ascii=False)}

【输出格式要求（严禁任何多余闲话，只输出纯 JSON）】：
{{
  "radar_items": [
    {{
      "categoryId": "ai 或 global 或 domestic 或 observatory",
      "category": "分类标签 // 英文代号 (如 智子推演 // AI & PARADOX)",
      "time": "TODAY // HH:MM UTC",
      "title": "尖锐有力的技术推演标题",
      "summary": "2-3句话剖析事件背后的技术本质与对极客创作者的启示。",
      "specTag": "[ INTEL: 来源或热度指标，如 HACKERNEWS #1 ]",
      "linkText": "READ INTEL // 展开内参 ↳",
      "url": "原文链接"
    }}
  ],
  "toolbox_items": [
    {{
      "categoryId": "audio 或 video 或 local 或 geek",
      "name": "软件名称 // 中文硬核定位 (如 MusicFree // 插件化多音源桌面音乐播放器)",
      "desc": "精准亮点解读：为什么这款开源工具是顶流神器，其架构与支持协议。",
      "badge": "如 MULTI-SOURCE · 16.8k★",
      "url": "GitHub 或项目官网链接",
      "launchText": "探查源码 ➔",
      "platform": "WIN · MAC · LINUX"
    }}
  ]
}}
请挑选 3 条最新的 radar_items 以及 2-3 条顶级开源 toolbox_items。
"""

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': USER_AGENT
    }

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are BC Studio's chief intelligence curator. Always return strictly valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.6,
        "max_tokens": 1500
    }

    try:
        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            res_json = json.loads(resp.read().decode('utf-8'))
            content = res_json['choices'][0]['message']['content'].strip()
            if content.startswith('```'):
                lines = content.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].startswith('```'):
                    lines = lines[:-1]
                content = '\n'.join(lines).strip()
            parsed = json.loads(content)
            print("[SUCCESS] AI 成功完成全景情报分类与语言重塑！")
            return parsed
    except Exception as e:
        print(f"[WARN] AI 接口异常: {e}，将启用高保真实体智能引擎。")
        return None


def generate_fallback_data(hn_news, v2_news, gh_tools):
    """智能降级引擎：生成符合分类的真实热点数据"""
    now_utc = datetime.now(timezone.utc).strftime("%H:%M UTC")
    
    radar_items = []
    
    if hn_news:
        top_hn = hn_news[0]
        radar_items.append({
            "categoryId": "global",
            "category": "寰宇前沿 // GLOBAL TECH",
            "time": f"TODAY // {now_utc}",
            "title": top_hn['title'],
            "summary": f"HackerNews 社区热榜头条（得分 {top_hn['score']}）。该项目引发全网架构师与开发者关于现代计算体系、开源生态与工程效率的深度论战。",
            "specTag": f"[ SOURCE: HACKERNEWS #{top_hn['score']}★ ]",
            "linkText": "READ INTEL // 展开内参 ↳",
            "url": top_hn['url']
        })
    
    if v2_news:
        top_v2 = v2_news[0]
        radar_items.append({
            "categoryId": "domestic",
            "category": "极客生态 // DOMESTIC DEV",
            "time": f"TODAY // {now_utc}",
            "title": top_v2['title'],
            "summary": f"来自国内开发者社区的热点思潮（讨论度 {top_v2['replies']} 节点：{top_v2['node']}）。折射出当下国内程序员在独立开发、日常生产力重构与工程落地中的真实呼声。",
            "specTag": f"[ RADAR FREQ: V2EX {top_v2['replies']} REPLIES ]",
            "linkText": "READ INTEL // 展开内参 ↳",
            "url": top_v2['url']
        })

    radar_items.append({
        "categoryId": "ai",
        "category": "智子推演 // AI & PARADOX",
        "time": f"TODAY // {now_utc}",
        "title": "多模态推演能否构建真正的“物理闭环密室”？",
        "summary": "实测最新前沿大模型在多重伪解答架构中的表现：虽然能瞬间生成海量障眼法，但在微观物理材质力学与时间线交叉口供的精确剪裁上，人类本格心机依然是不可替代的胜负手。",
        "specTag": "[ INTEL: DUAL-CHAMBER LOGIC ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://bckj.site"
    })

    return {
        "radar_items": radar_items,
        "toolbox_items": gh_tools[:3] if gh_tools else []
    }


def update_spatial_chambers_lifecycle(new_radar, new_tools):
    """
    全自动生命周期与容量控制体系：
    1. 今日雷达：FIFO 保持 15 条
    2. 开源装备库：当期 30 款（云盘置顶），超量沉淀至 archive 历史卷宗
    3. 神仙网站：当期 20 款，超量沉淀至 archive
    """
    if not os.path.exists(JSON_PATH):
        print(f"[ERROR] 找不到时空舱配置文件: {JSON_PATH}")
        sys.exit(1)

    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 写入中控分类矩阵
    data['radarChamber']['categories'] = RADAR_CATEGORIES
    data['toolboxChamber']['categories'] = TOOLBOX_CATEGORIES
    data['gemsChamber']['categories'] = GEMS_CATEGORIES

    if 'archive' not in data['toolboxChamber']:
        data['toolboxChamber']['archive'] = []
    if 'archive' not in data['gemsChamber']:
        data['gemsChamber']['archive'] = []

    # ----------------------------------------------------
    # 1. 今日热点雷达：15条容量先进先出滚动
    # ----------------------------------------------------
    existing_radar = data['radarChamber'].get('items', [])
    combined_radar = []
    seen_radar_urls = set()

    for item in (new_radar + existing_radar):
        url = item.get('url') or item.get('title')
        if url and url not in seen_radar_urls:
            seen_radar_urls.add(url)
            # 补齐 categoryId
            if 'categoryId' not in item:
                cat_lower = (item.get('category') or '').lower()
                if 'ai' in cat_lower or '推演' in cat_lower:
                    item['categoryId'] = 'ai'
                elif 'global' in cat_lower or '海外' in cat_lower or 'hackernews' in cat_lower:
                    item['categoryId'] = 'global'
                elif 'domestic' in cat_lower or '国内' in cat_lower or 'v2ex' in cat_lower:
                    item['categoryId'] = 'domestic'
                else:
                    item['categoryId'] = 'observatory'
            combined_radar.append(item)

    # 严格保持最多 15 条
    data['radarChamber']['items'] = combined_radar[:15]
    print(f"[LIFECYCLE] 今日雷达已同步：当期驻留 {len(data['radarChamber']['items'])}/15 条最前沿情报。")

    # ----------------------------------------------------
    # 2. 开源影音武器库：当期 30 款 + 历史归档卷宗
    # ----------------------------------------------------
    alist_permanent_card = {
        "name": "BC Cloud Drive // 个人私有高速云盘",
        "desc": "基于 AList 与百度网盘聚合的高速资源仓 · 包含插画课程、单机游戏与设计资产，直链极速下载。",
        "badge": "ONLINE · CLOUD",
        "categoryId": "local",
        "url": "http://111.229.205.54:5244",
        "isPrimary": True,
        "launchText": "打开云盘 ➔",
        "platform": "ALL PLATFORMS"
    }

    existing_tools = [t for t in data['toolboxChamber'].get('tools', []) if not t.get('isPrimary')]
    archive_tools = data['toolboxChamber'].get('archive', [])

    # 融合新增、现有和基准库
    raw_pool = new_tools + existing_tools + BENCHMARK_TOOLBOX_SEED
    unique_pool = []
    seen_tool_urls = set(['http://111.229.205.54:5244'])

    for t in raw_pool:
        url = t.get('url') or t.get('name')
        if url and url not in seen_tool_urls:
            seen_tool_urls.add(url)
            if 'categoryId' not in t:
                name_l = (t.get('name') or '').lower()
                desc_l = (t.get('desc') or '').lower()
                if 'music' in name_l or '音乐' in name_l or 'audio' in desc_l:
                    t['categoryId'] = 'audio'
                elif 'video' in name_l or '播放器' in name_l or 'stream' in desc_l or 'lossless' in name_l:
                    t['categoryId'] = 'video'
                elif 'devtoys' in name_l or 'localsend' in name_l or '离线' in desc_l:
                    t['categoryId'] = 'local'
                else:
                    t['categoryId'] = 'geek'
            unique_pool.append(t)

    # 当期精选上限 30 款（加上 AList 共 31 项）
    ACTIVE_LIMIT = 30
    active_tools = unique_pool[:ACTIVE_LIMIT]
    overflow_tools = unique_pool[ACTIVE_LIMIT:]

    # 超量自动沉淀到历史归档
    archive_seen = set(t.get('url') for t in archive_tools)
    now_month = datetime.now().strftime("%Y.%m")
    for ot in overflow_tools:
        if ot.get('url') not in archive_seen:
            archive_seen.add(ot.get('url'))
            ot['archivedAt'] = f"ARCHIVED · {now_month}"
            archive_tools.append(ot)

    data['toolboxChamber']['tools'] = [alist_permanent_card] + active_tools
    data['toolboxChamber']['archive'] = archive_tools
    print(f"[LIFECYCLE] 开源装备库已同步：当期精选 {len(data['toolboxChamber']['tools'])} 款 (AList 置顶)，历史卷宗沉淀 {len(archive_tools)} 款。")

    # ----------------------------------------------------
    # 3. 神仙网站灵感矿藏：当期 20 款 + 历史归档
    # ----------------------------------------------------
    existing_gems = data['gemsChamber'].get('gems', [])
    archive_gems = data['gemsChamber'].get('archive', [])

    raw_gems = existing_gems + BENCHMARK_GEMS_SEED
    unique_gems = []
    seen_gem_urls = set()
    for g in raw_gems:
        url = g.get('url') or g.get('title')
        if url and url not in seen_gem_urls:
            seen_gem_urls.add(url)
            if 'categoryId' not in g:
                g['categoryId'] = 'shader'
            unique_gems.append(g)

    GEMS_LIMIT = 20
    active_gems = unique_gems[:GEMS_LIMIT]
    overflow_gems = unique_gems[GEMS_LIMIT:]

    for og in overflow_gems:
        og['archivedAt'] = f"ARCHIVED · {now_month}"
        archive_gems.append(og)

    data['gemsChamber']['gems'] = active_gems
    data['gemsChamber']['archive'] = archive_gems
    print(f"[LIFECYCLE] 神仙网站已同步：当期矿藏 {len(active_gems)} 款，历史卷宗 {len(archive_gems)} 款。")

    # 写入配置文件
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] 成功更新时空舱配置文件: {JSON_PATH}")


def main():
    print("==================================================")
    print("  BC Studio // 时空舱三位一体智能情报与开源中枢  ")
    print("==================================================")

    hn_news = fetch_hacker_news(limit=6)
    v2_news = fetch_v2ex_hot(limit=6)
    gh_tools = fetch_github_tools()

    ai_result = call_llm_intelligence(hn_news, v2_news, gh_tools)

    if ai_result and 'radar_items' in ai_result and 'toolbox_items' in ai_result:
        radar_items = ai_result['radar_items']
        toolbox_items = ai_result['toolbox_items']
    else:
        fallback = generate_fallback_data(hn_news, v2_news, gh_tools)
        radar_items = fallback['radar_items']
        toolbox_items = fallback['toolbox_items']

    update_spatial_chambers_lifecycle(radar_items, toolbox_items)
    print("==================================================")
    print("  [OK] 数据全景生命周期处理完成！  ")
    print("==================================================")


if __name__ == '__main__':
    main()
