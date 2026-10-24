#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BC Studio - 每日热点雷达 & 开源影音武器库自动化聚合系统
- 抓取信源：GitHub Trending/Search (影音播放器/音视频源/开源神兵)、HackerNews Top 科技热榜、V2EX 开发者热议
- AI 深度推理：调用 LLM (DeepSeek / Gemini / OpenAI 格式) 生成符合 BC 赛博极客风格的情报摘要
- 智能降级保护：若无 API Key 或网络波动，自动激活内置模板引擎格式化真实数据，确保 100% 构建成功
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

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 BC-Intel-Bot/1.0'


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
        print(f"[WARN] HTTP GET failed for {url}: {e}")
        return None


def fetch_hacker_news(limit=5):
    """获取 HackerNews Top 科技头条"""
    print("[1/3] 正在拉取全球前沿科技情报 (HackerNews)...")
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


def fetch_v2ex_hot(limit=5):
    """获取国内开发者热议话题 (V2EX Hot)"""
    print("[2/3] 正在拉取国内极客热议话题 (V2EX)...")
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
    """搜索 GitHub 上热门的高端影音播放器、音频源、视频源与极客神兵"""
    print("[3/3] 正在扫描 GitHub 顶级开源影音神器 (Music/Video Players & Sources)...")
    
    # 标杆高分优质开源项目种子池（保证即使网络受限也有极高水准的基础库）
    benchmark_candidates = [
        {
            "name": "MusicFree // 插件化多音源桌面音乐播放器",
            "desc": "基于插件化架构的跨平台音乐神器。本身不集成任何音源，用户可通过自定义 JS 脚本插件自由接入全网无损音频与歌单，纯净无广告。",
            "badge": "MULTI-SOURCE · 16.8k★",
            "url": "https://github.com/maotoumao/MusicFree",
            "launchText": "探查源码 ➔"
        },
        {
            "name": "IINA // macOS 现代极简视频播放器天花板",
            "desc": "基于 mpv 内核深度定制的现代化开源播放器。完美契合 macOS 设计哲学，支持画中画、外挂字幕实时搜索、HDR 与任意流媒体协议解码。",
            "badge": "MACOS ELITE · 38.5k★",
            "url": "https://github.com/iina/iina",
            "launchText": "探查源码 ➔"
        },
        {
            "name": "Spotube // 纯净跨平台流媒体音乐客户端",
            "desc": "利用 Spotify API 抓取元数据并由 YouTube / Piped 提供无损无广告音频流，完全开源轻量，内存占用不足官方十分之一。",
            "badge": "CROSS-PLATFORM · 33.2k★",
            "url": "https://github.com/KRTirtho/spotube",
            "launchText": "探查源码 ➔"
        },
        {
            "name": "LosslessCut // 无损音视频极速裁剪拼接神兵",
            "desc": "基于 FFmpeg 打造的零编解码极速剪刀。无需二次渲染，光速粗剪 4K 巨型视频无画质损耗，极客工作流必备生产力。",
            "badge": "LOSSLESS · 22.4k★",
            "url": "https://github.com/mifi/lossless-cut",
            "launchText": "探查源码 ➔"
        },
        {
            "name": "MediaGo // 跨平台网页流媒体嗅探与下载器",
            "desc": "支持 m3u8 / MPD 自动解密与多线程合并抓取，内置极简浏览器自动嗅探网页视频源，快速保存公开高清素材。",
            "badge": "SNIFFER · 6.8k★",
            "url": "https://github.com/bistutu/MediaGo",
            "launchText": "探查源码 ➔"
        }
    ]

    # 尝试从 GitHub API 实时探测最新高赞播放器
    try:
        gh_headers = {'User-Agent': USER_AGENT}
        gh_token = os.environ.get('GITHUB_TOKEN')
        if gh_token:
            gh_headers['Authorization'] = f'Bearer {gh_token}'
        
        search_url = 'https://api.github.com/search/repositories?q=topic:music-player+sort:stars&per_page=5'
        data = http_get_json(search_url, timeout=6, headers=gh_headers)
        if data and 'items' in data:
            live_repos = []
            for item in data['items'][:3]:
                stars_k = f"{round(item.get('stargazers_count', 0) / 1000, 1)}k★"
                live_repos.append({
                    "name": f"{item.get('name')} // {item.get('description', '')[:35]}…",
                    "desc": item.get('description', '优质 GitHub 开源项目'),
                    "badge": f"GITHUB · {stars_k}",
                    "url": item.get('html_url'),
                    "launchText": "探查源码 ➔"
                })
            if live_repos:
                # 融合在线最新探查与精品推荐
                return live_repos + benchmark_candidates[:2]
    except Exception as e:
        print(f"[INFO] GitHub live search note: {e}, falling back to curated weapons pool.")

    return benchmark_candidates


