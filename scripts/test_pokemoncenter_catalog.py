
import urllib.request
import urllib.error
from urllib.parse import urlparse
import re

URL = (
    "https://www.pokemoncenter-online.com/search/"
    "?inStock=1&prefn1=releaseType&prefv1=1%7C2%7C3"
    "&srule=top-new-product"
)

def main():
    request = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "ja,en-US;q=0.9,en;q=0.8"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8", errors="replace")

            print("接続成功")
            print("HTTP:", response.status)
            print("最終URL:", response.geturl())
            print("取得文字数:", len(html))

            title = re.search(
                r"<title[^>]*>(.*?)</title>",
                html,
                re.IGNORECASE | re.DOTALL
            )

            if title:
                print("ページタイトル:", title.group(1).strip())

            print("商品らしい表示:", "商品" in html)
            print("価格表示:", "円" in html)
            print("画像タグ数:", len(re.findall(r"<img", html, re.I)))

    except urllib.error.HTTPError as error:
        print("接続拒否")
        print("HTTP:", error.code)
        print("転送先:", error.headers.get("Location", "なし"))

    except Exception as error:
        print("エラー:", type(error).__name__)
        print("詳細:", error)

if __name__ == "__main__":
    main()
