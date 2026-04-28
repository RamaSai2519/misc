from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

W, H = A4
OUT = "May_2026_Budget_Chandika.pdf"

doc = SimpleDocTemplate(OUT, pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=18*mm, bottomMargin=18*mm)

# Colors
C_TEAL      = colors.HexColor("#1D9E75")
C_TEAL_LT   = colors.HexColor("#E1F5EE")
C_CORAL     = colors.HexColor("#D85A30")
C_CORAL_LT  = colors.HexColor("#FAECE7")
C_BLUE      = colors.HexColor("#378ADD")
C_BLUE_LT   = colors.HexColor("#E6F1FB")
C_AMBER     = colors.HexColor("#EF9F27")
C_AMBER_LT  = colors.HexColor("#FAEEDA")
C_PURPLE    = colors.HexColor("#7F77DD")
C_PURPLE_LT = colors.HexColor("#EEEDFE")
C_GRAY      = colors.HexColor("#888780")
C_GRAY_LT   = colors.HexColor("#F1EFE8")
C_WARN      = colors.HexColor("#BA7517")
C_WARN_LT   = colors.HexColor("#FAC775")
C_BG        = colors.HexColor("#F8F7F4")
C_BORDER    = colors.HexColor("#D3D1C7")
C_TEXT      = colors.HexColor("#2C2C2A")
C_MUTED     = colors.HexColor("#5F5E5A")
C_WHITE     = colors.white

styles = getSampleStyleSheet()

def sty(name, **kw):
    base = styles.get(name, styles['Normal'])
    return ParagraphStyle(name+'_custom', parent=base, **kw)

title_sty    = sty('Normal', fontSize=22, fontName='Helvetica-Bold', textColor=C_TEXT, spaceAfter=2)
sub_sty      = sty('Normal', fontSize=13, fontName='Helvetica', textColor=C_MUTED, spaceAfter=0)
sec_sty      = sty('Normal', fontSize=10, fontName='Helvetica-Bold', textColor=C_MUTED, spaceBefore=16, spaceAfter=6, leading=14)
body_sty     = sty('Normal', fontSize=10, fontName='Helvetica', textColor=C_TEXT, leading=15)
small_sty    = sty('Normal', fontSize=9, fontName='Helvetica', textColor=C_MUTED, leading=13)
tip_sty      = sty('Normal', fontSize=9, fontName='Helvetica', textColor=C_TEAL, leading=14)
warn_sty     = sty('Normal', fontSize=9, fontName='Helvetica', textColor=C_WARN, leading=14)
bold_sty     = sty('Normal', fontSize=10, fontName='Helvetica-Bold', textColor=C_TEXT, leading=14)
right_sty    = sty('Normal', fontSize=10, fontName='Helvetica-Bold', textColor=C_TEXT, alignment=TA_RIGHT)
muted_r_sty  = sty('Normal', fontSize=9, fontName='Helvetica', textColor=C_MUTED, alignment=TA_RIGHT)

def fmt(n):
    return "Rs. {:,.0f}".format(n)

def pct_bar_text(amount, salary):
    p = min(100, round(amount / salary * 100))
    filled = int(p / 5)
    bar = chr(9608) * filled + chr(9617) * (20 - filled)
    return f"{bar}  {p}%"

# Budget values
SALARY   = 41500
RENT     = 10500
NETFLIX  = 199
LENDEN   = 3000
CANTEEN  = 1800
ZOMATO   = 2500
ZEPTO    = 800
AMAZON   = 1000
TRANSPORT= 500
WALLET   = 300
BUFFER   = 1000

FOOD_TOTAL   = CANTEEN + ZOMATO + ZEPTO
FIXED_TOTAL  = RENT + NETFLIX + LENDEN
DISC_TOTAL   = AMAZON + TRANSPORT + WALLET + BUFFER
TOTAL        = FIXED_TOTAL + FOOD_TOTAL + DISC_TOTAL
SURPLUS      = SALARY - TOTAL
LENDEN_RET   = 550  # estimated monthly return

