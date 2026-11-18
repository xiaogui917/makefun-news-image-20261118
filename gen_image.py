"""Image generator for make.fun competition news-image-20261118.
Generates a 1024x1024 newspaper front page summing up 18 November 2026 world news.
Deterministic rendering with Pillow.
"""

import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 1024
HEIGHT = 1024

# DejaVu Font paths
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_BOLD_PATH = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
FONT_REG_PATH = os.path.join(FONT_DIR, "DejaVuSans.ttf")

# Load fonts with specified sizes
def get_font(size, bold=False):
    path = FONT_BOLD_PATH if bold else FONT_REG_PATH
    return ImageFont.truetype(path, size)

# Color Palette
BG_PAPER = (248, 249, 250)       # Clean crisp newspaper off-white
BG_PANEL = (255, 255, 255)       # Pure white for panels
BORDER_LIGHT = (203, 213, 225)   # Slate 300
BORDER_DARK = (15, 23, 42)       # Slate 900
TEXT_MAIN = (15, 23, 42)         # Slate 900 dark charcoal
TEXT_MUTED = (71, 85, 105)       # Slate 600
TEXT_BODY = (30, 41, 59)         # Slate 800

# Category accent colors
COLOR_DIPLOMACY = (30, 58, 138)  # Deep Navy Blue
COLOR_CRIMEA = (153, 27, 27)     # Deep Crimson Red
COLOR_GULF = (194, 65, 12)       # Amber Rust
COLOR_NVIDIA = (6, 95, 70)       # Emerald Green
COLOR_CYCLONE = (15, 118, 110)   # Teal Ocean
COLOR_DHONI = (67, 56, 202)      # Indigo Blue
COLOR_YELLOW = (234, 179, 8)     # Gold Yellow
COLOR_CYAN = (6, 182, 212)       # Cyan Light Blue

