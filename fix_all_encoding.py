#!/usr/bin/env python3
"""Fix encoding corruption in games/ HTML files.
The corruption pattern: certain Chinese characters + following char were replaced by U+FFFD + '?' or just U+FFFD.
We fix by replacing known corrupted patterns with their correct text.
"""
import os

d = r'd:\node\games'

def fix_file(fname, replacements):
    """Apply a list of (corrupted, fixed) string replacements to a file."""
    path = os.path.join(d, fname)
    content = open(path, 'r', encoding='utf-8').read()
    orig_count = content.count('\ufffd')
    for old, new in replacements:
        content = content.replace(old, new)
    new_count = content.count('\ufffd')
    open(path, 'w', encoding='utf-8').write(content)
    print(f'{fname}: {orig_count} -> {new_count} corrupted chars remaining')

# ============================================================
# 2048.html (4 corrupted)
# ============================================================
fix_file('2048.html', [
    ('最\ufffd?/div>', '最佳</div>'),
    ('方向\ufffd?/b> \ufffd?<b>滑动', '方向键</b> 或<b>滑动'),
    ('新游\ufffd?/button>', '新游戏</button>'),
])

# ============================================================
# reaction.html (18 corrupted)
# ============================================================
fix_file('reaction.html', [
    ('">\ufffd?返回游戏列表', '">← 返回游戏列表'),
    ('<h1>\ufffd?反应速度', '<h1>⚡ 反应速度'),
    ('反应时\ufffd?/p>', '反应时间</p>'),
    ('最\ufffd?ms</div>', '最佳ms</div>'),
    ('变\ufffd?strong', '变成<strong'),
    ('5 轮测试\ufffd?/p>', '5 轮测试。</p>'),
    ('开始测\ufffd?/button>', '开始测试</button>'),
    ('等待\ufffd?..', '等待中...'),
    ('后点\ufffd?/div>', '后点击</div>'),
    ('再来一\ufffd?/button>', '再来一次</button>'),
    ('后立刻点\ufffd?;', '后立刻点击\';'),
    ('`最\ufffd?${best}ms', '`最快${best}ms'),
    ('· 最\ufffd?${worst}ms', '· 最慢${worst}ms'),
    ('· \ufffd?${TOTAL_ROU', '· 共${TOTAL_ROU'),
    ("rating = '\ufffd?非常敏捷\ufffd?;", "rating = '⚡ 非常敏捷！';"),
    ("= '\ufffd?非常敏捷", "= '⚡ 非常敏捷"),
    ('继续练\ufffd?;', '继续练习！\';'),
    ('多加练\ufffd?;', '多加练习！\';'),
])

# ============================================================
# memory-cards.html (10 corrupted)
# ============================================================
fix_file('memory-cards.html', [
    ('">\ufffd?返回游戏列表', '">← 返回游戏列表'),
    ('简\ufffd?4×3</button', '简单4×3</button'),
    ('开\ufffd?/button>', '开始</button>'),
    ('全部配对\ufffd?/h2>', '全部配对！</h2>'),
    ("','\ufffd?,'🥑','🧁','🍩'", "','🍒','🥑','🧁','🍩'"),
    ("= '进行\ufffd?..';", "= '进行中...';"),
    ("= '开\ufffd?;", "= '开始';"),
    ("'?\ufffd?.repeat(sta", "'⭐'.repeat(sta"),
    ("arCount) + '\ufffd?.repeat(3 -", "arCount) + '☆'.repeat(3 -"),
])