story = []

# ── Header block ──────────────────────────────────────────────────────────────
header_data = [[
    Paragraph("May 2026 — Monthly Budget", title_sty),
    Paragraph("Chandika Rama Sathya Sai", sub_sty)
]]
header_tbl = Table(header_data, colWidths=[doc.width])
header_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), C_BG),
    ('ROUNDEDCORNERS', [8]),
    ('TOPPADDING', (0,0), (-1,-1), 14),
    ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ('LEFTPADDING', (0,0), (-1,-1), 16),
    ('RIGHTPADDING', (0,0), (-1,-1), 16),
]))
story.append(header_tbl)
story.append(Spacer(1, 12))

# ── Summary cards ─────────────────────────────────────────────────────────────
card_w = (doc.width - 9) / 4

def metric_card(label, value, sub, bg, fg):
    inner = Table([
        [Paragraph(label, sty('Normal', fontSize=9, fontName='Helvetica', textColor=fg, spaceAfter=2))],
        [Paragraph(value, sty('Normal', fontSize=16, fontName='Helvetica-Bold', textColor=fg))],
        [Paragraph(sub,   sty('Normal', fontSize=8,  fontName='Helvetica', textColor=fg))],
    ], colWidths=[card_w - 16])
    inner.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
        ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    outer = Table([[inner]], colWidths=[card_w])
    outer.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), bg),
        ('ROUNDEDCORNERS',[6]),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
    ]))
    return outer

cards = [
    metric_card("Take-home salary", fmt(SALARY), "April salary", C_BLUE_LT, colors.HexColor("#185FA5")),
    metric_card("Total budgeted", fmt(TOTAL), f"{round(TOTAL/SALARY*100)}% of salary", C_GRAY_LT, colors.HexColor("#444441")),
    metric_card("Monthly surplus", fmt(SURPLUS), "To save / invest", C_TEAL_LT, colors.HexColor("#0F6E56")),
    metric_card("LendenClub returns", f"~{fmt(LENDEN_RET)}", "Estimated passive", C_AMBER_LT, colors.HexColor("#854F0B")),
]
cards_row = Table([cards], colWidths=[card_w]*4, hAlign='LEFT')
cards_row.setStyle(TableStyle([
    ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('COLPADDING',(0,0),(-1,-1),3),
]))
story.append(Paragraph("SUMMARY", sec_sty))
story.append(cards_row)
story.append(Spacer(1, 14))

