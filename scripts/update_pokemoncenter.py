
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

URL = "https://www.pokemoncenter-online.com/"
RSS_URLS = [
    "https://www.pokemoncenter-online.com/news/rss/",
    "https://www.pokemoncenter-online.com/rss/",
]

OUTPUT = Path("pokemoncenter_news.json")


def fetch_rss(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "PokemonGoodsHub/1.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    items = []

    for item in root.findall(".//item")[:20]:
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        pub_date = item.findtext("pubDate", "").strip()

        if title and link:
            items.append({
                "title": title,
                "url": link,
                "date": pub_date,
                "source": "ポケモンセンターオンライン"
            })

    return items


def main():
    jst = timezone(timedelta(hours=9))

    result = {
        "updatedAt": datetime.now(jst).strftime("%Y-%m-%d %H:%M"),
        "source": URL,
        "status": "未確認",
        "message": "",
        "news": []
    }

    errors = []

    for rss_url in RSS_URLS:
        try:
            news = fetch_rss(rss_url)

            if news:
                result["status"] = "接続成功"
                result["message"] = "公式RSSから情報を取得しました"
                result["news"] = news
                break

            errors.append("RSSに掲載記事がありません")

        except urllib.error.HTTPError as error:
            errors.append("HTTPエラー: " + str(error.code))

        except Exception as error:
            errors.append(type(error).__name__ + ": " + str(error))

    if result["status"] != "接続成功":
        result["status"] = "情報取得不可"
        result["message"] = (
            "公開RSSから情報を取得できませんでした。"
            "公式サイトで最新情報をご確認ください。"
            + " / ".join(errors)
        )

    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("ポケモンセンターオンライン確認結果")
    print("状態:", result["status"])
    print("内容:", result["message"])
    print("取得件数:", len(result["news"]))
    print("保存先:", OUTPUT)


if __name__ == "__main__":
    main()
