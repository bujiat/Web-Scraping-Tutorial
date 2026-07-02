# Scrapy — Guide and Architecture

## Installation

Install Scrapy with pip:

```bash
pip install scrapy
```

Create a new project:

```bash
scrapy startproject <project_name>
```

Generate a spider:

```bash
scrapy genspider <spider_name> <allowed_domain>
```

Run your spider:

```bash
scrapy crawl <spider_name>
```

List all spiders in the project:

```bash
scrapy list
```

Check directory structure (Windows):

```powershell
tree mySpider /F
```

---

## How Scrapy Works



### Timeline: From start to finish

**[1] You run** `scrapy crawl xxspider`

- Engine reads your `start_urls` (e.g., page=1, page=2)
- Spider generates 2 `Request` objects and hands them to Engine

**[2] Scheduler queues and deduplicates**

- Engine passes Requests to Scheduler
- Scheduler stores them in a queue (filters out duplicates)
- Queue: [Request page=1, Request page=2]

**[3] Downloader fetches pages asynchronously**

- Engine pulls Request page=1 from Scheduler → Downloader
- Downloader sends HTTP GET to xx.com
- While waiting for page=1 to arrive (for example:2 seconds), Engine pulls Request page=2 → Downloader
- Downloader also fetches page=2 in parallel
- **Both pages are downloading at the same time** (this is the "async" part)

**[4] Response arrives, Engine routes it to Spider**

- Response page=1 arrives: "Here's the HTML of page 1 with 20 projects"
- Engine: "This response belongs to parse(), so I'll call parse(response)"
- Spider's `parse()` method is invoked with Response page=1

**[5] Spider extracts data using XPath**

- `parse()` runs an XPath query: find all 20 project blocks in the HTML
- For each project block, it extracts  fields that you want.
- Creates an `Item` object for each project with these fields
- `yield item` sends the Item to Pipeline

**[6] Pipeline receives and saves Items**

- Pipeline's `process_item()` receives Items one by one
- Each item is validated, cleaned, and written to `xx.json`
- **Important rule:** `process_item()` must `return item`, or data is lost

**[7] Meanwhile, Response page=2 arrives**

- While `parse()` was processing page=1's 20 items, page=2 has already downloaded
- Engine routes Response page=2 to `parse()` again
- Another 20 items are extracted and saved

**Result:** Both pages downloaded and processed asynchronously. Total time ≈ 2 seconds, not 4 seconds.

### Why this design: the core insight

**Problem:** Downloading is slow. For example each page takes 2 seconds. If you download one at a time, 100 pages = 200 seconds.