# ── Category table builder ────────────────────────────────────────────────────
def section_table(title, rows_data, title_bg, title_fg):
    col_w = [doc.width*0.38, doc.width*0.25, doc.width*0.20, doc.width*0.17]

    header_row = [
        Paragraph(title, sty('Normal', fontSize=10, fontName='Helvetica-Bold', textColor=title_fg)),
        Paragraph("Budget", sty('Normal', fontSize=9, fontName='Helvetica-Bold', textColor=title_fg, alignment=TA_RIGHT)),
        Paragraph("% of salary", sty('Normal', fontSize=9, fontName='Helvetica-Bold', textColor=title_fg, alignment=TA_RIGHT)),
        Paragraph("Status", sty('Normal', fontSize=9, fontName='Helvetica-Bold', textColor=title_fg, alignment=TA_RIGHT)),
    ]

    table_data = [header_row]
    row_styles = [
        ('BACKGROUND', (0,0), (-1,0), title_bg),
        ('TOPPADDING', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_BG]),
        ('LINEBELOW', (0,0), (-1,-2), 0.3, C_BORDER),
        ('LINEBELOW', (0,-1), (-1,-1), 0.5, C_BORDER),
        ('LINEBEFORE', (0,0), (0,-1), 0.3, C_BORDER),
        ('LINEAFTER', (-1,0), (-1,-1), 0.3, C_BORDER),
    ]

    for i, (name, sub, amount, status, sfg, sbg) in enumerate(rows_data):
        p_pct = min(100, round(amount / SALARY * 100))
        table_data.append([
            Table([[Paragraph(name, bold_sty)],[Paragraph(sub, small_sty)]],
                colWidths=[col_w[0]-20],
                style=[('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
                       ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]),
            Paragraph(fmt(amount), right_sty),
            Paragraph(f"{p_pct}%", muted_r_sty),
            Paragraph(status, sty('Normal', fontSize=8, fontName='Helvetica-Bold',
                textColor=sfg, alignment=TA_RIGHT)),
        ])
        row_num = i + 1
        row_styles.append(('BACKGROUND', (3, row_num), (3, row_num), sbg))

    tbl = Table(table_data, colWidths=col_w)
    tbl.setStyle(TableStyle(row_styles))
    return tbl

# ── Fixed Commitments ─────────────────────────────────────────────────────────
story.append(Paragraph("FIXED COMMITMENTS", sec_sty))
story.append(section_table(
    "Category",
    [
        ("Rent (your share)", "Colive — split with Tejaswini", RENT, "Fixed", colors.HexColor("#993C1D"), C_CORAL_LT),
        ("LendenClub deployment", "P2P lending investment", LENDEN, "Invest", colors.HexColor("#0F6E56"), C_TEAL_LT),
        ("Netflix", "Streaming subscription", NETFLIX, "Fixed", colors.HexColor("#444441"), C_GRAY_LT),
    ],
    C_CORAL_LT, C_CORAL,
))
story.append(Spacer(1, 4))

# Totals row for fixed
fixed_total_tbl = Table([[
    Paragraph("Fixed total", sty('Normal', fontSize=9, fontName='Helvetica-Bold', textColor=C_MUTED)),
    Paragraph(fmt(FIXED_TOTAL), sty('Normal', fontSize=9, fontName='Helvetica-Bold', textColor=C_TEXT, alignment=TA_RIGHT)),
    Paragraph(f"{round(FIXED_TOTAL/SALARY*100)}% of salary", sty('Normal', fontSize=9, fontName='Helvetica', textColor=C_MUTED, alignment=TA_RIGHT)),
    Paragraph("", small_sty),
]], colWidths=[doc.width*0.38, doc.width*0.25, doc.width*0.20, doc.width*0.17])
fixed_total_tbl.setStyle(TableStyle([
    ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ('BACKGROUND',(0,0),(-1,-1),C_CORAL_LT),
    ('LINEABOVE',(0,0),(-1,0),0.5,C_CORAL),
]))
story.append(fixed_total_tbl)
story.append(Spacer(1, 14))

# ── Food & Groceries ──────────────────────────────────────────────────────────
story.append(Paragraph("FOOD & GROCERIES", sec_sty))
story.append(section_table(
    "Category",
    [
        ("Canteen meals", "Office / home canteen", CANTEEN, "Daily", colors.HexColor("#185FA5"), C_BLUE_LT),
        ("Zomato / Swiggy", "Food delivery orders", ZOMATO, "Variable", colors.HexColor("#854F0B"), C_AMBER_LT),
        ("Zepto / Instamart", "Grocery delivery", ZEPTO, "Variable", colors.HexColor("#5A3B9E"), C_PURPLE_LT),
    ],
    C_BLUE_LT, C_BLUE,
))
story.append(Spacer(1, 4))

food_total_tbl = Table([[
    Paragraph("Food total", sty('Normal', fontSize=9, fontName='Helvetica-Bold', textColor=C_MUTED)),
    Paragraph(fmt(FOOD_TOTAL), sty('Normal', fontSize=9, fontName='Helvetica-Bold', textColor=C_TEXT, alignment=TA_RIGHT)),
    Paragraph(f"{round(FOOD_TOTAL/SALARY*100)}% of salary", sty('Normal', fontSize=9, fontName='Helvetica', textColor=C_MUTED, alignment=TA_RIGHT)),
    Paragraph("", small_sty),
]], colWidths=[doc.width*0.38, doc.width*0.25, doc.width*0.20, doc.width*0.17])
food_total_tbl.setStyle(TableStyle([
    ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ('BACKGROUND',(0,0),(-1,-1),C_BLUE_LT),
    ('LINEABOVE',(0,0),(-1,0),0.5,C_BLUE),
]))
story.append(food_total_tbl)
story.append(Spacer(1, 14))

# ── Discretionary ─────────────────────────────────────────────────────────────
story.append(Paragraph("DISCRETIONARY", sec_sty))
story.append(section_table(
    "Category",
    [
        ("Amazon / Shopping", "Online purchases", AMAZON, "Capped", colors.HexColor("#854F0B"), C_AMBER_LT),
        ("Transport", "Auto / cab rides", TRANSPORT, "Variable", colors.HexColor("#444441"), C_GRAY_LT),
        ("Digital wallet", "UPI / petty cash top-up", WALLET, "Capped", colors.HexColor("#5A3B9E"), C_PURPLE_LT),
        ("Buffer / misc", "Unplanned small spends", BUFFER, "Buffer", colors.HexColor("#0F6E56"), C_TEAL_LT),
    ],
    C_AMBER_LT, C_AMBER,
))
story.append(Spacer(1, 4))

disc_total_tbl = Table([[
    Paragraph("Discretionary total", sty('Normal', fontSize=9, fontName='Helvetica-Bold', textColor=C_MUTED)),
    Paragraph(fmt(DISC_TOTAL), sty('Normal', fontSize=9, fontName='Helvetica-Bold', textColor=C_TEXT, alignment=TA_RIGHT)),
    Paragraph(f"{round(DISC_TOTAL/SALARY*100)}% of salary", sty('Normal', fontSize=9, fontName='Helvetica', textColor=C_MUTED, alignment=TA_RIGHT)),
    Paragraph("", small_sty),
]], colWidths=[doc.width*0.38, doc.width*0.25, doc.width*0.20, doc.width*0.17])
disc_total_tbl.setStyle(TableStyle([
    ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ('BACKGROUND',(0,0),(-1,-1),C_AMBER_LT),
    ('LINEABOVE',(0,0),(-1,0),0.5,C_AMBER),
]))
story.append(disc_total_tbl)
story.append(Spacer(1, 16))

# ── Grand total & surplus banner ──────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceAfter=10))

grand_data = [
    [
        Paragraph("GRAND TOTAL", sty('Normal', fontSize=11, fontName='Helvetica-Bold', textColor=C_TEXT)),
        Paragraph(fmt(TOTAL), sty('Normal', fontSize=11, fontName='Helvetica-Bold', textColor=C_TEXT, alignment=TA_RIGHT)),
        Paragraph(f"{round(TOTAL/SALARY*100)}% of salary", sty('Normal', fontSize=10, fontName='Helvetica', textColor=C_MUTED, alignment=TA_RIGHT)),
        Paragraph("", small_sty),
    ],
    [
        Paragraph("SURPLUS (save / invest)", sty('Normal', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor("#0F6E56"))),
        Paragraph(fmt(SURPLUS), sty('Normal', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor("#0F6E56"), alignment=TA_RIGHT)),
        Paragraph(f"{round(SURPLUS/SALARY*100)}% of salary", sty('Normal', fontSize=10, fontName='Helvetica', textColor=C_MUTED, alignment=TA_RIGHT)),
        Paragraph("", small_sty),
    ],
]
grand_tbl = Table(grand_data, colWidths=[doc.width*0.38, doc.width*0.25, doc.width*0.20, doc.width*0.17])
grand_tbl.setStyle(TableStyle([
    ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
    ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ('BACKGROUND',(0,0),(-1,0),C_GRAY_LT),
    ('BACKGROUND',(0,1),(-1,1),C_TEAL_LT),
    ('LINEBELOW',(0,0),(-1,0),0.5,C_BORDER),
    ('LINEBELOW',(0,1),(-1,1),0.5,C_TEAL),
    ('LINEBEFORE',(0,0),(0,-1),0.3,C_BORDER),
    ('LINEAFTER',(-1,0),(-1,-1),0.3,C_BORDER),
]))
story.append(grand_tbl)
story.append(Spacer(1, 16))

# ── Tips & notes ──────────────────────────────────────────────────────────────
story.append(Paragraph("NOTES & REMINDERS", sec_sty))

notes = [
    ("💡", C_TEAL_LT, C_TEAL, tip_sty,
     f"LendenClub earns an estimated <b>~{fmt(LENDEN_RET)}/mo</b> — treat this as a passive income bonus, not spending money."),
    ("⚠️", C_WARN_LT, C_WARN, warn_sty,
     f"Zomato + Zepto combined is <b>{fmt(ZOMATO+ZEPTO)}</b> ({round((ZOMATO+ZEPTO)/SALARY*100)}% of salary). Track weekly to stay within budget."),
    ("💡", C_TEAL_LT, C_TEAL, tip_sty,
     "Move the full surplus to a high-yield savings account or liquid mutual fund on salary day."),
    ("💡", C_TEAL_LT, C_TEAL, tip_sty,
     "Buffer of Rs. 1,000 covers small unplanned costs — any unused amount rolls into next month's savings."),
]

for icon, bg, border, p_sty, text in notes:
    note_tbl = Table([[Paragraph(f"{icon}  {text}", p_sty)]], colWidths=[doc.width])
    note_tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), bg),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
        ('LINEBEFORE',(0,0),(0,-1),3, border),
    ]))
    story.append(note_tbl)
    story.append(Spacer(1, 5))

