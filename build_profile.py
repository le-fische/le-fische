import os
import xml.sax.saxutils

def escape(s):
    return xml.sax.saxutils.escape(s)

# Trim ASCII art to max 34 characters per line so it stays strictly within x=15 to x=340
def trim_art(lines, max_cols=34):
    out = []
    for l in lines:
        trimmed = l[:max_cols].rstrip()
        out.append(trimmed)
    return out

RAW_ASCII_15 = [
    "                                  ",
    "          mkhhkmkur    rvli|      ",
    "     zh#M#M&%W##WMB$$&#WM##bbpqku ",
    "    pWbB$$$$@8@$$$$$$$$$$$@@@@&%@%",
    "  |#8@$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
    "  z@$$$$$$$$$$$$$&B@$$$$$$$$$$$$$$",
    "  uB$$$$$$$$$@u&8jbM$$@$$$$$$$%$$$",
    "   M$&M,;irzuxlj$|,+$BlWm@%xj|h%$M",
    "    mr  `-;+++~x`   'k+~~##h:-vj* ",
    "        `-,::::~l++!v*:;;~;;,`    ",
    "       .:~;:;~,:+il|+~,,-,::-     ",
    " ,;xxpkM$$MpwzxMx%&Wjvli|!~;u`    ",
    " jhh###p#%@$@pj*+~~:-'-,~+k$$W%%$#",
    " |h&8&BMbqp#$B@%bhzxrxjl*,8$$$$$$$",
    "~rhW$$$B&8%M$wmwzxrl*:` iilx$$$$$$"
]

RAW_ASCII_25 = [
    "                                  ",
    "          ||||||i                 ",
    "       |jukqhqqkkwxulvxxrvli||    ",
    "     |xh#bdbMbdp#d#$@M##dhqkmmwrv ",
    "    lmbWMM%B8&WMWW$$$&M%%WWMMbbpmr",
    "   |hb#B@$$$8W%$$$$$$$B$8BBB@8M#8W",
    "   mWB#&$$$$$$$$$$$$$$$$$$$$$$$@$B",
    "  |b8@$$$$$$$$$M$$$$$$$$$$$$$$$$$$",
    "  x$$@$B$B$$$$$$$&B@$$$8$$$$$$$$$$",
    "  zB$$$$$$$$$$$$$&B@$$$$$$$$$$$$$$",
    "  w@$$$$$$$$$$@@zrM%$$$$$$$$8B@$$$",
    "  v&$$#@8$$$$@xjBl+d@%x8k$@$@B$$$$",
    "   W$&W-:*jzzxvj$l,h$Bi%mkrzriq%$&",
    "   ;hhj .-;~;;;hq' .hW~~~+*~;'lw#!",
    "    ml ``-;+!!mr     wh++&Mp,,vv! ",
    "     |  `-,;;~:,*---!:,*!!+~,' |  ",
    "        ',,,--:!lvrjrl:.`--,,.    ",
    "       |,:;:::``:+*+:,'-'-::-     ",
    "     |B$$mrjlzB8$hhBBB8zl+~:'     ",
    "~k$%%Bkd$$$Whxllvbbbi*~~!!+~mx%q| ",
    "`umw$bbpMB$$%kv+!**+:-,:;++pbb$$pd",
    " jd#%W%dpdM$$$$j*;-'`',:!~h$$$dmB$",
    "  k&8$$Mdhqb$B$BWpwzzuzj!,@$$$$$$$",
    ".~$8@B@8B&##$bWWW#dqkzl!,`kz$$$$$$",
    "!Bh#$$$B%&8W$WWl|*!~-  |||iz$$$$$$"
]

ASCII_15 = trim_art(RAW_ASCII_15, 34)
ASCII_25 = trim_art(RAW_ASCII_25, 34)

# Line width on right: exactly 58 characters
LINE_WIDTH = 58
INFO_X = 385

def format_dots(key_len, val_len):
    # . Key: ..... Value
    # 2 ('. ') + key_len + 1 (':') + dots + val_len = 58
    gap = LINE_WIDTH - 2 - key_len - 1 - val_len
    if gap <= 0:
        return ' '
    if gap == 1:
        return ' '
    if gap == 2:
        return '. '
    return ' ' + '.' * (gap - 2) + ' '

