
import json
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin

SOURCE_URL = "https://www.pokemon-card.com/info/"
OUTPUT_FILE = Path("card_news.json")

class NewsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "a" and attrs.get("href"):
            self.current = {
                "url": urljoin(SOURCE_URL, attrs["href"]),
                "text": ""
            }

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += data

    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            text = " ".join(self.current["text"].split())

            if text.startswith("商品 "):
                self.items.append({
                    "title": text[3:].strip(),
                    "url": self.current["url"],
                    "category": "ポケモンカード",
                    "source": "ポケモンカード公式ニュース",
                    "image": ""
                })

            self.current = None


def main():
    request = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")

    parser = NewsParser()
    parser.feed(html)

    # URLで重複を除く
    unique = {}
    for item in parser.items:
        unique[item["url"]] = item

    news = list(unique.values())

    if not news:
        raise ValueError("商品ニュースを取得できませんでした")

    jst = timezone(timedelta(hours=9))
    result = {
        "updatedAt": datetime.now(jst).strftime("%Y-%m-%d %H:%M"),
        "source": SOURCE_URL,
        "news": news
    }

    OUTPUT_FILE.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("ポケカ公式商品ニュース取得成功:", len(news), "件")
    print("保存先:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
