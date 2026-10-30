
import urllib.request
import urllib.error

URL = "https://www.pokemoncenter-online.com/feature-list/"

class RedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        print("転送を検出しました")
        print("HTTP:", code)
        print("転送先:", newurl)
        return super().redirect_request(
            req, fp, code, msg, headers, newurl
        )

def main():
    opener = urllib.request.build_opener(RedirectHandler())

    request = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html"
        }
    )

    try:
        response = opener.open(request, timeout=20)
        print("最終URL:", response.geturl())
        print("HTTP status:", response.status)
        print("取得成功")
        response.close()

    except Exception as error:
        print("確認結果:", type(error).__name__)
        print("詳細:", error)

if __name__ == "__main__":
    main()
