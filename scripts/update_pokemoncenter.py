
import urllib.request
import urllib.error

URL = "https://www.pokemoncenter-online.com/feature-list/"

def main():
    request = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; PokemonGoodsHub/1.0)",
            "Accept": "text/html,application/xhtml+xml"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8", errors="replace")

            print("接続成功")
            print("HTTP status:", response.status)
            print("取得文字数:", len(html))
            print("商品ページのタイトル確認:",
                  "特集から探す" in html)

    except urllib.error.HTTPError as error:
        print("HTTPエラー:", error.code)
        raise

    except Exception as error:
        print("接続エラー:", str(error))
        raise

if __name__ == "__main__":
    main()
