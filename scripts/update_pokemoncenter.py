import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

URL = "https://www.pokemoncenter-online.com/"
OUTPUT = Path("pokemoncenter_news.json")

def main():
    jst = timezone(timedelta(hours=9))

    result = {
        "updatedAt": datetime.now(jst).strftime("%Y-%m-%d %H:%M"),
        "source": URL,
        "status": "未確認",
        "message": "",
        "news": []
    }

    try:
        request = urllib.request.Request(
            URL,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8", errors="replace")

        if "仮想待合室" in html or "アクセス制限" in html:
            result["status"] = "アクセス制限"
            result["message"] = "公式サイトのアクセス制限を確認しました"
        else:
            result["status"] = "接続成功"
            result["message"] = "公式サイトへの接続を確認しました"

    except urllib.error.HTTPError as error:
        result["status"] = "接続できません"
        result["message"] = "HTTPエラー: " + str(error.code)

    except Exception as error:
        result["status"] = "接続できません"
        result["message"] = str(error)

    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("ポケモンセンターオンライン確認結果")
    print("状態:", result["status"])
    print("内容:", result["message"])
    print("保存先:", OUTPUT)


if __name__ == "__main__":
    main()
