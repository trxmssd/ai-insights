#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重建知识库首页 index.html（数据内嵌，file:// 与 GitHub Pages 均可用）。每日归档后重跑一次。"""
import json, io, os
BASE = os.path.dirname(os.path.abspath(__file__))
idx = json.load(open(os.path.join(BASE,'search-index.json'), encoding='utf-8'))
idx.sort(key=lambda x: x['date'], reverse=True)
data = json.dumps(idx, ensure_ascii=False)
html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>亚太ICT MSSD · AI 洞察知识库</title>
<style>
:root { --red:#C7000B; --ink:#1a1a1a; --gray:#666; --line:#e8e8e8; --bg:#fafafa; }
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:"Microsoft YaHei","PingFang SC",sans-serif; background:var(--bg); color:var(--ink); }
.hero { background:#fff; border-bottom:3px solid var(--red); padding:36px 24px 28px; }
.hero .inner, .main { max-width:960px; margin:0 auto; }
.hero h1 { font-size:26px; letter-spacing:1px; }
.hero h1 span { color:var(--red); }
.hero p { color:var(--gray); font-size:13px; margin-top:8px; }
.stats { display:flex; gap:32px; margin-top:18px; }
.stat b { font-size:24px; color:var(--red); font-weight:700; }
.stat i { font-style:normal; font-size:12px; color:var(--gray); display:block; margin-top:2px; }
.insights { margin-top:18px; display:flex; gap:10px; flex-wrap:wrap; }
.insights a { display:inline-block; background:var(--red); color:#fff; text-decoration:none; font-size:13px; padding:8px 16px; border-radius:4px; }
.insights a.alt { background:#1a1a1a; }
.main { padding:24px; }
.searchbar { display:flex; gap:10px; margin-bottom:8px; }
#q { flex:1; padding:12px 16px; font-size:15px; border:1px solid var(--line); border-radius:6px; outline:none; background:#fff; }
#q:focus { border-color:var(--red); }
.hint { font-size:12px; color:#999; margin-bottom:20px; }
.month { font-size:14px; font-weight:700; color:var(--red); margin:26px 0 10px; border-left:4px solid var(--red); padding-left:10px; }
.card { background:#fff; border:1px solid var(--line); border-radius:8px; padding:18px 20px; margin-bottom:12px; display:block; text-decoration:none; color:inherit; transition:box-shadow .15s; }
.card:hover { box-shadow:0 4px 16px rgba(0,0,0,.08); }
.card .date { font-size:12px; color:var(--red); font-weight:700; }
.card .title { font-size:16px; font-weight:700; margin:6px 0 6px; line-height:1.5; }
.card .sum { font-size:13px; color:var(--gray); line-height:1.7; }
.card .hits { font-size:12px; color:#b05500; margin-top:8px; line-height:1.8; }
.card .hits em { font-style:normal; background:#fff3e0; padding:1px 4px; border-radius:3px; }
.empty { text-align:center; color:#999; padding:60px 0; font-size:14px; }
footer { text-align:center; color:#bbb; font-size:12px; padding:30px 0 40px; }
</style>
</head>
<body>
<div class="hero"><div class="inner">
<h1>亚太ICT MSSD · <span>AI 洞察知识库</span></h1>
<p>每日 AI 洞察日报归档 · 关键词全文检索 · 数据截至 __LATEST__</p>
<div class="stats">
<div class="stat"><b>__NDAYS__</b><i>累积日报（天）</i></div>
<div class="stat"><b>__NITEMS__</b><i>累积情报条目</i></div>
<div class="stat"><b>__SPAN__</b><i>覆盖区间</i></div>
</div>
__INSIGHTS__
</div></div>
<div class="main">
<div class="searchbar"><input id="q" type="search" placeholder="搜索关键词：如 CoreWeave、开源、算力、印尼、韩国、华为…"></div>
<div class="hint">搜索范围覆盖每日标题、摘要与全部新闻条目；点击卡片打开当日完整日报。</div>
<div id="list"></div>
<div id="empty" class="empty" style="display:none">没有匹配结果，换个关键词试试</div>
</div>
<footer>亚太ICT MSSD AI 洞察知识库 · 自动归档生成</footer>
<script>
const DATA = __DATA__;
const list = document.getElementById('list'), empty = document.getElementById('empty');
function render(q) {
  q = (q||'').trim().toLowerCase();
  let html = '', lastMonth = '', shown = 0;
  for (const d of DATA) {
    let hits = [];
    if (q) {
      const inTitle = d.title.toLowerCase().includes(q);
      const inSum = d.summary.toLowerCase().includes(q);
      hits = d.items.filter(it => it.toLowerCase().includes(q));
      if (!inTitle && !inSum && hits.length === 0) continue;
    }
    const month = d.date.slice(0,7);
    if (month !== lastMonth) { html += `<div class="month">${month.replace('-','年')}月</div>`; lastMonth = month; }
    let hitHtml = '';
    if (q && hits.length) {
      const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
      hitHtml = `<div class="hits">${hits.slice(0,5).map(h=>'· '+esc(h).replace(new RegExp(q.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&'),'gi'), m=>`<em>${m}</em>`)).join('<br>')}${hits.length>5?`<br>…共 ${hits.length} 条命中`:''}</div>`;
    }
    html += `<a class="card" href="reports/${d.date}.html">
      <div class="date">${d.date}</div>
      <div class="title">${d.title}</div>
      <div class="sum">${d.summary.slice(0,120)}${d.summary.length>120?'…':''}</div>
      ${hitHtml}</a>`;
    shown++;
  }
  list.innerHTML = html;
  empty.style.display = shown ? 'none' : 'block';
}
document.getElementById('q').addEventListener('input', e => render(e.target.value));
render('');
</script>
</body>
</html>"""
ins_dir = os.path.join(BASE,'insights')
links = ''
if os.path.isdir(ins_dir):
    files = sorted(os.listdir(ins_dir), reverse=True)
    links = ''.join(f'<a href="insights/{f}">观点报告 · {os.path.splitext(f)[0]}</a>' for f in files if f.endswith('.html'))
html = html.replace('__INSIGHTS__', f'<div class="insights">{links}</div>' if links else '')
n_items = sum(len(d['items']) for d in idx)
dates = sorted(d['date'] for d in idx)
html = (html.replace('__DATA__', data)
            .replace('__NDAYS__', str(len(idx)))
            .replace('__NITEMS__', str(n_items))
            .replace('__LATEST__', dates[-1])
            .replace('__SPAN__', dates[0][5:].replace('-','.') + '–' + dates[-1][5:].replace('-','.')))
io.open(os.path.join(BASE,'index.html'),'w',encoding='utf-8').write(html)
print('index.html written:', len(html), 'bytes')
