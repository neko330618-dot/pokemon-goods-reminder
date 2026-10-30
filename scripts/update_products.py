
import json
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

API_URL = "https://www.pokemon.co.jp/api/goods/index/"
DATA_FILE = Path("products.json")

JST = timezone(timedelta(hours=9))
now = datetime.now(JST)

def fetch_official_goods():
    request = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    results = data.get("results", [])

    if not isinstance(results, list) or not results:
        raise ValueError("公式商品データを取得できませんでした")

    products = []

    for item in results:
        name = item.get("title")
        image = item.get("img_1")
        url = item.get("full_uniq")

        if not name or not image or not url:
            continue

        products.append({
            "name": name,
            "category": "公式サイト掲載",
            "image": image,
            "releaseDate": (
                "公式掲載日: " + item["start_date"]
                if item.get("start_date") else ""
            ),
            "preorderDate": "",
            "price": "公式詳細ページで確認",
            "url": url,
            "source": "ポケモン公式サイト"
        })

    if not products:
        raise ValueError("有効な商品情報がありません")

    return products


def main():
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as file:
            saved = json.load(file)
    else:
        saved = {"updatedAt": "", "products": []}

    existing = saved.get("products", [])

    if not isinstance(existing, list):
        raise ValueError("products.json の形式が正しくありません")

    official_products = fetch_official_goods()

    # URLをキーにして重複を防ぎ、既存データを保持する
    merged = {}
    for product in existing:
        if product.get("url"):
            merged[product["url"]] = product

    for product in official_products:
        url = product["url"]
        if url in merged:
            merged[url].update(product)
        else:
            merged[url] = product

    saved["updatedAt"] = now.strftime("%Y-%m-%d %H:%M")
    saved["products"] = list(merged.values())

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(saved, file, ensure_ascii=False, indent=2)

    print("公式サイト取得成功:", len(official_products), "件")
    print("保存後の商品数:", len(saved["products"]), "件")
    print("更新日時:", saved["updatedAt"])


if __name__ == "__main__":
    main()