def call_llm_intelligence(hn_news, v2_news, gh_tools):
    """调用 AI 大模型（DeepSeek / Gemini / OpenAI 兼容接口）生成深度极客情报"""
    api_key = os.environ.get('AI_API_KEY') or os.environ.get('DEEPSEEK_API_KEY') or os.environ.get('GEMINI_API_KEY') or os.environ.get('OPENAI_API_KEY')
    base_url = os.environ.get('AI_BASE_URL', 'https://api.deepseek.com/v1').rstrip('/')
    model_name = os.environ.get('AI_MODEL', 'deepseek-chat')

    if not api_key:
        print("[INFO] 未检测到 AI_API_KEY 环境变量，自动启用内置极客智能模板引擎。")
        return None

    print(f"[AI] 正在接入 AI 大模型 ({model_name} @ {base_url}) 生成每日专属情报...")

    prompt = f"""
你现在是 BC Studio (独立游戏研发工坊 & 极客灵感数字枢纽) 的首席技术情报官。
请根据以下今日抓取的原始互联网动态与开源项目，提炼出【今日热点雷达 (radarChamber.items)】和【开源影音装备 (toolboxChamber.tools)】。

【原始国内国际科技热点】：
HackerNews: {json.dumps(hn_news[:4], ensure_ascii=False)}
V2EX: {json.dumps(v2_news[:4], ensure_ascii=False)}

【开源影音与工具候选项】：
GitHub: {json.dumps(gh_tools[:4], ensure_ascii=False)}

【格式与调性要求】：
1. 风格：本格推理、硬核极客、瑞士网格极简主义。语言精炼有力，绝无营销废话，充满技术推演感。
2. 必须输出合法且仅输出 JSON 格式（不要包含任何 ```json 之外的闲话）：
{{
  "radar_items": [
    {{
      "category": "分类标签 // 二级属性 (如 AI REVOLUTION // 大模型推演, GLOBAL TECH // 海外前沿, DOMESTIC INTEL // 国内极客)",
      "time": "TODAY // HH:MM UTC (当前时间戳)",
      "title": "极具吸引力且有深度的标题",
      "summary": "2-3句话剖析该事件对开发者、创作者或科技行业的深刻启示与技术本质。",
      "specTag": "[ INTEL: 来源或关键指标，如 HACKERNEWS #1 或 FREQ: 1420 MHz ]",
      "linkText": "READ INTEL // 展开内参 ↳",
      "url": "对应的原文链接"
    }}
  ],
  "toolbox_items": [
    {{
      "name": "项目名 // 中文一句话定位 (如 MusicFree // 插件化多音源桌面音乐播放器)",
      "desc": "精准亮点解读：为什么这款开源工具/播放器是顶流神器，其核心优势与协议支持。",
      "badge": "徽标 (如 MULTI-SOURCE · 16.8k★)",
      "url": "GitHub 或项目官网链接",
      "launchText": "探查源码 ➔"
    }}
  ]
}}
请挑选 3 条最硬核的 radar_items（必须兼顾国内、海外、AI/科技）以及 3 条最惊艳的 toolbox_items（专注于音乐播放器、视频播放器、音视频源、极客工具）。
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
            # 剥离 markdown ```json 包裹
            if content.startswith('```'):
                lines = content.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].startswith('```'):
                    lines = lines[:-1]
                content = '\n'.join(lines).strip()
            parsed = json.loads(content)
            print("[SUCCESS] AI 成功完成今日情报分析与极客语言重塑！")
            return parsed
    except Exception as e:
        print(f"[WARN] AI 调用异常: {e}，将启用高保真内置模板引擎。")
        return None


def generate_fallback_data(hn_news, v2_news, gh_tools):
    """智能降级引擎：当无 AI API 时，自动将抓取的数据格式化为 BC 赛博风格"""
    now_utc = datetime.now(timezone.utc).strftime("%H:%M UTC")
    
    radar_items = []
    
    # 1. 国际科技头条 (HackerNews)
    if hn_news:
        top_hn = hn_news[0]
        radar_items.append({
            "category": "GLOBAL TECH // 海外前沿聚焦",
            "time": f"TODAY // {now_utc}",
            "title": top_hn['title'],
            "summary": f"HackerNews 社区热榜头条（得分 {top_hn['score']}）。该项目引发全网架构师与开发者关于现代计算体系、开源生态与工程效率的深度论战。",
            "specTag": f"[ SOURCE: HACKERNEWS #{top_hn['score']}★ ]",
            "linkText": "READ INTEL // 展开内参 ↳",
            "url": top_hn['url']
        })
    
    # 2. 国内极客洞察 (V2EX)
    if v2_news:
        top_v2 = v2_news[0]
        radar_items.append({
            "category": "DEV ECOSYSTEM // 国内极客观察",
            "time": f"TODAY // {now_utc}",
            "title": top_v2['title'],
            "summary": f"来自国内开发者社区的热点思潮（讨论度 {top_v2['replies']} 节点：{top_v2['node']}）。折射出当下国内程序员在独立开发、日常生产力重构与工程落地中的真实呼声。",
            "specTag": f"[ RADAR FREQ: V2EX {top_v2['replies']} REPLIES ]",
            "linkText": "READ INTEL // 展开内参 ↳",
            "url": top_v2['url']
        })

    # 3. AI 叙事与逻辑演进经典专题
    radar_items.append({
        "category": "AI & NARRATIVE // 逻辑与密室推演",
        "time": f"TODAY // {now_utc}",
        "title": "多模态推演能否构建真正的“物理闭环密室”？",
        "summary": "实测最新前沿大模型在多重伪解答架构中的表现：虽然能瞬间生成海量障眼法，但在微观物理材质力学与时间线交叉口供的精确剪裁上，人类本格心机依然是不可替代的胜负手。",
        "specTag": "[ INTEL: DUAL-CHAMBER LOGIC ]",
        "linkText": "READ INTEL // 展开内参 ↳",
        "url": "https://bckj.site"
    })

    # 开源装备
    toolbox_items = gh_tools[:4] if gh_tools else []

    return {
        "radar_items": radar_items,
        "toolbox_items": toolbox_items
    }


def update_spatial_chambers_json(radar_items, toolbox_items):
    """更新 spatial-chambers.json 并确保 AList 个人云盘永久置顶"""
    if not os.path.exists(JSON_PATH):
        print(f"[ERROR] 找不到目标文件: {JSON_PATH}")
        sys.exit(1)

    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. 更新今日热点雷达
    if radar_items:
        data['radarChamber']['items'] = radar_items
        print(f"[UPDATE] 今日雷达已同步 {len(radar_items)} 条科技内参。")

    # 2. 更新极客实用工具箱 (确保个人高速云盘 AList 永远置顶第 1 位)
    alist_permanent_card = {
        "name": "BC Cloud Drive // 个人私有高速云盘",
        "desc": "基于 AList 与百度网盘聚合的高速资源仓 · 包含插画课程、单机游戏与设计资产，直链极速下载。",
        "badge": "ONLINE · CLOUD",
        "url": "http://111.229.205.54:5244",
        "isPrimary": True,
        "launchText": "打开云盘 ➔"
    }

    final_tools = [alist_permanent_card]
    for item in toolbox_items:
        # 避免与 AList 云盘重复
        if '111.229.205.54' not in (item.get('url') or ''):
            final_tools.append(item)

    data['toolboxChamber']['tools'] = final_tools[:5]
    print(f"[UPDATE] 极客装备库已装载 {len(data['toolboxChamber']['tools'])} 款开源神兵 (个人云盘永久置顶)。")

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] 成功写入时空舱配置文件: {JSON_PATH}")


def main():
    print("==================================================")
    print("  BC Studio // 每日科技雷达 & 开源影音武器库自动化系统  ")
    print("==================================================")

    # 1. 抓取多源实时动态
    hn_news = fetch_hacker_news(limit=5)
    v2_news = fetch_v2ex_hot(limit=5)
    gh_tools = fetch_github_tools()

    # 2. AI 赋能生成
    ai_result = call_llm_intelligence(hn_news, v2_news, gh_tools)

    if ai_result and 'radar_items' in ai_result and 'toolbox_items' in ai_result:
        radar_items = ai_result['radar_items']
        toolbox_items = ai_result['toolbox_items']
    else:
        fallback = generate_fallback_data(hn_news, v2_news, gh_tools)
        radar_items = fallback['radar_items']
        toolbox_items = fallback['toolbox_items']

    # 3. 写入数据
    update_spatial_chambers_json(radar_items, toolbox_items)
    print("==================================================")
    print("  [OK] 今日时空舱数据同步完毕，准备构建发布！  ")
    print("==================================================")


if __name__ == '__main__':
    main()
