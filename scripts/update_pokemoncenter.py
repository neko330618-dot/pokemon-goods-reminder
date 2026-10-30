
import urllib.request
import urllib.error

URL = (
    "https://www.pokemoncenter-online.com/"
    "search/?prefn1=releaseType&prefv1=1&srule=top-new-product"
)

def main():
    request = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8", errors="replace")

            print("接続成功")
            print("HTTP status:", response.status)
            print("最終URL:", response.geturl())
            print("取得文字数:", len(html))
            print("商品一覧の確認:", "商品一覧" in html)
            print("品切れ表示の確認:", "品切れ" in html)
            print("NEW表示の確認:", "NEW" in html)

    except Exception as error:
        print("接続確認結果:", type(error).__name__)
        print("詳細:", str(error))

if __name__ == "__main__":
    main()
