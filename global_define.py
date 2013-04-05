import datetime
TODAY = datetime.date.today()

RSS_DIR_LIST = [
    "http://rss.sina.com.cn/news/index.shtml",
    "http://rss.sina.com.cn/sports/index.shtml",
    "http://rss.sina.com.cn/blog/index.shtml",
    "http://rss.sina.com.cn/tech/index.shtml",
    "http://rss.sina.com.cn/finance/index.shtml",
    "http://rss.sina.com.cn/jczs/index.shtml",
    "http://rss.sina.com.cn/eladies/index.shtml",
    "http://rss.sina.com.cn/auto/index.shtml",
    "http://rss.sina.com.cn/ent/index.shtml",
    "http://rss.sina.com.cn/book/index.shtml",
    "http://rss.sina.com.cn/edu/index.shtml",
    "http://rss.sina.com.cn/house/index.shtml",
    "http://rss.sina.com.cn/games/index.shtml",
    "http://rss.sina.com.cn/astro/index.shtml",
    "http://rss.sina.com.cn/bn/index.shtml",
    "http://rss.sina.com.cn/baby/index.shtml"
]

TEXT_DIR = "./text/"
XML_DIR = "./xml/"
INDEX_INCREMENTAL_DIR = "/home/wyy/data/Henesys/index/incremental"
DATA_DIR = "/home/wyy/data/Henesys/data"
INDEX_PRIME_DIR = "./index/prime/"

#xml parser
XML_NODE_NAME = "item"
TITLE_K = "title"
LINK_K = "link"
PUBDATE_K = "pubDate"
DESC_K = "description"
