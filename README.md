# 亚太ICT MSSD · AI 洞察知识库

每日 AI 洞察日报的自动归档与检索站点。

- **在线首页**：https://trxmssd.github.io/ai-insights/ （日历索引 + 关键词全文搜索）
- `reports/` 每日日报原文（HTML）
- `insights/` 月度观点报告（列表页 `insights/index.html`）
- `deck/` 高层谈资 PPTX / 网页版（列表页 `deck/index.html`）
- `build_index.py` 首页与两个列表页的重建脚本：新增日报、观点报告或谈资后运行 `python3 build_index.py`（首页只放入口，具体条目在列表页）

数据流：每日日报（Gmail 发送）→ 自动归档至本仓库 → GitHub Pages 发布。
