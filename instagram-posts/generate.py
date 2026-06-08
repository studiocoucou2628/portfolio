#!/usr/bin/env python3
"""
Instagram投稿画像ジェネレーター
5つのサンプルLPを1080x1080のInstagram投稿画像として生成する
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ===== パス設定 =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # projects/
OUTPUT_DIR = os.path.join(BASE_DIR, "instagram-posts", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# フォント
FONT_JP   = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
FONT_EN   = "/Library/Fonts/Arial Unicode.ttf"

def load_font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()

# ===== カラー =====
BG        = (26, 26, 26)       # #1a1a1a
CARD_BG   = (35, 35, 35)       # #232323
BAR_BG    = (45, 45, 45)       # #2d2d2d
URL_BG    = (58, 58, 58)       # #3a3a3a
GOLD      = (200, 169, 110)    # #c8a96e
GOLD_DIM  = (200, 169, 110, 60)
WHITE     = (255, 255, 255)
GRAY      = (136, 136, 136)
DARK_GRAY = (80, 80, 80)

# ===== LP データ =====
LPS = [
    {
        "id": "01",
        "filename": "post-01-cafe.jpg",
        "img": "sample-cafe/images/hero.jpg",
        "url": "studiocoucou.jp / cafe-niigata",
        "type": "CAFE & RESTAURANT",
        "name": "Café Niigata",
        "desc": "新潟産食材にこだわるカフェの集客LP\n温かみのあるデザインと予約導線を実装",
    },
    {
        "id": "02",
        "filename": "post-02-seitai.jpg",
        "img": "sample-seitai/images/feature-01.jpg",
        "url": "studiocoucou.jp / seitai-reset",
        "type": "CHIROPRACTIC & TREATMENT",
        "name": "整体院 Re:set",
        "desc": "お悩み訴求とLINE予約導線を強化した\nコンバージョン重視の設計",
    },
    {
        "id": "03",
        "filename": "post-03-eikaiwa.jpg",
        "img": "sample-eikaiwa/images/hero.jpg",
        "url": "studiocoucou.jp / eigo-plus",
        "type": "ENGLISH SCHOOL & EDUCATION",
        "name": "EigoPlus",
        "desc": "体験申込・料金比較・講師紹介まで揃えた\n英会話スクールの集客LP",
    },
    {
        "id": "04",
        "filename": "post-04-gym.jpg",
        "img": "sample-gym/images/hero.jpg",
        "url": "studiocoucou.jp / rise-gym",
        "type": "PERSONAL GYM & FITNESS",
        "name": "RISE Personal Gym",
        "desc": "トレーナー実績・ビフォーアフターを押し出した\n信頼訴求型パーソナルジムLP",
    },
    {
        "id": "05",
        "filename": "post-05-jewelry.jpg",
        "img": "sample-jewelry/images/hero.jpg",
        "url": "studiocoucou.jp / eclat-bijoux",
        "type": "LUXURY JEWELRY & ACCESSORIES",
        "name": "ECLAT BIJOUX",
        "desc": "黒×ゴールドのラグジュアリーデザイン\n商品拡大ライトボックスを実装したジュエリーLP",
    },
]

# ===== 描画ヘルパー =====
def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_text_center(draw, text, y, font, fill, canvas_w=1080):
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    x = (canvas_w - w) // 2
    draw.text((x, y), text, font=font, fill=fill)

# ===== メイン生成 =====
def generate_post(lp_data):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")

    # ----- フォント -----
    f_logo_en  = load_font(FONT_JP, 22)
    f_tag      = load_font(FONT_EN, 14)
    f_url      = load_font(FONT_EN, 13)
    f_type     = load_font(FONT_EN, 13)
    f_name     = load_font(FONT_JP, 34)
    f_desc     = load_font(FONT_JP, 20)
    f_handle   = load_font(FONT_EN, 17)
    f_num      = load_font(FONT_EN, 13)
    f_dot      = load_font(FONT_EN, 11)

    # ----- 外枠（ゴールド細線） -----
    draw.rectangle([28, 28, W-28, H-28], outline=(*GOLD, 40), width=1)

    # ----- ヘッダー（上部） -----
    MARGIN = 68
    HEADER_Y = 68

    # ロゴ "Studio Coucou"
    draw.text((MARGIN, HEADER_Y), "Studio ", font=f_logo_en, fill=WHITE)
    bbox_s = f_logo_en.getbbox("Studio ")
    draw.text((MARGIN + bbox_s[2] - bbox_s[0], HEADER_Y), "Coucou", font=f_logo_en, fill=GOLD)

    # "PORTFOLIO" タグ（右）
    tag_text = "PORTFOLIO"
    tag_bbox = f_tag.getbbox(tag_text)
    tag_w = tag_bbox[2] - tag_bbox[0] + 28
    tag_h = 30
    tag_x = W - MARGIN - tag_w
    tag_y = HEADER_Y - 4
    draw.rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], outline=GOLD, width=1)
    draw.text((tag_x + 14, tag_y + 8), tag_text, font=f_tag, fill=GOLD)

    # ----- ブラウザモックアップ -----
    BR_X  = MARGIN        # 68
    BR_Y  = HEADER_Y + 60 # 128
    BR_W  = W - MARGIN * 2  # 944
    BAR_H = 42
    IMG_H = 556
    BR_H  = BAR_H + IMG_H

    # ブラウザ外枠（角丸）
    draw_rounded_rect(draw, [BR_X, BR_Y, BR_X+BR_W, BR_Y+BR_H], radius=10, fill=BAR_BG)

    # ブラウザバー（ドット + URL）
    dot_y = BR_Y + BAR_H // 2
    dot_colors = [(255, 95, 86), (255, 189, 46), (39, 201, 63)]
    for i, dc in enumerate(dot_colors):
        cx = BR_X + 18 + i * 22
        draw.ellipse([cx-6, dot_y-6, cx+6, dot_y+6], fill=dc)

    # URLバー
    url_x0 = BR_X + 80
    url_x1 = BR_X + 80 + 340
    url_bar_y0 = BR_Y + 10
    url_bar_y1 = BR_Y + BAR_H - 10
    draw_rounded_rect(draw, [url_x0, url_bar_y0, url_x1, url_bar_y1], radius=4, fill=URL_BG)
    url_text = lp_data["url"]
    url_text_y = url_bar_y0 + (url_bar_y1 - url_bar_y0 - 14) // 2
    draw.text((url_x0 + 10, url_text_y), url_text, font=f_url, fill=GRAY)

    # LP ヒーロー画像
    lp_img_path = os.path.join(BASE_DIR, lp_data["img"])
    if os.path.exists(lp_img_path):
        hero = Image.open(lp_img_path).convert("RGB")
        # アスペクト比を保ちながらクロップ
        target_w, target_h = BR_W, IMG_H
        hero_ratio = hero.width / hero.height
        target_ratio = target_w / target_h
        if hero_ratio > target_ratio:
            new_h = target_h
            new_w = int(hero.width * (target_h / hero.height))
        else:
            new_w = target_w
            new_h = int(hero.height * (target_w / hero.width))
        hero = hero.resize((new_w, new_h), Image.LANCZOS)
        # センタークロップ
        left = (new_w - target_w) // 2
        top = 0
        hero = hero.crop((left, top, left + target_w, top + target_h))
        img.paste(hero, (BR_X, BR_Y + BAR_H))
    else:
        # フォールバック: ダークグレー
        draw.rectangle([BR_X, BR_Y+BAR_H, BR_X+BR_W, BR_Y+BAR_H+IMG_H], fill=CARD_BG)

    # ブラウザ外枠（重ね描き）
    draw_rounded_rect(draw, [BR_X, BR_Y, BR_X+BR_W, BR_Y+BR_H], radius=10,
                      fill=None, outline=(*GOLD, 30), width=1)

    # ----- フッター情報 -----
    FOOTER_Y = BR_Y + BR_H + 44

    # 区切り線（ゴールドライン）
    div_y = FOOTER_Y - 20
    draw.rectangle([MARGIN, div_y, W-MARGIN, div_y+1], fill=(*GOLD, 50))

    # LP タイプ
    draw.text((MARGIN, FOOTER_Y), lp_data["type"], font=f_type, fill=GOLD)

    # LP 名
    name_y = FOOTER_Y + 28
    draw.text((MARGIN, name_y), lp_data["name"], font=f_name, fill=WHITE)

    # LP 説明
    desc_lines = lp_data["desc"].split("\n")
    desc_y = name_y + 52
    for line in desc_lines:
        draw.text((MARGIN, desc_y), line, font=f_desc, fill=GRAY)
        desc_y += 30

    # ハンドル（右寄せ）
    handle = "@studiocoucou.jp"
    hbbox = f_handle.getbbox(handle)
    handle_w = hbbox[2] - hbbox[0]
    handle_x = W - MARGIN - handle_w
    handle_y = FOOTER_Y + 16
    draw.text((handle_x, handle_y), handle, font=f_handle, fill=GOLD)

    # 制作・お問合せラベル
    label = "制作・お問合せ"
    lbbox = f_dot.getbbox(label)
    label_w = lbbox[2] - lbbox[0]
    label_x = W - MARGIN - label_w
    draw.text((label_x, handle_y - 20), label, font=f_dot, fill=DARK_GRAY)

    # 下部タグライン
    tagline = "新潟の大切なお店が、もっと多くの人に見つけてもらえるように。"
    tl_bbox = f_dot.getbbox(tagline)
    tl_w = tl_bbox[2] - tl_bbox[0]
    tl_x = (W - tl_w) // 2
    draw.text((tl_x, H - 68), tagline, font=f_dot, fill=(60, 60, 60))

    # 投稿番号（右下）
    num_text = f"{lp_data['id']} / 05"
    nbbox = f_num.getbbox(num_text)
    num_w = nbbox[2] - nbbox[0]
    draw.text((W - MARGIN - num_w, H - 46), num_text, font=f_num, fill=DARK_GRAY)

    # ----- 保存 -----
    out_path = os.path.join(OUTPUT_DIR, lp_data["filename"])
    img.save(out_path, "JPEG", quality=95)
    print(f"  生成: {lp_data['filename']}")
    return out_path

# ===== 実行 =====
print("Instagram投稿画像を生成中...\n")
for lp in LPS:
    generate_post(lp)
print(f"\n完了！出力先: {OUTPUT_DIR}")
