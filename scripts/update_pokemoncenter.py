
import json
import re
import urllib.request
import urllib.error
from html.parser import HTMLParser
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin

JST = timezone(timedelta(hours=9))

PAGES = [
    {
        "url": "https://www.pokemoncenter-online.com/",
        "label": "ポケモンセンターオンライン"
    },
    {
        "url": "https://www.pokemoncenter-online.com/feature-list/",
        "label": "特集・新商品"
    },
    {
        "url": (
            "https://www.pokemoncenter-online.com/"
            "search/?inStock=1&prefn1=releaseType"
            "&prefv1=1%7C2%7C3&srule=top-new-product"
        ),
        "label": "新商品・予約商品"
    }
]

OUTPUT_FILE = "pokemoncenter_news.json"

KEYWORDS = [
    "新商品", "新発売", "予約", "受注",
    "再入荷", "再販", "抽選", "追加抽選",
    "販売開始", "発売", "ポケモンセンター"
]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_url = None
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.current_url = dict(attrs).get("href")
            self.current_text = []

    def handle_data(self, data):
        if self.current_url:
            self.current_text.append(data.strip())

    def handle_endtag(self, tag):
        if tag == "a" and self.current_url:
            title = " ".join(
                part for part in self.current_text if part
            )
            if title:
                self.links.append((title, self.current_url))
            self.current_url = None
            self.current_text = []


def fetch_page(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml"
        }
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError("HTTP " + str(response.status))

        return response.read().decode(
            "utf-8", errors="replace"
        )


def main():
    now = datetime.now(JST).isoformat(timespec="seconds")
    results = []
    success_count = 0
    errors = []

    for page in PAGES:
        try:
            html = fetch_page(page["url"])
            success_count += 1

            parser = LinkParser()
            parser.feed(html)

            for title, href in parser.links:
                if any(word in title for word in KEYWORDS):
                    full_url = urljoin(page["url"], href)

                    if not full_url.startswith(
                        "https://www.pokemoncenter-online.com/"
                    ):
                        continue

                    results.append({
                        "title": title,
                        "url": full_url,
                        "source": page["label"]
                    })

        except Exception as error:
            errors.append(
                page["label"] + ": " +
                type(error).__name__ + " " + str(error)
            )

    unique = {}
    for item in results:
        unique[item["url"]] = item

    news = list(unique.values())

    if success_count:
        status = "接続成功"
        message = (
            "公式ページを確認しました。"
            + str(success_count)
            + "ページ取得成功、関連リンク"
            + str(len(news))
            + "件。"
        )
    else:
        status = "取得失敗"
        message = (
            "公式ページを取得できませんでした。"
            "アクセス制限などの可能性があります。"
        )

    data = {
        "status": status,
        "message": message,
        "updatedAt": now,
        "news": news,
        "errors": errors
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(message)
    print("検出リンク数:", len(news))

    for error in errors:
        print(error)


if __name__ == "__main__":
    main()
