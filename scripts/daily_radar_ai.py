#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BC Studio - 时空舱全自动情报、开源装备与灵感中枢 (Daily Autonomous Hub)
- 全境深度汉化引擎 (Full Chinese Localization Engine)：
  * 自动将 HackerNews 英文头条与全球前沿科技转化为通俗、犀利的中文深度解析
  * 自动将 GitHub 英文开源装备与工具说明翻译为接地气、极客范儿的中文功能解读
  * 平台标识、美学标签、技术规格全境中文汉化，彻底消除英语门槛
- 智能轮转与容量控制机制：
  * 今日雷达 (Chamber 03)：严格保持 15 条 FIFO 滚动缓冲（超量自动淘汰，保证每日最鲜活）
  * 开源装备 (Chamber 05)：严格保持 30 款当期精选（AList 私有云盘置顶），超量自动沉淀至【历史卷宗】永久可查
  * 神仙网站 (Chamber 04)：严格保持 20 款当期精选，超量自动沉淀至【历史卷宗】永久可查
- 目标数据文件：src/data/spatial-chambers.json
"""

import os
import sys
import json
import re
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


# ==========================================
# 全境汉化字典与智能转译引擎 (Localization Engine)
# ==========================================

# 1. 常见平台与系统汉化映射
PLATFORM_TRANSLATIONS = {
    'ALL PLATFORMS': '全系统通用',
    'CROSS-PLATFORM': '跨平台全端',
    'WIN · MAC · LINUX': 'Win · Mac · Linux',
    'WIN · MAC · ANDROID': 'Win · Mac · 安卓',
    'WIN · MAC · WEB': 'Win · Mac · 网页端',
    'CHROME · DESKTOP': 'Chrome插件 · 桌面端',
    'MACOS': 'macOS 专属',
    'WINDOWS': 'Windows 专属',
    'ALL TERMINALS': '命令行终端通用',
    'BROWSER / OFFLINE': '浏览器纯本地离线',
    'DOCKER · LINUX · WIN': 'Docker · 私有部署',
    'SERVER · CLIENT': '服务端 · 全端投屏',
    'PYTHON CLI': 'Python 终端神器'
}

# 2. 常见热门开源装备中英对照字典
KNOWN_TOOL_CHINESE = {
    'iina': ('IINA // 现代极简播放器天花板', 'macOS 现代极简视频播放器天花板，基于 mpv 内核深度定制，画中画与流媒体解码神器。', 'macOS 专属', '极影魔方'),
    'meetily': ('Meetily // 离线端侧AI会议助手', '隐私优先的本地端侧 AI 智能语音会议纪要与离线实时语音转录神器，100% 本地运算零云端泄露。', '跨平台全端', '离线神兵'),
    'rea': ('Rea // AI 智能二进制逆向平台', '结合 AI Agent 架构的现代化二进制程序与移动端 App 行为逆向解构平台。', '跨平台全端', '逆向兵刃'),
    'spotube': ('Spotube // 纯净流媒体音乐客户端', '纯净轻量开源流媒体音乐客户端，利用开放 API 获取无损音频流，桌面与移动双端通吃，内存占用极低。', '跨平台全端', '天籁之源'),
    'video.js': ('Video.js // 网页流媒体播放器内核', '全球知名开源 HTML5 与流媒体视频播放器内核框架，支持全格式视频播放与插件化扩展定制。', '跨平台全端', '极影魔方'),
    'react-boilerplate': ('React Boilerplate // 离线敏捷架构底座', '高可扩展、离线优先的现代化极客敏捷开发架构底座与工程范式。', '跨平台全端', '离线神兵'),
    'musicfree': ('MusicFree // 插件化多音源音乐播放器', '基于插件化架构的跨平台音乐神器。本身不集成任何音源，用户可通过自定义 JS 脚本插件自由接入全网无损音频与歌单，纯净无广告。', 'Win · Mac · 安卓', '天籁之源'),
    'lx-music-desktop': ('洛雪音乐 // 经典多源无损桌面端', '基于 Electron 与 Vue 打造的开源音频流客户端。支持各大平台歌曲搜索、歌词逐字同步与自定义音源解析脚本。', 'Win · Mac · Linux', '天籁之源'),
    'yesplaymusic': ('YesPlayMusic // 高颜值网易云客户端', '极具现代苹果设计美学的第三方音乐客户端。支持 UnblockNeteaseMusic 自动音源替换、Touch Bar 快捷控制与暗黑模式。', 'Win · Mac · 网页端', '天籁之源'),
    'listen1': ('Listen1 // 全网音乐聚合搜索播放器', '打破曲库壁垒，聚合各大平台曲库。一个搜索框搞定全网找歌与歌单导入，本地安全离线运行。', 'Chrome插件 · 桌面端', '天籁之源'),
    'moosync': ('Moosync // 本地流媒体双轨播放器', '专为极客音乐爱好者打造。同时管理本地高解析 FLAC 音乐库与 Spotify/YouTube 远程播放列表，支持自定义均衡器与扩展。', '跨平台全端', '天籁之源'),
    'navidrome': ('Navidrome // 自建私有云端音乐服务器', '现代高性能自建音乐服务器，基于 Go 语言开发，纯本地扫描无损音乐文件夹，支持全平台 Subsonic 协议客户端投屏与串流。', 'Docker · 私有部署', '天籁之源'),
    'blackhole': ('BlackHole // macOS 零延迟虚拟声卡', '解决 macOS 系统无法直接录制系统声音或各 App 间音频跳线的终极内核级开源虚拟声卡，混音与播客制作必备。', 'macOS 专属', '天籁之源'),
    'losslesscut': ('LosslessCut // 无损音视频极速剪刀', '基于 FFmpeg 打造的零编解码极速剪刀。无需二次渲染，光速粗剪 4K 巨型视频无画质损耗，极客工作流必备生产力。', '跨平台全端', '极影魔方'),
    'mediago': ('MediaGo // 网页流媒体嗅探下载器', '支持 m3u8 / MPD 自动解密与多线程合并抓取，内置极简浏览器自动嗅探网页视频源，快速保存公开高清素材。', 'Win · Mac · Linux', '极影魔方'),
    'mpv.net': ('mpv.net // 极客硬核视频渲染器', '基于 libmpv 架构的高性能视频播放器，具备完备的 GPU 着色器扩展与高画质升采样算法支持。', 'Windows 专属', '极影魔方'),
    'bbdown': ('BBDown // 命令行流媒体解构下载器', '多线程分块下载、杜比视界与真彩画质解析、多音轨分离抓取的硬核轻量级媒体终端工具。', '命令行终端通用', '极影魔方'),
    'bililiverecorder': ('录播姬 // 全自动无人值守录播器', '专为直播流保存设计的全自动守护进程。开播自动极速录制，智能跳过重连并无缝混流为标准 MP4，支持多主播并发。', '跨平台全端', '极影魔方'),
    'jellyfin': ('Jellyfin // 100% 自由开源媒体服务器', '无商业化绑架的纯净媒体中心。自动刮削电影与剧集海报墙、支持硬件转码与全家跨端协同流媒体点播。', '服务端 · 全端投屏', '极影魔方'),
    'handbrake': ('HandBrake // 通用硬件加速视频转码器', '近二十年开源常青树。支持 NVENC / QuickSync 硬件编码，精准裁切黑边、优化色彩空间与批量压缩 4K 大文件。', 'Win · Mac · Linux', '极影魔方'),
    'devtoys': ('DevToys // 瑞士军刀开发者离线工具箱', '纯本地离线运行的开发利器，涵盖 JSON/YAML 校验、JWT 解码、正则表达式演算、Hash 验算与色彩转换。', 'Win · Mac · Linux', '离线神兵'),
    'localsend': ('LocalSend // 局域网跨端无损极速传输', '无需连接互联网、纯局域网点对点互传文件神器。完全开源，秒杀 AirDrop 并通吃 iOS、Android、Windows、Mac。', '全系统通用', '离线神兵'),
    'flameshot': ('Flameshot // 现代化硬核截图标注工具', '支持像素级拾色、模糊马赛克、序号标注、多显示器协同与命令行截图自动化，完全本地隐私无后台。', '跨平台全端', '离线神兵'),
    'cyberchef': ('CyberChef // 极客密码学与数据转换台', '被称为网络安全界的厨师机。纯本地浏览器运行的加密解密、编码转换、反混淆与特征分析超级工作台。', '浏览器纯本地离线', '离线神兵'),
    'espanso': ('Espanso // Rust 驱动极速文本扩展器', '基于 Rust 开发的跨平台快捷键文本扩展神器。输入简短暗号自动展开为长邮件模板、代码片段或当前时间戳，完全离线。', '跨平台全端', '离线神兵'),
    'rustdesk': ('RustDesk // 开源自建中继远程桌面', '完全可替代 TeamViewer / AnyDesk 的自建远程协助利器。支持自建 Relay 中继服务器，端到端加密零商业限制。', '全系统通用', '离线神兵'),
    'sharex': ('ShareX // Windows 终极截图与录屏神兵', '拥有 15 年历史的 Windows 截屏与工作流自动化开源巨匠。支持 OCR 识别、颜色拾取与自定义目标自动上传。', 'Windows 专属', '离线神兵'),
    'bruno': ('Bruno // 本地离线优先 API 调试客户端', '告别 Postman 云端绑架与强制登录。采用纯文本 Bru 语言直接保存在 Git 仓库中，纯离线安全高速调试 API 请求。', '跨平台全端', '离线神兵'),
    'http toolkit': ('HTTP Toolkit // 现代化抓包嗅探重构台', '一键拦截、检查并重写 HTTP(S) 网络请求。精准调试 API 接口、解密 App 请求协议与流量分析。', 'Win · Mac · Linux', '逆向兵刃'),
    'caido': ('Caido // Rust 打造的现代 Web 渗透台', '专为安全研究员与协议分析师打造的现代网络审计工具。内存占用不足 Burp Suite 十分之一，UI 极具赛博现代感。', '跨平台全端', '逆向兵刃'),
    'scrcpy': ('Scrcpy // 极低延迟安卓终端投屏控制', '无需 Root、无需在手机安装任何 App。纯 ADB 管道实现 30-70ms 极低延迟 60FPS 安卓屏幕投射与键盘鼠标操控。', '跨平台全端', '逆向兵刃'),
    'ghidra': ('Ghidra // 软件逆向工程反编译架构', '由美国国家安全局开源的强大逆向工程套件。支持 x86/ARM/MIPS 全指令集反汇编与 C 语言高阶代码反编译还原。', '跨平台全端', '逆向兵刃'),
    'wireshark': ('Wireshark // 网络数据包深层协议分析器', '网络通信世界的终极听诊器。精准抓取以太网、TCP/IP、DNS 与 TLS 握手数据包，排查网络故障与协议逆向必备。', '全系统通用', '逆向兵刃'),
    'postcat': ('Postcat // 开源敏捷 API 全生命周期平台', '支持插件化扩展的高颜值 API 管理工具。纯本地数据存储、支持多协议调试与代码自动生成，完全开源免费。', '跨平台全端', '逆向兵刃'),
    'mitmproxy': ('Mitmproxy // 命令行 Python 拦截代理', '完全可编程的中间人代理工具。支持用 Python 脚本实时篡改请求头、解密流量并重放数据包，渗透测试利器。', 'Python 终端神器', '逆向兵刃'),
    'reqable': ('Reqable // API 调试抓包双合一利器', '基于 Flutter 开发的现代化跨平台抓包利器，将 Fiddler 抓包能力与 Postman 接口测试深度融合，速度飞快。', '跨平台全端', '逆向兵刃'),
    'pear': ('Pear // 音乐播放器极客扩展', '专为开源音乐播放器打造的多功能扩展插件套件，支持歌词与自建音源扩展。', '跨平台全端', '天籁之源')
}

# 3. 英文技术标题智能转译字典
HN_TITLE_TRANSLATIONS = {
    'lula wins brazilian election': '巴西大选尘埃落定与拉美数字科技生态新变局',
    'we should be more ambitious with the software we build': '我们应当对亲手构建的软件抱有更大雄心：反思现代技术的过度膨胀',
    'obs studio 33': 'OBS Studio 33 巨型版本发布：底层视频渲染流管道深度重构',
    'overgrown': 'Overgrown // 当绿植藤蔓攻占废弃标签页：数字园艺交互实验',
    'tailscale': 'Tailscale 零配置虚拟组网技术演进与全球极客内网穿透实践',
    'postgresql': 'PostgreSQL 新版本内核突破：极端并发下的事务吞吐调优',
    'sqlite': 'SQLite 架构精粹：单文件嵌入式数据库何以撑起千亿级应用底座',
    'linux kernel': 'Linux 核心模块架构升级：内存安全机制与驱动层演进实测',
    'rust': 'Rust 编译器最新优化：无开销抽象与跨架构编译提速实战'
}

# 4. 英文神仙网站标题映射字典
KNOWN_GEM_TITLES = {
    'antoine wodniack portfolio': 'Antoine Wodniack 瑞士极简作品集',
    'bruno simon 3d interactive world': 'Bruno Simon 3D 越野漫游世界',
    'wodniack creative lab': 'Wodniack 官方创意实验场',
    'apple design awards showcase': 'Apple Design Awards 苹果设计大奖展台',
    'lusion creative technical studio': 'Lusion 顶级先锋创意技术工坊'
}


def translate_platform(platform_str):
    """汉化平台标签"""
    if not platform_str:
        return '跨平台全端'
    p = platform_str.strip().upper()
    return PLATFORM_TRANSLATIONS.get(p, platform_str)


def is_mostly_english(text):
    """检测文本是否主要是英文"""
    if not text:
        return False
    cjk_chars = len(re.findall(r'[一-鿿]', text))
    if cjk_chars >= 3:
        return False
    eng_chars = len(re.findall(r'[a-zA-Z]', text))
    total_chars = len(re.findall(r'\S', text))
    if total_chars == 0:
        return False
    return (eng_chars / total_chars) > 0.4


def translate_github_tool_info(name, desc, default_cat):
    """将 GitHub 原始英文工具信息转译为流畅专业的中文"""
    name_clean = name.split('//')[0].strip()
    name_lower = name_clean.lower()

    # 查表精确汉化
    for key, val in KNOWN_TOOL_CHINESE.items():
        if key in name_lower:
            ch_name, ch_desc, ch_platform, _ = val
            return ch_name, ch_desc, ch_platform

    # 如果有已知映射，直接返回；否则进行智能润色
    if not is_mostly_english(desc):
        return f"{name_clean} // 极客开源神兵", desc, '跨平台全端'

    # 通用技术短语智能转译
    t_desc = desc
    replacements = [
        (r'The modern video player for macOS\.?', 'macOS 平台现代高颜值极简视频播放器，基于 mpv 内核深度定制。'),
        (r'Privacy first AI meeting note taker\.?.*', '隐私优先的本地端侧 AI 智能语音会议纪要与离线转录神兵，100% 本地运算零云端泄露。'),
        (r'Reverse engineer anything with agents.*', '结合 AI Agent 架构的现代化二进制程序与移动端 App 行为逆向解构平台。'),
        (r'Open source music streaming app!.*', '纯净开源流媒体音乐客户端，无损音频流与桌面/移动双端畅听，内存占用极低。'),
        (r'Video\.js v\d+ - open source media player.*', '全球知名开源 HTML5 与流媒体视频播放器内核框架，支持全格式视频播放与插件定制。'),
        (r'A highly scalable, offline-first foundation.*', '高可扩展、离线优先的现代化极客敏捷开发架构底座与工程范式。'),
        (r'cross-platform', '跨平台'),
        (r'open source', '开源'),
        (r'music player', '音乐播放器'),
        (r'video player', '视频播放器'),
        (r'privacy-first', '隐私优先'),
        (r'offline-first', '离线优先'),
        (r'fast and lightweight', '轻量高效'),
        (r'media downloader', '流媒体下载工具'),
        (r'packet sniffer', '网络抓包嗅探器'),
        (r'written in Rust', '基于高性能 Rust 构建')
    ]
    for pattern, repl in replacements:
        t_desc = re.sub(pattern, repl, t_desc, flags=re.IGNORECASE)

    # 如果替换后仍含有大量英文字符，生成通顺的中文保底简介
    if is_mostly_english(t_desc):
        cat_descs = {
            'audio': f'{name_clean} // 跨平台无损音频与音乐流媒体客户端，支持多音源与歌单解析。',
            'video': f'{name_clean} // 现代化高性能视频播放与流媒体解析工具，流畅解码高清素材。',
            'local': f'{name_clean} // 纯本地离线运行的生产力神兵，保障个人隐私与高速处理。',
            'geek': f'{name_clean} // 极客网络抓包嗅探与逆向架构调试台，深入协议底层。'
        }
        t_desc = cat_descs.get(default_cat, f'{name_clean} // 极客开源生产力工具，纯本地运行与极速响应。')

    ch_title = f"{name_clean} // 极客精选开源神兵"
    return ch_title, t_desc, '跨平台全端'


def translate_radar_headline(raw_title, cat):
    """将英文科技标题转换为高能有力的中文情报标题"""
    t_lower = raw_title.lower().strip()

    # 查表
    for k, v in HN_TITLE_TRANSLATIONS.items():
        if k in t_lower:
            return v

    if not is_mostly_english(raw_title):
        return raw_title

    # 常见英文前缀汉化
    title_cn = raw_title
    title_cn = re.sub(r'^Show HN:\s*', '极客首发：', title_cn, flags=re.IGNORECASE)
    title_cn = re.sub(r'^Ask HN:\s*', '技术思潮：', title_cn, flags=re.IGNORECASE)
    title_cn = re.sub(r'^Tell HN:\s*', '行业观察：', title_cn, flags=re.IGNORECASE)

    # 关键词转义
    k_map = [
        ('Lula Wins Brazilian Election', '巴西大选尘埃落定与拉美数字科技生态新局'),
        ('Why', '深度剖析：为什么'),
        ('How to', '极客实战：如何'),
        ('Architecture of', '深度解构系统架构：'),
        ('Memory Leak', '内存泄漏排查与机制修复'),
        ('Vulnerability', '重大安全漏洞预警与防御拓扑'),
        ('Performance', '极限性能基准测算与调优'),
        ('Open Source', '开源生态重构')
    ]
    for en_k, cn_v in k_map:
        if en_k.lower() in title_cn.lower():
            title_cn = re.sub(en_k, cn_v, title_cn, flags=re.IGNORECASE)

    # 保底汉化补充
    if is_mostly_english(title_cn):
        if cat == 'ai':
            return f"前沿推演：{title_cn} 引发的大模型本格逻辑论战"
        elif cat == 'observatory':
            return f"网络探秘：{title_cn} 背后的隐秘协议与数字线索"
        else:
            return f"寰宇观察：关于 {title_cn} 的全球架构演进思潮"

    return title_cn



BADGE_TRANSLATIONS = {
    'OFFLINE': '纯离线神兵',
    'TRAFFIC': '网络抓包',
    'MULTI-SOURCE': '多源聚合',
    'SNIFFER': '嗅探下载',
    'SWISS ARMY': '极客军刀',
    'CROSS-PLATFORM': '跨平台全端',
    'HIGH-PERF': '极致性能',
    'PRODUCTIVITY': '生产力利器',
    'SECURITY': '安全渗透',
    'DESIGN AWARD': '设计大奖',
    'CLI POWER': '终端神兵',
    'RUST SPEED': 'Rust极速',
    'ADB MIRROR': 'ADB低延迟',
    'AGGREGATION': '全网聚合',
    'AUTO STREAM': '自动录播',
    'REMOTE': '自建远控',
    'REVERSE': '逆向解构',
    'MODERN AUDIO': '现代流媒体',
    'MEDIA CENTER': '私有影院',
    'LOSSLESS': '无损剪辑',
    'GITHUB': '开源热门',
    'HOT ARSENAL': '热门军械',
    'API CLIENT': 'API客户端',
    'API HUB': 'API中枢',
    'CORE AUDIO': '底层音频驱动',
    'DUAL TOOLS': '双合一神兵',
    'P2P SHARE': '局域网P2P',
    'PACKET': '数据包分析',
    'PROXY': '中间人代理',
    'SELF-HOSTED': '私有化自建',
    'TRANSCODER': '硬件级转码',
    'WORKFLOW': '自动化工作流'
}

GEM_RANK_TRANSLATIONS = {
    'MASTERPIECE': '№ 01 · 瑞士排版典范',
    'THREE.JS CAR': '№ 02 · 3D越野漫游神作',
    'PIXEL MAGIC': '№ 03 · 像素着色圣殿',
    'PARTICLE FIELD': '№ 04 · 粒子流体力场',
    'CYBER PARALLAX': '№ 05 · 赛博视差空间',
    'WEBGPU VAULT': '№ 06 · 先锋商业交互典范',
    'SWISS POSTER': '№ 07 · 瑞士海报经典',
    'GRID CATALOG': '№ 08 · 极简网格图谱',
    'EDITORIAL GRID': '№ 09 · 网页美学年鉴',
    'TYPO CURATOR': '№ 10 · 西文字体搭配圣经',
    'EXPERIMENTAL': '№ 11 · 先锋实验交互',
    'RAW HTML': '№ 12 · 粗野主义设计年鉴',
    'KINETIC CRAFT': '№ 13 · 微动效体验巅峰',
    'SHADER & MATH': '№ 14 · 极坐标光影实验',
    'DESIGN ENGINEERING': '№ 15 · 交互工程手记',
    'TACTILE WEB': '№ 16 · 屏幕纸质触感',
    'MOTION LABORATORY': '№ 17 · 弹簧物理动效',
    'HUMAN INTERFACE': '№ 18 · 苹果设计大奖标杆',
    'INDUSTRIAL SYSTEM': '№ 19 · 黑白工业设计规范',
    'PURE AESTHETICS': '№ 20 · 无算法纯净策展',
    'TOP SHOWCASE': '№ 21 · 全球顶级设计每日展',
    'SITE OF THE DAY': '№ 22 · 全球创意评审标杆',
    'FUTURE ARCHIVE': '№ 23 · 先锋未来网页奖',
    'METICULOUS POD': '№ 24 · 微小细节解构笔记'
}


def sanitize_tool_badge(badge, cat):
    """深度汉化工具卡片角标与星标"""
    if not badge:
        cat_badge = {
            'audio': '天籁之源 · 音乐流媒体',
            'video': '极影魔方 · 高性能播放',
            'local': '离线神兵 · 纯本地利器',
            'geek': '逆向兵刃 · 协议嗅探'
        }
        return cat_badge.get(cat, '极客精选 · 开源神兵')
    b = str(badge)
    for en_k, cn_v in BADGE_TRANSLATIONS.items():
        if en_k in b:
            b = b.replace(en_k, cn_v)
    return b


def sanitize_radar_spec_tag(spec_tag, cat):
    """深度汉化热点雷达侦测徽章"""
    if not spec_tag:
        cat_tags = {
            'ai': '[ 前沿: 大模型架构 ]',
            'global': '[ 国际: 科技风向标 ]',
            'domestic': '[ 国内: 极客热议 ]',
            'observatory': '[ 探秘: 密码与奇闻 ]'
        }
        return cat_tags.get(cat, '[ 综合情报雷达 ]')
    s = str(spec_tag)
    s_map = {
        'MYSTERY: CICADA 3301': '极客探秘: 蝉3301',
        'PROTOCOL: NOSTR ARCH': '去中心化协议: NOSTR',
        'CRYPTO: NUMBERS STATION': '密码探秘: 幽灵数字电台',
        'LOCAL INFERENCE: WEBGPU': '端侧推理: WEBGPU',
        '深度解构: 大模型闭环逻辑': '内部: 硅谷闭环逻辑'
    }
    for en_k, cn_v in s_map.items():
        if en_k in s:
            s = s.replace(en_k, cn_v)
    return s


def sanitize_radar_title(title, cat):
    """去除多层嵌套前缀并规范汉化标题"""
    if not title:
        return '极客深度前沿情报跟踪'
    t = str(title)
    while True:
        prev = t
        t = re.sub(r'^(?:观察：【\s*|寰宇观察：关于\s*|前沿推演：\s*)+', '', t)
        t = re.sub(r'(?:\s*】全景架构拆解与思考|\s*的大模型本格逻辑论战|\s*的全球架构演进思潮)+$', '', t)
        t = t.strip()
        if t == prev:
            break

    t_lower = t.lower()
    if 'dolly parton' in t_lower:
        return '全球数字阅读普惠：Dolly Parton 想象力图书馆底层工程解构'
    if 'attention is not what you need' in t_lower:
        return '顶会先锋探索：无注意力机制架构(2025)能否颠覆大模型范式？'
    if 'f-zero x' in t_lower:
        return '极客硬核逆向：任天堂 3DS 平台移植 F-Zero X 引擎原理解析'
    if 'cicada 3301' in t_lower:
        return '全球密码未解之谜：Cicada 3301 密码学寻宝与暗网谜团'
    if 'numbers station' in t_lower:
        return '冷战短波电台频段中的“幽灵数字电台”密码监听录'
    if 'nostr' in t_lower:
        return '去中心化协议考察：从 Gopher、Usenet 到 Nostr 的极客暗涌'
    if 'webgpu' in t_lower:
        return '端侧推理突围：极小体积大模型借力 WebGPU 在浏览器满血狂飙'

    return translate_radar_headline(t, cat)


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
    """获取 HackerNews Top 科技头条并全境汉化"""
    print(f"[1/4] 正在拉取全球前沿科技情报 (HackerNews Top {limit})...")
    top_ids = http_get_json('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=8)
    if not top_ids:
        return []

    news_items = []
    for sid in top_ids[:limit]:
        item = http_get_json(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json', timeout=5)
        if item and 'title' in item:
            title_raw = item.get('title', '')
            title_lower = title_raw.lower()
            if any(k in title_lower for k in ['ai', 'gpt', 'llm', 'model', 'claude', 'deepseek', 'neural', 'reasoning', 'agent']):
                cat = 'ai'
            elif any(k in title_lower for k in ['security', 'vulnerability', 'hack', 'leak', 'dark', 'cipher', 'mystery', 'crypto']):
                cat = 'observatory'
            else:
                cat = 'global'

            # 全境汉化标题
            title_cn = translate_radar_headline(title_raw, cat)

            news_items.append({
                'title': title_cn,
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
    """跨维度探测 GitHub 顶级开源神兵并执行全境汉化"""
    print("[3/4] 正在跨维度探测 GitHub 顶级开源神兵并执行全境汉化...")
    live_tools = []
    gh_headers = {'User-Agent': USER_AGENT}
    gh_token = os.environ.get('GITHUB_TOKEN')
    if gh_token:
        gh_headers['Authorization'] = f'Bearer {gh_token}'

    queries = [
        ('topic:music-player+sort:stars', 'audio', '天籁之源 · 音乐流媒体客户端', '天籁之源 ·'),
        ('topic:video-player+sort:stars', 'video', '极影魔方 · 高性能极简视频播放器', '极影魔方 ·'),
        ('topic:offline-first+sort:stars', 'local', '离线神兵 · 本地高能生产力利器', '离线神兵 ·'),
        ('topic:reverse-engineering+sort:stars', 'geek', '逆向兵刃 · 网络抓包嗅探重构台', '逆向兵刃 ·')
    ]

    for q, cat, default_desc, badge_prefix in queries:
        try:
            search_url = f'https://api.github.com/search/repositories?q={q}&per_page=4'
            data = http_get_json(search_url, timeout=6, headers=gh_headers)
            if data and 'items' in data:
                for item in data['items'][:2]:
                    stars_k = f"{round(item.get('stargazers_count', 0) / 1000, 1)}k★"
                    name_raw = item.get('name')
                    desc_raw = item.get('description') or default_desc

                    # 全境深度汉化工具标题与亮点介绍
                    ch_name, ch_desc, ch_platform = translate_github_tool_info(name_raw, desc_raw, cat)

                    live_tools.append({
                        "name": ch_name,
                        "desc": ch_desc,
                        "badge": f"{badge_prefix} {stars_k}",
                        "categoryId": cat,
                        "url": item.get('html_url'),
                        "launchText": "探查源码 ➔",
                        "platform": ch_platform
                    })
        except Exception as e:
            print(f"[INFO] GitHub 在线探测日志 ({cat}): {e}")

    return live_tools


def fetch_live_gems():
    """探索全球创意网站矿脉并全境汉化"""
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
                    "badge": f"创意开源 · {stars_k}",
                    "badgeClass": "is-codepen",
                    "rank": "开源力场实验室",
                    "title": f"{name_clean} // 创意力场实验室",
                    "domain": "github.com ↗",
                    "categoryId": "shader",
                    "desc": "极具探索性的三维图形学与数学视觉算法实验项目，探索微交互动效天花板。",
                    "techTags": ["WebGL三维", "GLSL着色器", "2D画布", "创意编程"],
                    "footLabel": "开源灵感源码",
                    "linkText": "探查矿脉 ↳"
                })
    except Exception as e:
        print(f"[INFO] Web Gems 在线探索日志: {e}")

    return live_gems


# ==========================================
# 标杆高分热点基准库 (全境 100% 汉化)
# ==========================================
BENCHMARK_RADAR_SEED = [
    # 1. 智子推演 (AI & Paradox)
    {
        "categoryId": "ai",
        "category": "智子推演 // AI & PARADOX",
        "time": "今日发布 // 08:30 UTC",
        "title": "多模态推演能否构建真正的“物理闭环密室”？",
        "summary": "实测最新前沿大模型在多重伪解答架构中的表现：虽然能瞬间生成海量障眼法，但在微观物理材质力学与时间线交叉口供的精确剪裁上，人类本格心机依然是不可替代的胜负手。",
        "specTag": "[ 深度内参: 密室闭环逻辑 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://bckj.site"
    },
    {
        "categoryId": "ai",
        "category": "智子推演 // AI & PARADOX",
        "time": "今日发布 // 07:15 UTC",
        "title": "推理模型时代：从盲目补全到本格长链条自我证伪",
        "summary": "深度剖析 DeepSeek-R1 与 o1 类长思考模型的拓扑结构：大模型首次具备了推翻自身第一假设并回溯验证的能力，如同侦探在案发现场推演多条死胡同后的绝地反击。",
        "specTag": "[ 技术突破: 思考模型自我回溯 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://news.ycombinator.com"
    },
    {
        "categoryId": "ai",
        "category": "智子推演 // AI & PARADOX",
        "time": "今日发布 // 06:40 UTC",
        "title": "Agentic Coding 范式转移：写代码已演变为系统架构博弈",
        "summary": "当 AI 助手能自主分析数十万行跨模块依赖并执行精准重构，程序员的核心竞争力正在从语法敲击彻底迁徙为逻辑裁决与本格审美鉴赏。",
        "specTag": "[ 范式转移: 智能体系统裁决 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://github.com/trending"
    },
    {
        "categoryId": "ai",
        "category": "智子推演 // AI & PARADOX",
        "time": "今日发布 // 05:20 UTC",
        "title": "本地端侧算力突围：纯离线小参数模型赋能单机推理游戏",
        "summary": "基于 WebGPU 与 ONNX 架构的 1.5B/3B 参数端侧模型实测：无需连接云端即可实现亚秒级动态 NPC 心理博弈，彻底斩断隐私泄露与高昂服务器账单。",
        "specTag": "[ 离线端侧: WEBGPU 纯本地运算 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://huggingface.co"
    },

    # 2. 寰宇前沿 (Global Tech)
    {
        "categoryId": "global",
        "category": "寰宇前沿 // GLOBAL TECH",
        "time": "今日发布 // 08:10 UTC",
        "title": "我们应当对亲手构建的软件抱有更大雄心：反思现代技术的过度膨胀",
        "summary": "HackerNews 社区热榜头条批判现代软件被沉重框架与臃肿抽象束缚，呼吁回归瑞士钟表般的精密轻量原生体验与极致运行速度。",
        "specTag": "[ 深度长文: 反思软件膨胀 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://danluu.com/ambitious/"
    },
    {
        "categoryId": "global",
        "category": "寰宇前沿 // GLOBAL TECH",
        "time": "今日发布 // 07:05 UTC",
        "title": "OBS Studio 33 突破性更新：原生重构实时渲染流管线",
        "summary": "开源推流与录屏标杆工具 OBS 发布 33.0 巨型里程碑，重构跨平台音视频管道并降低 40% 渲染延迟，为创作者带来工业级实时推流底座。",
        "specTag": "[ 标杆发布: OBS 33 巨型重构 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://github.com/obsproject/obs-studio/releases"
    },
    {
        "categoryId": "global",
        "category": "寰宇前沿 // GLOBAL TECH",
        "time": "今日发布 // 06:12 UTC",
        "title": "Rust 与 Zig 在系统级低延迟图形引擎中的暗流争锋",
        "summary": "从 WebAssembly 到原生 GPU 驱动层，现代独立游戏开发者正在用无垃圾回收的内存安全语言重构游戏底层，彻底告别微卡顿与掉帧宿疾。",
        "specTag": "[ 底层架构: 零垃圾回收极速引擎 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://news.ycombinator.com"
    },
    {
        "categoryId": "global",
        "category": "寰宇前沿 // GLOBAL TECH",
        "time": "今日发布 // 04:50 UTC",
        "title": "WebKit 率先实现无损流体视口计算规范标准",
        "summary": "针对移动端动态地址栏导致的 100vh 遮挡痼疾，W3C 推进的新型 dvh 动态视口单位已全面在各大移动端内核实装，移动端全屏交互迎来纯净新基石。",
        "specTag": "[ 行业标准: DVH 动态视口实装 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://webkit.org/blog/"
    },

    # 3. 极客生态 (Domestic Dev)
    {
        "categoryId": "domestic",
        "category": "极客生态 // DOMESTIC DEV",
        "time": "今日发布 // 08:00 UTC",
        "title": "为什么很多人把 DeepSeek 神化了？看国内大模型工程落地思潮",
        "summary": "来自国内开发者社区的热点思潮（讨论度 60+ 节点：程序员）。折射出当下国内程序员在独立开发、日常生产力重构与工程落地中的真实呼声。",
        "specTag": "[ 极客讨论: V2EX 60+ 热议 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://www.v2ex.com/t/1251402"
    },
    {
        "categoryId": "domestic",
        "category": "极客生态 // DOMESTIC DEV",
        "time": "今日发布 // 07:30 UTC",
        "title": "一人独立游戏工坊全栈工作流：从剧本闭环到自建发行矩阵",
        "summary": "国内独立开发者分享如何凭借现代静态生成器与边缘网络托管搭建高逼格官网，以极低维护成本撬动高留存硬核推理用户圈层。",
        "specTag": "[ 独立全栈: BC 工坊方法论 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://bckj.site"
    },
    {
        "categoryId": "domestic",
        "category": "极客生态 // DOMESTIC DEV",
        "time": "今日发布 // 05:45 UTC",
        "title": "私有云盘 AList 生态爆发：家庭微型服务器如何重构数字资产仓",
        "summary": "探讨基于 Linux 迷你主机与 Docker 容器聚合全网网盘直链的实战经验，彻底解决插画资产与高清无损影音的跨设备高速传输痛点。",
        "specTag": "[ 个人资产: ALIST 私有存储仓 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://www.v2ex.com"
    },
    {
        "categoryId": "domestic",
        "category": "极客生态 // DOMESTIC DEV",
        "time": "今日发布 // 03:50 UTC",
        "title": "逆向嗅探与私有协议解析：极客创作者的日常兵刃考究",
        "summary": "从桌面音频解析插件到无损剪刀 LosslessCut，国内极客群体正在用纯粹开源免费的轻巧小工具打破大厂壁垒，守护个人离线数字主权。",
        "specTag": "[ 极客装备: 个人离线数字主权 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://www.v2ex.com"
    },

    # 4. 视界暗线 (Observatory)
    {
        "categoryId": "observatory",
        "category": "视界暗线 // OBSERVATORY",
        "time": "今日发布 // 07:50 UTC",
        "title": "网络考古：1999 年消失的网页暗号与早期密室迷踪解构",
        "summary": "探秘 Web 1.0 时代隐藏在 HTML 注释与纯文本论坛中的暗线解谜游戏，本格派推理如何在早期赛博空间生根发芽并影响当下一代创作者。",
        "specTag": "[ 网络考古: 1999 暗号密室 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://news.ycombinator.com"
    },
    {
        "categoryId": "observatory",
        "category": "视界暗线 // OBSERVATORY",
        "time": "今日发布 // 06:30 UTC",
        "title": "暗网通信协议中的时延混淆算法与反向测谎模型",
        "summary": "深层解构基于发条式随机延迟网络包的匿名通信原理，该机制与本格推理中“利用留声机与定时器构筑不在场证明”的物理诡计高度同构。",
        "specTag": "[ 密码破译: 时钟延迟障眼法 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://bckj.site"
    },
    {
        "categoryId": "observatory",
        "category": "视界暗线 // OBSERVATORY",
        "time": "今日发布 // 05:10 UTC",
        "title": "被遗忘的冷战短波电台：频段中的“林肯郡偷猎者”机械密码",
        "summary": "数字电台（Numbers Station）二十年未解之谜复盘：全自动磁带循环播报、一次性密码本（OTP）与不可破译的绝对数学盲区。",
        "specTag": "[ 密码迷踪: 数字电台未解之谜 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://en.wikipedia.org/wiki/Numbers_station"
    },
    {
        "categoryId": "observatory",
        "category": "视界暗线 // OBSERVATORY",
        "time": "今日发布 // 04:15 UTC",
        "title": "全网未解数字谜题：Cicada 3301 经典密码学拓扑复盘",
        "summary": "回顾互联网历史上最富神秘色彩的本格密码学挑战，融合了物理书本密钥、微积分极坐标与暗网洋葱路由的跨维度脑力激荡。",
        "specTag": "[ 终极谜题: CICADA 3301 拓扑 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://en.wikipedia.org/wiki/Cicada_3301"
    },
    {
        "categoryId": "observatory",
        "category": "视界暗线 // OBSERVATORY",
        "time": "今日发布 // 03:00 UTC",
        "title": "深网协议考古：从 Gopher、Usenet 到 Nostr 的极客抗审查暗线",
        "summary": "当主流互联网被封闭花园与算法投喂彻底隔绝，极客开发者正在用纯粹端到端公私钥对与中继网络重构不受限的自由信息暗网。",
        "specTag": "[ 协议暗线: 自由信息拓扑 ]",
        "linkText": "展开深度内参 ↳",
        "url": "https://github.com/nostr-protocol"
    }
]


# ==========================================
# 标杆高分开源装备库 (全境 100% 汉化)
# ==========================================
BENCHMARK_TOOLBOX_SEED = [
    # 1. 音频与音源 (Audio & Source)
    {
        "name": "MusicFree // 插件化多音源音乐播放器",
        "desc": "基于插件化架构的跨平台音乐神器。本身不集成任何音源，用户可通过自定义 JS 脚本插件自由接入全网无损音频与歌单，纯净无广告。",
        "badge": "多音源插件 · 16.8k★",
        "categoryId": "audio",
        "url": "https://github.com/maotoumao/MusicFree",
        "launchText": "探查源码 ➔",
        "platform": "Win · Mac · 安卓"
    },
    {
        "name": "Spotube // 纯净跨平台流媒体客户端",
        "desc": "利用公开接口抓取元数据并获取无损无广告音频流，完全开源轻量，内存占用不足官方十分之一，跨端体验极度丝滑。",
        "badge": "跨平台全端 · 33.2k★",
        "categoryId": "audio",
        "url": "https://github.com/KRTirtho/spotube",
        "launchText": "探查源码 ➔",
        "platform": "Win · Mac · Linux"
    },
    {
        "name": "洛雪音乐 // 经典多源无损桌面端",
        "desc": "基于 Electron 与 Vue 打造的开源音频流客户端。支持各大平台歌曲搜索、歌词逐字同步与自定义音源解析脚本。",
        "badge": "开源顶流 · 54.7k★",
        "categoryId": "audio",
        "url": "https://github.com/lyswhut/lx-music-desktop",
        "launchText": "探查源码 ➔",
        "platform": "Win · Mac · Linux"
    },
    {
        "name": "YesPlayMusic // 高颜值第三方网易云桌面端",
        "desc": "极具现代苹果设计美学的第三方音乐客户端。支持自动音源替换、Touch Bar 快捷控制与暗黑模式，视觉质感极佳。",
        "badge": "设计金奖 · 31.5k★",
        "categoryId": "audio",
        "url": "https://github.com/qier222/YesPlayMusic",
        "launchText": "探查源码 ➔",
        "platform": "Win · Mac · 网页端"
    },
    {
        "name": "Listen1 // 全网音乐多合一聚合播放器",
        "desc": "打破曲库壁垒，聚合各大平台曲库。一个搜索框搞定全网找歌与歌单导入，本地安全离线运行。",
        "badge": "全网聚合 · 14.1k★",
        "categoryId": "audio",
        "url": "https://github.com/listen1/listen1_desktop",
        "launchText": "探查源码 ➔",
        "platform": "Chrome插件 · 桌面端"
    },
    {
        "name": "Moosync // 本地与流媒体双轨音乐播放器",
        "desc": "专为极客音乐爱好者打造。同时管理本地高解析 FLAC 音乐库与在线播放列表，支持自定义均衡器与扩展插件。",
        "badge": "双轨播放 · 3.8k★",
        "categoryId": "audio",
        "url": "https://github.com/Moosync/Moosync",
        "launchText": "探查源码 ➔",
        "platform": "跨平台全端"
    },
    {
        "name": "Navidrome // 轻量自建私有云端无损音乐服",
        "desc": "现代高性能自建音乐服务器，基于 Go 语言开发，纯本地扫描无损音乐文件夹，支持全平台 Subsonic 协议客户端投屏与串流。",
        "badge": "自建私有云 · 14.2k★",
        "categoryId": "audio",
        "url": "https://github.com/navidrome/navidrome",
        "launchText": "探查源码 ➔",
        "platform": "Docker · 私有部署"
    },
    {
        "name": "BlackHole // macOS 零延迟虚拟声卡驱动",
        "desc": "解决 macOS 系统无法直接录制系统声音或各 App 间音频跳线的终极内核级开源虚拟声卡，混音与播客制作必备神卡。",
        "badge": "内核虚拟驱动 · 17.5k★",
        "categoryId": "audio",
        "url": "https://github.com/ExistentialAudio/BlackHole",
        "launchText": "探查源码 ➔",
        "platform": "macOS 专属"
    },

    # 2. 视频与流媒体源 (Video & Stream)
    {
        "name": "IINA // macOS 现代极简播放器天花板",
        "desc": "基于 mpv 内核深度定制的现代化开源播放器。完美契合 macOS 设计哲学，支持画中画、外挂字幕实时搜索、HDR 与任意流媒体协议解码。",
        "badge": "macOS天花板 · 38.5k★",
        "categoryId": "video",
        "url": "https://github.com/iina/iina",
        "launchText": "探查源码 ➔",
        "platform": "macOS 专属"
    },
    {
        "name": "LosslessCut // 无损音视频极速裁剪拼接神兵",
        "desc": "基于 FFmpeg 打造的零编解码极速剪刀。无需二次渲染，光速粗剪 4K 巨型视频无画质损耗，极客工作流必备生产力。",
        "badge": "零渲染无损剪 · 22.4k★",
        "categoryId": "video",
        "url": "https://github.com/mifi/lossless-cut",
        "launchText": "探查源码 ➔",
        "platform": "跨平台全端"
    },
    {
        "name": "MediaGo // 网页流媒体嗅探与多线程下载器",
        "desc": "支持 m3u8 / MPD 自动解密与多线程合并抓取，内置极简浏览器自动嗅探网页视频源，快速保存公开高清素材。",
        "badge": "网页流嗅探 · 6.8k★",
        "categoryId": "video",
        "url": "https://github.com/bistutu/MediaGo",
        "launchText": "探查源码 ➔",
        "platform": "Win · Mac · Linux"
    },
    {
        "name": "mpv.net // 极客硬核视频着色渲染播放器",
        "desc": "基于 libmpv 架构的高性能视频播放器，具备完备的 GPU 着色器扩展与高画质升采样算法支持。",
        "badge": "高性能GPU渲染 · 4.9k★",
        "categoryId": "video",
        "url": "https://github.com/mpvnet-player/mpv.net",
        "launchText": "探查源码 ➔",
        "platform": "Windows 专属"
    },
    {
        "name": "BBDown // 命令行高画质流媒体解构下载器",
        "desc": "多线程分块下载、杜比视界与真彩画质解析、多音轨分离抓取的硬核轻量级媒体终端工具。",
        "badge": "硬核终端解析 · 12.3k★",
        "categoryId": "video",
        "url": "https://github.com/nilaoda/BBDown",
        "launchText": "探查源码 ➔",
        "platform": "命令行终端通用"
    },
    {
        "name": "录播姬 // 全自动无人值守高清录播守护程序",
        "desc": "专为直播流保存设计的全自动守护进程。开播自动极速录制，智能跳过重连并无缝混流为标准 MP4，支持多主播并发。",
        "badge": "无人值守录播 · 3.5k★",
        "categoryId": "video",
        "url": "https://github.com/BililiveRecorder/BililiveRecorder",
        "launchText": "探查源码 ➔",
        "platform": "跨平台全端"
    },
    {
        "name": "Jellyfin // 100% 自由开源媒体服务器",
        "desc": "无商业化绑架的纯净媒体中心。自动刮削电影与剧集海报墙、支持硬件转码与全家跨端协同流媒体点播。",
        "badge": "自由媒体中心 · 36.8k★",
        "categoryId": "video",
        "url": "https://github.com/jellyfin/jellyfin",
        "launchText": "探查源码 ➔",
        "platform": "服务端 · 全端投屏"
    },
    {
        "name": "HandBrake // 通用硬件加速视频压制转码利器",
        "desc": "近二十年开源常青树。支持 NVENC / QuickSync 硬件编码，精准裁切黑边、优化色彩空间与批量压缩 4K 大文件。",
        "badge": "硬件加速压制 · 16.5k★",
        "categoryId": "video",
        "url": "https://github.com/HandBrake/HandBrake",
        "launchText": "探查源码 ➔",
        "platform": "Win · Mac · Linux"
    },

    # 3. 离线神兵 (Local First)
    {
        "name": "DevToys // 瑞士军刀开发者离线工具箱",
        "desc": "纯本地离线运行的开发利器，涵盖 JSON/YAML 校验、JWT 解码、正则表达式演算、Hash 验算与色彩转换。",
        "badge": "纯离线生产力 · 25.1k★",
        "categoryId": "local",
        "url": "https://github.com/DevToys-app/DevToys",
        "launchText": "探查源码 ➔",
        "platform": "Win · Mac · Linux"
    },
    {
        "name": "LocalSend // 局域网跨端无损极速传输协议",
        "desc": "无需连接互联网、纯局域网点对点互传文件神器。完全开源，秒杀 AirDrop 并通吃 iOS、Android、Windows、Mac。",
        "badge": "局域网秒传 · 49.8k★",
        "categoryId": "local",
        "url": "https://github.com/localsend/localsend",
        "launchText": "探查源码 ➔",
        "platform": "全系统通用"
    },
    {
        "name": "Flameshot // 现代化硬核极简截图标注工具",
        "desc": "支持像素级拾色、模糊马赛克、序号标注、多显示器协同与命令行截图自动化，完全本地隐私无后台。",
        "badge": "像素级标注 · 24.6k★",
        "categoryId": "local",
        "url": "https://github.com/flameshot-org/flameshot",
        "launchText": "探查源码 ➔",
        "platform": "跨平台全端"
    },
    {
        "name": "CyberChef // 极客密码学与数据转换瑞士军刀",
        "desc": "被称为网络安全界的厨师机。纯本地浏览器运行的加密解密、编码转换、反混淆与特征分析超级工作台。",
        "badge": "极客瑞士军刀 · 30.2k★",
        "categoryId": "local",
        "url": "https://github.com/gchq/CyberChef",
        "launchText": "探查源码 ➔",
        "platform": "浏览器纯本地离线"
    },
    {
        "name": "Espanso // Rust 驱动极速文本扩展补全器",
        "desc": "基于 Rust 开发的跨平台快捷键文本扩展神器。输入简短暗号自动展开为长邮件模板、代码片段或当前时间戳，完全离线。",
        "badge": "Rust极速补全 · 14.9k★",
        "categoryId": "local",
        "url": "https://github.com/espanso/espanso",
        "launchText": "探查源码 ➔",
        "platform": "跨平台全端"
    },
    {
        "name": "RustDesk // 100% 开源自建中继远程桌面",
        "desc": "完全可替代 TeamViewer / AnyDesk 的自建远程协助利器。支持自建 Relay 中继服务器，端到端加密零商业限制。",
        "badge": "开源自建远控 · 81.2k★",
        "categoryId": "local",
        "url": "https://github.com/rustdesk/rustdesk",
        "launchText": "探查源码 ➔",
        "platform": "全系统通用"
    },
    {
        "name": "ShareX // Windows 终极截图与录屏工作流武器",
        "desc": "拥有 15 年历史的 Windows 截屏与工作流自动化开源巨匠。支持 OCR 识别、颜色拾取与自定义目标自动上传。",
        "badge": "自动化截屏录制 · 28.5k★",
        "categoryId": "local",
        "url": "https://github.com/ShareX/ShareX",
        "launchText": "探查源码 ➔",
        "platform": "Windows 专属"
    },
    {
        "name": "Bruno // 本地离线优先轻量级 API 调试端",
        "desc": "告别 Postman 云端绑架与强制登录。采用纯文本 Bru 语言直接保存在 Git 仓库中，纯离线安全高速调试 API 请求。",
        "badge": "离线API调试 · 27.8k★",
        "categoryId": "local",
        "url": "https://github.com/usebruno/bruno",
        "launchText": "探查源码 ➔",
        "platform": "跨平台全端"
    },

    # 4. 逆向兵刃 (Geek Arsenal)
    {
        "name": "HTTP Toolkit // 现代化网络抓包嗅探重构台",
        "desc": "一键拦截、检查并重写 HTTP(S) 网络请求。精准调试 API 接口、解密 App 请求协议与流量分析。",
        "badge": "全协议抓包重构 · 9.8k★",
        "categoryId": "geek",
        "url": "https://github.com/httptoolkit/httptoolkit",
        "launchText": "探查源码 ➔",
        "platform": "Win · Mac · Linux"
    },
    {
        "name": "Caido // Rust 打造的现代 Web 安全渗透台",
        "desc": "专为安全研究员与协议分析师打造的现代网络审计工具。内存占用不足 Burp Suite 十分之一，UI 极具赛博现代感。",
        "badge": "现代网络渗透 · 4.8k★",
        "categoryId": "geek",
        "url": "https://github.com/caido/caido",
        "launchText": "探查源码 ➔",
        "platform": "跨平台全端"
    },
    {
        "name": "Scrcpy // 极低延迟安卓终端投屏与控制神兵",
        "desc": "无需 Root、无需在手机安装任何 App。纯 ADB 管道实现 30-70ms 极低延迟 60FPS 安卓屏幕投射与键盘鼠标操控。",
        "badge": "极速安卓投屏 · 119k★",
        "categoryId": "geek",
        "url": "https://github.com/Genymobile/scrcpy",
        "launchText": "探查源码 ➔",
        "platform": "跨平台全端"
    },
    {
        "name": "Ghidra // 软件逆向工程与二进制反编译架构",
        "desc": "由美国国家安全局开源的强大逆向工程套件。支持 x86/ARM/MIPS 全指令集反汇编与 C 语言高阶代码反编译还原。",
        "badge": "军工级反编译 · 53.6k★",
        "categoryId": "geek",
        "url": "https://github.com/NationalSecurityAgency/ghidra",
        "launchText": "探查源码 ➔",
        "platform": "跨平台全端"
    },
    {
        "name": "Wireshark // 全球标杆网络数据包深层协议听诊器",
        "desc": "网络通信世界的终极听诊器。精准抓取以太网、TCP/IP、DNS 与 TLS 握手数据包，排查网络故障与协议逆向必备。",
        "badge": "底层协议听诊 · 3.5k★",
        "categoryId": "geek",
        "url": "https://gitlab.com/wireshark/wireshark",
        "launchText": "探查源码 ➔",
        "platform": "全系统通用"
    },
    {
        "name": "Postcat // 开源敏捷 API 全生命周期协作台",
        "desc": "支持插件化扩展的高颜值 API 管理工具。纯本地数据存储、支持多协议调试与代码自动生成，完全开源免费。",
        "badge": "敏捷接口研测 · 4.2k★",
        "categoryId": "geek",
        "url": "https://github.com/Postcatlab/postcat",
        "launchText": "探查源码 ➔",
        "platform": "跨平台全端"
    },
    {
        "name": "Mitmproxy // 命令行 Python 拦截中间人代理",
        "desc": "完全可编程的中间人代理工具。支持用 Python 脚本实时篡改请求头、解密流量并重放数据包，渗透测试利器。",
        "badge": "可编程中间人 · 35.8k★",
        "categoryId": "geek",
        "url": "https://github.com/mitmproxy/mitmproxy",
        "launchText": "探查源码 ➔",
        "platform": "Python 终端神器"
    },
    {
        "name": "Reqable // 新一代 API 调试与 HTTPS 抓包利器",
        "desc": "基于 Flutter 开发的现代化跨平台抓包利器，将 Fiddler 抓包能力与 Postman 接口测试深度融合，速度飞快。",
        "badge": "调试抓包二合一 · 7.5k★",
        "categoryId": "geek",
        "url": "https://reqable.com",
        "launchText": "探查官网 ➔",
        "platform": "跨平台全端"
    }
]


# ==========================================
# 标杆高分神仙网站矿藏库 (全境 100% 汉化)
# ==========================================
BENCHMARK_GEMS_SEED = [
    # 1. 视觉力场 (Shader & 3D)
    {
        "url": "https://wodniack.dev",
        "badge": "2025 韦比设计奖提名",
        "badgeClass": "is-webby",
        "rank": "№ 01 · 瑞士排版典范",
        "title": "Antoine Wodniack 极简作品集",
        "domain": "wodniack.dev ↗",
        "categoryId": "shader",
        "desc": "瑞士平面网格设计、极限排版美学与 Matter.js 刚体物理交互的教科书级天花板典范。",
        "techTags": ["刚体物理仿真", "2D画布", "丝滑平滑滚动", "瑞士国际排版"],
        "footLabel": "交互档案库",
        "linkText": "打开灵感 ↳"
    },
    {
        "url": "https://bruno-simon.com",
        "badge": "3D 物理交互神作",
        "badgeClass": "is-codepen",
        "rank": "№ 02 · 3D越野漫游神作",
        "title": "Bruno Simon 3D 越野漫游世界",
        "domain": "bruno-simon.com ↗",
        "categoryId": "shader",
        "desc": "在网页中开着越野车漫游探索的 WebGL 3D 物理交互神作，Three.js 交互叙事里程碑。",
        "techTags": ["Three.js三维", "3D物理仿真", "GLSL着色器", "键盘驾驶微交互"],
        "footLabel": "三维漫游世界",
        "linkText": "启动漫游 ↳"
    },
    {
        "url": "https://www.shadertoy.com",
        "badge": "数学与光影艺术",
        "badgeClass": "is-webby",
        "rank": "№ 03 · 像素着色圣殿",
        "title": "Shadertoy // 纯算法着色器圣殿",
        "domain": "shadertoy.com ↗",
        "categoryId": "shader",
        "desc": "仅用纯数学公式与像素着色器渲染出逼真黑洞、云海与机械奇迹的代码圣殿。",
        "techTags": ["光线步进算法", "GLSL着色器", "纯数学公式", "GPU硬件加速"],
        "footLabel": "算法艺术殿堂",
        "linkText": "破译算力 ↳"
    },
    {
        "url": "https://lusion.co",
        "badge": "顶级创意实验室",
        "badgeClass": "is-webby",
        "rank": "№ 04 · 粒子流体力场",
        "title": "Lusion 顶级先锋创意技术工坊",
        "domain": "lusion.co ↗",
        "categoryId": "shader",
        "desc": "将数百万粒子流体动力学与三维着色器发挥到极限的全球顶级创意实验室官网，极富未来感。",
        "techTags": ["3D粒子力场", "流体动力学", "着色器特效", "空间音效协同"],
        "footLabel": "创意工作室展台",
        "linkText": "探查力场 ↳"
    },
    {
        "url": "https://keitayamada.com",
        "badge": "赛博视差空间",
        "badgeClass": "is-codepen",
        "rank": "№ 05 · 赛博视差空间",
        "title": "山田启太 // 赛博视差空间",
        "domain": "keitayamada.com ↗",
        "categoryId": "shader",
        "desc": "融合日本动漫机械美学与全屏 WebGL 视差滚动的独立作品集，光影漫反射与动效丝滑无比。",
        "techTags": ["Three.js三维", "赛博朋克风", "视差滚动", "交互音效驱动"],
        "footLabel": "独立制作人空间",
        "linkText": "进入视界 ↳"
    },
    {
        "url": "https://activetheory.net",
        "badge": "先锋商业叙事",
        "badgeClass": "is-webby",
        "rank": "№ 06 · 先锋商业交互",
        "title": "Active Theory // 创意叙事交互殿堂",
        "domain": "activetheory.net ↗",
        "categoryId": "shader",
        "desc": "十年蝉联全球创意大奖的先锋技术团队，独家自研 WebGL/WebGPU 渲染引擎赋能前沿商业叙事。",
        "techTags": ["自研3D引擎", "WebGPU高能渲染", "互动叙事电影", "光影着色器"],
        "footLabel": "全球机构标杆",
        "linkText": "探查殿堂 ↳"
    },

    # 2. 瑞士排版 (Typo & Grid)
    {
        "url": "https://www.swissted.com",
        "badge": "国际排版朋克",
        "badgeClass": "is-webby",
        "rank": "№ 07 · 瑞士海报经典",
        "title": "Swissted // 国际主义平面设计海报展",
        "domain": "swissted.com ↗",
        "categoryId": "typo",
        "desc": "将经典朋克摇滚海报用严谨的瑞士国际字体排版风格进行重构，黑白线框与红黑撞色的教科书。",
        "techTags": ["国际主义排版", "Helvetica经典", "严谨网格系统", "粗野主义色彩"],
        "footLabel": "瑞士排版大师",
        "linkText": "探查海报 ↳"
    },
    {
        "url": "https://www.curated.design",
        "badge": "版式网格图谱",
        "badgeClass": "is-codepen",
        "rank": "№ 08 · 极简网格图谱",
        "title": "Curated Design // 极简网格灵感图谱",
        "domain": "curated.design ↗",
        "categoryId": "typo",
        "desc": "按版式网格、衬线排版、动效曲线严苛分类的全球数字设计索引库，寻找神仙审美的必看矿脉。",
        "techTags": ["网格目录索引", "微动效分类", "社论排版美学", "人工纯净策展"],
        "footLabel": "灵感索引图谱",
        "linkText": "查阅图谱 ↳"
    },
    {
        "url": "https://www.siteinspire.com",
        "badge": "极简主义年鉴",
        "badgeClass": "is-webby",
        "rank": "№ 09 · 网页美学年鉴",
        "title": "siteInspire // 极简主义网页美学库",
        "domain": "siteinspire.com ↗",
        "categoryId": "typo",
        "desc": "历经十余年纯人工筛选的数字排版档案。没有浮夸特效，专注纯粹字体层次与优雅空间节奏。",
        "techTags": ["纯净排版", "优雅层次感", "十年经典归档", "留白空间艺术"],
        "footLabel": "版式美学年鉴",
        "linkText": "查阅归档 ↳"
    },
    {
        "url": "https://www.typewolf.com",
        "badge": "西文字体搭配圣经",
        "badgeClass": "is-codepen",
        "rank": "№ 10 · 西文字体搭配圣经",
        "title": "Typewolf // 全球西文字体搭配圣经",
        "domain": "typewolf.com ↗",
        "categoryId": "typo",
        "desc": "全网最权威的字体搭配与版式趋势分析站。深入拆解现代衬线、无衬线几何字体的黄金组合。",
        "techTags": ["西文字体设计", "字体层级搭配", "排版系统工程", "现代衬线美学"],
        "footLabel": "西文字体指南",
        "linkText": "研读指南 ↳"
    },
    {
        "url": "https://hoverstat.es",
        "badge": "先锋实验交互",
        "badgeClass": "is-webby",
        "rank": "№ 11 · 先锋实验交互",
        "title": "Hover States // 先锋与另类交互站",
        "domain": "hoverstat.es ↗",
        "categoryId": "typo",
        "desc": "专注收集不按常理出牌的狂野排版、反主流交互与先锋数字艺术实验，打破设计思维定式。",
        "techTags": ["粗野主义", "反常规交互", "数字艺术实验", "前卫设计思潮"],
        "footLabel": "先锋异象阵地",
        "linkText": "发现异象 ↳"
    },
    {
        "url": "https://brutalistwebsites.com",
        "badge": "粗野主义年鉴",
        "badgeClass": "is-codepen",
        "rank": "№ 12 · 粗野主义年鉴",
        "title": "Brutalist Websites // 粗野主义网页年鉴",
        "domain": "brutalistwebsites.com ↗",
        "categoryId": "typo",
        "desc": "抛弃现代框架的繁冗打磨，拥抱原生 HTML 线框、单色高对比度与极限反叛态度的先锋阵地。",
        "techTags": ["原生线框美学", "极限高对比度", "复古极简结构", "反向纯粹主义"],
        "footLabel": "粗野主义归档",
        "linkText": "审视粗野 ↳"
    },

    # 3. 奇趣交互 (Kinetic UX)
    {
        "url": "https://linear.app",
        "badge": "微动效体验巅峰",
        "badgeClass": "is-webby",
        "rank": "№ 13 · 微动效体验巅峰",
        "title": "Linear // 极致微交互与暗黑质感巅峰",
        "domain": "linear.app ↗",
        "categoryId": "kinetic",
        "desc": "被全网前端与产品设计师奉为神作的软件官网。光影渐变漫反射、精密快捷键交互与极致帧率体验。",
        "techTags": ["纯键盘微交互", "奢华暗黑质感", "微光着色漫反射", "极致60帧流体"],
        "footLabel": "微动效卓越典范",
        "linkText": "研读微动效 ↳"
    },
    {
        "url": "https://codepen.io/wodniack",
        "badge": "极坐标光影实验",
        "badgeClass": "is-codepen",
        "rank": "№ 14 · 极坐标光影实验",
        "title": "Wodniack 官方创意实验场",
        "domain": "codepen.io/wodniack ↗",
        "categoryId": "kinetic",
        "desc": "Wormhole 虫洞穿梭、SVG 几何极速透视与 Canvas 极坐标光速星流特效的官方开源实验场。",
        "techTags": ["超空间跃迁", "矢量网格透视", "极坐标粒子流", "纯原生开源源码"],
        "footLabel": "开源灵感源码",
        "linkText": "探查源码 ↳"
    },
    {
        "url": "https://rauno.me/craft",
        "badge": "交互工程手记",
        "badgeClass": "is-webby",
        "rank": "№ 15 · 交互工程手记",
        "title": "Rauno Craft // 交互工程手记",
        "domain": "rauno.me/craft ↗",
        "categoryId": "kinetic",
        "desc": "Vercel 设计工程副总监的个人实验手札。解构磁吸光标、弹簧物理阻尼与流体界面计算模型。",
        "techTags": ["弹簧物理阻尼", "磁吸式光标", "微工艺打磨", "人机交互工程"],
        "footLabel": "设计工程手札",
        "linkText": "研读手札 ↳"
    },
    {
        "url": "https://press.stripe.com",
        "badge": "屏幕纸质触感",
        "badgeClass": "is-codepen",
        "rank": "№ 16 · 屏幕纸质触感",
        "title": "Stripe Press // 纸质触感在屏幕上的重生",
        "domain": "press.stripe.com ↗",
        "categoryId": "kinetic",
        "desc": "用高保真物理渲染呈现出实体精装书的质感。随着鼠标移动呈现逼真的光泽反光与纸张折叠微动效。",
        "techTags": ["拟真触觉界面", "WebGL纸张着色", "极致光影反光", "实体翻页微动效"],
        "footLabel": "实体纸质触感",
        "linkText": "翻阅纸质 ↳"
    },
    {
        "url": "https://emilkowal.ski",
        "badge": "弹簧物理动效",
        "badgeClass": "is-webby",
        "rank": "№ 17 · 弹簧物理动效",
        "title": "Emil Kowalski // 弹簧物理动效实验室",
        "domain": "emilkowal.ski ↗",
        "categoryId": "kinetic",
        "desc": "全面解构 iOS 级别手势拖拽、弹簧阻尼回弹与微动效心流体验的现代前端动效交互指南。",
        "techTags": ["手势流体拖拽", "弹簧阻尼曲线", "动效人机工程", "精工微交互"],
        "footLabel": "弹簧物理曲线",
        "linkText": "探求阻尼 ↳"
    },
    {
        "url": "https://www.apple.com/design/awards/",
        "badge": "苹果设计大奖标杆",
        "badgeClass": "is-webby",
        "rank": "№ 18 · 苹果设计大奖标杆",
        "title": "Apple Design Awards 历届展示台",
        "domain": "apple.com ↗",
        "categoryId": "kinetic",
        "desc": "每年一度全球软件设计奥斯卡。严苛剖析包容性、趣味交互与前沿人机工程学创新的巅峰殿堂。",
        "techTags": ["人机交互规范", "苹果设计美学", "巧思微动效", "包容性无障碍"],
        "footLabel": "人机交互圣殿",
        "linkText": "研读标杆 ↳"
    },

    # 4. 灵感矿脉 (Studio Vault)
    {
        "url": "https://vercel.com/design",
        "badge": "黑白工业设计规范",
        "badgeClass": "is-webby",
        "rank": "№ 19 · 黑白工业设计规范",
        "title": "Vercel Geist // 黑白工业设计系统",
        "domain": "vercel.com/design ↗",
        "categoryId": "studio",
        "desc": "定义了当今全球极客审美基调的现代工业级设计规范。黑白灰严苛层次、高精度微动效与排版力学。",
        "techTags": ["Geist设计系统", "极简工业美学", "极客体验规范", "高精组件力学"],
        "footLabel": "工业设计规范",
        "linkText": "拆解规范 ↳"
    },
    {
        "url": "https://www.cosmos.so",
        "badge": "无算法纯净策展",
        "badgeClass": "is-codepen",
        "rank": "№ 20 · 无算法纯净策展",
        "title": "Cosmos // 无算法纯净视觉策展",
        "domain": "cosmos.so ↗",
        "categoryId": "studio",
        "desc": "被称为数字时代的极简 Pinterest。拒绝社交成瘾算法与广告垃圾，只保留纯粹视觉审美与策展灵魂。",
        "techTags": ["纯人工策展", "灵感情绪板", "零算法打扰", "高品位视觉库"],
        "footLabel": "纯净灵感画板",
        "linkText": "漫步星云 ↳"
    },
    {
        "url": "https://godly.website",
        "badge": "全球顶级设计每日展",
        "badgeClass": "is-webby",
        "rank": "№ 21 · 全球顶级设计每日展",
        "title": "Godly // 全球顶级设计每日展台",
        "domain": "godly.website ↗",
        "categoryId": "studio",
        "desc": "每日严选全球最令人惊叹的现代 Web 界面与动效神作，附带完整录屏与交互细节标签索引。",
        "techTags": ["每日人工严选", "全动态录屏", "前沿网页天花板", "交互趋势指南"],
        "footLabel": "每日先锋神作",
        "linkText": "阅览神迹 ↳"
    },
    {
        "url": "https://www.awwwards.com",
        "badge": "全球创意评审标杆",
        "badgeClass": "is-webby",
        "rank": "№ 22 · 全球创意评审标杆",
        "title": "Awwwards // 全球创意设计评审标杆",
        "domain": "awwwards.com ↗",
        "categoryId": "studio",
        "desc": "数字设计领域的最高荣誉评审殿堂。按设计、代码、可用性与内容四维量化打分，数字工匠的竞技场。",
        "techTags": ["每日最佳网站", "全球评委量化", "国际荣誉殿堂", "数字匠人标准"],
        "footLabel": "全球评审权威",
        "linkText": "查阅榜单 ↳"
    },
    {
        "url": "https://thefwa.com",
        "badge": "先锋未来网页奖",
        "badgeClass": "is-webby",
        "rank": "№ 23 · 先锋未来网页奖",
        "title": "FWA // 先锋未来网页奖",
        "domain": "thefwa.com ↗",
        "categoryId": "studio",
        "desc": "始于 2000 年的数字前沿见证者。专注发现突破技术天花板、超越时代维度的沉浸式未来体验。",
        "techTags": ["每日未来项目", "先锋数字艺术", "沉浸交互空间", "前沿技术突破"],
        "footLabel": "跨维度未来体验",
        "linkText": "见证前沿 ↳"
    },
    {
        "url": "https://designdetails.fm",
        "badge": "微小细节解构",
        "badgeClass": "is-codepen",
        "rank": "№ 24 · 微小细节解构",
        "title": "Design Details // 产品细节解构手记",
        "domain": "designdetails.fm ↗",
        "categoryId": "studio",
        "desc": "深入剖析互联网头部产品中最微小却至关重要的构件、像素间距与阴影扩散半径的设计解构手札。",
        "techTags": ["软件构件解构", "像素级细节", "产品工程深度", "前沿播客沉淀"],
        "footLabel": "界面构件解构",
        "linkText": "研读微构 ↳"
    }
]


def generate_fallback_radar(hn_news, v2_news):
    """智能融合真实抓取资讯与工坊标杆基准库，生成 100% 汉化中文情报"""
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
            "time": f"今日发布 // {now_utc}",
            "title": hn['title'],
            "summary": f"HackerNews 社区热榜头条（得分 {hn['score']}）。该议题引发全球架构师与开发者关于现代计算体系、开源生态与工程效率的深度论战。",
            "specTag": f"[ 社区热榜 #{hn['score']}★ ]",
            "linkText": "展开深度内参 ↳",
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
            "time": f"今日发布 // {now_utc}",
            "title": v2['title'],
            "summary": f"来自国内极客社区的热议思潮（讨论度 {v2['replies']} 节点：{v2['node']}）。折射出当下国内程序员在独立开发、日常生产力重构与工程落地中的真实呼声。",
            "specTag": f"[ 社区频段: {v2['replies']} 条热议 ]",
            "linkText": "展开深度内参 ↳",
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
    全自动生命周期与严格容量控制体系 (全境汉化加固)：
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
    for r in raw_radar_pool:
        r['title'] = sanitize_radar_title(r.get('title', ''), r.get('categoryId', 'global'))
        r['specTag'] = sanitize_radar_spec_tag(r.get('specTag', ''), r.get('categoryId', 'global'))

    active_radar, _ = balance_pool(raw_radar_pool, 15, ['ai', 'global', 'domestic', 'observatory'])
    for r in active_radar:
        r['title'] = sanitize_radar_title(r.get('title', ''), r.get('categoryId', 'global'))
        r['specTag'] = sanitize_radar_spec_tag(r.get('specTag', ''), r.get('categoryId', 'global'))

    data['radarChamber']['items'] = active_radar
    print(f"[LIFECYCLE] 今日雷达已同步：当期驻留 {len(data['radarChamber']['items'])}/15 条最前沿情报。")

    # ----------------------------------------------------
    # 2. 开源影音武器库：当期 30 款 (四大阵营平衡) + 历史归档卷宗
    # ----------------------------------------------------
    alist_permanent_card = {
        "name": "BC Cloud Drive // 个人私有高速云盘",
        "desc": "基于 AList 与百度网盘聚合的高速资源仓 · 包含插画课程、单机游戏与设计资产，直链极速下载。",
        "badge": "在线直连 · 私有云盘",
        "categoryId": "local",
        "url": "http://111.229.205.54:5244",
        "isPrimary": True,
        "launchText": "打开云盘 ➔",
        "platform": "全系统通用"
    }

    existing_tools = [t for t in data['toolboxChamber'].get('tools', []) if not t.get('isPrimary')]
    archive_tools = data['toolboxChamber'].get('archive', [])

    raw_tool_pool = new_tools + existing_tools + BENCHMARK_TOOLBOX_SEED
    for t in raw_tool_pool:
        ch_name, ch_desc, ch_platform = translate_github_tool_info(t.get('name', ''), t.get('desc', ''), t.get('categoryId', 'local'))
        t['name'] = ch_name
        t['desc'] = ch_desc
        t['platform'] = ch_platform

    active_tools, overflow_tools = balance_pool(raw_tool_pool, 30, ['audio', 'video', 'local', 'geek'])

    # 全境深度汉化与角标规范
    for t in active_tools:
        t['platform'] = translate_platform(t.get('platform', ''))
        t['badge'] = sanitize_tool_badge(t.get('badge', ''), t.get('categoryId', 'local'))
    for ot in overflow_tools:
        ot['platform'] = translate_platform(ot.get('platform', ''))
        ot['badge'] = sanitize_tool_badge(ot.get('badge', ''), ot.get('categoryId', 'local'))

    archive_seen = set(t.get('url') for t in archive_tools)
    for ot in overflow_tools:
        url = ot.get('url') or ot.get('name')
        if url and url not in archive_seen:
            archive_seen.add(url)
            ot_copy = dict(ot)
            ot_copy['archivedAt'] = f"军械封存 · {now_month}"
            archive_tools.append(ot_copy)

    # 深度汉化所有历史归档军械，确保无遗漏
    for at in archive_tools:
        ch_name, ch_desc, ch_platform = translate_github_tool_info(at.get('name', ''), at.get('desc', ''), at.get('categoryId', 'local'))
        at['name'] = ch_name
        at['desc'] = ch_desc
        at['platform'] = translate_platform(at.get('platform') or ch_platform)
        at['badge'] = sanitize_tool_badge(at.get('badge', ''), at.get('categoryId', 'local'))
        if not at.get('archivedAt'):
            at['archivedAt'] = f"军械封存 · 往期"

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
            og_copy['archivedAt'] = f"矿脉封存 · {now_month}"
            archive_gems.append(og_copy)

    # 全境汉化所有神仙网站卡片（当期 + 归档）
    for g in active_gems + archive_gems:
        t_low = g.get('title', '').lower().strip()
        for k, v in KNOWN_GEM_TITLES.items():
            if k in t_low:
                g['title'] = v
        r_val = g.get('rank', '')
        for en_rank, cn_rank in GEM_RANK_TRANSLATIONS.items():
            if en_rank in r_val:
                g['rank'] = cn_rank
                break
        if not g.get('linkText') or 'VISIT' in g.get('linkText', ''):
            g['linkText'] = '探索站点 ➔'

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
    print("  [OK] 数据全景生命周期与全境汉化处理完成！  ")
    print("==================================================")


if __name__ == '__main__':
    main()
