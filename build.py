#!/usr/bin/env python3
"""
AI Portfolio - Static Site Builder
===================================
posts/ 内のMarkdown記事を読み込み、HTML（index.html + 個別記事ページ）を生成する。
images/ 内の画像を出力先にコピーし、記事内の画像参照を正しいパスに変換する。

使い方:
    python build.py

出力:
    - index.html         : カード一覧トップページ
    - articles/*.html    : 各記事の個別ページ
    - images/*           : 画像ファイル（そのまま配信）
"""

import os
import re
import shutil
import sys
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader


# ============================================================
# 設定
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
POSTS_DIR = BASE_DIR / "posts"
TEMPLATES_DIR = BASE_DIR / "templates"
ARTICLES_DIR = BASE_DIR / "articles"
IMAGES_DIR = BASE_DIR / "images"
OUTPUT_INDEX = BASE_DIR / "index.html"

# 画像の拡張子
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


# ============================================================
# ユーティリティ
# ============================================================
def parse_frontmatter(filepath: Path) -> tuple[dict, str]:
    """
    YAMLフロントマター付きMarkdownファイルを読み込み、
    (メタデータdict, 本文Markdown文字列) を返す。
    """
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not match:
        print(f"  [WARN] フロントマターが見つかりません: {filepath.name}")
        return {}, text

    meta = yaml.safe_load(match.group(1)) or {}
    body = match.group(2)
    return meta, body


def slug_from_filename(filename: str) -> str:
    """ファイル名から拡張子を除いたスラッグを生成する。"""
    return Path(filename).stem


def format_date(date_value) -> str:
    """date を表示用文字列に変換する。"""
    if hasattr(date_value, "strftime"):
        return date_value.strftime("%Y-%m-%d")
    return str(date_value) if date_value else ""


def fix_image_paths_for_article(html: str) -> str:
    """
    記事HTML内の画像パスを articles/ からの相対パスに修正する。
    ../images/xxx.png → ../images/xxx.png（すでに正しい場合はそのまま）
    images/xxx.png → ../images/xxx.png（postsからの相対パスを修正）
    """
    # images/ で始まるパスを ../images/ に変換（articles/ 配下からの参照用）
    html = re.sub(
        r'src="images/',
        'src="../images/',
        html,
    )
    return html


def get_thumbnail(meta: dict, slug: str) -> str:
    """
    記事のサムネイル画像パスを取得する。
    フロントマターの thumbnail が指定されていればそれを使い、
    なければ images/{slug}-thumb.* を探す。見つからなければ空文字。
    """
    # フロントマターで明示指定
    if meta.get("thumbnail"):
        return meta["thumbnail"]

    # 自動探索: images/{slug}-thumb.png 等
    for ext in IMAGE_EXTENSIONS:
        thumb_path = IMAGES_DIR / f"{slug}-thumb{ext}"
        if thumb_path.exists():
            return f"images/{slug}-thumb{ext}"

    return ""


# ============================================================
# メイン処理
# ============================================================
def load_posts() -> list[dict]:
    """posts/ 内の全Markdown記事を読み込み、メタデータ＋HTML本文のリストを返す。"""
    md = markdown.Markdown(extensions=["extra", "codehilite", "toc"])
    posts = []

    if not POSTS_DIR.exists():
        print(f"[ERROR] posts/ ディレクトリが見つかりません: {POSTS_DIR}")
        sys.exit(1)

    md_files = sorted(POSTS_DIR.glob("*.md"))
    if not md_files:
        print("[WARN] posts/ に記事がありません。空のindex.htmlを生成します。")
        return posts

    for filepath in md_files:
        meta, body_md = parse_frontmatter(filepath)

        # テンプレートファイルはスキップ
        if not meta:
            continue

        md.reset()
        body_html = md.convert(body_md)

        slug = slug_from_filename(filepath.name)
        thumbnail = get_thumbnail(meta, slug)
        post = {
            "title": meta.get("title", "無題"),
            "client": meta.get("client", ""),
            "period": meta.get("period", ""),
            "purpose": meta.get("purpose", ""),
            "ai_tools": meta.get("ai_tools", []),
            "summary": meta.get("summary", ""),
            "date": meta.get("date", ""),
            "date_display": format_date(meta.get("date", "")),
            "tags": meta.get("tags", []),
            "thumbnail": thumbnail,
            "slug": slug,
            "body_html": body_html,
        }
        posts.append(post)

    # 日付降順でソート
    posts.sort(key=lambda p: str(p["date"]), reverse=True)
    return posts


def build_site():
    """サイト全体をビルドする。"""
    print("=" * 50)
    print("AI Portfolio - Build Start")
    print("=" * 50)

    # Jinja2 環境セットアップ
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
    )

    base_template = env.get_template("base.html")
    card_template = env.get_template("card.html")
    article_template = env.get_template("article.html")

    # 記事読み込み
    posts = load_posts()
    print(f"\n[INFO] {len(posts)} 件の記事を読み込みました。")

    # articles/ ディレクトリの作成
    ARTICLES_DIR.mkdir(exist_ok=True)

    # --- 個別記事ページの生成 ---
    print("\n--- 個別記事ページを生成中 ---")
    for post in posts:
        # 記事本文内の画像パスを articles/ からの相対パスに修正
        article_body = fix_image_paths_for_article(post["body_html"])

        article_content = article_template.render(
            title=post["title"],
            client=post["client"],
            period=post["period"],
            purpose=post["purpose"],
            ai_tools=post["ai_tools"],
            tags=post["tags"],
            date=post["date_display"],
            body=article_body,
            base_path="../",
        )

        page_html = base_template.render(
            title=post["title"],
            content=article_content,
            css_path="../",
            base_path="../",
        )

        output_path = ARTICLES_DIR / f"{post['slug']}.html"
        output_path.write_text(page_html, encoding="utf-8")
        print(f"  [OK] {output_path.name}")

    # --- トップページ（カード一覧）の生成 ---
    print("\n--- トップページを生成中 ---")
    cards_html = ""
    for post in posts:
        card_html = card_template.render(
            slug=post["slug"],
            title=post["title"],
            client=post["client"],
            ai_tools=post["ai_tools"],
            summary=post["summary"],
            date=post["date_display"],
            tags=post["tags"],
            thumbnail=post["thumbnail"],
        )
        cards_html += card_html + "\n"

    index_content = f"""
<h1 class="page-title">AI活用事例一覧 <span class="page-count">({len(posts)}件)</span></h1>
<div class="card-grid">
{cards_html}
</div>
"""

    index_html = base_template.render(
        title="トップ",
        content=index_content,
        css_path="",
        base_path="",
    )

    OUTPUT_INDEX.write_text(index_html, encoding="utf-8")
    print(f"  [OK] index.html")

    # --- 画像ファイルの確認 ---
    image_count = 0
    if IMAGES_DIR.exists():
        image_count = sum(
            1 for f in IMAGES_DIR.iterdir()
            if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
        )

    print("\n" + "=" * 50)
    print("Build Complete!")
    print(f"  - index.html: 生成済み")
    print(f"  - articles/: {len(posts)} ページ生成済み")
    print(f"  - images/: {image_count} 画像ファイル")
    print("=" * 50)


# ============================================================
# エントリーポイント
# ============================================================
if __name__ == "__main__":
    build_site()
