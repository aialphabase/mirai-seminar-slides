# -*- coding: utf-8 -*-
"""
第6回（2026-10-01）なぜ米国のニュースで、世界の相場が動くのか？
使い方: python3 source06/build.py  →  sessions/06/index.html

作りは第4回・第5回と同じ（1440×810・章ナビ・1.25秒フェード・右矢印だけで進む）。
先に SPEC（場面ごとの振り分け表）を決め、部品に流し込む。数字は第27回ミライニュース台本にあるものだけ。
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / 'sessions' / '06' / 'index.html'
NAV = ['はじめに', '1 なぜ米国', '2 金利と為替', '3 日本株', '4 ビットコイン', '5 読み方']

# ───────── 部品 ─────────
slides = []
def add(ch, content, cls=''):
    slides.append(f'<section class="slide {cls}" data-ch="{ch}">{content}</section>')

def head(n, title, sub=''):
    return (f'<div class="eyebrow">{n}</div><h2>{title}</h2>' +
            (f'<p class="lead">{sub}</p>' if sub else ''))

def st(n, html, cls='', tag='div'):
    return f'<{tag} class="st {cls}" data-step="{n}">{html}</{tag}>'

def question(ch, q, a, art, op=.5):
    add(ch, f'<div class="answer-art" style="background-image:url(\'{art}\');--art-opacity:{op}" aria-hidden="true"></div>'
            '<div class="answer-shade" aria-hidden="true"></div>'
            f'<div class="question"><span class="tag">考えてみてください</span><h2>{q}</h2>'
            f'<div class="cover-wrap"><div class="answer">{a}</div>'
            '<button class="cover" type="button">クリックで開く</button></div></div>', 'think')

def scene(ch, art, copy, extra=''):
    add(ch, f'<div class="scene-art" style="background-image:url(\'{art}\')"></div>{extra}'
            f'<div class="hero-copy">{copy}</div>', 'scene')

CUR = ('<svg class="currents" viewBox="0 0 1440 810" aria-hidden="true">'
       '<path d="M550 820C700 650 820 660 920 515S1100 420 1480 390"/>'
       '<path d="M520 840C760 670 780 590 950 590S1120 650 1480 535"/>'
       '<path d="M680 850C820 710 990 755 1100 540S1280 330 1500 270"/></svg>')
A = 'assets/rate05/'

# ───────── 0 はじめに ─────────
add(0, f'<div class="city"></div>{CUR}<div class="title-copy"><div class="eyebrow">ニュースと経済がわかるシリーズ ｜ 特別編</div>'
       '<h1>なぜ米国のニュースで、<br>世界の相場が動くのか？</h1>'
       '<p class="subtitle">金利・為替・日本株・ビットコインをつなぐ</p><div class="rule"></div>'
       '<p class="catch">ニュースは、別々に届く。<br><em>お金は、つながって動く。</em></p></div>', 'title')

add(0, head('これまでの5回', '5つの視点を、<br>今日は1本の線にする。') +
    '<div class="x-five">' + ''.join(
        st(i + 1, f'<small>第{i+1}回</small><b>{t}</b><span>{d}</span>', 'x-chip')
        for i, (t, d) in enumerate([('経済', 'お金の流れ'), ('株価', '期待の値段'), ('物価', 'お金の価値'),
                                    ('バブル', '期待の行き過ぎ'), ('金利', 'お金のレンタル料')])) +
    '</div>' + st(6, '別々に学んだ5つは、同じニュースの中で<b>同時に</b>動いている。', 'x-note'), 'steps')

add(0, head('今日の入口', '日本とアメリカが、<br>2日続けて金利を上げた。') +
    '<div class="x-rates">' +
    st(1, '<small>アメリカ FRB ／ 9月17日</small><b>3.75〜4.00%</b><ul><li>3年2カ月ぶりの利上げ</li><li>投票は12対0の全会一致</li></ul>', 'x-rate', 'article') +
    st(2, '<small>日本 日銀 ／ 9月18日</small><b>1.25%</b><ul><li>1995年以来、31年ぶりの水準</li><li>投票は7対2</li></ul>', 'x-rate', 'article') +
    '</div>', 'steps')

add(0, head('今日の見方', 'ニュースを、<br>二つの問いで聞く。') +
    '<div class="two-q">' +
    st(1, '<small>問い 1</small><h3>なぜ米国の金利で、<br>世界の相場が動くのか</h3>', 'x-q') +
    st(2, '<small>問い 2</small><h3>日本も金利を上げたのに、<br>なぜ円安になったのか</h3>', 'x-q') +
    '</div>', 'steps')

# ───────── 1 なぜ米国 ─────────
add(1, head('01｜なぜ米国なのか', '世界のお金は、<br>ドルで測られている。',
            '貿易も、原油も、借金も。多くの値段がドルで決まる。'), 'chapter')

HUB = [('為替', 'ドル円', 330, 230), ('日本株', '日経平均', 1110, 230),
       ('ビットコイン', 'ドル建ての資産', 330, 600), ('原油・金', 'ドル建ての値段', 1110, 600)]
hub = '<svg class="x-hub" viewBox="0 0 1440 810" aria-hidden="true">'
for i, (_, _, x, y) in enumerate(HUB, 1):
    hub += f'<path class="st x-wire" data-step="{i}" pathLength="1" d="M720 415 Q{(720+x)/2:.0f} {y} {x} {y}"/>'
hub += '<circle class="x-core-ring" cx="720" cy="415" r="118"/><circle class="x-core" cx="720" cy="415" r="92"/></svg>'
hub += '<div class="x-core-txt"><small>米国の金利</small><b>ドル</b></div>'
for i, (t, d, x, y) in enumerate(HUB, 1):
    hub += st(i, f'<b>{t}</b><span>{d}</span>', 'x-node', 'div').replace('class="st x-node"', f'class="st x-node" style="left:{x}px;top:{y}px"')
add(1, '<div class="eyebrow x-top">01-1｜つながりの地図</div>' + hub +
    st(5, 'ドルの金利が動くと、ドルで測っている<b>すべての値段</b>が測り直される。', 'x-note x-bottom'), 'steps hubpage')

question(1, '米国の金利が上がると、<br>世界のお金はどこへ向かう？',
         '金利の高いドルへ、戻ろうとする。<br>他の通貨や資産からは、お金が抜けやすくなる。', A + 'expectation-scene-v1.png', .55)
scene(1, A + 'interest-city-v1.png', '金利は、<br><em>お金の引力。</em>', CUR)

# ───────── 2 金利と為替 ─────────
def gap(step, y, jp, us, cap):
    W = 1000
    return st(step,
              f'<div class="x-gap-cap">{cap}</div>'
              f'<div class="x-gap-row"><span>日本</span><div class="x-track"><i style="--w:{jp/4*100:.1f}%"></i><em>{jp:.2f}%</em></div></div>'
              f'<div class="x-gap-row us"><span>アメリカ</span><div class="x-track"><i style="--w:{us/4*100:.1f}%"></i><em>{us:.2f}%</em></div></div>',
              'x-gap')
add(2, head('02｜金利と為替', '為替は、金利の「差」を見ている。') +
    '<div class="x-gaps">' + gap(1, 0, 1.00, 3.75, '利上げの前') + gap(2, 0, 1.25, 4.00, '利上げの後') + '</div>' +
    st(3, '<span>日米の金利差</span><b>2.75% → 2.75%</b><em>両方が同じだけ上げたので、差は変わっていない。</em>', 'x-diff'), 'steps')

question(2, '日銀が金利を上げた日、<br>円は買われた？',
         '売られた。ドル円は1.2円の円安、157円台へ。<br>日本が上げても、アメリカとの差は2.75%のまま残っていた。', A + 'bond-harbor-v1.jpg', .6)
scene(2, A + 'bond-harbor-v1.jpg', '上げたか、ではない。<br><em>差が、縮んだか。</em>')

# ───────── 3 日本株 ─────────
add(3, head('03｜為替と日本株', '円安は、日本株にどう届くか。') +
    '<div class="x-flow">' +
    st(1, '<small>9月18日</small><b>円安</b><span>ドル円 +1.2円</span>', 'x-box') + st(2, '→', 'x-arrow') +
    st(2, '<small>企業</small><b>海外の売上</b><span>円に直すと増えやすい</span>', 'x-box') + st(3, '→', 'x-arrow') +
    st(3, '<small>株価</small><b>日経平均</b><span>+1,114円</span>', 'x-box gold') +
    '</div>' + st(4, '円安は輸入する物の値段も上げる。<b>得をする会社と、負担が増える会社</b>がある。', 'x-note'), 'steps')

add(3, head('03-1｜教科書どおりにならなかった2日', '動いたもの、動かなかったもの。') +
    '<div class="x-cmp">' +
    st(1, '<div class="day">9/17　FRBが上げた日</div>'
          '<div class="row down"><span>NYダウ</span><b>−631</b></div>'
          '<div class="row mark"><span>米10年債の金利</span><b>+0.01pt</b></div>', 'x-blk') +
    st(2, '<div class="day">9/18　日銀が上げた日</div>'
          '<div class="row up"><span>ドル円</span><b>+1.2円の円安</b></div>'
          '<div class="row up"><span>日経平均</span><b>+1,114</b></div>', 'x-blk') +
    '</div>', 'steps')

question(3, '金利を決める会議の日、<br>金利はどれだけ動いた？',
         '0.01ポイント。ほとんど動いていない。<br>市場は、発表の前に動き終えていた。これが「織り込み済み」。', A + 'interest-city-v1.png', .45)

# ───────── 4 ビットコイン ─────────
Wc, Hc, L, R, T, B = 880, 440, 100, 840, 70, 350
lo, hi = 73900, 83300
Y = lambda v: round(B - (v - lo) / (hi - lo) * (B - T), 1)
X = lambda i: round(L + i * (R - L) / 3, 1)
chart = (f'<div class="x-chart"><svg viewBox="0 0 {Wc} {Hc}" aria-hidden="true">'
         f'<line class="ax" x1="50" y1="{B+8}" x2="{R+20}" y2="{B+8}"/>'
         f'<line class="ev" x1="{X(1)}" y1="{T-24}" x2="{X(1)}" y2="{B}"/>'
         f'<line class="ref" x1="50" y1="{Y(75500)}" x2="{R+20}" y2="{Y(75500)}"/>'
         f'<path class="st ln" data-step="1" pathLength="1" d="M{X(0)},{Y(75612)} C{X(0)+160},{Y(75612)-4} {X(3)-200},{Y(81702)+90} {X(3)},{Y(81702)}"/>'
         f'<g class="st" data-step="2"><circle cx="{X(0)}" cy="{Y(75612)}" r="8"/><circle cx="{X(3)}" cy="{Y(81702)}" r="8"/></g></svg>' +
         ''.join(f'<div class="lb tick" style="left:{X(i)}px;top:{B+40}px">{d}</div>' for i, d in enumerate(['9/15', '9/16', '9/17', '9/18'])) +
         f'<div class="lb ev" style="left:{X(1)}px;top:{T-56}px">FRB 0.25%利上げ</div>'
         f'<div class="lb ref r" style="left:{R}px;top:{Y(75500)+16}px">記事が挙げた下限 75,500</div>' +
         st(2, '安値 75,612', 'lb big').replace('class="st lb big"', f'class="st lb big" style="left:{X(0)+18}px;top:{Y(75612)-112}px"') +
         st(2, '81,702', 'lb big r').replace('class="st lb big r"', f'class="st lb big r" style="left:{X(3)-16}px;top:{Y(81702)-84}px"') +
         '</div>')
side = ('<div class="x-side">' +
        st(3, '<small>売っていた人の買い戻し</small><b>1億9,200万ドル</b><p>強制清算。うち売り方 1億8,300万</p>') +
        st(4, '<small>現物ETFへの資金流入</small><b>1億5,900万ドル</b><p>金利ではなく、資金の流れが動かした</p>') + '</div>')
add(4, head('04｜ビットコイン', '利上げの週に、ビットコインは上がった。') +
    f'<div class="x-chartwrap">{chart}{side}</div>', 'steps')

add(4, head('04-1｜値段を動かす3つの力', '金利だけでは、決まらない。') +
    '<div class="cards">' +
    st(1, '<small>01</small><h3>金利</h3><p>ドルの金利が上がると、金利のつかない資産からお金が離れやすい。</p>', '', 'article') +
    st(2, '<small>02</small><h3>資金の流れ</h3><p>現物ETFへお金が入ると、買う力がそのまま値段に出る。</p>', '', 'article') +
    st(3, '<small>03</small><h3>売り買いの偏り</h3><p>売りに偏りすぎると、買い戻しが一気に起きて跳ねる。</p>', '', 'article') +
    '</div>', 'steps')

scene(4, A + 'expectation-scene-v1.png', '理由は、ひとつではない。<br><em>力の合計で、値段は動く。</em>')

# ───────── 5 読み方 ─────────
add(5, head('05｜明日からのニュース', 'まず、この3つの数字を見る。') +
    '<div class="x-three">' +
    st(1, '<small>01</small><h3>米10年債の金利</h3><b>5.00%</b><p>世界のお金の「基準」</p>', '', 'article') +
    st(2, '<small>02</small><h3>ドル円と金利差</h3><b>2.75%</b><p>差が縮むか、広がるか</p>', '', 'article') +
    st(3, '<small>03</small><h3>原油</h3><b>100ドル</b><p>物価と、次の金利を左右する</p>', '', 'article') +
    '</div>', 'steps')

CH = [('米国の金利', '基準が動く'), ('ドル', '引力が変わる'), ('円', '差で動く'), ('日本株', '円安が届く'), ('ビットコイン', '資金の流れで動く')]
chain = '<div class="x-chain">' + ''.join(
    st(i + 1, f'<b>{t}</b><span>{d}</span>', 'x-link') + (st(i + 2, '', 'x-join') if i < len(CH) - 1 else '')
    for i, (t, d) in enumerate(CH)) + '</div>'
add(5, head('総まとめ', 'ニュースを、1本の線で読む。') + chain +
    st(6, '特定の商品や売買時期のご案内ではありません。仕組みを知って、自分で読めるようになるための整理です。', 'x-fine'), 'steps')

add(5, head('二つの問いの答え', '今日、持ち帰ること。') +
    '<div class="two-q">' +
    st(1, '<small>問い 1　なぜ米国の金利で世界が動くのか</small><h3>世界の値段が、<br>ドルで測られているから。</h3>', 'x-q') +
    st(2, '<small>問い 2　なぜ利上げしたのに円安なのか</small><h3>為替は「差」で動き、<br>差が縮まらなかったから。</h3>', 'x-q') +
    '</div>', 'steps')

add(5, head('次の一歩', '学んだ見方を、<br>使いながら身につける。',
            'ミライテラシー2.0 先行体験のご案内') +
    '<div class="cards">' +
    st(1, '<small>見る</small><h3>毎週のニュース</h3><p>今日の3つの数字を、同じ順番で追う。</p>', '', 'article') +
    st(2, '<small>考える</small><h3>自分の見立て</h3><p>次に何が起きるかを、先に言葉にする。</p>', '', 'article') +
    st(3, '<small>確かめる</small><h3>答え合わせ</h3><p>翌週の数字で、見立てを確かめる。</p>', '', 'article') +
    '</div>', 'steps')

add(5, '<div class="city finale"></div><svg class="currents finale" viewBox="0 0 1440 810" aria-hidden="true">'
       '<path d="M1095 840C1120 640 1180 420 1268 246"/><path d="M1105 840C1135 660 1195 440 1270 248"/>'
       '<path class="teal" d="M690 322C850 430 1000 560 1120 840"/><path d="M1440 600C1370 470 1315 340 1270 246"/></svg>'
       '<div class="dawn-glow"></div><div class="hero-copy final"><small>明日、ニュースを開いたら</small>'
       'ニュースは、別々に届く。<br><em>お金は、つながって動く。</em></div>', 'scene ending')

# ───────── 見た目（第5回のCSS＋今回の部品）─────────
base = (HERE / 'base.css').read_text(encoding='utf-8')
extra = r'''
.question{width:1200px;position:relative;z-index:2}.question .tag{display:inline-block;font:700 30px 'Hiragino Sans',sans-serif;background:#eac77e;color:#211c11;border-radius:8px;padding:12px 30px;margin-bottom:26px}.question h2{font-size:46px;line-height:1.5;margin-bottom:34px}
.cover-wrap{position:relative;border-radius:16px;overflow:hidden;border:1px solid #455269}.answer{min-height:170px;padding:30px 40px;display:flex;align-items:center;justify-content:center;font-size:29px;line-height:1.7;background:#1a2438;transition:background 1s}
.cover{position:absolute;inset:0;border:0;font-size:26px;letter-spacing:.14em;color:#8bbdb9;background:linear-gradient(160deg,#233150,#16203a);cursor:pointer;transition:transform .5s cubic-bezier(.7,-0.2,.3,1.1),opacity .4s ease}.cover:before{content:'▼';margin-right:12px;color:#eac77e}
.revealed .cover{transform:translateY(101%);opacity:0;pointer-events:none}.answer-art{position:absolute;inset:0;background:center/cover no-repeat;opacity:0;transform:scale(1.055);transition:opacity 1.5s ease,transform 2.5s ease}.revealed .answer-art{opacity:var(--art-opacity,.5);transform:scale(1)}
.answer-shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,10,22,.68),rgba(5,10,22,.3));pointer-events:none}.revealed .answer{background:rgba(11,18,34,.78)}
.scene{padding:0}.scene-art{position:absolute;inset:0;background:#0b1220 center/cover no-repeat}.scene-art:after{content:'';position:absolute;inset:0;background:linear-gradient(0deg,rgba(3,8,18,.88),transparent 38%,rgba(3,8,18,.12) 82%,rgba(3,8,18,.6))}
.slide.on .hero-copy{animation:caption 2.2s ease both}@keyframes caption{from{opacity:0}30%{opacity:0}to{opacity:1}}
.title-copy h1{font-size:62px;line-height:1.35}
.answer{opacity:1}.slide.think .answer{visibility:visible}
.two-q{display:grid;grid-template-columns:1fr 1fr;gap:28px;width:1200px;margin-top:10px}
.hero-copy.final small{display:block;font:24px "Hiragino Sans",sans-serif;letter-spacing:.1em;color:#cbd4e2;margin-bottom:14px}
.scene .scene-art+.currents{z-index:1}.scene .hero-copy{z-index:2}
.st{opacity:0;transform:translateY(16px);transition:opacity .8s ease,transform .8s cubic-bezier(.2,.8,.3,1)}.st.in{opacity:1;transform:none}
.x-note{width:1180px;margin-top:34px;text-align:left;border-left:3px solid #8bbdb9;padding:14px 26px;font-size:27px;line-height:1.7;background:linear-gradient(90deg,#8bbdb920,transparent)}.x-note b{color:#eac77e}
.x-fine{font:17px/1.7 "Hiragino Sans",sans-serif;color:#8d9bb0;margin-top:34px}
.x-five{display:grid;grid-template-columns:repeat(5,1fr);gap:16px;width:1240px;margin-top:16px}.x-chip{background:#12203a;border:1px solid #33425c;border-top:2px solid #b89a5c;border-radius:14px;padding:22px 16px;text-align:center}
.x-chip small{display:block;font:15px "Hiragino Sans",sans-serif;letter-spacing:.14em;color:#8bbdb9}.x-chip b{display:block;font-size:34px;color:#eac77e;margin:8px 0 6px}.x-chip span{font:18px "Hiragino Sans",sans-serif;color:#cbd4e2}
.x-rates{display:grid;grid-template-columns:1fr 1fr;gap:34px;width:1180px;margin-top:12px}.x-rate{background:#12203a;border:1px solid #33425c;border-radius:16px;padding:30px 34px;text-align:center}
.x-rate small{font:17px "Hiragino Sans",sans-serif;letter-spacing:.1em;color:#8bbdb9}.x-rate b{display:block;font-size:60px;color:#eac77e;margin:10px 0 14px}.x-rate ul{margin:0;padding:0}.x-rate li{list-style:none;font:20px/1.8 "Hiragino Sans",sans-serif;color:#cfd8e6}
.x-q{background:#12203a;border:1px solid #33425c;border-radius:16px;padding:32px 34px;text-align:left}.x-q small{font:17px "Hiragino Sans",sans-serif;letter-spacing:.1em;color:#8bbdb9}.x-q h3{font-size:33px;line-height:1.55;margin-top:14px}
.hubpage{padding:0}.x-top{position:absolute;top:96px;left:0;right:0;text-align:center}.x-hub{position:absolute;inset:0;width:100%;height:100%}
.x-wire{fill:none;stroke:#eac77e;stroke-width:3;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;transform:none;opacity:1;transition:stroke-dashoffset 1.4s cubic-bezier(.4,.1,.3,1)}.x-wire.in{stroke-dashoffset:0}
.x-core{fill:#16243f;stroke:#eac77e;stroke-width:2}.x-core-ring{fill:none;stroke:#eac77e55;stroke-width:1;animation:ring 3.6s ease-in-out infinite}@keyframes ring{0%,100%{r:106;opacity:.7}50%{r:128;opacity:.15}}
.x-core-txt{position:absolute;left:720px;top:415px;transform:translate(-50%,-50%);text-align:center}.x-core-txt small{display:block;font:16px "Hiragino Sans",sans-serif;letter-spacing:.12em;color:#8bbdb9}.x-core-txt b{font-size:46px;color:#eac77e}
.x-node{position:absolute;width:250px;margin:-52px 0 0 -125px;background:#12203a;border:1px solid #3a4862;border-radius:14px;padding:16px 12px;text-align:center;transition-delay:.9s}.x-node.st{transform:scale(.92)}.x-node.st.in{transform:none}
.x-node b{display:block;font-size:30px}.x-node span{font:17px "Hiragino Sans",sans-serif;color:#9fb0c6}
.x-bottom{position:absolute;left:130px;right:130px;bottom:46px;width:auto;margin:0;font-size:25px}
.x-gaps{display:grid;grid-template-columns:1fr 1fr;gap:40px;width:1240px;margin-top:6px}.x-gap{background:#101b31;border:1px solid #2f3d55;border-radius:16px;padding:24px 28px}
.x-gap-cap{font:18px "Hiragino Sans",sans-serif;letter-spacing:.1em;color:#8bbdb9;margin-bottom:14px;text-align:left}.x-gap-row{display:grid;grid-template-columns:96px 1fr;align-items:center;gap:14px;margin:10px 0}.x-gap-row span{font:19px "Hiragino Sans",sans-serif;color:#cfd8e6;text-align:right}
.x-track{position:relative;height:52px;background:#0c1526;border:1px solid #2b3850;border-radius:9px}.x-track i{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:8px;background:linear-gradient(90deg,#3d5c7a,#6f92b5);transition:width 1.1s cubic-bezier(.25,.9,.3,1) .25s}
.us .x-track i{background:linear-gradient(90deg,#8a6f34,#eac77e)}.x-gap.in .x-track i{width:var(--w)}.x-track em{position:absolute;right:14px;top:0;line-height:52px;font-style:normal;font-size:25px;color:#f4f2e9}
.x-diff{width:1240px;margin-top:26px;display:flex;align-items:baseline;gap:26px;background:#12203a;border:1px solid #eac77e88;border-radius:14px;padding:20px 30px}.x-diff span{font:20px "Hiragino Sans",sans-serif;color:#9fb0c6}.x-diff b{font-size:40px;color:#eac77e}.x-diff em{font-style:normal;font-size:23px;color:#e7e3d6;margin-left:auto}
.x-flow{display:flex;align-items:center;justify-content:center;gap:18px;width:1240px;margin-top:16px}.x-box{width:330px;background:#12203a;border:1px solid #33425c;border-radius:16px;padding:26px 20px;text-align:center}.x-box.gold{border-color:#eac77e}
.x-box small{font:16px "Hiragino Sans",sans-serif;letter-spacing:.12em;color:#8bbdb9}.x-box b{display:block;font-size:38px;margin:8px 0 6px}.x-box.gold b{color:#eac77e}.x-box span{font:20px "Hiragino Sans",sans-serif;color:#cfd8e6}.x-arrow{font-size:40px;color:#eac77e}
.x-cmp{display:grid;grid-template-columns:1fr 1fr;gap:34px;width:1220px;margin-top:10px}.x-blk{background:#101b31;border:1px solid #2f3d55;border-radius:16px;padding:26px 30px;text-align:left}.x-blk .day{font:19px "Hiragino Sans",sans-serif;letter-spacing:.08em;color:#8bbdb9;margin-bottom:12px}
.x-blk .row{display:flex;align-items:baseline;justify-content:space-between;padding:14px 0;border-top:1px solid #253149}.x-blk .row span{font:21px "Hiragino Sans",sans-serif;color:#b8c4d5}.x-blk .row b{font-size:40px}.row.up b{color:#8bbdb9}.row.down b{color:#d98a8a}.row.mark{background:#eac77e14;border-radius:10px;padding:14px 16px;border-top:0}.row.mark b{color:#eac77e}
.x-chartwrap{display:grid;grid-template-columns:880px 340px;gap:40px;width:1260px;align-items:center;margin-top:-6px}.x-chart{position:relative;width:880px;height:440px}.x-chart svg{position:absolute;left:0;top:0;width:880px;height:440px;overflow:visible}
.x-chart .ax{stroke:#2b3850}.x-chart .ev{stroke:#44536e;stroke-dasharray:4 6}.x-chart .ref{stroke:#8bbdb9;stroke-width:2;stroke-dasharray:8 8}.x-chart circle{fill:#eac77e}.x-chart g.st{transform:none}
.x-chart .ln{fill:none;stroke:#eac77e;stroke-width:4;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;transform:none;opacity:1;transition:stroke-dashoffset 1.8s cubic-bezier(.4,.1,.3,1)}.x-chart .ln.in{stroke-dashoffset:0}
.lb{position:absolute;font-family:"Hiragino Sans",sans-serif;white-space:nowrap;line-height:1.3}.lb.big{font-size:31px;color:#f4f2e9}.lb.tick,.lb.ev{font-size:18px;color:#9fb0c6;transform:translateX(-50%)}.lb.ref{font-size:19px;color:#8bbdb9}.lb.r{transform:translateX(-100%)}.lb.r.st{transform:translateX(-100%) translateY(16px)}.lb.r.st.in{transform:translateX(-100%)}
.x-side{display:flex;flex-direction:column;gap:22px;text-align:left}.x-side>div{background:#12203a;border:1px solid #33425c;border-left:3px solid #8bbdb9;border-radius:12px;padding:22px 24px}.x-side small{font:16px "Hiragino Sans",sans-serif;letter-spacing:.06em;color:#9fb0c6}.x-side b{display:block;font-size:32px;color:#eac77e;margin:8px 0 6px}.x-side p{font:16px/1.6 "Hiragino Sans",sans-serif;color:#b8c4d5}
.x-three{display:grid;grid-template-columns:repeat(3,1fr);gap:30px;width:1220px;margin-top:12px}.x-three article{background:#12203a;border:1px solid #33425c;border-top:3px solid #8bbdb9;border-radius:16px;padding:32px 28px;text-align:center}
.x-three small{font:16px "Hiragino Sans",sans-serif;letter-spacing:.2em;color:#8bbdb9}.x-three h3{margin:12px 0 6px;font-size:27px;color:#cfd8e6}.x-three b{display:block;font-size:54px;color:#eac77e}.x-three p{margin-top:10px;font:19px "Hiragino Sans",sans-serif;color:#9fb0c6}
.x-chain{display:flex;align-items:center;justify-content:center;width:1300px;margin-top:40px}.x-link{width:212px;background:#12203a;border:1px solid #33425c;border-radius:14px;padding:22px 10px;text-align:center}.x-link b{display:block;font-size:29px;color:#eac77e}.x-link span{font:17px "Hiragino Sans",sans-serif;color:#cbd4e2}
.x-join{width:60px;height:2px;background:linear-gradient(90deg,#eac77e,#8bbdb9);transform:scaleX(0);transform-origin:left;opacity:1;transition:transform .7s ease}.x-join.in{transform:scaleX(1)}
.slide .cards article.st{transition:opacity .8s ease,transform .8s cubic-bezier(.2,.8,.3,1)}
:fullscreen nav,:fullscreen .fullscreen,:fullscreen .pager{display:none}
@media(prefers-reduced-motion:reduce){.st,.x-wire,.x-track i,.x-chart .ln,.x-join{transition:none}.x-core-ring{animation:none}}
'''
script = r'''const slides=[...document.querySelectorAll('.slide')],nav=[...document.querySelectorAll('nav button')];let current=0,stepN=0;
const maxStep=s=>Math.max(0,...[...s.querySelectorAll('.st')].map(e=>+e.dataset.step||0));
function paint(){slides[current].querySelectorAll('.st').forEach(e=>e.classList.toggle('in',(+e.dataset.step||0)<=stepN))}
function show(n,end){if(n<0||n>=slides.length)return;current=n;slides.forEach((s,i)=>{s.classList.toggle('on',i===n);s.inert=i!==n;if(i!==n)s.classList.remove('revealed')});
 stepN=end?maxStep(slides[n]):0;if(end&&slides[n].querySelector('.cover'))slides[n].classList.add('revealed');paint();
 nav.forEach(b=>b.classList.toggle('active',b.dataset.ch===slides[n].dataset.ch));document.querySelector('#count').textContent=(n+1)+' / '+slides.length}
let lockedUntil=0;function step(d){if(performance.now()<lockedUntil)return;const s=slides[current];
 if(s.querySelector('.cover')){if(d>0&&!s.classList.contains('revealed')){s.classList.add('revealed');lockedUntil=performance.now()+850;return}if(d<0&&s.classList.contains('revealed')){s.classList.remove('revealed');return}}
 const m=maxStep(s);if(d>0&&stepN<m){stepN++;paint();return}if(d<0&&stepN>0){stepN--;paint();return}show(current+d,d<0)}
document.querySelector('#next').onclick=()=>step(1);document.querySelector('#prev').onclick=()=>step(-1);
nav.forEach(b=>b.onclick=()=>show(slides.findIndex(s=>s.dataset.ch===b.dataset.ch)));
document.querySelectorAll('.cover').forEach(c=>c.onclick=e=>{e.stopPropagation();c.blur();step(1)});
addEventListener('keydown',e=>{if(e.repeat)return;const btn=e.target.closest('button');if(btn&&!btn.classList.contains('cover')&&[' ','Enter'].includes(e.key))return;
 if(['ArrowRight','PageDown',' ','Enter'].includes(e.key)){e.preventDefault();step(1)}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();step(-1)}if(e.key==='Home')show(0)});
document.querySelector('#fullscreen').onclick=()=>{document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()};
function fit(){document.documentElement.style.setProperty('--scale',Math.min(innerWidth/1440,innerHeight/810))}addEventListener('resize',fit);fit();
const q=new URLSearchParams(location.search);show(Math.max(0,(+q.get('s')||1)-1),q.get('full')==='1');'''

page = ('<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>なぜ米国のニュースで、世界の相場が動くのか？</title>'
        f'<style>{base}{extra}</style></head><body><main id="stage"><nav aria-label="章へ移動"><b>特別編</b>' +
        ''.join(f'<button data-ch="{i}">{t}</button>' for i, t in enumerate(NAV)) + '</nav>' + ''.join(slides) +
        '<button class="fullscreen" id="fullscreen" style="left:28px;bottom:25px;right:auto;top:auto;width:auto;height:auto">全画面 ⛶</button>'
        '<div class="pager"><button id="prev" aria-label="前へ">‹</button><span id="count"></span><button id="next" aria-label="次へ">›</button></div>'
        f'</main><script>{script}</script></body></html>')
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page, encoding='utf-8')
print(len(slides), 'slides ->', OUT)
