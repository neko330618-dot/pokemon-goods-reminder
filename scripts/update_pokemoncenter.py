
import json
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

URL = "https://www.pokemoncenter-online.com/"
OUTPUT = Path("pokemoncenter_news.json")

def main():
    request = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")
        status = response.status
        content_type = response.headers.get("Content-Type", "")

    if status != 200 or "<html" not in html.lower():
        raise ValueError("公式サイトのページを正常に取得できませんでした")

    if "仮想待合室" in html or "アクセス制限" in html:
        raise ValueError("アクセス制限が検出されました。取得を中止します")

    jst = timezone(timedelta(hours=9))

    result = {
        "updatedAt": datetime.now(jst).strftime("%Y-%m-%d %H:%M"),
        "source": URL,
        "status": status,
        "contentType": content_type,
        "pageTitle": "ポケモンセンターオンライン",
        "message": "公式サイトへの接続を確認しました",
        "news": []
    }

    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("ポケモンセンターオンライン接続成功")
    print("HTTP status:", status)
    print("HTML取得文字数:", len(html))
    print("保存先:", OUTPUT)

if __name__ == "__main__":
    main()