def draw_rounded_panel(draw, bbox, fill, outline=BORDER_LIGHT, width=1, radius=6):
    """Draw a rectangle or rounded rectangle with a clean outline."""
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_badge(draw, text, x, y, bg_color, text_color=(255, 255, 255), font_size=11):
    """Draw a category pill badge."""
    font = get_font(font_size, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_h = 7
    pad_v = 4
    badge_rect = [x, y, x + tw + pad_h * 2, y + th + pad_v * 2]
    draw.rounded_rectangle(badge_rect, radius=4, fill=bg_color)
    draw.text((x + pad_h, y + pad_v - 1), text, fill=text_color, font=font)
    return badge_rect[2]  # Returns right edge X coordinate

def draw_wrapped_text(draw, text, x, y, max_w, font, fill=TEXT_BODY, line_spacing=4):
    """Draw text wrapped to fit within max_w pixels. Returns the bottom Y."""
    words = text.split()
    lines = []
    curr_line = []
    
    for word in words:
        test_line = " ".join(curr_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_w:
            curr_line.append(word)
        else:
            if curr_line:
                lines.append(" ".join(curr_line))
                curr_line = [word]
            else:
                lines.append(word)
                curr_line = []
    if curr_line:
        lines.append(" ".join(curr_line))
        
    curr_y = y
    for line in lines:
        draw.text((x, curr_y), line, fill=fill, font=font)
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        curr_y += line_height + line_spacing
    return curr_y

def draw_footer(draw, y=994):
    """Draw the newspaper bottom bar."""
    draw.rectangle([0, y, WIDTH, HEIGHT], fill=BORDER_DARK)
    footer_text = "THE INTERNATIONAL CHRONICLE  •  VERIFIED WORLD NEWS RECORD  •  WEDNESDAY, 18 NOVEMBER 2026"
    font = get_font(12, bold=True)
    bbox = draw.textbbox((0, 0), footer_text, font=font)
    tw = bbox[2] - bbox[0]
    tx = (WIDTH - tw) // 2
    draw.text((tx, y + 8), footer_text, fill=(241, 245, 249), font=font)


def draw_masthead(draw):
    """Draw the newspaper masthead and top date bar."""
    # Top thin line
    draw.line([(24, 18), (1000, 18)], fill=BORDER_LIGHT, width=1)
    
    # Weather & index top ear labels
    font_ear = get_font(11, bold=True)
    draw.text((28, 22), "GLOBAL EDITION", fill=TEXT_MUTED, font=font_ear)
    draw.text((865, 22), "24-HOUR WORLD WIRE", fill=TEXT_MUTED, font=font_ear)

    # Newspaper Main Title
    title = "THE WORLD CHRONICLE"
    font_title = get_font(44, bold=True)
    t_bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = t_bbox[2] - t_bbox[0]
    draw.text(((WIDTH - tw) // 2, 34), title, fill=TEXT_MAIN, font=font_title)

    # Sub-masthead Bar: Date, Edition, Volume
    bar_y = 86
    draw.line([(24, bar_y), (1000, bar_y)], fill=BORDER_DARK, width=2)
    
    font_bar = get_font(13, bold=True)
    date_str = "WEDNESDAY, 18 NOVEMBER 2026"
    draw.text((28, bar_y + 4), date_str, fill=COLOR_CRIMEA, font=font_bar)
    
    vol_str = "INTERNATIONAL DESK  •  VOL. CLXII NO. 42"
    v_bbox = draw.textbbox((0, 0), vol_str, font=font_bar)
    draw.text(((WIDTH - (v_bbox[2] - v_bbox[0])) // 2, bar_y + 4), vol_str, fill=TEXT_MUTED, font=font_bar)
    
    price_str = "FINAL RECORD EDITION"
    p_bbox = draw.textbbox((0, 0), price_str, font=font_bar)
    draw.text((1000 - (p_bbox[2] - p_bbox[0]) - 4, bar_y + 4), price_str, fill=TEXT_MAIN, font=font_bar)

    # Double separating rule
    draw.line([(24, 108), (1000, 108)], fill=BORDER_DARK, width=3)
    draw.line([(24, 113), (1000, 113)], fill=BORDER_LIGHT, width=1)


def draw_lead_story(draw, bbox):
    """Draw the prominent lead story covering the APEC, Quad, and Trilateral Summits."""
    x0, y0, x1, y1 = bbox
    draw_rounded_panel(draw, bbox, fill=BG_PANEL, outline=BORDER_LIGHT, radius=6)

    # Category Badge
    badge_right = draw_badge(draw, "DIPLOMATIC SUMMITS · ASIA-PACIFIC", x0 + 16, y0 + 12, COLOR_DIPLOMACY, font_size=11)
    
    # Secondary Location Badge
    draw_badge(draw, "SHENZHEN & MANILA", badge_right + 8, y0 + 12, (51, 65, 85), font_size=11)

    # Main Lead Headline (wrapped to avoid right-panel collision)
    hl_text = "APEC OPENS IN SHENZHEN AS QUAD CONVENES IN MANILA"
    font_hl = get_font(20, bold=True)
    hl_end_y = draw_wrapped_text(draw, hl_text, x0 + 16, y0 + 38, 560, font_hl, fill=TEXT_MAIN, line_spacing=2)

    # Subhead (Trilateral announcement wrapped)
    subhead_text = "First-Ever US-China-Russia Trilateral Summit Set for Tomorrow (19 Nov) in Shenzhen"
    font_sub = get_font(13, bold=True)
    sub_end_y = draw_wrapped_text(draw, subhead_text, x0 + 16, hl_end_y + 4, 560, font_sub, fill=COLOR_DIPLOMACY, line_spacing=2)

    # Left Column: Story details
    col_w = 560
    font_lead_bold = get_font(11, bold=True)
    font_lead_body = get_font(11, bold=False)

    bullets = [
        ("• APEC Summit Opens in Shenzhen: ", 
         "Leaders across the Pacific Rim open high-level economic dialogue in Shenzhen today, focusing on regional trade frameworks."),
        ("• Quad Leaders Convene in Manila: ", 
         "Trump arrives in Manila as US, India, Japan, and Australia confer on Indo-Pacific maritime security, cybersecurity, and AI."),
        ("• Historic Trilateral Summit Tomorrow: ", 
         "Trump, Xi, and Putin will hold a groundbreaking first-ever US-China-Russia trilateral summit on 19 November in Shenzhen."),
        ("• Canada-China Trade Pact Extended: ", 
         "President Xi Jinping meets Canadian envoy ahead of APEC, agreeing to extend bilateral trade pact.")
    ]

    curr_y = sub_end_y + 8
    for b_title, b_desc in bullets:
        draw.text((x0 + 16, curr_y), b_title, fill=TEXT_MAIN, font=font_lead_bold)
        curr_y += 16
        curr_y = draw_wrapped_text(draw, b_desc, x0 + 26, curr_y, col_w - 20, font_lead_body, fill=TEXT_BODY, line_spacing=2)
        curr_y += 4

    # Right Column: Visual Diagram / Infographic Panel (x: 615 to x1 - 14, y: y0 + 12 to y1 - 12)
    info_x0 = x0 + 592
    info_y0 = y0 + 12
    info_x1 = x1 - 14
    info_y1 = y1 - 12
    draw.rounded_rectangle([info_x0, info_y0, info_x1, info_y1], radius=6, fill=(241, 245, 249), outline=BORDER_LIGHT, width=1)

    # Infographic Header
    draw.rectangle([info_x0, info_y0, info_x1, info_y0 + 24], fill=COLOR_DIPLOMACY)
    draw.text((info_x0 + 12, info_y0 + 5), "SUMMIT DIPLOMACY MATRIX · 18 NOV 2026", fill=(255, 255, 255), font=get_font(10, bold=True))

    # Shenzhen Card
    sz_y0 = info_y0 + 30
    draw.rounded_rectangle([info_x0 + 10, sz_y0, info_x1 - 10, sz_y0 + 64], radius=4, fill=(255, 255, 255), outline=(203, 213, 225))
    draw_badge(draw, "SHENZHEN", info_x0 + 14, sz_y0 + 6, (220, 38, 38), font_size=9)
    draw.text((info_x0 + 88, sz_y0 + 8), "APEC SUMMIT OPENS", fill=TEXT_MAIN, font=get_font(11, bold=True))
    draw.text((info_x0 + 14, sz_y0 + 28), "• Pacific Rim economic & trade opening today", fill=TEXT_MUTED, font=get_font(9, bold=False))
    draw.text((info_x0 + 14, sz_y0 + 44), "• Historic US-China-Russia Summit TOMORROW (Nov 19)", fill=COLOR_CRIMEA, font=get_font(9, bold=True))

    # Manila Card
    mn_y0 = sz_y0 + 70
    draw.rounded_rectangle([info_x0 + 10, mn_y0, info_x1 - 10, mn_y0 + 62], radius=4, fill=(255, 255, 255), outline=(203, 213, 225))
    draw_badge(draw, "MANILA", info_x0 + 14, mn_y0 + 6, COLOR_DIPLOMACY, font_size=9)
    draw.text((info_x0 + 72, mn_y0 + 8), "QUAD LEADERS SUMMIT", fill=TEXT_MAIN, font=get_font(11, bold=True))
    draw.text((info_x0 + 14, mn_y0 + 28), "• Members: US, India, Japan, Australia", fill=TEXT_BODY, font=get_font(9, bold=True))
    draw.text((info_x0 + 14, mn_y0 + 43), "• Focus: Maritime security, AI, cyber & critical minerals", fill=TEXT_MUTED, font=get_font(9, bold=False))

    # Trilateral Schematic Graphic (Three leaders meeting at Shenzhen)
    tr_y0 = mn_y0 + 68
    draw.rounded_rectangle([info_x0 + 10, tr_y0, info_x1 - 10, info_y1 - 8], radius=4, fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((info_x0 + 14, tr_y0 + 6), "NOV 19 TRILATERAL SUMMIT AXIS:", fill=TEXT_MAIN, font=get_font(10, bold=True))

    # Three leader nodes
    box_w = 100
    gap = 14
    start_x = info_x0 + 14
    nodes = [
        ("TRUMP (US)", start_x, tr_y0 + 24, (30, 58, 138)),
        ("XI (CHINA)", start_x + box_w + gap, tr_y0 + 24, (220, 38, 38)),
        ("PUTIN (RUSSIA)", start_x + (box_w + gap) * 2, tr_y0 + 24, (71, 85, 105))
    ]
    for n_title, nx, ny, nc in nodes:
        draw.rounded_rectangle([nx, ny, nx + box_w, ny + 22], radius=3, fill=nc)
        t_box = draw.textbbox((0, 0), n_title, font=get_font(9, bold=True))
        tw = t_box[2] - t_box[0]
        draw.text((nx + (box_w - tw) // 2, ny + 4), n_title, fill=(255, 255, 255), font=get_font(9, bold=True))

    # Connective line to Shenzhen meeting center
    center_y = tr_y0 + 66
    mid_x = (info_x0 + info_x1) // 2
    draw.line([(start_x + box_w // 2, tr_y0 + 46), (mid_x, center_y)], fill=(148, 163, 184), width=1)
    draw.line([(start_x + box_w + gap + box_w // 2, tr_y0 + 46), (mid_x, center_y)], fill=(148, 163, 184), width=1)
    draw.line([(start_x + (box_w + gap) * 2 + box_w // 2, tr_y0 + 46), (mid_x, center_y)], fill=(148, 163, 184), width=1)
    
    center_text = "★ SHENZHEN TRILATERAL ROUNDTABLE ★"
    c_box = draw.textbbox((0, 0), center_text, font=get_font(9, bold=True))
    cw = c_box[2] - c_box[0]
    draw.rounded_rectangle([mid_x - cw//2 - 8, center_y, mid_x + cw//2 + 8, center_y + 18], radius=3, fill=(15, 23, 42))
    draw.text((mid_x - cw//2, center_y + 3), center_text, fill=(250, 204, 21), font=get_font(9, bold=True))


def draw_ukraine_block(draw, bbox):
    """Draw the Eastern Europe story block: Kerch Bridge strike."""
    x0, y0, x1, y1 = bbox
    draw_rounded_panel(draw, bbox, fill=BG_PANEL, outline=BORDER_LIGHT, radius=6)

    # Category Badge
    draw_badge(draw, "EASTERN EUROPE", x0 + 12, y0 + 10, COLOR_CRIMEA, font_size=10)

    # Headline
    hl_text = "UKRAINE STRIKES KERCH BRIDGE 2ND DAY"
    draw.text((x0 + 12, y0 + 32), hl_text, fill=TEXT_MAIN, font=get_font(13, bold=True))

    # Graphic: Tactical Kerch Bridge / Strait diagram
    gx0, gy0, gx1, gy1 = x0 + 12, y0 + 54, x1 - 12, y0 + 114
    draw.rounded_rectangle([gx0, gy0, gx1, gy1], radius=4, fill=(30, 41, 59))
    # Water channel
    draw.rectangle([gx0, gy0 + 20, gx1, gy1 - 10], fill=(15, 23, 42))
    # Bridge spans across water
    draw.line([(gx0 + 15, gy0 + 30), (gx1 - 15, gy0 + 30)], fill=(203, 213, 225), width=3)
    # Bridge arches
    draw.arc([gx0 + 40, gy0 + 15, gx0 + 110, gy0 + 45], start=180, end=0, fill=(250, 204, 21), width=2)
    draw.arc([gx0 + 120, gy0 + 15, gx0 + 190, gy0 + 45], start=180, end=0, fill=(250, 204, 21), width=2)
    # Strike impact marker
    draw.ellipse([gx0 + 145, gy0 + 22, gx0 + 165, gy0 + 38], fill=(239, 68, 68), outline=(254, 240, 138), width=2)
    draw.text((gx0 + 10, gy0 + 5), "KERCH STRAIT BRIDGE", fill=(203, 213, 225), font=get_font(9, bold=True))
    draw.text((gx1 - 118, gy0 + 44), "TARGET HIT: DAY 2", fill=(248, 113, 113), font=get_font(9, bold=True))

    # Bullet points
    font_b = get_font(10, bold=False)
    font_bold = get_font(10, bold=True)
    bullets = [
        "• Ukraine strikes Kerch/Crimea Bridge for a second consecutive day.",
        "• Russia retaliates with heavy strikes targeting bridges in Kyiv.",
        "• UN reports 372 civilian casualties in Ukraine during October."
    ]
    curr_y = y0 + 122
    for b in bullets:
        curr_y = draw_wrapped_text(draw, b, x0 + 12, curr_y, (x1 - x0) - 24, font_b, fill=TEXT_BODY, line_spacing=3)
        curr_y += 3


def draw_iran_bahrain_block(draw, bbox):
    """Draw the Middle East story block: Iran drone strike on US radar in Bahrain & Kuwait intercepts."""
    x0, y0, x1, y1 = bbox
    draw_rounded_panel(draw, bbox, fill=BG_PANEL, outline=BORDER_LIGHT, radius=6)

    # Category Badge
    draw_badge(draw, "MIDDLE EAST", x0 + 12, y0 + 10, COLOR_GULF, font_size=10)

    # Headline
    hl_text = "IRAN DRONES TARGET US RADAR IN BAHRAIN"
    draw.text((x0 + 12, y0 + 32), hl_text, fill=TEXT_MAIN, font=get_font(12, bold=True))

    # Graphic: Tactical Radar & Drone Intercept
    gx0, gy0, gx1, gy1 = x0 + 12, y0 + 54, x1 - 12, y0 + 114
    draw.rounded_rectangle([gx0, gy0, gx1, gy1], radius=4, fill=(15, 23, 42))
    # Radar display
    rcx, rcy = gx0 + 46, gy0 + 30
    draw.ellipse([rcx - 22, rcy - 22, rcx + 22, rcy + 22], outline=(16, 185, 129), width=1)
    draw.ellipse([rcx - 12, rcy - 12, rcx + 12, rcy + 12], outline=(16, 185, 129), width=1)
    draw.line([(rcx - 22, rcy), (rcx + 22, rcy)], fill=(5, 150, 105), width=1)
    draw.line([(rcx, rcy - 22), (rcx, rcy + 22)], fill=(5, 150, 105), width=1)
    draw.line([(rcx, rcy), (rcx + 16, rcy - 16)], fill=(52, 211, 153), width=2)
    # Tactical badges
    draw.text((gx0 + 78, gy0 + 8), "SHEIKH ISA BASE RADAR", fill=(203, 213, 225), font=get_font(9, bold=True))
    draw_badge(draw, "KUWAIT: DRONES INTERCEPTED", gx0 + 78, gy0 + 24, (30, 58, 138), font_size=8)
    draw_badge(draw, "BAHRAIN ALERT LIFTED", gx0 + 78, gy0 + 42, (180, 83, 9), font_size=8)

    # Bullet points
    font_b = get_font(10, bold=False)
    bullets = [
        "• IRGC claims drone strike on US military radar facility in Bahrain.",
        "• Kuwait reports air defenses intercepted drones over territory.",
        "• Bahrain issues potential security alert across Gulf, later cleared."
    ]
    curr_y = y0 + 122
    for b in bullets:
        curr_y = draw_wrapped_text(draw, b, x0 + 12, curr_y, (x1 - x0) - 24, font_b, fill=TEXT_BODY, line_spacing=3)
        curr_y += 3


def draw_nvidia_block(draw, bbox):
    """Draw the Markets/Tech story block: Nvidia Q3 doubled revenue."""
    x0, y0, x1, y1 = bbox
    draw_rounded_panel(draw, bbox, fill=BG_PANEL, outline=BORDER_LIGHT, radius=6)

    # Category Badge
    draw_badge(draw, "MARKETS & TECH", x0 + 12, y0 + 10, COLOR_NVIDIA, font_size=10)

    # Headline
    hl_text = "NVIDIA REVENUE DOUBLES TO $115.8B"
    draw.text((x0 + 12, y0 + 32), hl_text, fill=TEXT_MAIN, font=get_font(13, bold=True))

    # Graphic: Revenue surge comparison chart
    gx0, gy0, gx1, gy1 = x0 + 12, y0 + 54, x1 - 12, y0 + 114
    draw.rounded_rectangle([gx0, gy0, gx1, gy1], radius=4, fill=(241, 245, 249), outline=(203, 213, 225))
    # Bar 1 (Prior Year)
    draw.rectangle([gx0 + 20, gy0 + 32, gx0 + 55, gy1 - 6], fill=(148, 163, 184))
    draw.text((gx0 + 20, gy0 + 18), "1X", fill=TEXT_MUTED, font=get_font(9, bold=True))
    # Bar 2 (Q3 Doubled Revenue)
    draw.rectangle([gx0 + 65, gy0 + 10, gx0 + 100, gy1 - 6], fill=(5, 150, 105))
    draw.text((gx0 + 65, gy0 - 2), "2X", fill=(5, 150, 105), font=get_font(9, bold=True))
    # Surge badge
    draw.text((gx0 + 115, gy0 + 10), "Q3 REVENUE: $115.84B", fill=TEXT_MAIN, font=get_font(10, bold=True))
    draw.text((gx0 + 115, gy0 + 26), "• Doubled year-over-year", fill=(5, 150, 105), font=get_font(9, bold=True))
    draw.text((gx0 + 115, gy0 + 42), "• Jensen Huang ouster stands", fill=COLOR_CRIMEA, font=get_font(9, bold=False))

    # Bullet points
    font_b = get_font(10, bold=False)
    bullets = [
        "• Nvidia reports record $115.84B revenue, doubling year-over-year.",
        "• First earnings since surprise board ouster of CEO Jensen Huang.",
        "• Board confirms removal stands despite Trump backing reinstatement."
    ]
    curr_y = y0 + 122
    for b in bullets:
        curr_y = draw_wrapped_text(draw, b, x0 + 12, curr_y, (x1 - x0) - 24, font_b, fill=TEXT_BODY, line_spacing=3)
        curr_y += 3


def draw_cyclone_block(draw, bbox):
    """Draw the Bay of Bengal / Weather story block: Cyclone Akvan."""
    x0, y0, x1, y1 = bbox
    draw_rounded_panel(draw, bbox, fill=BG_PANEL, outline=BORDER_LIGHT, radius=6)

    # Category Badge
    draw_badge(draw, "WEATHER & CLIMATE", x0 + 14, y0 + 10, COLOR_CYCLONE, font_size=10)
    
    # Headline across top
    hl_text = "CYCLONE AKVAN INTENSIFIES IN BAY OF BENGAL"
    draw.text((x0 + 14, y0 + 30), hl_text, fill=TEXT_MAIN, font=get_font(14, bold=True))

    # Left Column: Story details (width = 270)
    font_b = get_font(10, bold=False)
    bullets = [
        "• Severe cyclonic storm Akvan strengthens rapidly over Bay of Bengal.",
        "• Tracking northwest toward east coast of India with rising intensity.",
        "• Forecast landfall on 20 November along Andhra Pradesh coast.",
        "• Regional authorities issue storm warnings and mobilize relief units."
    ]
    curr_y = y0 + 56
    for b in bullets:
        curr_y = draw_wrapped_text(draw, b, x0 + 14, curr_y, 270, font_b, fill=TEXT_BODY, line_spacing=3)
        curr_y += 3

    # Right Column: Satellite storm radar map (below headline)
    rx0, ry0, rx1, ry1 = x1 - 176, y0 + 56, x1 - 14, y1 - 14
    draw.rounded_rectangle([rx0, ry0, rx1, ry1], radius=6, fill=(15, 23, 42), outline=BORDER_LIGHT)

    # Coastline sketch (India East Coast)
    draw.line([(rx0 + 18, ry0 + 10), (rx0 + 32, ry0 + 50), (rx0 + 42, ry0 + 105), (rx0 + 68, ry1 - 32)], fill=(71, 85, 105), width=3)
    draw.text((rx0 + 8, ry0 + 10), "INDIA", fill=(148, 163, 184), font=get_font(9, bold=True))
    draw.text((rx0 + 8, ry0 + 65), "ANDHRA", fill=(250, 204, 21), font=get_font(9, bold=True))
    draw.text((rx0 + 8, ry0 + 78), "PRADESH", fill=(250, 204, 21), font=get_font(9, bold=True))

    # Cyclone Vortex & Spiral Arcs in Bay of Bengal
    cx, cy = rx0 + 105, ry0 + 75
    draw.arc([cx - 28, cy - 28, cx + 28, cy + 28], start=45, end=270, fill=(56, 189, 248), width=3)
    draw.arc([cx - 18, cy - 18, cx + 18, cy + 18], start=180, end=45, fill=(125, 211, 252), width=2)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(239, 68, 68), outline=(255, 255, 255), width=2)

    # Forecast trajectory arrow
    draw.line([(cx - 8, cy - 2), (rx0 + 44, ry0 + 72)], fill=(248, 113, 113), width=2)

    # Radar map labels
    draw.text((rx0 + 60, ry0 + 10), "BAY OF BENGAL", fill=(56, 189, 248), font=get_font(8, bold=True))
    draw.rounded_rectangle([rx0 + 14, ry1 - 26, rx1 - 14, ry1 - 8], radius=3, fill=(185, 28, 28))
    draw.text((rx0 + 22, ry1 - 22), "LANDFALL: 20 NOV", fill=(255, 255, 255), font=get_font(9, bold=True))


def draw_dhoni_block(draw, bbox):
    """Draw the Sports story block: MS Dhoni IPL Retirement."""
    x0, y0, x1, y1 = bbox
    draw_rounded_panel(draw, bbox, fill=BG_PANEL, outline=BORDER_LIGHT, radius=6)

    # Category Badge
    draw_badge(draw, "CRICKET & SPORTS", x0 + 14, y0 + 10, COLOR_DHONI, font_size=10)
    
    # Headline across top
    hl_text = "MS DHONI RETIRES FROM IPL, NAMED CSK MENTOR"
    draw.text((x0 + 14, y0 + 30), hl_text, fill=TEXT_MAIN, font=get_font(14, bold=True))

    # Left Column: Story details (width = 270)
    font_b = get_font(10, bold=False)
    bullets = [
        "• Legendary captain MS Dhoni officially retires as an active IPL player.",
        "• Transitions immediately into full-time mentorship role for CSK.",
        "• Concludes historic playing career with Chennai Super Kings.",
        "• Celebrated as one of cricket's all-time greatest captains and finishers."
    ]
    curr_y = y0 + 56
    for b in bullets:
        curr_y = draw_wrapped_text(draw, b, x0 + 14, curr_y, 270, font_b, fill=TEXT_BODY, line_spacing=3)
        curr_y += 3

    # Right Column: CSK Tribute Badge / Cricket Crest (below headline)
    rx0, ry0, rx1, ry1 = x1 - 176, y0 + 56, x1 - 14, y1 - 14
    draw.rounded_rectangle([rx0, ry0, rx1, ry1], radius=6, fill=(254, 240, 138), outline=(234, 179, 8))

    # Crest Header
    draw.rectangle([rx0, ry0, rx1, ry0 + 22], fill=(30, 58, 138))
    draw.text((rx0 + 18, ry0 + 5), "CHENNAI SUPER KINGS", fill=(255, 255, 255), font=get_font(8, bold=True))

    # Big #7 Icon
    draw.ellipse([rx0 + 54, ry0 + 30, rx1 - 54, ry0 + 74], fill=(30, 58, 138), outline=(234, 179, 8), width=2)
    draw.text((rx0 + 66, ry0 + 38), "#7", fill=(250, 204, 21), font=get_font(20, bold=True))

    # Cricket equipment: Bat & Wickets sketch
    wx = rx0 + 32
    wy = ry0 + 84
    # 3 Wickets
    draw.line([(wx, wy), (wx, wy + 32)], fill=(180, 83, 9), width=2)
    draw.line([(wx + 8, wy), (wx + 8, wy + 32)], fill=(180, 83, 9), width=2)
    draw.line([(wx + 16, wy), (wx + 16, wy + 32)], fill=(180, 83, 9), width=2)
    draw.line([(wx - 2, wy), (wx + 18, wy)], fill=(180, 83, 9), width=2)
    # Cricket Bat
    draw.line([(wx + 62, wy - 4), (wx + 34, wy + 32)], fill=(146, 64, 14), width=4)
    # Red Cricket Ball
    draw.ellipse([wx + 76, wy + 14, wx + 90, wy + 28], fill=(220, 38, 38), outline=(255, 255, 255), width=1)

    # Bottom tribute label
    draw.rounded_rectangle([rx0 + 10, ry1 - 26, rx1 - 10, ry1 - 8], radius=3, fill=(15, 23, 42))
    draw.text((rx0 + 16, ry1 - 22), "LEGEND • CSK MENTOR", fill=(250, 204, 21), font=get_font(9, bold=True))


def main():
    """Generate the deterministic 1024x1024 front page image."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_PAPER)
    draw = ImageDraw.Draw(img)

    # 1. Masthead
    draw_masthead(draw)

    # 2. Lead Story Block (APEC / Quad / Trilateral Summit)
    draw_lead_story(draw, [24, 118, 1000, 442])

    # 3. Row 1 Blocks (Ukraine, Bahrain/US Radar, Nvidia)
    draw_ukraine_block(draw, [24, 452, 340, 714])
    draw_iran_bahrain_block(draw, [354, 452, 670, 714])
    draw_nvidia_block(draw, [684, 452, 1000, 714])

    # 4. Row 2 Blocks (Cyclone Akvan, MS Dhoni)
    draw_cyclone_block(draw, [24, 724, 506, 986])
    draw_dhoni_block(draw, [520, 724, 1000, 986])

    # 5. Bottom Footer
    draw_footer(draw, 994)

    # Save deterministic image
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "picture.png")
    img.save(output_path, "PNG", optimize=True)
    print(f"Generated {output_path} successfully. Size: {os.path.getsize(output_path)} bytes.")


if __name__ == "__main__":
    main()


