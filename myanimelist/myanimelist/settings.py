

BOT_NAME = "myanimelist"

SPIDER_MODULES = ["myanimelist.spiders"]
NEWSPIDER_MODULE = "myanimelist.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 1. SPEED + POLITENESS (perfect balance)
# ------------------------------------------------------------------
# THIS IS THE MAGIC THAT PREVENTS 1327 STOP
CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 4
DOWNLOAD_DELAY = 2.0                    # 2 seconds between requests
RANDOMIZE_DOWNLOAD_DELAY = True         # 1.0–3.0 seconds random
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 3.0



# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "myanimelist.middlewares.MyanimelistSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "myanimelist.middlewares.MyanimelistDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "myanimelist.pipelines.MyanimelistPipeline": 300,
#}


# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# ------------------------------------------------------------------
# 4. RETRY + RESUME (never lose progress!)
# ------------------------------------------------------------------
RETRY_TIMES = 12
RETRY_HTTP_CODES = [403, 429, 500, 502, 503, 504, 522, 524, 408, 407]

# THIS IS THE MOST IMPORTANT LINE – saves your progress!
JOBDIR = 'crawls/myanimelist-full-2025'   # ← Will create this folder automatically

# ------------------------------------------------------------------
# 5. CACHE & PERFORMANCE
# ------------------------------------------------------------------
HTTPCACHE_ENABLED = False
#HTTPCACHE_EXPIRATION_SECS = 3600 * 24 * 30   # 30 days
#HTTPCACHE_DIR = 'httpcache'

FEED_EXPORT_ENCODING = 'utf-8'
