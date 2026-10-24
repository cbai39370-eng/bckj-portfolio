/**
 * 每日经典电影名台词与正文双向适配信数据库
 * (Daily Film & Philosophy Motto Engine with Full In-Article Content Harmonization)
 * - 每天 00:00 自动根据公历日期哈希轮换；
 * - 顶栏 MOTTO 标语、横幅与下方的 About 第四段正文 100% 严丝合缝呼应；
 * - 完美适配中英双语国际化 (i18n)。
 */

export interface DailyMotto {
  id: string;
  badge: string;
  movieTitleZh: string;
  movieTitleEn: string;
  quoteZh: string;
  quoteEn: string;
  aboutZh: string;
  aboutEn: string;
}

export const dailyMottos: DailyMotto[] = [
  {
    id: 'truman',
    badge: 'TRUMAN SHOW // MOTTO',
    movieTitleZh: '楚门的世界',
    movieTitleEn: 'The Truman Show',
    quoteZh: '“早上好，以防再也见不到你，祝你下午好，晚上好，晚安！”',
    quoteEn: '“Good morning, and in case I don\'t see ya, good afternoon, good evening, and good night!”',
    aboutZh: '正如《楚门的世界》那句著名的问候：“早上好，以防再也见不到你，祝你下午好，晚上好，晚安！”愿每一个踏入这里的旅人，都能在此捕获一丝灵感的火花或推理的纯粹乐趣。',
    aboutEn: 'In the famous words of The Truman Show: "Good morning, and in case I don\'t see ya, good afternoon, good evening, and good night!" May every visitor finding their way here discover a spark of inspiration or the pure joy of deduction.',
  },
  {
    id: 'interstellar',
    badge: 'INTERSTELLAR // MOTTO',
    movieTitleZh: '星际穿越',
    movieTitleEn: 'Interstellar',
    quoteZh: '“不要温和地走进那个良夜，怒斥吧，怒斥光的消逝。”',
    quoteEn: '“Do not go gentle into that good night. Rage, rage against the dying of the light.”',
    aboutZh: '正如《星际穿越》中穿透星海的低语：“不要温和地走进那个良夜，怒斥吧，怒斥光的消逝。”愿每一个踏入这里的旅人，都能在数字宇宙与生活航程中，永远保留对未知、真理与远方的终极执念。',
    aboutEn: 'As echoed in Interstellar: "Do not go gentle into that good night. Rage, rage against the dying of the light." May every visitor entering this domain hold fast to an undying flame of curiosity for the deep unknown.',
  },
  {
    id: 'shawshank',
    badge: 'SHAWSHANK // MOTTO',
    movieTitleZh: '肖申克的救赎',
    movieTitleEn: 'The Shawshank Redemption',
    quoteZh: '“有些鸟儿是关不住的，它们的羽翼蕴辉着自由的光芒。”',
    quoteEn: '“Some birds aren\'t meant to be caged, their feathers are just too bright.”',
    aboutZh: '正如《肖申克的救赎》中那段对希望的颂歌：“有些鸟儿是关不住的，它们的羽翼蕴辉着自由的光芒。”愿每一个踏入这里的旅人，都能在此找到冲破平庸算法的纯粹执着与独立灵魂。',
    aboutEn: 'As celebrated in The Shawshank Redemption: "Some birds aren\'t meant to be caged, their feathers are just too bright." May every voyager finding this sanctuary discover the unyielding spark of freedom and craft.',
  },
  {
    id: 'deadpoets',
    badge: 'DEAD POETS // MOTTO',
    movieTitleZh: '死亡诗社',
    movieTitleEn: 'Dead Poets Society',
    quoteZh: '“抓紧时间，让你的生命变得与众不同。”',
    quoteEn: '“Carpe diem. Seize the day, boys. Make your lives extraordinary.”',
    aboutZh: '正如《死亡诗社》中那句掷地有声的箴言：“抓紧时间，让你的生命变得与众不同。”愿每一个踏入这里的旅人，都能在精密交错的代码逻辑与物证推演中，雕琢属于自己的非凡诗篇。',
    aboutEn: 'As immortalized in Dead Poets Society: "Carpe diem. Seize the day, make your lives extraordinary." May every creator passing through carve out their own unforgettable verse in the digital ether.',
  },
  {
    id: 'matrix',
    badge: 'THE MATRIX // MOTTO',
    movieTitleZh: '黑客帝国',
    movieTitleEn: 'The Matrix',
    quoteZh: '“知道道路与走过道路，是完全不同的两件事。”',
    quoteEn: '“There is a difference between knowing the path and walking the path.”',
    aboutZh: '正如《黑客帝国》中墨菲斯的叩问：“知道道路与走过道路，是两码事。”愿每一个踏入这里的旅人，不仅能读懂线索与构想，更能亲历从底层算法推演至独立作品落成的真实旅程。',
    aboutEn: 'As Morpheus reminds us in The Matrix: "There is a difference between knowing the path and walking the path." May every creator here not merely contemplate the clues, but boldly tread the ground of creation.',
  },
  {
    id: 'forrestgump',
    badge: 'FORREST GUMP // MOTTO',
    movieTitleZh: '阿甘正传',
    movieTitleEn: 'Forrest Gump',
    quoteZh: '“生活就像一盒巧克力，你永远不知道下一块会是什么味道。”',
    quoteEn: '“Life was like a box of chocolates. You never know what you\'re gonna get.”',
    aboutZh: '正如《阿甘正传》中那句经典的独白：“生活就像一盒巧克力，你永远不知道下一块是什么。”愿每一个踏入这里的旅人，都能在充满反转的案卷推理与数字交互中，邂逅意想不到的惊喜。',
    aboutEn: 'As Forrest Gump famously reflects: "Life is like a box of chocolates, you never know what you\'re gonna get." May every detective stepping in find an unexpected revelation hidden behind the next riddle.',
  },
  {
    id: 'spiritedaway',
    badge: 'SPIRITED AWAY // MOTTO',
    movieTitleZh: '千与千寻',
    movieTitleEn: 'Spirited Away',
    quoteZh: '“曾经发生过的事情不可能忘记，只不过是想不起罢了。”',
    quoteEn: '“Once you\'ve met someone, you never really forget them. It just takes a while for your memories to return.”',
    aboutZh: '正如《千与千寻》中钱婆婆的低语：“发生过的事不可能忘记，只是想不起来罢了。”愿每一个踏入这里的旅人，都能在精密咬合的剧情记忆与证物链条里，唤醒那些被遗忘的真相与温柔。',
    aboutEn: 'As whispered in Spirited Away: "Once you meet someone, you never really forget them." May every traveler exploring these evidence archives find the echoes of deep memories waiting to be rediscovered.',
  },
  {
    id: 'threebody',
    badge: 'THREE BODY // MOTTO',
    movieTitleZh: '三体',
    movieTitleEn: 'The Three-Body Problem',
    quoteZh: '“给岁月以文明，而不是给文明以岁月。”',
    quoteEn: '“Make time for civilization, rather than civilization for time.”',
    aboutZh: '正如《三体》中沉静而宏大的宣告：“给岁月以文明，而不是给文明以岁月。”愿每一个踏入这里的旅人，都能在有限的时间跨度里，用纯粹的极客热忱，留下有厚度、有回响的作品。',
    aboutEn: 'As declared in The Three-Body Problem: "Make time for civilization, rather than civilization for time." May every artisan stepping in pour their boundless soul into works that truly stand the test of time.',
  },
  {
    id: 'inception',
    badge: 'INCEPTION // MOTTO',
    movieTitleZh: '盗梦空间',
    movieTitleEn: 'Inception',
    quoteZh: '“一个意念就像病毒，具有极强的传染性和顽强的生命力。”',
    quoteEn: '“An idea is like a virus. Resilient, highly contagious. The smallest seed of an idea can grow.”',
    aboutZh: '正如《盗梦空间》中对潜意识的解剖：“最微小的一个意念，也能生根发芽、重塑现实。”愿每一个踏入这里的旅人，都能在此种下一枚关于剧情、美学或独立架构的灵感种子。',
    aboutEn: 'As Cobb reminds us in Inception: "The smallest seed of an idea can grow to define or destroy your world." May every mind wandering into this lab plant a spark of imagination that flourishes into reality.',
  },
  {
    id: 'lifeofpi',
    badge: 'LIFE OF PI // MOTTO',
    movieTitleZh: '少年派的奇幻漂流',
    movieTitleEn: 'Life of Pi',
    quoteZh: '“人生就是不断地放下，但最遗憾的是，我们来不及好好道别。”',
    quoteEn: '“I suppose, in the end, the whole of life becomes an act of letting go.”',
    aboutZh: '正如《少年派的奇幻漂流》中对航程的追忆：“人生是一场向前的远航，唯有信念能穿越风暴。”愿每一个踏入这里的旅人，在探寻复杂人性案卷与数字浪潮时，始终守护内心的灯塔。',
    aboutEn: 'As recounted in Life of Pi: "Belief is a house of a thousand rooms." May every traveler sailing through these digital waters keep their inner compass steady against the storm.',
  },
  {
    id: 'bladerunner',
    badge: 'BLADE RUNNER // MOTTO',
    movieTitleZh: '银翼杀手 2049',
    movieTitleEn: 'Blade Runner 2049',
    quoteZh: '“所有的记忆终将消逝在时光中，如同泪水消失在雨中。”',
    quoteEn: '“All those moments will be lost in time, like tears in rain.”',
    aboutZh: '正如《银翼杀手》中在霓虹雨夜下的凝视：“在人造的精密代码与真实的人性之间，灵魂自有其重量。”愿每一个踏入这里的旅人，都能在数字洪流中感受纯粹手工编织的情感震颤。',
    aboutEn: 'As contemplated in Blade Runner: "More human than human." May every guest stepping into this studio perceive the fragile, exquisite warmth woven deep within mechanical logic.',
  },
  {
    id: 'goodwill',
    badge: 'GOOD WILL // MOTTO',
    movieTitleZh: '心灵捕手',
    movieTitleEn: 'Good Will Hunting',
    quoteZh: '“你不完美，但问题是你们是否对彼此而言足够完美。”',
    quoteEn: '“You\'re not perfect, sport. The question is whether or not you\'re perfect for each other.”',
    aboutZh: '正如《心灵捕手》中在湖畔的长谈：“真正的智慧不在于背诵百科全书，而在于勇敢地感受真实的生活。”愿每一个踏入这里的旅人，都能卸下防备，在纯粹的思考与创作中找到同频者。',
    aboutEn: 'As Sean gently reminds Will: "You\'ll have bad times, but it\'ll always wake you up to the good stuff." May every creator finding their way here embrace life\'s raw texture beyond cold computation.',
  },
  {
    id: 'coco',
    badge: 'COCO // MOTTO',
    movieTitleZh: '寻梦环游记',
    movieTitleEn: 'Coco',
    quoteZh: '“真正的死亡是世界上再没有一个人记得你。”',
    quoteEn: '“The real death is that no one in the world remembers you.”',
    aboutZh: '正如《寻梦环游记》中对记忆的温情诠释：“唯有被遗忘才是真正的终点。”愿每一个踏入这里的旅人，都能在工坊留存的故事、案卷与工具中，感知那些跨越时空的共鸣与温度。',
    aboutEn: 'As tenderly told in Coco: "Remember me though I have to say goodbye." May every explorer within these chambers encounter stories crafted with love, built to echo long in memory.',
  },
  {
    id: 'scent',
    badge: 'SCENT OF A WOMAN // MOTTO',
    movieTitleZh: '闻香识女人',
    movieTitleEn: 'Scent of a Woman',
    quoteZh: '“跳探戈没有犯错这一说，只要步子乱了，跳下去就行了。”',
    quoteEn: '“No mistakes in the tango, darling. If you get all tangled up, just tango on.”',
    aboutZh: '正如《闻香识女人》中那段经典的舞步哲学：“跳探戈没有走错这一说，即便步子乱了，继续跳下去就是。”愿每一个踏入这里的旅人，面对未知的 Bug 或错综的剧情时，都能从容起舞、继续向前。',
    aboutEn: 'As Lieutenant Colonel Slade declares: "If you get all tangled up, just tango on." May every artisan encountering complexity dance fearlessly through life and code.',
  },
];

/**
 * 获取今日适配信 (基于公历一年的天数哈希，全自动每日 00:00 准时轮换)
 * 支持传入 offset 用于用户手动点击骰子随机切换体验
 */
export function getDailyMotto(offset: number = 0): DailyMotto {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now.getTime() - start.getTime();
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay);
  
  const index = Math.abs(dayOfYear + offset) % dailyMottos.length;
  return dailyMottos[index];
}