def make_card_svg(theme='dark', rows=15):
    ascii_lines = ASCII_15 if rows == 15 else ASCII_25
    height = 340 if rows == 15 else 530
    
    bg = '#161b22' if theme == 'dark' else '#f6f8fa'
    fg = '#c9d1d9' if theme == 'dark' else '#24292f'
    key_color = '#ffa657' if theme == 'dark' else '#953800'
    val_color = '#a5d6ff' if theme == 'dark' else '#0a3069'
    cc_color = '#616e7f' if theme == 'dark' else '#c2cfde'
    
    fields = [
        ("header", "houze@ubc"),
        ("OS", "Linux, macOS, Windows 11"),
        ("Uptime", "21 years, 6 months, 0 days", "age_data"),
        ("Host", "University of British Columbia"),
        ("Kernel", "Computer Engineering Undergraduate"),
        ("IDE", "VS Code, Altium Designer, SolidWorks"),
        ("blank", ""),
        ("Languages.Programming", "Python, C++, TypeScript, C"),
        ("Languages.Computer", "SystemVerilog, SQL, HTML, CSS"),
        ("Languages.Real", "English, Mandarin, Indonesian"),
        ("blank", ""),
        ("Hobbies.Software", "Chess Engines, 3D Graphics, Web Dev"),
        ("Hobbies.Hardware", "PCB Design, Avionics, 3D Printing"),
    ]
    
    svg = []
    svg.append(f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ui-monospace,'SF Mono','Cascadia Code',Consolas,Menlo,monospace" width="1000px" height="{height}px" viewBox="0 0 1000 {height}" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {key_color};}}
.value {{fill: {val_color};}}
.cc {{fill: {cc_color};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="1000px" height="{height}px" fill="{bg}" rx="15"/>

<!-- ASCII Portrait -->
<text x="15" y="30" fill="{fg}" class="ascii">""")

    for i, line in enumerate(ascii_lines):
        y = 30 + i * 20
        svg.append(f'<tspan x="15" y="{y}">{escape(line)}</tspan>')
    svg.append('</text>\n')

    # Info Column
    svg.append(f'<text x="{INFO_X}" y="30" fill="{fg}">')
    
    cur_y = 30
    for item in fields:
        kind = item[0]
        if kind == "header":
            user_text = item[1]
            rule_dash = ' -' + '—' * (LINE_WIDTH - len(user_text) - 5) + '-—-'
            svg.append(f'<tspan x="{INFO_X}" y="{cur_y}">{user_text}</tspan><tspan fill="{cc_color}">{rule_dash}</tspan>')
        elif kind == "blank":
            svg.append(f'<tspan x="{INFO_X}" y="{cur_y}" class="cc">. </tspan>')
        else:
            key = item[0]
            val = item[1]
            eid = item[2] if len(item) > 2 else None
            dots = format_dots(len(key), len(val))
            
            parts = key.split('.')
            key_tspans = []
            for p_idx, part in enumerate(parts):
                if p_idx > 0:
                    key_tspans.append(f'<tspan fill="{fg}">.</tspan>')
                key_tspans.append(f'<tspan class="key">{part}</tspan>')
            key_html = "".join(key_tspans)
            
            dots_id_attr = f' id="{eid}_dots"' if eid else ''
            val_id_attr = f' id="{eid}"' if eid else ''
            
            svg.append(f'<tspan x="{INFO_X}" y="{cur_y}" class="cc">. </tspan>{key_html}<tspan fill="{fg}">:</tspan><tspan class="cc"{dots_id_attr}>{dots}</tspan><tspan class="value"{val_id_attr}>{val}</tspan>')
        cur_y += 20

    svg.append('</text>')
    svg.append('</svg>')
    return "\n".join(svg)

def make_radar_svg(commits_pct=96, prs_pct=4, issues_pct=0, review_pct=0, theme='dark'):
    bg = '#161b22' if theme == 'dark' else '#ffffff'
    axis_color = '#3fb950' if theme == 'dark' else '#1a7f37'
    text_color = '#c9d1d9' if theme == 'dark' else '#24292f'
    muted_text = '#8b949e' if theme == 'dark' else '#57606a'
    poly_fill = 'rgba(63, 185, 80, 0.35)' if theme == 'dark' else 'rgba(26, 127, 55, 0.25)'
    dot_stroke = '#3fb950' if theme == 'dark' else '#1a7f37'
    dot_fill = '#ffffff'
    border_color = '#30363d' if theme == 'dark' else '#d0d7de'

    width, height = 460, 310
    cx, cy = 230, 155
    arm_len = 92

    pt_commits = (cx - (arm_len * commits_pct / 100.0), cy)
    pt_prs = (cx, cy + (arm_len * prs_pct / 100.0))
    pt_review = (cx, cy - (arm_len * review_pct / 100.0))
    pt_issues = (cx + (arm_len * issues_pct / 100.0), cy)

    pts = [pt_review, pt_issues, pt_prs, pt_commits]
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none">
  <rect width="{width}" height="{height}" rx="12" fill="{bg}" stroke="{border_color}" stroke-width="1"/>
  <text x="24" y="32" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="14" font-weight="600" fill="{text_color}">Activity Overview</text>
  
  <!-- Cross axes -->
  <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - arm_len}" stroke="{axis_color}" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy + arm_len}" stroke="{axis_color}" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="{cx}" y1="{cy}" x2="{cx - arm_len}" y2="{cy}" stroke="{axis_color}" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="{cx}" y1="{cy}" x2="{cx + arm_len}" y2="{cy}" stroke="{axis_color}" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Shaded polygon -->
  <polygon points="{pts_str}" fill="{poly_fill}" stroke="{axis_color}" stroke-width="1.5"/>

  <!-- Data point dots -->
  <circle cx="{pt_commits[0]:.1f}" cy="{pt_commits[1]:.1f}" r="4.5" fill="{dot_fill}" stroke="{dot_stroke}" stroke-width="2.5"/>
  <circle cx="{pt_prs[0]:.1f}" cy="{pt_prs[1]:.1f}" r="4.5" fill="{dot_fill}" stroke="{dot_stroke}" stroke-width="2.5"/>

  <!-- Axis Labels -->
  <text x="{cx}" y="{cy - arm_len - 14}" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="13" font-weight="500" fill="{muted_text}">Code review</text>
  <text x="{cx + arm_len + 14}" y="{cy + 4}" text-anchor="start" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="13" font-weight="500" fill="{muted_text}">Issues</text>
  
  <text x="{cx}" y="{cy + arm_len + 20}" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="12" font-weight="600" fill="{text_color}">{prs_pct}%</text>
  <text x="{cx}" y="{cy + arm_len + 35}" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="13" font-weight="500" fill="{muted_text}">Pull requests</text>

  <text x="{cx - arm_len - 14}" y="{cy - 4}" text-anchor="end" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="12" font-weight="600" fill="{text_color}">{commits_pct}%</text>
  <text x="{cx - arm_len - 14}" y="{cy + 12}" text-anchor="end" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="13" font-weight="500" fill="{muted_text}">Commits</text>
</svg>"""
    return svg

# Write SVGs
os.makedirs("/Users/le/Documents/Projects/github profile", exist_ok=True)

with open("/Users/le/Documents/Projects/github profile/dark_mode.svg", "w", encoding="utf-8") as f:
    f.write(make_card_svg('dark', 15))

with open("/Users/le/Documents/Projects/github profile/light_mode.svg", "w", encoding="utf-8") as f:
    f.write(make_card_svg('light', 15))

with open("/Users/le/Documents/Projects/github profile/dark_mode_tall.svg", "w", encoding="utf-8") as f:
    f.write(make_card_svg('dark', 25))

with open("/Users/le/Documents/Projects/github profile/light_mode_tall.svg", "w", encoding="utf-8") as f:
    f.write(make_card_svg('light', 25))

with open("/Users/le/Documents/Projects/github profile/activity_dark.svg", "w", encoding="utf-8") as f:
    f.write(make_radar_svg(theme='dark'))

with open("/Users/le/Documents/Projects/github profile/activity_light.svg", "w", encoding="utf-8") as f:
    f.write(make_radar_svg(theme='light'))

print("All profile SVGs successfully regenerated!")
