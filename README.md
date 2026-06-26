# 爬虫教程

从零开始学习 Python 爬虫：HTTP 基础 → 轻量爬虫 → Scrapy 框架 → 动态页面 → 反爬与存储。

## 环境要求

- Python 3.10+
- Windows / macOS / Linux

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 第 4 章 Playwright 需额外安装浏览器
playwright install chromium
```

## 学习路线

| 章节 | 文档 | 示例代码 | 说明 |
|------|------|----------|------|
| 00 | [总览](docs/00-overview.md) | — | 爬虫概念、合规边界 |
| 01 | [HTTP 与 HTML](docs/01-http-and-html-basics.md) | [examples/01-http-basics](examples/01-http-basics/) | 请求响应、DOM、选择器 |
| 02 | [requests + BS4](docs/02-requests-beautifulsoup.md) | [examples/02-requests-bs4](examples/02-requests-bs4/) | 轻量爬虫入门 |
| 03 | [Scrapy](docs/03-scrapy.md) | [examples/03-scrapy-giteepr](examples/03-scrapy-giteepr/) | 框架架构与实战 |
| 04 | [动态页面](docs/04-dynamic-pages.md) | [examples/04-playwright](examples/04-playwright/) | Playwright 抓 JS 渲染页 |
| 05 | [反爬对抗](docs/05-anti-crawling.md) | [examples/05-anti-crawl](examples/05-anti-crawl/) | Headers、限速、代理 |
| 06 | [数据存储](docs/06-data-storage.md) | [examples/06-storage](examples/06-storage/) | SQLite 持久化 |
| 07 | [分布式爬虫](docs/07-distributed-crawling.md) | — | Scrapy-Redis 概念 |
| 08 | [工程实践](docs/08-best-practices.md) | — | 日志、测试、部署 |

```mermaid
flowchart LR
    A[00 总览] --> B[01 HTTP/HTML]
    B --> C[02 requests+BS4]
    C --> D[03 Scrapy]
    D --> E[04 动态页面]
    E --> F[05 反爬]
    F --> G[06 存储]
    G --> H[07 分布式]
    H --> I[08 工程实践]
```

**推荐路径**：00 → 01 → 02 → 03（核心）→ 04 → 05 → 06

## 快速开始（Scrapy 示例）

```bash
cd examples/03-scrapy-giteepr
scrapy crawl giteespider
# 运行后在项目根目录生成 gitee.json（已加入 .gitignore）
# 样例输出见 output/gitee.json
```

## 目录结构

```
crawler/
├── README.md
├── requirements.txt
├── docs/           # 教程文档
├── examples/       # 每章可运行示例
├── assets/         # 配图
└── scripts/        # 辅助脚本
```