**Solution (Scrapy's async approach):**

- Don't wait for one page to download before starting the next
- Fire off 100 requests at once
- Process pages as they arrive
- While page=1 is being parsed, page=2 is downloading; while page=2 is being parsed, page=3 is downloading
- Total time for 100 pages ≈ 2 seconds (time for the slowest page)

This is why Scrapy separates concerns:

- **Scheduler** keeps a queue of unprocessed requests → prevents waste
- **Downloader** handles network I/O independently → network can work in background
- **Spider** processes responses sequentially → clear logic
- **Engine** coordinates between them → ensures smooth flow
- **Pipeline** is decoupled from spider → easy to change how data is saved

Example pipeline setting in `settings.py`:

```python
ITEM_PIPELINES = {
	'myproject.pipelines.ValidatePipeline': 100,
	'myproject.pipelines.SaveToJsonPipeline': 300,
}
```

---

## Example: giteespider.py

Code: `examples/03-scrapy/demo/spiders/giteespider.py`

The simplest flow: `start_urls` → `parse()` → XPath extracts each block → `yield item` → Pipeline saves to `giteespider.json`. One page, no pagination, no extra requests.



---

## Example: quote.py & quote2.py

Code: `examples/03-scrapy/demo/spiders/quote.py`, `qutoe2.py`

Both crawl the same site ([quotes.toscrape.com](https://quotes.toscrape.com/)), but collect **different fields** and write to **different JSON files**.

**quote.py** — list page + pagination + author link

- `parse()` reads quotes on the list page, builds a `QuoteItem`
- `yield scrapy.Request(..., callback=self.parse_author, meta={'item': item})` — follow the author link; `meta` carries the half-filled item into the next callback
- `parse_author()` adds address and birthday, then `yield item`
- `yield scrapy.Request(..., callback=self.parse)` — follow the "next" link for pagination
- Output: `quote.json`

**quote2.py** (`qutoe2`) — list page + pagination only

- Same list page parsing, but `yield item` directly — no author page
- Output: `qutoe2.json` (content, name, link only)

**Two JSON files from one site:** register two pipelines in `settings.py`. Each checks `spider.name` — `JsonWriterPipeline` handles `quote`, `Quote2Pipeline` handles `qutoe2`. Same website, different spiders, different output files.

**scrapy.Request**:

```python
scrapy.Request(url[, callback, method='GET', headers, body, cookies, meta, dont_filter=False])
```

- **callback** — which method handles the response
- **meta** — pass data between callbacks (e.g. the partial item)
- **dont_filter** — default `False` (skip duplicate URLs); `True` to request the same URL again
- **method / headers / cookies / body** — for POST or custom headers

Docs: [Request and Response](https://docs.scrapy.org/en/latest/topics/request-response.html)

---

## Middleware

Middleware is a hook on the Request/Response chain. Register it in `settings.py`; Scrapy calls it automatically — you never invoke it in the spider.

```
Request → [Downloader Middleware] → download → Response → Spider
```

Write Middleware when **every request** needs the same treatment (UA, login token, proxy). Simple spiders don't need it.

---

### Example 1: douban.py — random User-Agent

Code: `examples/03-scrapy/demo/spiders/douban.py`, `demo/middlewares.py`

Crawls [Douban Top 250](https://movie.douban.com/top250). Some sites block the default Scrapy UA — `DoubanUA` picks a random UA in `process_request` before each download.

```python
# settings.py
DOWNLOADER_MIDDLEWARES = {
    "demo.middlewares.DoubanUA": 543,
}
```

Run: `cd examples/03-scrapy && scrapy crawl douban`

---

### Example 2: srmeb_middleware — authori-zation header

Code: `examples/03-scrapy/srmeb_middleware/`

Crawls a **login-protected API** ([CRMEB admin](https://pro.crmeb.net/adminapi/home/header)). The spider only sets `start_urls`; all auth logic lives in Middleware.

**Problem:** the API returns 401 without a valid `authori-zation` header. You can't hard-code a token — it expires.

**Solution:** `LoginSpiderMiddleware` runs once before the first request:

1. Open the login page with **[Selenium](#selenium)**, click login, read cookies/token
2. Store the token on `self.authorization`
3. In `process_request`, attach it to every Request:

```python
request.headers["authori-zation"] = f"Bearer {token}"
```

**Flow:**

```
scrapy crawl crmeb
  → first Request hits LoginSpiderMiddleware.process_request()
  → Selenium logs in (once) → get token
  → all Requests carry authori-zation header
  → Spider parse() receives JSON from protected API
```

```python
# srmeb_middleware/settings.py
DOWNLOADER_MIDDLEWARES = {
    "srmeb_middleware.middlewares.LoginSpiderMiddleware": 543,
}
```

Run:

```bash
cd examples/03-scrapy/srmeb_middleware
scrapy crawl crmeb
```

**Why Middleware here?** Login is a one-time setup step that applies to all requests — the same pattern as UA, but for `authori-zation`. Keeps the spider clean; swap auth logic without touching `crmeb.py`.

---

## Selenium

Selenium appears in `srmeb_middleware` for login. Scrapy alone cannot click buttons or run login JS — Selenium fills that gap.

### What is it?

**Selenium** controls a real browser (Chrome, Firefox, …) from Python — open a page, click, type, read cookies. It is **not** a crawler framework like Scrapy; it is **browser automation**.

```
Scrapy  → sends HTTP requests, parses responses (fast, no browser)
Selenium → drives Chrome like a user (slow, runs JavaScript)
```

### Why use it here?

The CRMEB admin API needs an `authori-zation` token. Middleware uses Selenium **once** to log in and grab cookies, then Scrapy sends all API requests with that token.

Use Selenium when:

- Login requires clicking / JS (this example)
- Data appears only after browser actions
- You can't find a usable API in DevTools

Skip Selenium when:

- Static HTML or a known API with headers is enough (giteespider, quote, douban)

### How to use (minimal)

Install:

```bash
pip install selenium
```

Download [ChromeDriver](https://chromedriver.chromium.org/) matching your Chrome version, place `chromedriver.exe` in the project folder.

Core steps (same pattern as `middlewares.py`):

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://pro.crmeb.net/admin/login")
driver.find_element(By.XPATH, "//button[...]").click()
cookies = driver.get_cookies()   # read token from cookies
driver.quit()
```

Then pass the token to Scrapy requests via Middleware — Selenium does **not** crawl every page, only the login step.

### Selenium vs Playwright

Both drive a browser. Selenium is older and widely used; Playwright is newer and often easier for new projects. Same role: **when Scrapy can't get the data alone, use a browser tool for that step.**

---

### Downloader vs Spider Middleware

- **Downloader Middleware** — `process_request` / `process_response`. Used for UA, authori-zation, proxy. **Both examples above use this.**
- **Spider Middleware** — hooks around `parse()`. Used less often.

Only classes listed in `settings.py` run. Template classes from `scrapy startproject` are ignored until registered.