story.append(Spacer(1, 10))

# ── Salary allocation mini-chart (text bars) ──────────────────────────────────
story.append(Paragraph("SALARY ALLOCATION AT A GLANCE", sec_sty))

alloc_items = [
    ("Rent",              RENT,      C_CORAL,  C_CORAL_LT),
    ("LendenClub",        LENDEN,    C_TEAL,   C_TEAL_LT),
    ("Food & Groceries",  FOOD_TOTAL,C_BLUE,   C_BLUE_LT),
    ("Discretionary",     DISC_TOTAL,C_AMBER,  C_AMBER_LT),
    ("Surplus",           SURPLUS,   C_PURPLE, C_PURPLE_LT),
    ("Netflix",           NETFLIX,   C_GRAY,   C_GRAY_LT),
]

bar_rows = []
for label, amount, fg, bg in alloc_items:
    bar_text = pct_bar_text(amount, SALARY)
    bar_rows.append([
        Paragraph(label, sty('Normal', fontSize=9, fontName='Helvetica', textColor=C_TEXT)),
        Paragraph(fmt(amount), sty('Normal', fontSize=9, fontName='Helvetica-Bold', textColor=fg, alignment=TA_RIGHT)),
        Paragraph(bar_text, sty('Normal', fontSize=8, fontName='Courier', textColor=fg)),
    ])

bar_tbl = Table(bar_rows, colWidths=[doc.width*0.30, doc.width*0.20, doc.width*0.50])
bar_tbl.setStyle(TableStyle([
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ('ROWBACKGROUNDS',(0,0),(-1,-1),[C_WHITE, C_BG]),
    ('LINEBELOW',(0,0),(-1,-2),0.3,C_BORDER),
    ('LINEBEFORE',(0,0),(0,-1),0.3,C_BORDER),
    ('LINEAFTER',(-1,0),(-1,-1),0.3,C_BORDER),
    ('LINEBELOW',(0,-1),(-1,-1),0.5,C_BORDER),
]))
story.append(bar_tbl)
story.append(Spacer(1, 18))

# ── Footer ────────────────────────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER, spaceAfter=6))
story.append(Paragraph(
    "Generated for Chandika Rama Sathya Sai · May 2026 · All amounts in Indian Rupees (₹)",
    sty('Normal', fontSize=8, fontName='Helvetica', textColor=C_MUTED, alignment=TA_CENTER)
))

# ── Build PDF ─────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF saved to {OUT}")
