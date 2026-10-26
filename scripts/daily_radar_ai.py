#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BC Studio - 时空舱全自动情报、开源装备与灵感中枢 (Daily Autonomous Hub)
- 抓取信源：
  * HackerNews API 全球前沿科技要闻 (Top 15)
  * V2EX API 国内极客思潮与开发者生态 (Hot 15)
  * GitHub Multi-topic 实时探测 (Audio / Video / Local / Geek 武器库)
  * Creative Web Showcase 每日惊艳交互设计动态
- 智能轮转与容量控制机制：
  * 今日雷达 (Chamber 03)：严格保持 15 条 FIFO 滚动缓冲（超量自动淘汰，保证每日最鲜活）
  * 开源装备 (Chamber 05)：严格保持 30 款当期精选（AList 私有云盘置顶），超量自动沉淀至【历史卷宗】永久可查
  * 神仙网站 (Chamber 04)：严格保持 20 款当期精选，超量自动沉淀至【历史卷宗】永久可查
- 目标数据文件：src/data/spatial-chambers.json
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JSON_PATH = os.path.join(WORKSPACE_DIR, 'src', 'data', 'spatial-chambers.json')

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 BC-Intel-Bot/3.0'

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


def fetch_hacker_news(limit=12):
    """获取 HackerNews Top 科技头条并智能分流"""
    print(f"[1/4] 正在拉取全球前沿科技情报 (HackerNews Top {limit})...")
    top_ids = http_get_json('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=8)
    if not top_ids:
        return []

    news_items = []
    for sid in top_ids[:limit]:
        item = http_get_json(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json', timeout=5)
        if item and 'title' in item:
            title = item.get('title', '')
            title_lower = title.lower()
            # 智能分类判断
            if any(k in title_lower for k in ['ai', 'gpt', 'llm', 'model', 'claude', 'deepseek', 'neural', 'reasoning', 'agent']):
                cat = 'ai'
            elif any(k in title_lower for k in ['security', 'vulnerability', 'hack', 'leak', 'dark', 'cipher', 'mystery', 'crypto']):
                cat = 'observatory'
            else:
                cat = 'global'

            news_items.append({
                'title': title,
                'url': item.get('url') or f"https://news.ycombinator.com/item?id={sid}",
                'score': item.get('score', 0),
                'by': item.get('by', 'anon'),
                'categoryId': cat,
                'source': 'HackerNews'
            })
    return news_items


def fetch_v2ex_hot(limit=10):
    """获取国内开发者热议话题 (V2EX Hot)"""
    print(f"[2/4] 正在拉取国内极客热议话题 (V2EX Hot {limit})...")
    topics = http_get_json('https://www.v2ex.com/api/topics/hot.json', timeout=8)
    if not topics:
        return []

    domestic_items = []
    for t in topics[:limit]:
        title = t.get('title', '')
        title_l = title.lower()
        if any(k in title_l for k in ['ai', 'deepseek', 'gpt', '大模型', 'agent']):
            cat = 'ai'
        elif any(k in title_l for k in ['黑客', '安全', '漏洞', '隐私', '离奇', '探秘']):
            cat = 'observatory'
        else:
            cat = 'domestic'

        domestic_items.append({
            'title': title,
            'url': t.get('url') or f"https://www.v2ex.com/t/{t.get('id')}",
            'replies': t.get('replies', 0),
            'node': (t.get('node') or {}).get('title', '开发者生态'),
            'categoryId': cat,
            'source': 'V2EX'
        })
    return domestic_items


def fetch_github_tools():
    """多维度扫描 GitHub 上的开源影音播放器、音频源、视频源与极客神兵"""
    print("[3/4] 正在跨维度探测 GitHub 顶级开源神兵 (Audio / Video / Local / Geek)...")
    live_tools = []
    gh_headers = {'User-Agent': USER_AGENT}
    gh_token = os.environ.get('GITHUB_TOKEN')
    if gh_token:
        gh_headers['Authorization'] = f'Bearer {gh_token}'

    queries = [
        ('topic:music-player+sort:stars', 'audio', '跨平台音乐流媒体客户端', 'AUDIO ·'),
        ('topic:video-player+sort:stars', 'video', '高性能极简视频渲染播放器', 'VIDEO ·'),
        ('topic:offline-first+sort:stars', 'local', '离线优先本地生产力利器', 'LOCAL ·'),
        ('topic:reverse-engineering+sort:stars', 'geek', '网络抓包嗅探与逆向架构台', 'GEEK ·')
    ]

    for q, cat, default_desc, badge_prefix in queries:
        try:
            search_url = f'https://api.github.com/search/repositories?q={q}&per_page=4'
            data = http_get_json(search_url, timeout=6, headers=gh_headers)
            if data and 'items' in data:
                for item in data['items'][:2]:
                    stars_k = f"{round(item.get('stargazers_count', 0) / 1000, 1)}k★"
                    name_clean = item.get('name')
                    desc = item.get('description') or default_desc
                    live_tools.append({
                        "name": f"{name_clean} // {default_desc}",
                        "desc": desc,
                        "badge": f"{badge_prefix} {stars_k}",
                        "categoryId": cat,
                        "url": item.get('html_url'),
                        "launchText": "探查源码 ➔",
                        "platform": "CROSS-PLATFORM"
                    })
        except Exception as e:
            print(f"[INFO] GitHub 在线探测日志 ({cat}): {e}")

    return live_tools


def fetch_live_gems():
    """实时探索 GitHub 与设计生态中的高颜值创意编程与惊艳交互项目"""
    print("[4/4] 正在探索全球先锋 WebGL / 瑞士排版 / 创意网站矿脉...")
    live_gems = []
    try:
        gh_headers = {'User-Agent': USER_AGENT}
        gh_token = os.environ.get('GITHUB_TOKEN')
        if gh_token:
            gh_headers['Authorization'] = f'Bearer {gh_token}'

        search_url = 'https://api.github.com/search/repositories?q=topic:creative-coding+sort:stars&per_page=4'
        data = http_get_json(search_url, timeout=6, headers=gh_headers)
        if data and 'items' in data:
            for item in data['items'][:2]:
                stars_k = f"{round(item.get('stargazers_count', 0) / 1000, 1)}k★"
                name_clean = item.get('name')
                live_gems.append({
                    "url": item.get('html_url'),
                    "badge": f"CODE · {stars_k}",
                    "badgeClass": "is-codepen",
                    "rank": "CREATIVE REPO",
                    "title": f"{name_clean} // 创意力场实验室",
                    "domain": "github.com ↗",
                    "categoryId": "shader",
                    "desc": item.get('description') or "极具探索性的三维图形学与数学视觉算法实验项目。",
                    "techTags": ["WEBGL", "GLSL", "CANVAS", "CREATIVE"],
                    "footLabel": "CREATIVE SOURCE",
                    "linkText": "VISIT REPO // 探查矿脉 ↳"
                })
    except Exception as e:
        print(f"[INFO] Web Gems 在线探索日志: {e}")

    return live_gems


# ==========================================
# 标杆高分热点基准库 (Radar 15 槽位基石)
# ==========================================
BENCHMARK_RADAR_SEED = [
    # 1. 智子推演 (AI & Paradox)
    {
        "categoryId": "ai",
        "category": "智子推演 // AI & PARADOX",
        "time": "TODAY // 08:30 UTC",
        "title": "多模态推演能否构建真正的“物理闭环密室”？",
        "summary": "实测最新前沿大模型在多重伪解答架构中的表现：虽然能瞬间生成海量障眼法，但在微观物理材质力学与时间线交叉口供的精确剪裁上，人类本格心机依然是不可替代的胜负手。",
        "specTag": "[ INTEL: DUAL-CHAMBER LOGIC ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://bckj.site"
    },
    {
        "categoryId": "ai",
        "category": "智子推演 // AI & PARADOX",
        "time": "TODAY // 07:15 UTC",
        "title": "Reasoning Models 时代：从盲目补全到本格长链条自我证伪",
        "summary": "深度剖析 DeepSeek-R1 与 o1 类思考模型的拓扑结构，大模型首次具备了推翻自身第一假设并回溯验证的能力，如同侦探在案发现场推演多条死胡同后的绝地反击。",
        "specTag": "[ BREAKTHROUGH: REASONING R1 ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://news.ycombinator.com"
    },
    {
        "categoryId": "ai",
        "category": "智子推演 // AI & PARADOX",
        "time": "TODAY // 06:40 UTC",
        "title": "Agentic Coding 范式转移：写代码已演变为系统架构博弈",
        "summary": "当 AI 助手能自主分析数十万行跨模块依赖并执行精准重构，程序员的核心竞争力正在从语法敲击彻底迁徙为逻辑裁决与本格审美鉴赏。",
        "specTag": "[ PARADIGM: AGENTIC CODING ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://github.com/trending"
    },
    {
        "categoryId": "ai",
        "category": "智子推演 // AI & PARADOX",
        "time": "TODAY // 05:20 UTC",
        "title": "本地端侧算力突围：纯离线小参数模型赋能单机推理游戏",
        "summary": "基于 WebGPU 与 ONNX 架构的 1.5B/3B 参数端侧模型实测，无需连接云端即可实现亚秒级动态 NPC 心理博弈，彻底斩断隐私泄露与高昂服务器账单。",
        "specTag": "[ LOCAL INFERENCE: WEBGPU ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://huggingface.co"
    },

    # 2. 寰宇前沿 (Global Tech)
    {
        "categoryId": "global",
        "category": "寰宇前沿 // GLOBAL TECH",
        "time": "TODAY // 08:10 UTC",
        "title": "We should be more ambitious with the software we build",
        "summary": "HackerNews 社区热榜头条：技术作者批判现代软件被沉重框架与臃肿抽象束缚，呼吁回归瑞士钟表般的精密轻量原生体验与极致运行速度。",
        "specTag": "[ ESSAY: AMBITIOUS SOFTWARE ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://danluu.com/ambitious/"
    },
    {
        "categoryId": "global",
        "category": "寰宇前沿 // GLOBAL TECH",
        "time": "TODAY // 07:05 UTC",
        "title": "OBS Studio 33 突破性更新：原生重构实时渲染流管线",
        "summary": "开源推流与录屏标杆工具 OBS 发布 33.0 巨型里程碑，重构跨平台音视频管道并降低 40% 渲染延迟，为创作者带来工业级实时推流底座。",
        "specTag": "[ RELEASE: OBS STUDIO 33 ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://github.com/obsproject/obs-studio/releases"
    },
    {
        "categoryId": "global",
        "category": "寰宇前沿 // GLOBAL TECH",
        "time": "TODAY // 06:12 UTC",
        "title": "Rust 与 Zig 在系统级低延迟图形引擎中的暗流争锋",
        "summary": "从 WebAssembly 到原生 GPU 驱动层，现代独立游戏开发者正在用无垃圾回收的内存安全语言重构游戏底层，彻底告别微卡顿与掉帧宿疾。",
        "specTag": "[ ARCHITECTURE: SYSTEMS SPEED ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://news.ycombinator.com"
    },
    {
        "categoryId": "global",
        "category": "寰宇前沿 // GLOBAL TECH",
        "time": "TODAY // 04:50 UTC",
        "title": "WebKit 率先实现无损流体视口计算规范标准",
        "summary": "针对移动端动态地址栏导致的 100vh 遮挡痼疾，W3C 推进的新型 svh/lvh/dvh 单位已全面在各大移动端内核实装，移动端全屏交互迎来纯净新基石。",
        "specTag": "[ STANDARD: VIEWPORT UNITS ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://webkit.org/blog/"
    },

    # 3. 极客生态 (Domestic Dev)
    {
        "categoryId": "domestic",
        "category": "极客生态 // DOMESTIC DEV",
        "time": "TODAY // 08:00 UTC",
        "title": "为什么很多人把 DeepSeek 神化了？看国内大模型工程落地思潮",
        "summary": "来自国内开发者社区的热点思潮（讨论度 60+ 节点：程序员）。折射出当下国内程序员在独立开发、日常生产力重构与工程落地中的真实呼声。",
        "specTag": "[ RADAR FREQ: V2EX 61 REPLIES ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://www.v2ex.com/t/1251402"
    },
    {
        "categoryId": "domestic",
        "category": "极客生态 // DOMESTIC DEV",
        "time": "TODAY // 07:30 UTC",
        "title": "一人独立游戏工坊全栈工作流：从剧本闭环到自建发行矩阵",
        "summary": "国内独立开发者分享如何凭借现代静态生成器与边缘网络托管搭建高逼格官网，以极低维护成本撬动高留存硬核推理用户圈层。",
        "specTag": "[ INDIE STACK: BC STUDIO ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://bckj.site"
    },
    {
        "categoryId": "domestic",
        "category": "极客生态 // DOMESTIC DEV",
        "time": "TODAY // 05:45 UTC",
        "title": "私有云盘 AList 生态爆发：家庭微型服务器如何重构数字资产仓",
        "summary": "探讨基于 Linux 迷你主机与 Docker 容器聚合全网网盘直链的实战经验，彻底解决插画资产与高清无损影音的跨设备高速传输痛点。",
        "specTag": "[ STORAGE: ALIST VAULT ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://www.v2ex.com"
    },
    {
        "categoryId": "domestic",
        "category": "极客生态 // DOMESTIC DEV",
        "time": "TODAY // 03:50 UTC",
        "title": "逆向嗅探与私有协议解析：极客创作者的日常兵刃考究",
        "summary": "从桌面音频解析插件到无损剪刀 LosslessCut，国内极客群体正在用纯粹开源免费的轻巧小工具打破大厂壁垒，守护个人离线数字主权。",
        "specTag": "[ GEEK LIFE: TOOLBOX ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://www.v2ex.com"
    },

    # 4. 视界暗线 (Observatory)
    {
        "categoryId": "observatory",
        "category": "视界暗线 // OBSERVATORY",
        "time": "TODAY // 07:50 UTC",
        "title": "网络考古：1999 年消失的网页暗号与早期密室迷踪解构",
        "summary": "探秘 Web 1.0 时代隐藏在 HTML 注释与纯文本论坛中的暗线解谜游戏，本格派推理如何在早期赛博空间生根发芽并影响当下一代创作者。",
        "specTag": "[ ARCHAEOLOGY: 1999 CIPHER ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://news.ycombinator.com"
    },
    {
        "categoryId": "observatory",
        "category": "视界暗线 // OBSERVATORY",
        "time": "TODAY // 06:30 UTC",
        "title": "暗网通信协议中的时延混淆算法与反向测谎模型",
        "summary": "深层解构基于发条式随机延迟网络包的匿名通信原理，该机制与本格推理中“利用留声机与定时器构筑不在场证明”的物理诡计高度同构。",
        "specTag": "[ DECODE: TIMING ATTACK ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://bckj.site"
    },
    {
        "categoryId": "observatory",
        "category": "视界暗线 // OBSERVATORY",
        "time": "TODAY // 05:10 UTC",
        "title": "被遗忘的冷战短波电台：频段中的“林肯郡偷猎者”机械密码",
        "summary": "数字电台（Numbers Station）二十年未解之谜复盘：全自动磁带循环播报、一次性密码本（OTP）与不可破译的绝对数学盲区。",
        "specTag": "[ CRYPTO: NUMBERS STATION ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://en.wikipedia.org/wiki/Numbers_station"
    },
    {
        "categoryId": "observatory",
        "category": "视界暗线 // OBSERVATORY",
        "time": "TODAY // 04:15 UTC",
        "title": "全网未解数字谜题：Cicada 3301 经典密码学拓扑复盘",
        "summary": "回顾互联网历史上最富神秘色彩的本格密码学挑战，融合了物理书本密钥、微积分极坐标与暗网洋葱路由的跨维度脑力激荡。",
        "specTag": "[ MYSTERY: CICADA 3301 ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://en.wikipedia.org/wiki/Cicada_3301"
    },
    {
        "categoryId": "observatory",
        "category": "视界暗线 // OBSERVATORY",
        "time": "TODAY // 03:00 UTC",
        "title": "深网协议考古：从 Gopher、Usenet 到 Nostr 的极客抗审查暗线",
        "summary": "当主流互联网被封闭花园与算法投喂彻底隔绝，极客开发者正在用纯粹端到端公私钥对与中继网络重构不受限的自由信息暗网。",
        "specTag": "[ PROTOCOL: NOSTR ARCH ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://github.com/nostr-protocol"
    }
]


# ==========================================
# 标杆高分开源装备库 (36 款全领域极客装备)
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
        "name": "YesPlayMusic // 高颜值第三方网易云桌面客户端",
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
    {
        "name": "Moosync // 现代化本地与流媒体双轨音乐播放器",
        "desc": "专为极客音乐爱好者打造。同时管理本地高解析 FLAC 音乐库与 Spotify/YouTube 远程播放列表，支持自定义均衡器与扩展。",
        "badge": "MODERN AUDIO · 3.8k★",
        "categoryId": "audio",
        "url": "https://github.com/Moosync/Moosync",
        "launchText": "探查源码 ➔",
        "platform": "CROSS-PLATFORM"
    },
    {
        "name": "Navidrome // 轻量自建私有云端无损音乐服务器",
        "desc": "现代高性能自建音乐服务器，基于 Go 语言开发，纯本地扫描无损音乐文件夹，支持全平台 Subsonic 协议客户端投屏与串流。",
        "badge": "SELF-HOSTED · 14.2k★",
        "categoryId": "audio",
        "url": "https://github.com/navidrome/navidrome",
        "launchText": "探查源码 ➔",
        "platform": "DOCKER · LINUX · WIN"
    },
    {
        "name": "BlackHole // macOS 零延迟虚拟音频路由内录驱动",
        "desc": "解决 macOS 系统无法直接录制系统声音或各 App 间音频跳线的终极内核级开源虚拟声卡，混音与播客制作必备。",
        "badge": "CORE AUDIO · 17.5k★",
        "categoryId": "audio",
        "url": "https://github.com/ExistentialAudio/BlackHole",
        "launchText": "探查源码 ➔",
        "platform": "MACOS"
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
    {
        "name": "BililiveRecorder // 全自动无人值守高清流媒体录播姬",
        "desc": "专为直播流保存设计的全自动守护进程。开播自动极速录制，智能跳过重连并无缝混流为标准 MP4，支持多主播并发。",
        "badge": "AUTO STREAM · 3.5k★",
        "categoryId": "video",
        "url": "https://github.com/BililiveRecorder/BililiveRecorder",
        "launchText": "探查源码 ➔",
        "platform": "CROSS-PLATFORM"
    },
    {
        "name": "Jellyfin // 100% 自由开源媒体服务器全端投屏系统",
        "desc": "无商业化绑架的纯净媒体中心。自动刮削电影与剧集海报墙、支持硬件转码与全家跨端协同流媒体点播。",
        "badge": "MEDIA CENTER · 36.8k★",
        "categoryId": "video",
        "url": "https://github.com/jellyfin/jellyfin",
        "launchText": "探查源码 ➔",
        "platform": "SERVER · CLIENT"
    },
    {
        "name": "HandBrake // 跨平台硬件加速通用视频压制转码利器",
        "desc": "近二十年开源常青树。支持 NVENC / QuickSync 硬件编码，精准裁切黑边、优化色彩空间与批量压缩 4K 大文件。",
        "badge": "TRANSCODER · 16.5k★",
        "categoryId": "video",
        "url": "https://github.com/HandBrake/HandBrake",
        "launchText": "探查源码 ➔",
        "platform": "WIN · MAC · LINUX"
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
    {
        "name": "CyberChef // 极客密码学与数据转换瑞士军刀",
        "desc": "被称为网络安全界的厨师机。纯本地浏览器运行的加密解密、编码转换、反混淆与特征分析超级工作台。",
        "badge": "SWISS ARMY · 30.2k★",
        "categoryId": "local",
        "url": "https://github.com/gchq/CyberChef",
        "launchText": "探查源码 ➔",
        "platform": "BROWSER / OFFLINE"
    },
    {
        "name": "Espanso // 全平台 Rust 驱动极速文本扩展补全器",
        "desc": "基于 Rust 开发的跨平台快捷键文本扩展神器。输入简短暗号自动展开为长邮件模板、代码片段或当前时间戳，完全离线。",
        "badge": "RUST SPEED · 14.9k★",
        "categoryId": "local",
        "url": "https://github.com/espanso/espanso",
        "launchText": "探查源码 ➔",
        "platform": "CROSS-PLATFORM"
    },
    {
        "name": "RustDesk // 100% 开源自建中继远程桌面控制软件",
        "desc": "完全可替代 TeamViewer / AnyDesk 的自建远程协助利器。支持自建 Relay 中继服务器，端到端加密零商业限制。",
        "badge": "REMOTE · 81.2k★",
        "categoryId": "local",
        "url": "https://github.com/rustdesk/rustdesk",
        "launchText": "探查源码 ➔",
        "platform": "ALL PLATFORMS"
    },
    {
        "name": "ShareX // Windows 终极截图与屏幕录制自动化武器",
        "desc": "拥有 15 年历史的 Windows 截屏与工作流自动化开源巨匠。支持 OCR 识别、颜色拾取与自定义目标自动上传。",
        "badge": "WORKFLOW · 28.5k★",
        "categoryId": "local",
        "url": "https://github.com/ShareX/ShareX",
        "launchText": "探查源码 ➔",
        "platform": "WINDOWS"
    },
    {
        "name": "Bruno // 本地离线优先轻量级 API 调试客户端",
        "desc": "告别 Postman 云端绑架与强制登录。采用纯文本 Bru 语言直接保存在 Git 仓库中，纯离线安全高速调试 API 请求。",
        "badge": "API CLIENT · 27.8k★",
        "categoryId": "local",
        "url": "https://github.com/usebruno/bruno",
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
        "name": "Caido // 轻量高效 Rust 打造的现代化 Web 安全渗透台",
        "desc": "专为安全研究员与协议分析师打造的现代网络审计工具。内存占用不足 Burp Suite 十分之一，UI 极具赛博现代感。",
        "badge": "SECURITY · 4.8k★",
        "categoryId": "geek",
        "url": "https://github.com/caido/caido",
        "launchText": "探查源码 ➔",
        "platform": "CROSS-PLATFORM"
    },
    {
        "name": "Scrcpy // 极低延迟安卓终端投屏与反向键盘鼠标控制",
        "desc": "无需 Root、无需在手机安装任何 App。纯 ADB 管道实现 30-70ms 极低延迟 60FPS 安卓屏幕投射与键盘鼠标操控。",
        "badge": "ADB MIRROR · 119k★",
        "categoryId": "geek",
        "url": "https://github.com/Genymobile/scrcpy",
        "launchText": "探查源码 ➔",
        "platform": "CROSS-PLATFORM"
    },
    {
        "name": "Ghidra // 软件逆向工程与二进制反编译架构",
        "desc": "由美国国家安全局开源的强大逆向工程套件。支持 x86/ARM/MIPS 全指令集反汇编与 C 语言高阶代码反编译还原。",
        "badge": "REVERSE · 53.6k★",
        "categoryId": "geek",
        "url": "https://github.com/NationalSecurityAgency/ghidra",
        "launchText": "探查源码 ➔",
        "platform": "CROSS-PLATFORM"
    },
    {
        "name": "Wireshark // 全球标杆网络数据包深层协议解构分析器",
        "desc": "网络通信世界的终极听诊器。精准抓取以太网、TCP/IP、DNS 与 TLS 握手数据包，排查网络故障与协议逆向必备。",
        "badge": "PACKET · 3.5k★",
        "categoryId": "geek",
        "url": "https://gitlab.com/wireshark/wireshark",
        "launchText": "探查源码 ➔",
        "platform": "ALL PLATFORMS"
    },
    {
        "name": "Postcat // 开源敏捷 API 研发全生命周期协作工作台",
        "desc": "支持插件化扩展的高颜值 API 管理工具。纯本地数据存储、支持多协议调试与代码自动生成，完全开源免费。",
        "badge": "API HUB · 4.2k★",
        "categoryId": "geek",
        "url": "https://github.com/Postcatlab/postcat",
        "launchText": "探查源码 ➔",
        "platform": "CROSS-PLATFORM"
    },
    {
        "name": "Mitmproxy // 交互式命令行与 Python 扩展 HTTPS 拦截代理",
        "desc": "完全可编程的中间人代理工具。支持用 Python 脚本实时篡改请求头、解密流量并重放数据包，渗透测试利器。",
        "badge": "PROXY · 35.8k★",
        "categoryId": "geek",
        "url": "https://github.com/mitmproxy/mitmproxy",
        "launchText": "探查源码 ➔",
        "platform": "PYTHON CLI"
    },
    {
        "name": "Reqable // 新一代 API 调试与 HTTPS 抓包双合一客户端",
        "desc": "基于 Flutter 开发的现代化跨平台抓包利器，将 Fiddler 抓包能力与 Postman 接口测试深度融合，速度飞快。",
        "badge": "DUAL TOOLS · 7.5k★",
        "categoryId": "geek",
        "url": "https://reqable.com",
        "launchText": "探查官网 ➔",
        "platform": "CROSS-PLATFORM"
    }
]


# ==========================================
# 标杆高分神仙网站矿藏库 (25 款顶级设计与交互标杆)
# ==========================================
BENCHMARK_GEMS_SEED = [
    # 1. 视觉力场 (Shader & 3D)
    {
        "url": "https://wodniack.dev",
        "badge": "2025 WEBBY NOMINEE",
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
    {
        "url": "https://lusion.co",
        "badge": "CREATIVE STUDIO",
        "badgeClass": "is-webby",
        "rank": "№ 04 · PARTICLE FIELD",
        "title": "Lusion Creative Technical Studio",
        "domain": "lusion.co ↗",
        "categoryId": "shader",
        "desc": "将数百万粒子流体动力学与三维着色器发挥到极限的全球顶级创意实验室官网，极富未来感。",
        "techTags": ["PARTICLE 3D", "WEBGL FLUID", "CUSTOM SHADER", "SOUND FX"],
        "footLabel": "STUDIO SHOWCASE",
        "linkText": "EXPLORE LUSION // 探查力场 ↳"
    },
    {
        "url": "https://keitayamada.com",
        "badge": "NEO-TOKYO 3D",
        "badgeClass": "is-codepen",
        "rank": "№ 05 · CYBER PARALLAX",
        "title": "Keita Yamada // 赛博视差空间",
        "domain": "keitayamada.com ↗",
        "categoryId": "shader",
        "desc": "融合日本动漫机械美学与全屏 WebGL 视差滚动的独立作品集，光影漫反射与动效丝滑无比。",
        "techTags": ["THREE.JS", "CYBER STYLE", "PARALLAX", "WEBAUDIO"],
        "footLabel": "INDIE PORTFOLIO",
        "linkText": "ENTER LAB // 进入视界 ↳"
    },
    {
        "url": "https://activetheory.net",
        "badge": "LEGENDARY AGENCY",
        "badgeClass": "is-webby",
        "rank": "№ 06 · WEBGPU VAULT",
        "title": "Active Theory // 创意叙事交互殿堂",
        "domain": "activetheory.net ↗",
        "categoryId": "shader",
        "desc": "十年蝉联全球创意大奖的先锋技术团队，独家自研 WebGL/WebGPU 渲染引擎赋能前沿商业叙事。",
        "techTags": ["CUSTOM ENGINE", "WEBGPU", "INTERACTIVE FILM", "GLSL"],
        "footLabel": "AGENCY VAULT",
        "linkText": "VISIT STUDIO // 探查殿堂 ↳"
    },

    # 2. 瑞士排版 (Typo & Grid)
    {
        "url": "https://www.swissted.com",
        "badge": "VINTAGE PUNK",
        "badgeClass": "is-webby",
        "rank": "№ 07 · SWISS POSTER",
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
        "rank": "№ 08 · GRID CATALOG",
        "title": "Curated Design // 极简网格灵感图谱",
        "domain": "curated.design ↗",
        "categoryId": "typo",
        "desc": "按版式网格、衬线排版、动效曲线严苛分类的全球数字设计索引库，寻找神仙审美的必看矿脉。",
        "techTags": ["GRID CATALOG", "MICRO-INTERACTIONS", "EDITORIAL", "CURATION"],
        "footLabel": "INSPIRATION HUB",
        "linkText": "SEARCH CATALOG // 查阅图谱 ↳"
    },
    {
        "url": "https://www.siteinspire.com",
        "badge": "TIMELESS ARCHIVE",
        "badgeClass": "is-webby",
        "rank": "№ 09 · EDITORIAL GRID",
        "title": "siteInspire // 极简主义网页美学库",
        "domain": "siteinspire.com ↗",
        "categoryId": "typo",
        "desc": "历经十余年纯人工筛选的数字排版档案。没有浮夸特效，专注纯粹字体层次与优雅空间节奏。",
        "techTags": ["EDITORIAL", "CLEAN TYPO", "ARCHIVE", "ELEGANCE"],
        "footLabel": "EDITORIAL VAULT",
        "linkText": "BROWSE ARCHIVE // 查阅归档 ↳"
    },
    {
        "url": "https://www.typewolf.com",
        "badge": "FONT BIBLE",
        "badgeClass": "is-codepen",
        "rank": "№ 10 · TYPO CURATOR",
        "title": "Typewolf // 全球西文字体搭配圣经",
        "domain": "typewolf.com ↗",
        "categoryId": "typo",
        "desc": "全网最权威的字体搭配与版式趋势分析站。深入拆解现代衬线、无衬线几何字体的黄金组合。",
        "techTags": ["TYPOGRAPHY", "FONT PAIRING", "DESIGN SYSTEM", "SERIF"],
        "footLabel": "TYPO GUIDE",
        "linkText": "READ GUIDE // 研读指南 ↳"
    },
    {
        "url": "https://hoverstat.es",
        "badge": "ALTERNATIVE WEB",
        "badgeClass": "is-webby",
        "rank": "№ 11 · EXPERIMENTAL",
        "title": "Hover States // 先锋与另类交互站",
        "domain": "hoverstat.es ↗",
        "categoryId": "typo",
        "desc": "专注收集不按常理出牌的狂野排版、反主流交互与先锋数字艺术实验，打破设计思维定式。",
        "techTags": ["BRUTALISM", "WILD UX", "EXPERIMENT", "AVANT-GARDE"],
        "footLabel": "ALTERNATIVE HUB",
        "linkText": "DISCOVER // 发现异象 ↳"
    },
    {
        "url": "https://brutalistwebsites.com",
        "badge": "BRUTALISM PURE",
        "badgeClass": "is-codepen",
        "rank": "№ 12 · RAW HTML",
        "title": "Brutalist Websites // 粗野主义网页年鉴",
        "domain": "brutalistwebsites.com ↗",
        "categoryId": "typo",
        "desc": "抛弃现代框架的繁冗打磨，拥抱原生 HTML 线框、单色高对比度与极限反叛态度的先锋阵地。",
        "techTags": ["RAW WEB", "HIGH CONTRAST", "RETRO ARCH", "MINIMAL"],
        "footLabel": "RAW ARCHIVE",
        "linkText": "VIEW RAW // 审视粗野 ↳"
    },

    # 3. 奇趣交互 (Kinetic UX)
    {
        "url": "https://linear.app",
        "badge": "CRAFT CELEBRITY",
        "badgeClass": "is-webby",
        "rank": "№ 13 · KINETIC CRAFT",
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
        "rank": "№ 14 · SHADER & MATH",
        "title": "Wodniack Creative Lab",
        "domain": "codepen.io/wodniack ↗",
        "categoryId": "kinetic",
        "desc": "Wormhole 虫洞穿梭、SVG 几何极速透视与 Canvas 极坐标光速星流特效的官方开源实验场。",
        "techTags": ["HYPERSPACE WARP", "SVG MESH", "POLAR SHADER", "OPEN SOURCE"],
        "footLabel": "CREATIVE SOURCE",
        "linkText": "EXPLORE PEN // 探查源码 ↳"
    },
    {
        "url": "https://rauno.me/craft",
        "badge": "INDIE ENGINEER",
        "badgeClass": "is-webby",
        "rank": "№ 15 · DESIGN ENGINEERING",
        "title": "Rauno Craft // 交互工程手记",
        "domain": "rauno.me/craft ↗",
        "categoryId": "kinetic",
        "desc": "Vercel 设计工程副总监的个人实验手札。解构磁吸光标、弹簧物理阻尼与流体界面计算模型。",
        "techTags": ["SPRING PHYSICS", "MAGNETIC CURSOR", "MICRO-CRAFT", "INTERACTION"],
        "footLabel": "ENGINEERING NOTES",
        "linkText": "READ CRAFT // 研读手札 ↳"
    },
    {
        "url": "https://press.stripe.com",
        "badge": "DIGITAL PAPER",
        "badgeClass": "is-codepen",
        "rank": "№ 16 · TACTILE WEB",
        "title": "Stripe Press // 纸质触感在屏幕上的重生",
        "domain": "press.stripe.com ↗",
        "categoryId": "kinetic",
        "desc": "用高保真物理渲染呈现出实体精装书的质感。随着鼠标移动呈现逼真的光泽反光与纸张折叠微动效。",
        "techTags": ["TACTILE UX", "WebGL PAPER", "METICULOUS DETAIL", "SHADOW FX"],
        "footLabel": "TACTILE DESIGN",
        "linkText": "TOUCH PAPER // 翻阅纸质 ↳"
    },
    {
        "url": "https://emilkowal.ski",
        "badge": "SPRING MASTER",
        "badgeClass": "is-webby",
        "rank": "№ 17 · MOTION LABORATORY",
        "title": "Emil Kowalski // 弹簧物理动效实验室",
        "domain": "emilkowal.ski ↗",
        "categoryId": "kinetic",
        "desc": "全面解构 iOS 级别手势拖拽、弹簧阻尼回弹与微动效心流体验的现代前端动效交互指南。",
        "techTags": ["MOTION DESIGN", "SPRING CURVE", "FLUID DRAG", "CRAFT"],
        "footLabel": "MOTION GUIDE",
        "linkText": "STUDY MOTION // 探求阻尼 ↳"
    },
    {
        "url": "https://www.apple.com/design/awards/",
        "badge": "DESIGN BENCHMARK",
        "badgeClass": "is-webby",
        "rank": "№ 18 · HUMAN INTERFACE",
        "title": "Apple Design Awards Showcase",
        "domain": "apple.com ↗",
        "categoryId": "kinetic",
        "desc": "每年一度全球软件设计奥斯卡。严苛剖析包容性、趣味交互与前沿人机工程学创新的巅峰殿堂。",
        "techTags": ["HUMAN INTERFACE", "APPLE DESIGN", "DELIGHT", "INCLUSION"],
        "footLabel": "AWARDS VAULT",
        "linkText": "INSPECT WINNERS // 研读标杆 ↳"
    },

    # 4. 灵感矿脉 (Studio Vault)
    {
        "url": "https://vercel.com/design",
        "badge": "GEIST DESIGN",
        "badgeClass": "is-webby",
        "rank": "№ 19 · INDUSTRIAL SYSTEM",
        "title": "Vercel Geist // 黑白工业设计系统",
        "domain": "vercel.com/design ↗",
        "categoryId": "studio",
        "desc": "定义了当今全球极客审美基调的现代工业级设计规范。黑白灰严苛层次、高精度微动效与排版力学。",
        "techTags": ["GEIST SYSTEM", "INDUSTRIAL DESIGN", "DEVELOPER UX", "COMPONENTS"],
        "footLabel": "DESIGN SYSTEM",
        "linkText": "READ GEIST // 拆解规范 ↳"
    },
    {
        "url": "https://www.cosmos.so",
        "badge": "ALGO-FREE",
        "badgeClass": "is-codepen",
        "rank": "№ 20 · PURE AESTHETICS",
        "title": "Cosmos // 无算法纯净视觉策展",
        "domain": "cosmos.so ↗",
        "categoryId": "studio",
        "desc": "被称为数字时代的极简 Pinterest。拒绝社交成瘾算法与广告垃圾，只保留纯粹视觉审美与策展灵魂。",
        "techTags": ["CURATION", "VISUAL MOODBOARD", "ALGO FREE", "INSPIRATION"],
        "footLabel": "MOODBOARD HUB",
        "linkText": "EXPLORE COSMOS // 漫步星云 ↳"
    },
    {
        "url": "https://godly.website",
        "badge": "DAILY GOLD",
        "badgeClass": "is-webby",
        "rank": "№ 21 · TOP SHOWCASE",
        "title": "Godly // 全球顶级设计每日展台",
        "domain": "godly.website ↗",
        "categoryId": "studio",
        "desc": "每日严选全球最令人惊叹的现代 Web 界面与动效神作，附带完整录屏与交互细节标签索引。",
        "techTags": ["DAILY CURATED", "SHOWCASE", "BEST OF WEB", "TRENDS"],
        "footLabel": "DAILY INSPIRATION",
        "linkText": "BROWSE GODLY // 阅览神迹 ↳"
    },
    {
        "url": "https://www.awwwards.com",
        "badge": "INDUSTRY JURY",
        "badgeClass": "is-webby",
        "rank": "№ 22 · SITE OF THE DAY",
        "title": "Awwwards // 全球创意设计评审标杆",
        "domain": "awwwards.com ↗",
        "categoryId": "studio",
        "desc": "数字设计领域的最高荣誉评审殿堂。按设计、代码、可用性与内容四维量化打分，数字工匠的竞技场。",
        "techTags": ["SOTD", "JURY RATED", "GLOBAL HONORS", "DIGITAL CRAFT"],
        "footLabel": "GLOBAL JURY",
        "linkText": "EXPLORE AWWWARDS // 查阅榜单 ↳"
    },
    {
        "url": "https://thefwa.com",
        "badge": "FWA LEGACY",
        "badgeClass": "is-webby",
        "rank": "№ 23 · FUTURE ARCHIVE",
        "title": "FWA // 先锋未来网页奖",
        "domain": "thefwa.com ↗",
        "categoryId": "studio",
        "desc": "始于 2000 年的数字前沿见证者。专注发现突破技术天花板、超越时代维度的沉浸式未来体验。",
        "techTags": ["FOTD", "AVANT-GARDE", "IMMERSIVE WEB", "INNOVATION"],
        "footLabel": "FUTURE AWARDS",
        "linkText": "VISIT FWA // 见证前沿 ↳"
    },
    {
        "url": "https://designdetails.fm",
        "badge": "DESIGN DECONSTRUCT",
        "badgeClass": "is-codepen",
        "rank": "№ 24 · METICULOUS POD",
        "title": "Design Details // 产品细节解构手记",
        "domain": "designdetails.fm ↗",
        "categoryId": "studio",
        "desc": "深入剖析互联网头部产品中最微小却至关重要的构件、像素间距与阴影扩散半径的设计解构手札。",
        "techTags": ["PRODUCT DESIGN", "MICRO-DETAILS", "DECONSTRUCT", "PODCAST"],
        "footLabel": "DETAILS VAULT",
        "linkText": "READ DETAILS // 研读微构 ↳"
    }
]


def generate_fallback_radar(hn_news, v2_news):
    """
    智能融合真实抓取资讯与工坊标杆基准库
    严格保持 15 条完整丰富阵容，横跨四大极客暗号分类
    """
    now_utc = datetime.now(timezone.utc).strftime("%H:%M UTC")
    live_items = []

    # 1. 转换 HackerNews
    for hn in hn_news[:6]:
        cat = hn.get('categoryId', 'global')
        cat_label = {
            'ai': '智子推演 // AI & PARADOX',
            'global': '寰宇前沿 // GLOBAL TECH',
            'domestic': '极客生态 // DOMESTIC DEV',
            'observatory': '视界暗线 // OBSERVATORY'
        }.get(cat, '寰宇前沿 // GLOBAL TECH')

        live_items.append({
            "categoryId": cat,
            "category": cat_label,
            "time": f"TODAY // {now_utc}",
            "title": hn['title'],
            "summary": f"HackerNews 社区热榜头条（得分 {hn['score']}）。该议题引发全球架构师与开发者关于现代计算体系、开源生态与工程效率的深度论战。",
            "specTag": f"[ HN HOT #{hn['score']}★ ]",
            "linkText": "READ INTEL // 展开内参 ↳",
            "url": hn['url']
        })

    # 2. 转换 V2EX
    for v2 in v2_news[:6]:
        cat = v2.get('categoryId', 'domestic')
        cat_label = {
            'ai': '智子推演 // AI & PARADOX',
            'global': '寰宇前沿 // GLOBAL TECH',
            'domestic': '极客生态 // DOMESTIC DEV',
            'observatory': '视界暗线 // OBSERVATORY'
        }.get(cat, '极客生态 // DOMESTIC DEV')

        live_items.append({
            "categoryId": cat,
            "category": cat_label,
            "time": f"TODAY // {now_utc}",
            "title": v2['title'],
            "summary": f"来自国内极客社区的热议思潮（讨论度 {v2['replies']} 节点：{v2['node']}）。折射出当下国内程序员在独立开发、日常生产力重构与工程落地中的真实呼声。",
            "specTag": f"[ V2EX FREQ: {v2['replies']} REPLIES ]",
            "linkText": "READ INTEL // 展开内参 ↳",
            "url": v2['url']
        })

    # 3. 混合基准库补充（确保 4 大分类平衡，总量达到 15 条）
    combined = []
    seen_urls = set()

    for it in live_items + BENCHMARK_RADAR_SEED:
        url = it.get('url') or it.get('title')
        if url and url not in seen_urls:
            seen_urls.add(url)
            combined.append(it)
            if len(combined) >= 15:
                break

    return combined[:15]


def balance_pool(items, target_count, category_keys):
    """确保各个核心分类均衡覆盖，总数精准锁定 target_count"""
    by_cat = {c: [] for c in category_keys}
    other = []
    seen = set()
    for it in items:
        url = it.get('url') or it.get('name') or it.get('title')
        if not url or url in seen:
            continue
        seen.add(url)
        cat = it.get('categoryId')
        if cat in by_cat:
            by_cat[cat].append(it)
        else:
            other.append(it)

    selected = []
    # 轮流从每个分类抽取，保证所有分类均有代表性精品展示
    added = True
    while len(selected) < target_count and added:
        added = False
        for c in category_keys:
            if by_cat[c] and len(selected) < target_count:
                selected.append(by_cat[c].pop(0))
                added = True

    for c in category_keys:
        while by_cat[c] and len(selected) < target_count:
            selected.append(by_cat[c].pop(0))

    for o in other:
        if len(selected) < target_count:
            selected.append(o)

    # 剩余所有项目进入 overflow
    overflow = []
    for c in category_keys:
        overflow.extend(by_cat[c])
    overflow.extend(other[len(selected):])
    return selected, overflow


def update_spatial_chambers_lifecycle(new_radar, new_tools, new_gems):
    """
    全自动生命周期与严格容量控制体系：
    1. 今日雷达：FIFO 保持 15 条 (四大极客暗号均衡覆盖)
    2. 开源装备库：当期精选 30 款（云盘置顶），超量沉淀至 archive 历史卷宗
    3. 神仙网站：当期精选 20 款，超量沉淀至 archive 历史卷宗
    """
    if not os.path.exists(JSON_PATH):
        print(f"[ERROR] 找不到时空舱配置文件: {JSON_PATH}")
        sys.exit(1)

    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 写入最新中控分类矩阵
    data['radarChamber']['categories'] = RADAR_CATEGORIES
    data['toolboxChamber']['categories'] = TOOLBOX_CATEGORIES
    data['gemsChamber']['categories'] = GEMS_CATEGORIES

    if 'archive' not in data['toolboxChamber']:
        data['toolboxChamber']['archive'] = []
    if 'archive' not in data['gemsChamber']:
        data['gemsChamber']['archive'] = []

    now_month = datetime.now().strftime("%Y.%m")

    # ----------------------------------------------------
    # 1. 今日热点雷达：均衡容纳 15 条，四大分类皆有深层情报
    # ----------------------------------------------------
    existing_radar = data['radarChamber'].get('items', [])
    raw_radar_pool = new_radar + existing_radar + BENCHMARK_RADAR_SEED
    active_radar, _ = balance_pool(raw_radar_pool, 15, ['ai', 'global', 'domestic', 'observatory'])

    data['radarChamber']['items'] = active_radar
    print(f"[LIFECYCLE] 今日雷达已同步：当期驻留 {len(data['radarChamber']['items'])}/15 条最前沿情报。")

    # ----------------------------------------------------
    # 2. 开源影音武器库：当期 30 款 (四大阵营平衡) + 历史归档卷宗
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

    raw_tool_pool = new_tools + existing_tools + BENCHMARK_TOOLBOX_SEED
    active_tools, overflow_tools = balance_pool(raw_tool_pool, 30, ['audio', 'video', 'local', 'geek'])

    archive_seen = set(t.get('url') for t in archive_tools)
    for ot in overflow_tools:
        url = ot.get('url') or ot.get('name')
        if url and url not in archive_seen:
            archive_seen.add(url)
            ot_copy = dict(ot)
            ot_copy['archivedAt'] = f"ARCHIVED · {now_month}"
            archive_tools.append(ot_copy)

    data['toolboxChamber']['tools'] = [alist_permanent_card] + active_tools
    data['toolboxChamber']['archive'] = archive_tools
    print(f"[LIFECYCLE] 开源装备库已同步：当期精选 {len(active_tools)} 款 (AList 置顶共 {len(data['toolboxChamber']['tools'])} 项)，历史卷宗沉淀 {len(archive_tools)} 款。")

    # ----------------------------------------------------
    # 3. 神仙网站灵感矿藏：当期 20 款 (四大美学平衡) + 历史归档
    # ----------------------------------------------------
    existing_gems = data['gemsChamber'].get('gems', [])
    archive_gems = data['gemsChamber'].get('archive', [])

    raw_gem_pool = new_gems + existing_gems + BENCHMARK_GEMS_SEED
    active_gems, overflow_gems = balance_pool(raw_gem_pool, 20, ['shader', 'typo', 'kinetic', 'studio'])

    gem_archive_seen = set(g.get('url') for g in archive_gems)
    for og in overflow_gems:
        url = og.get('url') or og.get('title')
        if url and url not in gem_archive_seen:
            gem_archive_seen.add(url)
            og_copy = dict(og)
            og_copy['archivedAt'] = f"ARCHIVED · {now_month}"
            archive_gems.append(og_copy)

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

    hn_news = fetch_hacker_news(limit=12)
    v2_news = fetch_v2ex_hot(limit=10)
    gh_tools = fetch_github_tools()
    live_gems = fetch_live_gems()

    # 极客降级与智能合成引擎 (无需依赖外部 AI API 即可全天候满血运转)
    radar_items = generate_fallback_radar(hn_news, v2_news)

    update_spatial_chambers_lifecycle(radar_items, gh_tools, live_gems)
    print("==================================================")
    print("  [OK] 数据全景生命周期处理完成！  ")
    print("==================================================")


if __name__ == '__main__':
    main()