# ============================================================
# number-memory.html (16 corrupted)
# ============================================================
fix_file('number-memory.html', [
    ('">\ufffd?返回游戏列表', '">← 返回游戏列表'),
    ('最高位\ufffd?/div>', '最高位数</div>'),
    ('启动训\ufffd?/div>', '启动训练</div>'),
    ('开\ufffd?/button>', '开始</button>'),
    ("= '进行\ufffd?..';", "= '进行中...';"),
    ('">\ufffd?/div>', '">←</div>'),
    ("? '\ufffd?完全正确\ufffd? : '\ufffd", "? '✅ 完全正确！' : '❌"),
    ("? : '\ufffd?记忆有误'", "? : '❌ 记忆有误'"),
    ("'下一\ufffd? : '查看结果", "'下一步' : '查看结果"),
    ('最高记忆位\ufffd? <span', '最高记忆位数 <span'),
    ('到达\ufffd?${currentLe', '到达第${currentLe'),
    ('} \ufffd?/div>', '} 关</div>'),
    ("= '重新开\ufffd?;", "= '重新开始';"),
    ("启动训\ufffd?/div>';", "启动训练</div>';"),
    ("= '开\ufffd?;", "= '开始';"),
])

# ============================================================
# path-memory.html (17 corrupted)
# ============================================================
fix_file('path-memory.html', [
    ('">\ufffd?返回游戏列表', '">← 返回游戏列表'),
    ('🗺\ufffd?路径记忆', '🗺️ 路径记忆'),
    ('最高关\ufffd?/div>', '最高关卡</div>'),
    ('点击开\ufffd?/div>', '点击开始</div>'),
    ('亮起\ufffd?br>', '亮起。<br>'),
    ('点击格子\ufffd?/p>', '点击格子。</p>'),
    ('开始游\ufffd?/button>', '开始游戏</button>'),
    ('1<span>\ufffd?/span>', '1<span>关</span>'),
    ('再来一\ufffd?/button>', '再来一次</button>'),
    ("'按顺序点击路\ufffd?;", "'按顺序点击路径';"),
    ("'完美！进入下一\ufffd?..';", "'完美！进入下一关...';"),
    ("= '\ufffd?;", "= '开始';"),
    ("'路径错误\ufffd?;", "'路径错误！';"),
    ('历史最高：\ufffd?${bestLevel', '历史最高：第${bestLevel'),
    ("'<span>\ufffd?/span>'", "'<span>关</span>'"),
    ('到达\ufffd?${reached}', '到达第${reached}'),
    ('} \ufffd?· 路径', '} 关 · 路径'),
])

# ============================================================
# pomodoro.html (9 corrupted)
# ============================================================
fix_file('pomodoro.html', [
    ('短休\ufffd?/button>', '短休息</button>'),
    ('长休\ufffd?/button>', '长休息</button>'),
    ('开\ufffd?/button>', '开始</button>'),
    ('已完\ufffd?/div>', '已完成</div>'),
    ("'短休\ufffd?',", "'短休息',"),
    ("'长休\ufffd?',", "'长休息',"),
    ("= '开\ufffd?;", "= '开始';"),
    ("'?\ufffd?休息结束", "'🔔 休息结束"),
])

# ============================================================
# quick-math.html (13 corrupted)
# ============================================================
fix_file('quick-math.html', [
    ('">\ufffd?返回游戏列表', '">← 返回游戏列表'),
    ('<h1>\ufffd?速算挑战', '<h1>⚡ 速算挑战'),
    ('剩余\ufffd?/div>', '剩余题数</div>'),
    ('题目\ufffd?br>', '题目。<br>'),
    ('简\ufffd?/button>', '简单</button>'),
    ('开始挑\ufffd?/button>', '开始挑战</button>'),
    ('0<span>\ufffd?/span>', '0<span>题</span>'),
    ('再来一\ufffd?/button>', '再来一次</button>'),
    ('`?\ufffd?答案', '`💡 答案'),
    ("'<span>\ufffd?/span>'", "'<span>题</span>'"),
    ('正确\ufffd?${accuracy}', '正确率${accuracy}'),
    ('最长连\ufffd?${bestCombo', '最长连击${bestCombo}'),
    ("'简\ufffd? : difficul", "'简单' : difficul"),
])

