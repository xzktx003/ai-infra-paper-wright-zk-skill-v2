#!/usr/bin/env python3
"""竖屏小红书宣传片：确认写作逻辑，套模板，对照三大顶会，流水线成稿。

配音 zh-CN-XiaoxiaoNeural，字幕烧进画面。重跑：

    python3 build_video.py --preview
    python3 build_video.py --cues
    python3 build_video.py
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import os
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

os.umask(0o022)

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
FONT_DIR = ROOT / "fonts"
FRAMES = BUILD / "frames"
PREVIEW = ROOT / "preview"

W, H = 1080, 1920
COVER_W, COVER_H = 1080, 1440
SR = 48000
VOICE = "zh-CN-XiaoxiaoNeural"
DEFAULT_RATE = "-2%"
LEAD = 0.16
TAIL = 0.55

CINNABAR = (214, 73, 52)
DEEP = (168, 46, 32)
PAPER = (243, 238, 230)
INK = (20, 22, 26)
MIST = (186, 192, 198)
GOLD = (204, 168, 112)
DARK_CARD = (30, 35, 42)
WHITE = (247, 244, 238)

BOLD_TTC = (
    FONT_DIR
    / "extract/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
)
REG_TTC = (
    FONT_DIR
    / "extract/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
)
MONO_TTF = Path("/data01/home/xuzk/anaconda3/fonts/SourceCodePro-Semibold.ttf")
DEB_URL = (
    "http://mirrors.aliyun.com/debian/pool/main/f/fonts-noto-cjk/"
    "fonts-noto-cjk_20220127+repack1-1_all.deb"
)

FACES: dict[str, tuple[str, int]] = {}
BG: Image.Image | None = None
PROBE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def S(sid: str, scene: str, voice: str, **kwargs) -> dict:
    item = {"id": sid, "scene": scene, "voice": voice, "hi": kwargs.pop("hi", None)}
    item.update(kwargs)
    return item


SEGMENTS = [
    S("s01", "hook", "实验已经验证过了。论文，还没成形。", gap_after=0.28),
    S("s02", "stuck", "卡住的通常不是句子，是写作逻辑还没定下来。"),
    S("s03", "logic", "所以第一步，先确认写作逻辑。", min_hold=1.05),
    S("s04", "checks", "代码先执行到 B，并不代表 B 依赖 A。", hi=0),
    S("s05", "checks", "模块多，也不等于贡献多。", hi=1),
    S("s06", "checks", "路由看主贡献，不看文件夹。", hi=2),
    S("s07", "templates", "逻辑定了，再套模板。七类叙事，二十个二级模板。", hi=0),
    S("s08", "templates", "主模板选一个。必要时，再加一个。", hi=1),
    S("s09", "venues", "再粗看三大顶会怎么起笔。ICLR，ICML，NeurIPS。"),
    S("s10", "corpus", "二零二五到二零二六，官方录用记录四十二篇。", hi=0),
    S("s11", "corpus", "二十二篇看过引言和部分正文。二十篇停在摘要。", hi=1),
    S("s12", "corpus", "这是粗看写作逻辑。不是通读，更不是复现。", hi=2),
    S("s13", "taste", "也拿来提高学术品味。现象，机制，设计，结果。", hi=-1),
    S("s14", "taste", "它不打分，也不预测录用。只问这件事该不该这样讲。", hi=4),
    S("s15", "pipe", "然后收成一条流水线。", hi=-1),
    S("s16", "pipe", "验证过的 idea 进去。", hi=0),
    S("s16b", "pipe", "先确认逻辑。", hi=1),
    S("s16c", "pipe", "再套模板。", hi=2),
    S("s17", "pipe", "写出带缺口标记的中文初稿。缺的证据继续标着。", hi=3),
    S("s18", "english", "要写英文主会稿，再过名词冻结。同一个概念，不换着叫。"),
    S("s19", "version", "诊断、段落计划和初稿，放进新建目录，不覆盖旧稿。"),
    S("s20", "bounds", "默认只读。不跑训练，也不改你的仓库。", hi=0),
    S("s21", "bounds", "它不是新的大模型，也不保证录用。", hi=1),
    S("s22", "close", "后摩论文科研研究 Skill。", gap_after=0.18),
    S("s23", "close", "把刚验证过的 idea，铺成一篇完整初稿。", min_hold=1.7, gap_after=0.2),
    S("s24", "close", "整包都在仓库里。手册、模板、语料、脚本。", min_hold=1.45),
]


def run(cmd: list[str], **kwargs) -> None:
    subprocess.run(cmd, check=True, **kwargs)


def ensure_fonts() -> None:
    if BOLD_TTC.exists() and REG_TTC.exists():
        return
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    deb = FONT_DIR / "noto-cjk.deb"
    if not deb.exists() or deb.stat().st_size < 1_000_000:
        run(["curl", "-fL", "--retry", "3", "-o", str(deb), DEB_URL])
    extract = FONT_DIR / "extract"
    extract.mkdir(parents=True, exist_ok=True)
    if subprocess.call(["dpkg-deb", "-x", str(deb), str(extract)]) != 0:
        run(["ar", "x", str(deb)], cwd=FONT_DIR)
        data = next(FONT_DIR.glob("data.tar.*"))
        run(["tar", "-xf", str(data), "-C", str(extract)])
    if not BOLD_TTC.exists():
        raise SystemExit(f"未找到中文字体：{BOLD_TTC}")


def init_faces() -> None:
    FACES["bold"] = (str(BOLD_TTC), 2)
    FACES["regular"] = (str(REG_TTC), 2)
    if MONO_TTF.exists():
        FACES["mono"] = (str(MONO_TTF), 0)
    else:
        FACES["mono"] = (str(BOLD_TTC), 7)


from functools import lru_cache


@lru_cache(maxsize=256)
def load_font(path: str, size: int, index: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=index)


def face(weight: str, size: int) -> ImageFont.FreeTypeFont:
    path, index = FACES[weight]
    return load_font(path, max(12, int(size)), index)


def make_bg(width: int, height: int) -> Image.Image:
    y = np.linspace(0, 1, height, dtype=np.float32)[:, None, None]
    top = np.array([22, 26, 32], np.float32)
    bot = np.array([9, 10, 12], np.float32)
    rgb = top * (1 - y) + bot * y
    base = np.broadcast_to(rgb, (height, width, 3)).astype(np.float32).copy()
    yy, xx = np.ogrid[0:height, 0:width]
    glow = np.clip(1 - ((xx - width * 0.84) ** 2 + (yy - height * 0.12) ** 2) / (height * 0.42) ** 2, 0, 1)
    glow = glow**2
    base[..., 0] += glow * 42
    base[..., 1] += glow * 16
    base[..., 2] += glow * 12
    glow2 = np.clip(1 - ((xx - width * 0.1) ** 2 + (yy - height * 0.86) ** 2) / (height * 0.5) ** 2, 0, 1)
    base[..., 0] += glow2**2 * 18
    arr = np.clip(base, 0, 255).astype(np.uint8)
    rgba = np.dstack([arr, np.full((height, width), 255, np.uint8)])
    rgba[:, :14, 0] = CINNABAR[0]
    rgba[:, :14, 1] = CINNABAR[1]
    rgba[:, :14, 2] = CINNABAR[2]
    return Image.fromarray(rgba, "RGBA")


def panel(img: Image.Image, box, fill, radius=28, shadow=True) -> None:
    x0, y0, x1, y1 = box
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    if shadow:
        d.rounded_rectangle((x0, y0 + 8, x1, y1 + 8), radius=radius, fill=(0, 0, 0, 70))
    d.rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=fill + (255,))
    img.alpha_composite(ov)


def draw_header(img: Image.Image) -> None:
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((68, 84, 92, 108), radius=4, fill=CINNABAR)
    d.text((108, 96), "后摩论文科研研究 Skill", font=face("bold", 30), fill=PAPER, anchor="lm")


def fit(weight: str, text: str, max_w: float, size: int, min_size: int = 24):
    current = size
    while current > min_size:
        font = face(weight, current)
        if PROBE.textlength(text, font=font) <= max_w:
            return font
        current -= 2
    return face(weight, min_size)


def draw_spaced(img, text, cx, y, weight, size, min_size, max_w, fill, tracking):
    current = size
    chosen = face(weight, min_size)
    total = max_w
    while current >= min_size:
        font = face(weight, current)
        widths = [PROBE.textlength(ch, font=font) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        if total <= max_w:
            chosen = font
            break
        current -= 4
    else:
        widths = [PROBE.textlength(ch, font=chosen) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
    d = ImageDraw.Draw(img)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=chosen, fill=fill, anchor="lt")
        x += w + tracking
    return chosen.size


def chips(img, labels, cx, y, font, fg=INK, bg=PAPER) -> float:
    d = ImageDraw.Draw(img)
    widths = [d.textlength(lab, font=font) + 44 for lab in labels]
    gap = 14
    total = sum(widths) + gap * (len(labels) - 1)
    x = cx - total / 2
    bbox = d.textbbox((0, 0), "测", font=font)
    th = bbox[3] - bbox[1]
    h = th + 22
    for lab, w in zip(labels, widths):
        panel(img, (x, y, x + w, y + h), bg, radius=h / 2, shadow=False)
        d = ImageDraw.Draw(img)
        d.text((x + w / 2, y + h / 2), lab, font=font, fill=fg, anchor="mm")
        x += w + gap
    return y + h



def kicker(img: Image.Image, text: str, y: int = 176) -> None:
    d = ImageDraw.Draw(img)
    d.text((72, y), text, font=face("bold", 32), fill=GOLD, anchor="lt")


def draw_hook(img: Image.Image) -> None:
    cx = W / 2
    d = ImageDraw.Draw(img)
    d.text((cx, 300), "HOUMO", font=face("bold", 32), fill=GOLD, anchor="mt")
    d.text((cx, 390), "实验已经验证过了", font=face("bold", 52), fill=PAPER, anchor="mt")
    giant_y = 500
    giant = draw_spaced(img, "还没成形", cx, giant_y, "bold", 168, 120, 960, CINNABAR, 10)
    y = giant_y + int(giant * 1.18)
    d = ImageDraw.Draw(img)
    d.rectangle((cx - 64, y, cx + 64, y + 7), fill=GOLD)
    d.text((cx, y + 40), "论文还停在实验和代码里", font=face("bold", 40), fill=MIST, anchor="mt")
    d.text((cx, y + 130), "确认逻辑  →  套模板  →  流水线成稿", font=face("bold", 34), fill=GOLD, anchor="mt")


def draw_stuck(img: Image.Image) -> None:
    draw_header(img)
    cx = W / 2
    d = ImageDraw.Draw(img)
    d.text((cx, 360), "真正卡住的", font=face("bold", 40), fill=GOLD, anchor="mt")
    d.text((cx, 520), "不是句子", font=face("regular", 64), fill=MIST, anchor="mt")
    d.text((cx, 680), "是写作逻辑", font=face("bold", 92), fill=CINNABAR, anchor="mt")
    d.text((cx, 860), "还没定下来", font=face("bold", 64), fill=PAPER, anchor="mt")


def draw_logic(img: Image.Image) -> None:
    draw_header(img)
    cx = W / 2
    d = ImageDraw.Draw(img)
    d.text((cx, 420), "第一步", font=face("bold", 40), fill=GOLD, anchor="mt")
    d.text((cx, 540), "先确认", font=face("bold", 88), fill=PAPER, anchor="mt")
    d.text((cx, 700), "写作逻辑", font=face("bold", 120), fill=CINNABAR, anchor="mt")
    d.text((cx, 920), "代码顺序，还不是论文顺序", font=face("regular", 36), fill=MIST, anchor="mt")


def draw_checks(img: Image.Image, hi: int) -> None:
    draw_header(img)
    kicker(img, "确认逻辑时，先卡住这三句")
    rows = [
        ("依赖", "代码先执行到 B", "不等于 B 依赖 A"),
        ("贡献", "模块多", "不等于贡献多"),
        ("路由", "看主贡献", "不看文件夹"),
    ]
    y = 260
    h, gap = 300, 20
    for i, (label, a, b) in enumerate(rows):
        active = i == hi
        panel(img, (72, y, 1008, y + h), PAPER if active else DARK_CARD, radius=30)
        d = ImageDraw.Draw(img)
        d.text((112, y + 36), label, font=face("bold", 28), fill=DEEP if active else GOLD, anchor="lt")
        d.text((112, y + 108), a, font=face("bold", 52), fill=INK if active else MIST, anchor="lt")
        line_b = fit("bold", b, 820, 48, 32)
        d.text((112, y + 196), b, font=line_b, fill=DEEP if active else CINNABAR, anchor="lt")
        y += h + gap


def draw_templates(img: Image.Image, hi: int) -> None:
    draw_header(img)
    kicker(img, "逻辑定了，再套模板")
    cards = [("7", "类叙事"), ("20", "二级模板")]
    for i, (num, label) in enumerate(cards):
        x = 72 + i * 478
        active = hi == 0
        panel(img, (x, 250, x + 458, 500), PAPER if active else DARK_CARD, radius=30)
        d = ImageDraw.Draw(img)
        d.text((x + 36, 278), num, font=face("bold", 120), fill=DEEP if active else CINNABAR, anchor="lt")
        d.text((x + 36, 420), label, font=face("bold", 40), fill=INK if active else PAPER, anchor="lt")
    rule_on = hi == 1
    panel(img, (72, 528, 1008, 668), CINNABAR if rule_on else DARK_CARD, radius=26)
    d = ImageDraw.Draw(img)
    d.text((108, 598), "主模板一个，必要时再加一个", font=face("bold", 40), fill=WHITE if rule_on else PAPER, anchor="lm")
    families = ["发现驱动", "数学结构", "约束框架", "系统驱动", "理解规律", "理论", "问题与评价"]
    positions = []
    y = 692
    h, step = 128, 140
    for index in range(0, 6, 2):
        positions.append((72, y, 530, y + h, families[index]))
        positions.append((550, y, 1008, y + h, families[index + 1]))
        y += step
    positions.append((72, y, 1008, y + h, families[6]))
    for x0, y0, x1, y1, label in positions:
        panel(img, (x0, y0, x1, y1), DARK_CARD, radius=24)
        d = ImageDraw.Draw(img)
        d.text(((x0 + x1) / 2, (y0 + y1) / 2), label, font=face("bold", 40), fill=PAPER, anchor="mm")


def draw_venues(img: Image.Image) -> None:
    draw_header(img)
    kicker(img, "粗看三大顶会怎么起笔")
    rows = ["ICLR", "ICML", "NeurIPS"]
    y = 270
    h, gap = 220, 16
    for name in rows:
        panel(img, (72, y, 1008, y + h), DARK_CARD, radius=28)
        d = ImageDraw.Draw(img)
        d.rectangle((116, y + 46, 184, y + 56), fill=CINNABAR)
        d.text((116, y + 128), name, font=face("bold", 68), fill=PAPER, anchor="lm")
        d.text((760, y + h / 2), "写作逻辑", font=face("bold", 36), fill=CINNABAR, anchor="lm")
        y += h + gap
    panel(img, (72, y + 12, 1008, y + 156), DARK_CARD, radius=26)
    d = ImageDraw.Draw(img)
    d.text((W / 2, y + 84), "对照起笔，不是整个会议的画像", font=face("bold", 36), fill=PAPER, anchor="mm")


def draw_corpus(img: Image.Image, hi: int) -> None:
    draw_header(img)
    kicker(img, "看过的范围，写在明处")
    rows = [
        ("42", "官方录用记录", "ICLR · ICML · NeurIPS"),
        ("22", "引言和部分正文", "能对照结构，不是通读"),
        ("20", "停在摘要", "只能定位，不能当模板证据"),
    ]
    y = 260
    h, gap = 250, 18
    for i, (num, label, note) in enumerate(rows):
        active = (hi == 0 and i == 0) or (hi == 1 and i > 0)
        panel(img, (72, y, 1008, y + h), PAPER if active else DARK_CARD, radius=28)
        d = ImageDraw.Draw(img)
        d.text((112, y + h / 2), num, font=face("bold", 92), fill=DEEP if active else CINNABAR, anchor="lm")
        d.text((360, y + 70), label, font=face("bold", 44), fill=INK if active else PAPER, anchor="lt")
        d.text((360, y + 150), note, font=face("regular", 30), fill=(90, 78, 70) if active else MIST, anchor="lt")
        y += h + gap
    note_on = hi == 2
    panel(img, (72, 1088, 1008, 1228), CINNABAR if note_on else DARK_CARD, radius=24)
    d = ImageDraw.Draw(img)
    d.text((W / 2, 1158), "粗看写作逻辑，不是复现，也不是穷尽", font=face("bold", 34), fill=WHITE if note_on else PAPER, anchor="mm")


def draw_taste(img: Image.Image, hi: int) -> None:
    draw_header(img)
    kicker(img, "学术品味，收成可以检查的四层")
    layers = [
        ("01", "现象", "改变了什么理解"),
        ("02", "机制", "排除了哪些别的解释"),
        ("03", "设计", "每一步回应什么要求"),
        ("04", "结果", "行为和代价是否对得上"),
    ]
    y = 260
    h, gap = 180, 14
    for i, (num, title, desc) in enumerate(layers):
        active = hi < 0 or hi == i
        panel(img, (72, y, 1008, y + h), PAPER if hi == i else DARK_CARD, radius=26)
        d = ImageDraw.Draw(img)
        d.text((112, y + h / 2), num, font=face("bold", 36), fill=DEEP if hi == i else GOLD, anchor="lm")
        d.text((230, y + 42), title, font=face("bold", 48), fill=INK if hi == i else (PAPER if active else MIST), anchor="lt")
        d.text((230, y + 108), desc, font=face("regular", 30), fill=(90, 78, 70) if hi == i else MIST, anchor="lt")
        y += h + gap
    footer_on = hi == 4
    panel(img, (72, y + 8, 1008, y + 128), CINNABAR if footer_on else DARK_CARD, radius=24)
    d = ImageDraw.Draw(img)
    d.text((W / 2, y + 68), "不打分，也不预测录用", font=face("bold", 40), fill=WHITE if footer_on else PAPER, anchor="mm")


def draw_pipe(img: Image.Image, hi: int) -> None:
    draw_header(img)
    kicker(img, "从验证过的 idea，到一篇初稿")
    steps = [
        ("01", "已验证的 idea", "实验、代码、配置、推导"),
        ("02", "确认写作逻辑", "依赖、贡献、主路线"),
        ("03", "套上模板", "一个主模板，必要时再加一个"),
        ("04", "中文初稿", "缺口继续标着，不拿数字填"),
        ("05", "英文再过契约", "需要时才做，名词先冻结"),
    ]
    y = 250
    h, gap = 176, 12
    for i, (num, title, desc) in enumerate(steps):
        active = i == hi
        panel(img, (72, y, 1008, y + h), PAPER if active else DARK_CARD, radius=24)
        d = ImageDraw.Draw(img)
        d.text((108, y + h / 2), num, font=face("bold", 36), fill=DEEP if active else GOLD, anchor="lm")
        d.text((210, y + 38), title, font=face("bold", 40), fill=INK if active else PAPER, anchor="lt")
        d.text((210, y + 104), desc, font=face("regular", 30), fill=(90, 78, 70) if active else MIST, anchor="lt")
        y += h + gap


def draw_english(img: Image.Image) -> None:
    draw_header(img)
    kicker(img, "要写英文主会稿，再走这一步")
    d = ImageDraw.Draw(img)
    d.text((72, 280), "名词冻结", font=face("bold", 96), fill=PAPER, anchor="lt")
    d.text((72, 420), "同一个概念，不换着叫", font=face("bold", 44), fill=CINNABAR, anchor="lt")
    panel(img, (72, 560, 1008, 1040), DARK_CARD, radius=30)
    d = ImageDraw.Draw(img)
    d.text((112, 640), "quantization", font=face("mono", 48), fill=PAPER, anchor="lt")
    d.text((112, 750), "后面还是这个名字", font=face("bold", 44), fill=GOLD, anchor="lt")
    d.text((112, 870), "句子可以改。概念不改名。", font=face("regular", 36), fill=MIST, anchor="lt")


def draw_version(img: Image.Image) -> None:
    draw_header(img)
    kicker(img, "流水线的出口")
    d = ImageDraw.Draw(img)
    d.text((72, 250), "不覆盖旧稿", font=face("bold", 72), fill=PAPER, anchor="lt")
    panel(img, (72, 380, 1008, 490), DARK_CARD, radius=20, shadow=False)
    d = ImageDraw.Draw(img)
    d.text((104, 435), "papers/vN", font=face("mono", 42), fill=GOLD, anchor="lm")
    items = [("诊断", 72, 540), ("段落计划", 550, 540), ("带标记初稿", 72, 760), ("审查意见", 550, 760)]
    for text, x, y in items:
        panel(img, (x, y, x + 438, y + 180), DARK_CARD, radius=26)
        d = ImageDraw.Draw(img)
        d.text((x + 36, y + 90), text, font=face("bold", 40), fill=PAPER, anchor="lm")
    d = ImageDraw.Draw(img)
    d.text((72, 1000), "新建目录。旧稿留在原地。", font=face("regular", 34), fill=MIST, anchor="lt")


def draw_bounds(img: Image.Image, hi: int) -> None:
    draw_header(img)
    kicker(img, "流水线也有边界")
    rows = [
        ("默认只读", "不跑训练，不改仓库"),
        ("不保证录用", "不是新模型，也不是自动科研"),
    ]
    y = 280
    h = 360
    for i, (title, desc) in enumerate(rows):
        active = i == hi
        panel(img, (72, y, 1008, y + h), PAPER if active else DARK_CARD, radius=32)
        d = ImageDraw.Draw(img)
        d.text((112, y + 110), title, font=face("bold", 64), fill=DEEP if active else PAPER, anchor="lt")
        d.text((112, y + 220), desc, font=face("bold", 36), fill=INK if active else MIST, anchor="lt")
        y += h + 24


def draw_close(img: Image.Image) -> None:
    cx = W / 2
    d = ImageDraw.Draw(img)
    d.text((cx, 280), "HOUMO", font=face("bold", 32), fill=GOLD, anchor="mt")
    name = fit("bold", "后摩论文科研研究 Skill", 920, 48, 36)
    d.text((cx, 360), "后摩论文科研研究 Skill", font=name, fill=PAPER, anchor="mt")
    giant_y = 500
    giant = draw_spaced(img, "完整初稿", cx, giant_y, "bold", 148, 100, 980, CINNABAR, 8)
    y = giant_y + int(giant * 1.18)
    d = ImageDraw.Draw(img)
    d.rectangle((cx - 64, y, cx + 64, y + 7), fill=GOLD)
    d.text((cx, y + 44), "把验证过的 idea 铺成一篇", font=face("bold", 40), fill=PAPER, anchor="mt")
    chips(img, ["手册", "模板", "语料", "脚本"], cx, y + 150, face("bold", 32), INK, PAPER)


def draw_subtitle(img: Image.Image, text: str) -> None:
    text = (text or "").strip()
    if not text:
        return
    font = fit("bold", text, 820, 52, 32)
    d = ImageDraw.Draw(img)
    tw = d.textlength(text, font=font)
    bbox = d.textbbox((0, 0), text, font=font)
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 28, 16
    cx, cy = W / 2, 1468
    x0 = cx - tw / 2 - pad_x
    y0 = cy - th / 2 - pad_y
    x1 = cx + tw / 2 + pad_x
    y1 = cy + th / 2 + pad_y
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=(5, 6, 8, 188))
    img.alpha_composite(ov)
    d = ImageDraw.Draw(img)
    d.text((cx, cy), text, font=font, fill=WHITE, anchor="mm")


def render_frame(seg: dict, subtitle: str, guides: bool = False, label: str | None = None) -> Image.Image:
    assert BG is not None
    img = BG.copy()
    scene = seg["scene"]
    hi = seg.get("hi")
    if scene == "hook":
        draw_hook(img)
    elif scene == "stuck":
        draw_stuck(img)
    elif scene == "logic":
        draw_logic(img)
    elif scene == "checks":
        draw_checks(img, 0 if hi is None else hi)
    elif scene == "templates":
        draw_templates(img, 0 if hi is None else hi)
    elif scene == "venues":
        draw_venues(img)
    elif scene == "corpus":
        draw_corpus(img, 0 if hi is None else hi)
    elif scene == "taste":
        draw_taste(img, -1 if hi is None else hi)
    elif scene == "pipe":
        draw_pipe(img, -1 if hi is None else hi)
    elif scene == "english":
        draw_english(img)
    elif scene == "version":
        draw_version(img)
    elif scene == "bounds":
        draw_bounds(img, 0 if hi is None else hi)
    elif scene == "close":
        draw_close(img)
    else:
        raise SystemExit(f"未知画面：{scene}")
    draw_subtitle(img, subtitle)
    if guides:
        d = ImageDraw.Draw(img)
        d.rectangle((64, 170, 1016, 1368), outline=(214, 73, 52, 180), width=2)
        d.rectangle((120, 1454, 960, 1590), outline=(204, 168, 112, 180), width=2)
    if label:
        d = ImageDraw.Draw(img)
        d.text((68, 1848), label, font=face("regular", 24), fill=GOLD, anchor="lt")
    return img


def preview_caption(voice: str) -> str:
    text = voice.strip().rstrip("。")
    if "，" in text:
        head = text.split("，")[0]
        if len(head) >= 4:
            return head
    return text[:18]


def write_voice_md() -> None:
    lines = [
        "# 口播稿",
        "",
        "声音：微软 Edge TTS，`zh-CN-XiaoxiaoNeural`。主线是确认写作逻辑、套模板、对照三大顶会、流水线成稿。",
        "小红书正文不在这里，见 `文案.md`。",
        "",
    ]
    for i, seg in enumerate(SEGMENTS, 1):
        lines.append(f"{i:02d}. {seg['voice']}")
    lines.append("")
    (ROOT / "口播稿.md").write_text("\n".join(lines), encoding="utf-8")


def render_preview(guides: bool) -> None:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    frames = PREVIEW / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    paths = []
    for seg in SEGMENTS:
        phrases = display_phrases(seg)
        caption = max(phrases, key=unit_len) if phrases else preview_caption(seg["voice"])
        img = render_frame(seg, caption, guides=guides, label=f"{seg['id']}  {seg['scene']}")
        path = frames / f"{seg['id']}.png"
        img.convert("RGB").save(path, quality=95)
        paths.append(path)
    cover = render_cover_image()
    cover.convert("RGB").save(PREVIEW / "cover.png", quality=95)
    cols = 5
    tw, th = 216, 384
    label_h = 32
    rows = math.ceil(len(paths) / cols)
    sheet = Image.new("RGB", (cols * tw, rows * (th + label_h)), (8, 8, 8))
    label_font = face("bold", 16)
    for i, path in enumerate(paths):
        im = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        r, c = divmod(i, cols)
        x, y = c * tw, r * (th + label_h)
        sheet.paste(im, (x, y))
        d = ImageDraw.Draw(sheet)
        d.text((x + 4, y + th + 4), path.stem, font=label_font, fill=(240, 240, 240))
    sheet.save(PREVIEW / "contact.jpg", quality=86)
    print(f"preview {PREVIEW/'contact.jpg'}")


def render_cover_image() -> Image.Image:
    img = make_bg(COVER_W, COVER_H)
    cx = COVER_W / 2
    d = ImageDraw.Draw(img)
    d.text((cx, 250), "HOUMO", font=face("bold", 30), fill=GOLD, anchor="mt")
    name = fit("bold", "后摩论文科研研究 Skill", 940, 46, 34)
    d.text((cx, 322), "后摩论文科研研究 Skill", font=name, fill=PAPER, anchor="mt")
    d.text((cx, 490), "实验已经验证过了", font=face("bold", 44), fill=MIST, anchor="mt")
    giant_y = 590
    giant = draw_spaced(img, "还没成形", cx, giant_y, "bold", 156, 110, 960, CINNABAR, 8)
    y = giant_y + int(giant * 1.18)
    d = ImageDraw.Draw(img)
    d.rectangle((cx - 64, y, cx + 64, y + 7), fill=GOLD)
    y += 36
    d.text((cx, y), "先确认写作逻辑，再铺成初稿", font=face("bold", 36), fill=PAPER, anchor="mt")
    y += 78
    chip_bottom = chips(img, ["套模板", "三大顶会", "学术品味", "流水线"], cx, y, face("bold", 28), INK, PAPER)
    d = ImageDraw.Draw(img)
    d.text((cx, chip_bottom + 64), "完整初稿  ·  整包可看  ·  不保证录用", font=face("bold", 28), fill=MIST, anchor="mt")
    return img


def sec_to_n(seconds: float) -> int:
    return int(round(seconds * SR))


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as handle:
        return handle.getnframes() / handle.getframerate()


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as handle:
        if handle.getframerate() != SR or handle.getnchannels() != 1 or handle.getsampwidth() != 2:
            raise SystemExit(f"音频格式不符：{path}")
        frames = handle.readframes(handle.getnframes())
    return np.frombuffer(frames, dtype=np.int16).copy()


def write_wav(path: Path, samples: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(SR)
        handle.writeframes(samples.astype(np.int16).tobytes())


def cache_key(seg: dict) -> str:
    raw = f"{seg['voice']}|{seg.get('rate', DEFAULT_RATE)}|{VOICE}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def detect_scale(raw: list[dict], clip_dur: float) -> float:
    if not raw:
        return 1e7
    end = max(item["offset"] + item["duration"] for item in raw)
    for scale in (1e7, 1e6, 1e4):
        if end / scale <= clip_dur + 1.2:
            return scale
    return 1e7


def normalize_words(raw: list[dict], scale: float) -> list[dict]:
    punct = set("，。、；：！？,.!?; ")
    words = []
    for item in raw:
        text = str(item.get("text") or "")
        start = item["offset"] / scale
        end = start + item["duration"] / scale
        stripped = text.strip()
        if stripped in punct and words:
            words[-1]["text"] += stripped
            words[-1]["end"] = end
            continue
        if not stripped:
            continue
        words.append({"text": text, "start": start, "end": end})
    return words


def polish_sub(text: str) -> str:
    text = text.strip()
    while text.endswith(("。", "，", "、", "；")):
        text = text[:-1]
    text = text.strip()
    if "“我们发现”" not in text:
        text = text.replace("我们发现", "“我们发现”")
    if "不编“首次”" not in text:
        text = text.replace("不编首次", "不编“首次”")
    return text


def unit_len(text: str) -> float:
    skip = set("，。、；：！？“”\"''")
    total = 0.0
    for ch in text:
        if ch.isspace() or ch in skip:
            continue
        total += 0.55 if ord(ch) < 128 else 1.0
    return total


def norm_chars(text: str) -> str:
    skip = set("，。、；：！？“”\"''")
    out = []
    for ch in text:
        if ch.isspace() or ch in skip:
            continue
        out.append(ch.lower() if ord(ch) < 128 else ch)
    return "".join(out)


def break_long(part: str, limit: float = 15.0) -> list[str]:
    part = part.strip()
    if not part or unit_len(part) <= limit:
        return [part] if part else []
    best = None
    best_score = 10**9
    for index, ch in enumerate(part):
        if ch not in "、，" or index <= 0 or index >= len(part) - 1:
            continue
        left, right = part[:index].strip("，、 "), part[index + 1 :].strip("，、 ")
        if not left or not right:
            continue
        score = abs(unit_len(left) - unit_len(right))
        if score < best_score:
            best_score = score
            best = (left, right)
    if best is None:
        mid = max(1, len(part) // 2)
        while mid < len(part) and ord(part[mid]) < 128:
            mid += 1
        best = (part[:mid].strip(), part[mid:].strip())
    pieces = []
    for piece in best:
        if piece:
            pieces.extend(break_long(piece, limit))
    return pieces


def display_phrases(seg: dict) -> list[str]:
    custom = seg.get("subs")
    if custom:
        return [polish_sub(item) for item in custom if str(item).strip()]
    raw = []
    buf = ""
    for ch in seg["voice"].strip():
        buf += ch
        if ch in "，。；":
            raw.append(buf.strip())
            buf = ""
    if buf.strip():
        raw.append(buf.strip())
    phrases = []
    for part in raw:
        phrases.extend(break_long(part))
    glued = []
    index = 0
    while index < len(phrases):
        current = phrases[index]
        if unit_len(current) <= 2.2 and index + 1 < len(phrases):
            nxt = phrases[index + 1].lstrip("，。 ")
            current = current.rstrip("，。 ") + "，" + nxt
            index += 2
            glued.append(current)
        else:
            glued.append(current)
            index += 1
    return [polish_sub(item) for item in glued if polish_sub(item)]


def phrases_to_cues(seg: dict, words: list[dict], clip_dur: float) -> list[dict]:
    phrases = display_phrases(seg)
    stream = []
    for word in words:
        for ch in str(word["text"]):
            if ch.isspace() or ch in "，。、；：！？“”":
                continue
            token = ch.lower() if ord(ch) < 128 else ch
            stream.append((token, word["start"], word["end"]))
    idx = 0
    cues = []
    for phrase in phrases:
        target = norm_chars(phrase)
        if not target:
            continue
        if idx >= len(stream):
            print(f"ALIGN-SHORT {seg['id']} leftover {phrase}")
            break
        start_i = idx
        matched = ""
        while idx < len(stream) and len(matched) < len(target):
            matched += stream[idx][0]
            idx += 1
        if matched != target:
            print(f"ALIGN {seg['id']} want={target} got={matched}")
        end_i = max(start_i, min(idx, len(stream)) - 1)
        cues.append({"text": phrase, "start": stream[start_i][1], "end": stream[end_i][2]})
    if not cues:
        return [{"start": 0.0, "end": clip_dur, "text": polish_sub(seg["voice"])}]
    cues[0]["start"] = 0.0
    for index in range(len(cues) - 1):
        cues[index]["end"] = max(cues[index]["end"], cues[index + 1]["start"])
    cues[-1]["end"] = max(cues[-1]["end"], clip_dur)
    return cues


async def synth_one(seg: dict, force: bool) -> None:
    key = cache_key(seg)
    wav_path = BUILD / "audio" / f"{seg['id']}-{key}.wav"
    json_path = wav_path.with_suffix(".json")
    seg["wav"] = wav_path
    seg["words_path"] = json_path
    if wav_path.exists() and json_path.exists() and not force:
        return
    wav_path.parent.mkdir(parents=True, exist_ok=True)
    import edge_tts

    last_error = None
    for attempt in range(3):
        try:
            comm = edge_tts.Communicate(
                seg["voice"],
                VOICE,
                rate=seg.get("rate", DEFAULT_RATE),
                boundary="WordBoundary",
                receive_timeout=120,
            )
            audio = bytearray()
            raw_words = []
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    audio += chunk["data"]
                elif chunk["type"] == "WordBoundary":
                    raw_words.append(
                        {"text": chunk["text"], "offset": chunk["offset"], "duration": chunk["duration"]}
                    )
            if not audio:
                raise RuntimeError("空音频")
            mp3_path = wav_path.with_suffix(".mp3")
            mp3_path.write_bytes(audio)
            run(
                [
                    "ffmpeg",
                    "-y",
                    "-v",
                    "error",
                    "-i",
                    str(mp3_path),
                    "-ac",
                    "1",
                    "-ar",
                    str(SR),
                    "-c:a",
                    "pcm_s16le",
                    str(wav_path),
                ]
            )
            json_path.write_text(json.dumps(raw_words, ensure_ascii=False), encoding="utf-8")
            return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            await asyncio.sleep(1.2 * (attempt + 1))
    raise RuntimeError(f"{seg['id']} 配音失败：{last_error}")


async def synth_all(force: bool) -> None:
    sem = asyncio.Semaphore(3)

    async def bound(seg: dict) -> None:
        async with sem:
            await synth_one(seg, force)
            print("voice", seg["id"], flush=True)

    await asyncio.gather(*(bound(seg) for seg in SEGMENTS))


def gap_after(seg: dict, nxt: dict | None) -> float:
    if "gap_after" in seg:
        return float(seg["gap_after"])
    if nxt is None:
        return 0.0
    if nxt["scene"] != seg["scene"]:
        return 0.16
    return 0.09


def build_timeline() -> tuple[list[dict], np.ndarray]:
    pieces: list[np.ndarray] = []
    spans: list[dict] = []
    cursor = 0

    def add(samples: np.ndarray, seg_index: int, text: str) -> None:
        nonlocal cursor
        if len(samples) == 0:
            return
        spans.append({"s0": cursor, "s1": cursor + len(samples), "seg": seg_index, "sub": text})
        pieces.append(samples)
        cursor += len(samples)

    add(np.zeros(sec_to_n(LEAD), np.int16), 0, "")
    for index, seg in enumerate(SEGMENTS):
        samples = read_wav(seg["wav"])
        raw = json.loads(seg["words_path"].read_text(encoding="utf-8"))
        clip_dur = len(samples) / SR
        scale = detect_scale(raw, clip_dur)
        words = normalize_words(raw, scale)
        cues = phrases_to_cues(seg, words, clip_dur)
        ranges = []
        for cue in cues:
            start_n = int(round(cue["start"] * SR))
            end_n = int(round(cue["end"] * SR))
            ranges.append([start_n, end_n, cue["text"]])
        if not ranges:
            ranges = [[0, len(samples), polish_sub(seg["voice"])]]
        ranges[0][0] = 0
        ranges[-1][1] = len(samples)
        for left, right in zip(ranges, ranges[1:]):
            left[1] = right[0]
        walked = 0
        last_text = ranges[-1][2]
        for start_n, end_n, text in ranges:
            start_n = max(walked, min(start_n, len(samples)))
            end_n = max(start_n, min(end_n, len(samples)))
            if end_n > start_n:
                add(samples[start_n:end_n], index, text)
                last_text = text
                walked = end_n
        if walked < len(samples):
            add(samples[walked:], index, last_text)
        extra = max(0, sec_to_n(float(seg.get("min_hold", 0))) - len(samples))
        if extra:
            add(np.zeros(extra, np.int16), index, last_text)
        nxt = SEGMENTS[index + 1] if index + 1 < len(SEGMENTS) else None
        gap_n = sec_to_n(gap_after(seg, nxt))
        if gap_n:
            add(np.zeros(gap_n, np.int16), index, last_text)
    add(np.zeros(sec_to_n(TAIL), np.int16), len(SEGMENTS) - 1, spans[-1]["sub"] if spans else "")
    merged = []
    for span in spans:
        if (
            merged
            and merged[-1]["seg"] == span["seg"]
            and merged[-1]["sub"] == span["sub"]
            and merged[-1]["s1"] == span["s0"]
        ):
            merged[-1]["s1"] = span["s1"]
        else:
            merged.append(span)
    audio = np.concatenate(pieces)
    if merged[-1]["s1"] != len(audio):
        raise SystemExit("时间轴和音频长度不一致")
    return merged, audio


def write_srt(spans: list[dict]) -> None:
    cues = []
    for span in spans:
        text = span["sub"].strip()
        if not text:
            continue
        start = span["s0"] / SR
        end = span["s1"] / SR
        if cues and cues[-1]["text"] == text and abs(cues[-1]["end"] - start) < 0.02:
            cues[-1]["end"] = end
        else:
            cues.append({"start": start, "end": end, "text": text})

    def stamp(seconds: float) -> str:
        ms = max(0, int(round(seconds * 1000)))
        hours, ms = divmod(ms, 3_600_000)
        minutes, ms = divmod(ms, 60_000)
        secs, ms = divmod(ms, 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"

    blocks = []
    for index, cue in enumerate(cues, 1):
        blocks.append(f"{index}\n{stamp(cue['start'])} --> {stamp(cue['end'])}\n{cue['text']}\n")
    (ROOT / "字幕.srt").write_text("\n".join(blocks), encoding="utf-8")


def assemble(spans: list[dict], audio: np.ndarray) -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    total = len(audio)
    concat_path = BUILD / "frames.txt"
    lines = ["ffconcat version 1.0"]
    for index, span in enumerate(spans):
        frame = render_frame(SEGMENTS[span["seg"]], span["sub"])
        path = FRAMES / f"frame_{index:04d}.png"
        frame.convert("RGB").save(path)
        duration = (span["s1"] - span["s0"]) / SR
        lines.append(f"file '{path}'")
        lines.append(f"duration {duration:.6f}")
        if index % 10 == 0:
            print(f"frame {index+1}/{len(spans)}  p={span['s1']/total:.2f}", flush=True)
    lines.append(f"file '{FRAMES / f'frame_{len(spans)-1:04d}.png'}'")
    concat_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    voice = BUILD / "voice.wav"
    write_wav(voice, audio)
    normal = BUILD / "voice-normal.wav"
    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(voice),
            "-af",
            "loudnorm=I=-16:LRA=11:TP=-1.5",
            str(normal),
        ]
    )
    silent = BUILD / "silent.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_path),
            "-vf",
            "fps=30,format=yuv420p",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(silent),
        ]
    )

    def probe(path: Path) -> float:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
            text=True,
        )
        return float(out.strip())

    video_dur = probe(silent)
    audio_dur = probe(normal)
    video_filter = []
    audio_filter = []
    if video_dur + 0.04 < audio_dur:
        video_filter = ["-vf", f"tpad=stop_mode=clone:stop_duration={audio_dur - video_dur + 0.05}"]
    if audio_dur + 0.04 < video_dur:
        audio_filter = ["-af", f"apad=pad_dur={video_dur - audio_dur + 0.05}"]
    out = ROOT / "后摩论文科研研究Skill-写作流水线-小红书.mp4"
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(normal)]
    # tpad must be on video stream; putting -vf before output is ok with two inputs if mapped.
    if video_filter:
        cmd += video_filter
    if audio_filter:
        cmd += audio_filter
    cmd += ["-map", "0:v:0", "-map", "1:a:0"]
    if video_filter:
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p"]
    else:
        cmd += ["-c:v", "copy"]
    cmd += [
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "48000",
        "-movflags",
        "+faststart",
        "-shortest",
        str(out),
    ]
    run(cmd)
    final_dur = probe(out)
    print(f"video {out}")
    print(f"duration {final_dur:.2f}s  spans {len(spans)}  video {video_dur:.2f}  audio {audio_dur:.2f}")
    if not (60 <= final_dur <= 180):
        print("WARNING: duration outside 1–3 minutes")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--guides", action="store_true")
    parser.add_argument("--cues", action="store_true")
    parser.add_argument("--force-audio", action="store_true")
    args = parser.parse_args()
    global BG
    ensure_fonts()
    init_faces()
    BG = make_bg(W, H)
    write_voice_md()
    if args.preview:
        render_preview(args.guides)
        return
    if args.cues:
        asyncio.run(synth_all(args.force_audio))
        spans, audio = build_timeline()
        print(f"timeline {len(audio)/SR:.2f}s  spans {len(spans)}")
        for span in spans:
            if span["sub"]:
                print(f"{span['s0']/SR:6.2f} {SEGMENTS[span['seg']]['id']} {span['sub']}")
        return
    asyncio.run(synth_all(args.force_audio))
    spans, audio = build_timeline()
    duration = len(audio) / SR
    print(f"timeline {duration:.2f}s  spans {len(spans)}")
    per = []
    for index, seg in enumerate(SEGMENTS):
        owned = [span for span in spans if span["seg"] == index]
        if not owned:
            continue
        per.append(f"{seg['id']} {(owned[-1]['s1']-owned[0]['s0'])/SR:.1f}s")
    print(" ".join(per))
    write_srt(spans)
    render_cover_image().convert("RGB").save(ROOT / "封面.png", quality=95)
    assemble(spans, audio)


if __name__ == "__main__":
    main()
