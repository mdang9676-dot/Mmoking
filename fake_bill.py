"""Module Fake Bill v5 — Template based with NotoSans font
/fakebill bank_gui so_tien bdsd bank_nhan ten_gui ten_nhan noidung
VD: /fakebill agribank 5000000 yes acb Nguyen_Van_A Tran_Thi_B Chuyen tien
"""
import os, random, re
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# ── Font helpers ──
# Tự động tìm font trên mọi hệ thống (Linux, Android, Windows, macOS)
_FONT_CANDIDATES_REG = [
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/system/fonts/Roboto-Regular.ttf",
    "/system/fonts/DroidSans.ttf",
    "/system/fonts/NotoSansCJK-Regular.ttc",
    "/system/fonts/NotoSans-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/Library/Fonts/Arial.ttf",
]
_FONT_CANDIDATES_BOLD = [
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/system/fonts/Roboto-Bold.ttf",
    "/system/fonts/DroidSans-Bold.ttf",
    "/system/fonts/NotoSansCJK-Bold.ttc",
    "/system/fonts/NotoSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]

def _find_font(candidates):
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

_FONT_REG = _find_font(_FONT_CANDIDATES_REG)
_FONT_BOLD = _find_font(_FONT_CANDIDATES_BOLD)

# Nếu không có font nào, dùng default (nhưng sẽ nhỏ)
def _font(size, bold=False):
    path = _FONT_BOLD if bold else _FONT_REG
    if path:
        try:
            return ImageFont.truetype(path, size)
        except:
            pass
    # Fallback: default font (cố gắng set size nếu Pillow hỗ trợ)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()

def _text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def _draw_text(img, draw, text, cfg, img_w):
    font = _font(cfg["size"], cfg.get("bold", False))
    color = cfg["color"]
    tw, th = _text_size(draw, text, font)
    if cfg.get("center"):
        x = (img_w - tw) // 2 + cfg.get("offset_x", 0)
        y = cfg["y"]
    elif cfg.get("align_right"):
        x = img_w - tw - cfg["align_right"]
        y = cfg["y"]
    else:
        x, y = cfg["pos"]
    draw.text((x, y), text, font=font, fill=color)

# ── Helpers ──
def _fmt_money(amount):
    try:
        num = int(str(amount).replace(",", "").replace(".", ""))
        return f"{num:,}"
    except:
        return amount

def _rand_time(custom_time=None):
    from datetime import datetime, timedelta
    if custom_time:
        parts = custom_time.split(":")
        hour = int(parts[0])
        minute = int(parts[1])
        second = int(parts[2]) if len(parts) > 2 else random.randint(0, 59)
        dt = datetime.now().replace(hour=hour, minute=minute, second=second, microsecond=0)
        dt = dt - timedelta(days=random.randint(0, 7))
        return custom_time, dt.strftime("%d-%m-%Y %H:%M:%S")
    dt = datetime.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return dt.strftime("%H:%M"), dt.strftime("%d-%m-%Y %H:%M:%S")

def _rand_trans():
    return "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(12)])

def _rand_acc():
    return "".join([str(random.randint(0, 9)) for _ in range(random.randint(10, 16))])

# ── Bank Templates ──
BANK_TEMPLATES = {
    "agribank": {
        "name": "Agribank",
        "template": "agribank/argibank.png",
        "android": "agribank/agri910.png",
        "fields": {
            "time_dt":     {"pos": (33, 43),  "size": 22, "color": (0, 0, 0),       "bold": False},
            "amount":      {"y": 245,        "size": 44, "color": (167, 39, 71),   "bold": True,  "center": True},
            "magiaodich":  {"pos": (340, 255),"size": 22, "color": (74, 74, 74),    "bold": False},
            "name_nhan":   {"pos": (300, 405),"size": 22, "color": (59, 59, 59),    "bold": True},
            "stk_nhan":    {"pos": (300, 455),"size": 22, "color": (59, 59, 59),    "bold": True},
            "bank_nhan":   {"pos": (300, 505),"size": 20, "color": (59, 59, 59),    "bold": True},
            "time_bill":   {"pos": (300, 605),"size": 22, "color": (59, 59, 59),    "bold": True},
            "noidung":     {"pos": (300, 685),"size": 20, "color": (59, 59, 59),    "bold": True},
        },
        "pin_dir": "agribank",
        "pin_pos": {"x": -60, "y": 27, "w": -51, "h": -23},
        "noti": "agribank/noti.png",
        "noti_pos": (7, 65),
        "noti_text": [
            {"pos": (100, 107), "size": 15, "color": (11, 11, 11), "text": "Argibank thong bao"},
            {"pos": (100, 137), "size": 14, "color": (11, 11, 11), "text": "bdsd_msg"},
        ],
    },
    "acb": {
        "name": "ACB",
        "template": "acb/acb.png",
        "fields": {
            "time_dt":     {"pos": (115, 78),  "size": 40, "color": (0, 0, 0),       "bold": False},
            "amount":      {"y": 520,          "size": 56, "color": (0, 117, 255),   "bold": True,  "center": True},
            "name_gui":    {"pos": (330, 640),  "size": 30, "color": (68, 75, 81),    "bold": True},
            "stk_gui":     {"pos": (330, 690),  "size": 26, "color": (68, 75, 81),    "bold": False},
            "name_nhan":   {"pos": (330, 800), "size": 30, "color": (68, 75, 81),    "bold": True},
            "stk_nhan":    {"pos": (330, 850), "size": 26, "color": (68, 75, 81),    "bold": False},
            "bank_nhan":   {"y": 2140,         "size": 44, "color": (50, 63, 75),    "bold": False, "align_right": 130},
            "time_bill":   {"pos": (330, 1020), "size": 32, "color": (68, 75, 81),    "bold": False},
            "magiaodich":  {"pos": (330, 1120), "size": 28, "color": (68, 75, 81),    "bold": False},
            "noidung":     {"pos": (58, 1260),  "size": 30, "color": (68, 75, 81),    "bold": False},
        },
        "pin_dir": "acb",
        "pin_pos": {"x": -150, "y": 47, "w": 65, "h": 35},
        "bdsd_template": "acb/bdsd-acb.png",
        "bdsd_pos": (7, 120),
        "bdsd_text": [
            {"pos": (63, 340), "size": 21, "color": (0, 0, 0), "text": "acb_bdsd1"},
            {"pos": (63, 390), "size": 21, "color": (0, 0, 0), "text": "acb_bdsd2"},
            {"pos": (63, 440), "size": 21, "color": (0, 0, 0), "text": "acb_bdsd3"},
        ],
    },
    "bidv": {
        "name": "BIDV",
        "template": "bidv/bidv.png",
        "fields": {
            "amount":      {"y": 640,  "size": 52, "color": (0, 122, 94),  "bold": True,  "center": True},
            "vnd_label":   {"y": 705,  "size": 28, "color": (0, 122, 94),  "bold": False, "center": True},
            "magiaodich":  {"y": 745,  "size": 24, "color": (80, 80, 80),  "bold": False, "center": True},
            "time_bill":   {"y": 780,  "size": 24, "color": (80, 80, 80),  "bold": False, "center": True},
            "name_gui":    {"y": 830,  "size": 28, "color": (50, 50, 50),  "bold": True,  "center": True},
            "name_nhan":   {"y": 875,  "size": 28, "color": (50, 50, 50),  "bold": True,  "center": True},
            "noidung":     {"y": 920,  "size": 24, "color": (80, 80, 80),  "bold": False, "center": True},
        },
        "pin_dir": "bidv",
        "pin_pos": {"x": -120, "y": 35, "w": 80, "h": 38},
        "bdsd_template": "bidv/bdsd-bidv.png",
        "bdsd_crop": (0, 0, 947, 280),
        "bdsd_pos": (10, 100),
        "bdsd_text": [
            {"pos": (80, 140), "size": 20, "color": (0, 0, 0), "text": "bidv_bdsd1"},
            {"pos": (80, 180), "size": 20, "color": (0, 0, 0), "text": "bidv_bdsd2"},
        ],
    },
    "binance": {
        "name": "Binance",
        "template": "binance/bg-wifi.png",
        "template_4g": "binance/bg-4g.png",
        "fields": {
            "time_dt":     {"pos": (150, 110), "size": 52, "color": (255, 255, 255), "bold": False},
            "amount_vnd":  {"y": 680,  "size": 82, "color": (255, 255, 255), "bold": True,  "center": True, "padding": 30},
            "amount_usdt": {"y": 780,  "size": 48, "color": (255, 255, 255), "bold": False, "center": True},
            "vnd_symbol":  {"y": 670,  "size": 60, "color": (255, 255, 255), "bold": True,  "center": True, "offset_x": -250},
        },
        "pin_dir": "binance",
        "pin_pos": {"x": 1079, "y": 62, "w": 97, "h": 46},
    },
}

ALL_BANKS = ["Agribank", "ACB", "BIDV", "Binance"]

# ── Main function ──
def create_fake_bill(bank_code, amount, bdsd, content, bank_nhan, output_path, ten_gui="", ten_nhan="", custom_time=None):
    bank_code = bank_code.lower().strip()
    if bank_code not in BANK_TEMPLATES:
        return f"❌ Ngan hang khong ho tro: {bank_code}.\nCac bank co template: {', '.join(BANK_TEMPLATES.keys())}"

    cfg = BANK_TEMPLATES[bank_code]
    template_path = os.path.join(ASSETS_DIR, cfg["template"])
    if not os.path.exists(template_path):
        return f"❌ Khong tim thay template: {template_path}"

    img = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    img_w, img_h = img.size

    time_dt, time_bill = _rand_time(custom_time)
    magd = _rand_trans()
    stk_nhan = _rand_acc()
    stk_gui = _rand_acc()
    bank_nhan_name = bank_nhan.upper() if bank_nhan else cfg["name"].upper()
    amount_fmt = _fmt_money(amount)

    bdsd_enabled = bdsd.lower() in ("yes", "co", "1", "true")

    values = {
        "time_dt": time_dt,
        "amount": amount_fmt + " VND",
        "magiaodich": magd,
        "name_nhan": (ten_nhan or "NGUYEN VAN A").upper(),
        "stk_nhan": stk_nhan,
        "bank_nhan": bank_nhan_name,
        "time_bill": time_bill,
        "noidung": (content or "CHUYEN TIEN").upper(),
        "name_gui": (ten_gui or "TRAN THI B").upper(),
        "stk_gui": stk_gui,
        "amount_vnd": amount_fmt,
        "amount_usdt": f"Ban thanh cong {amount} USDT",
        "vnd_symbol": "đ",
        "vnd_label": "VND",
    }

    for field_key, field_cfg in cfg["fields"].items():
        text = values.get(field_key, "")
        if text:
            _draw_text(img, draw, text, field_cfg, img_w)

    # ── BDSD: Agribank notification ──
    if bdsd_enabled and "noti" in cfg:
        noti_path = os.path.join(ASSETS_DIR, cfg["noti"])
        if os.path.exists(noti_path):
            try:
                noti_img = Image.open(noti_path).convert("RGBA")
                nw = img_w - 20
                nh = noti_img.height + 10
                noti_img = noti_img.resize((nw, nh), Image.LANCZOS)
                img.paste(noti_img, cfg["noti_pos"], noti_img)
                bdsd_msg = f"Argibank: {time_bill} TK: {stk_gui} (VND) - {amount_fmt} VND. ND: {content[:20]}..."
                for tcfg in cfg["noti_text"]:
                    txt = bdsd_msg if tcfg["text"] == "bdsd_msg" else tcfg["text"]
                    font = _font(tcfg["size"])
                    draw.text(tcfg["pos"], txt, font=font, fill=tcfg["color"])
            except:
                pass

    # ── BDSD: ACB / BIDV template overlay ──
    if bdsd_enabled and "bdsd_template" in cfg:
        bdsd_path = os.path.join(ASSETS_DIR, cfg["bdsd_template"])
        if os.path.exists(bdsd_path):
            try:
                bdsd_img = Image.open(bdsd_path).convert("RGBA")
                if "bdsd_crop" in cfg:
                    bdsd_img = bdsd_img.crop(cfg["bdsd_crop"])
                nw = img_w - 20
                nh = int(bdsd_img.height * (nw / bdsd_img.width))
                bdsd_img = bdsd_img.resize((nw, nh), Image.LANCZOS)
                img.paste(bdsd_img, cfg["bdsd_pos"], bdsd_img)

                if bank_code == "acb":
                    bdsd1 = f"ACB: TK {stk_gui}(VND) - {amount_fmt} luc {time_bill[:5]}."
                    bdsd2 = f"So du: {_fmt_money(random.randint(100000, 5000000))}. GD: {content[:30]}"
                    bdsd3 = f"-{time_bill[:10].replace('-', '')}"
                    for tcfg in cfg["bdsd_text"]:
                        font = _font(tcfg["size"])
                        txt = {"acb_bdsd1": bdsd1, "acb_bdsd2": bdsd2, "acb_bdsd3": bdsd3}.get(tcfg["text"], tcfg["text"])
                        draw.text(tcfg["pos"], txt, font=font, fill=tcfg["color"])
                elif bank_code == "bidv":
                    bdsd1 = f"BIDV: TK {stk_gui} - {amount_fmt} VND"
                    bdsd2 = f"{content[:35]} | {time_bill}"
                    for tcfg in cfg["bdsd_text"]:
                        font = _font(tcfg["size"])
                        txt = {"bidv_bdsd1": bdsd1, "bidv_bdsd2": bdsd2}.get(tcfg["text"], tcfg["text"])
                        draw.text(tcfg["pos"], txt, font=font, fill=tcfg["color"])
            except:
                pass

    # ── Pin battery overlay ──
    pin_dir = os.path.join(ASSETS_DIR, cfg["pin_dir"])
    pin_files = [f for f in os.listdir(pin_dir) if f.endswith(".png") and f[0].isdigit()]
    if pin_files:
        try:
            pin_file = random.choice(pin_files)
            pin_img = Image.open(os.path.join(pin_dir, pin_file)).convert("RGBA")
            pc = cfg["pin_pos"]
            pw = pin_img.width + pc["w"] if pc["w"] < 0 else pc["w"]
            ph = pin_img.height + pc["h"] if pc["h"] < 0 else pc["h"]
            px = img_w + pc["x"] if pc["x"] < 0 else pc["x"]
            py = pc["y"]
            pin_img = pin_img.resize((pw, ph), Image.LANCZOS)
            img.paste(pin_img, (px, py), pin_img)
        except:
            pass

    img = img.convert("RGB")
    img.save(output_path, "PNG")
    return output_path


def get_bank_list():
    lines = [
        "<b>🏦 DANH SACH NGAN HANG HO TRO</b>",
        "=" * 35,
        "",
        "<b>✅ Cac ngan hang co template:</b>",
    ]
    for code, info in BANK_TEMPLATES.items():
        lines.append(f"  • <code>{code}</code> — {info['name']}")
    lines.append("")
    lines.append("<b>Cach dung:</b>")
    lines.append("/fakebill bank_gui so_tien bdsd bank_nhan ten_gui ten_nhan noidung")
    lines.append("VD: /fakebill agribank 5000000 yes acb Nguyen_Van_A Tran_Thi_B Chuyen tien")
    lines.append("VD: /fakebill acb 10000000 no vietcombank Le_Quang_C Pham_Thi_D Thanh toan")
    lines.append("VD: /fakebill bidv 5000000 yes bidv Do_Van_Hung Nguyen_Thanh_Tung Chuyen tien")
    return "\n".join(lines)