# ============================================================
# sequence-memory.html (20 corrupted)
# ============================================================
fix_file('sequence-memory.html', [
    ('">\ufffd?返回游戏列表', '">← 返回游戏列表'),
    ('最\ufffd?/div></div>', '最高</div></div>'),
    ('启动训\ufffd?/div>', '启动训练</div>'),
    ('开\ufffd?/button>', '开始</button>'),
    ('记忆中断\ufffd?/h2>', '记忆中断！</h2>'),
    ('0<span>\ufffd?/span>', '0<span>关</span>'),
    ('再来一\ufffd?/button>', '再来一次</button>'),
    ("= '进行\ufffd?..';", "= '进行中...';"),
    ("'你的回合！重复序\ufffd?;", "'你的回合！重复序列';"),
    ("= '\ufffd?正确！准备下一\ufffd?..';", "= '✅ 正确！准备下一关...';"),
    ("= '\ufffd?序列错误\ufffd?;", "= '❌ 序列错误！';"),
    ("= '开\ufffd?;", "= '开始';"),
    ("'<span>\ufffd?/span>'", "'<span>关</span>'"),
    ('本局到达\ufffd?${currentLe', '本局到达第${currentLe'),
    ('关，记忆\ufffd?${(currentL', '关，记忆了${(currentL'),
    ('历史最\ufffd? ${best}', '历史最高 ${best}'),
    ("'点击「开始」启动训\ufffd?;", "'点击「开始」启动训练';"),
])

# ============================================================
# stroop.html (14 corrupted)
# ============================================================
fix_file('stroop.html', [
    ('">\ufffd?返回游戏列表', '">← 返回游戏列表'),
    ('剩余\ufffd?/div>', '剩余题数</div>'),
    ('不同\ufffd?br>', '不同。<br>'),
    ('文字\ufffd?strong', '文字的<strong'),
    ('">\ufffd?/span>', '">←</span>'),
    ('红色 \ufffd?/span>', '红色 ←</span>'),
    ('文字\ufffd?蓝色', '文字"蓝色"'),
    ('开始测\ufffd?/button>', '开始测试</button>'),
    ('显示颜\ufffd?/div>', '显示颜色</div>'),
    ('0<span>\ufffd?/span>', '0<span>题</span>'),
    ('再来一\ufffd?/button>', '再来一次</button>'),
    ("'<span>\ufffd?/span>'", "'<span>题</span>'"),
    ('正确\ufffd?${accuracy}', '正确率${accuracy}'),
    ('最长连\ufffd?${bestStrea', '最长连击${bestStrea'),
])

# ============================================================
# word-memory.html (17 corrupted)
# ============================================================
fix_file('word-memory.html', [
    ('">\ufffd?返回游戏列表', '">← 返回游戏列表'),
    ('正确的\ufffd?/p>', '正确的。</p>'),
    ('词语\ufffd?/div>', '词语数</div>'),
    ('最高关\ufffd?/div>', '最高关卡</div>'),
    ('点击开\ufffd?/div>', '点击开始</div>'),
    ('选项\ufffd?br>', '选项。<br>'),
    ('递增\ufffd?/p>', '递增。</p>'),
    ('开始游\ufffd?/button>', '开始游戏</button>'),
    ('1<span>\ufffd?/span>', '1<span>关</span>'),
    ('再来一\ufffd?/button>', '再来一次</button>'),
    ('选出刚才\ufffd?${correctCo', '选出刚才记忆的${correctCo'),
    ("'完美！进入下一\ufffd?..';", "'完美！进入下一关...';"),
    ('错\ufffd?${wrong}', '错选${wrong}'),
    ('历史最高：\ufffd?${bestLevel', '历史最高：第${bestLevel'),
    ("'<span>\ufffd?/span>'", "'<span>关</span>'"),
    ('到达\ufffd?${reached}', '到达第${reached}'),
    ('} \ufffd?· 记忆', '} 关 · 记忆'),
])

print('\nAll files processed!')