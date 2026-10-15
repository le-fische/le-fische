import os
import xml.sax.saxutils

def escape(s):
    return xml.sax.saxutils.escape(s)

LINE_WIDTH = 58
INFO_X = 385

def format_dots(key_len, val_len):
    gap = LINE_WIDTH - 2 - key_len - 1 - val_len
    if gap <= 0:
        return ' '
    if gap == 1:
        return ' '
    if gap == 2:
        return '. '
    return ' ' + '.' * (gap - 2) + ' '

# Exact Steam Avatar Fish Doodle with animated bubbles
STEAM_FISH = [
    ("space",  "                                 "),
    ("space",  "                                 "),
    ("bubble", "             .                   "),
    ("bubble", "               o                 "),
    ("fish",   "              /\\                 "),
    ("fish",   "           _./  \\_    _          "),
    ("fish",   "       _.-'       '--' \\_     /| "),
    ("fish",   "    .-'  (o)             \\___/ | "),
    ("fish",   "  <                           <  "),
    ("fish",   "    '-._     /\\      /\\   ___\\ | "),
    ("fish",   "        '---'  \\____/  '-'    \\| "),
    ("space",  "                                 "),
    ("space",  "                                 "),
    ("space",  "                                 "),
    ("space",  "                                 "),
    ("space",  "                                 "),
]

def make_card_svg(theme='dark'):
    height = 380
    
    bg = '#161b22' if theme == 'dark' else '#f6f8fa'
    fg = '#c9d1d9' if theme == 'dark' else '#24292f'
    key_color = '#ffa657' if theme == 'dark' else '#953800'
    val_color = '#a5d6ff' if theme == 'dark' else '#0a3069'
    cc_color = '#616e7f' if theme == 'dark' else '#c2cfde'
    fish_color = '#3fb950' if theme == 'dark' else '#1a7f37'
    bubble_color = '#a5d6ff' if theme == 'dark' else '#0969da'
    
    fields = [
        ("header", "houze@ubc"),
        ("AKA", "Le"),
        ("OS", "Linux, macOS, Windows 11"),
        ("Uptime", "19 years, 7 months, 17 days", "age_data"),
        ("Host", "UBC, UBC AeroDesign"),
        ("Kernel", "Computer Engineering Undergraduate"),
        ("IDE", "VS Code, Altium Designer, SolidWorks"),
        ("Status", "Need more Red Bull and sleep"),
        ("blank", ""),
        ("Languages.Programming", "C, C++, Python, Java, TypeScript"),
        ("Languages.Hardware", "SystemVerilog, Altium, RTL"),
        ("Languages.Real", "English, Mandarin, Indonesian"),
        ("blank", ""),
        ("Hobbies.Software", "Chess Engines, 3D Graphics, Web Dev"),
        ("Hobbies.Hardware", "PCB Design, Avionics, 3D Printing"),
        ("Hobbies.Real", "Counter-Strike, Ready or Not, Chess"),
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
.fish {{fill: {fish_color}; font-weight: 500;}}
.bubble {{fill: {bubble_color}; animation: float 2.5s ease-in-out infinite;}}
@keyframes float {{
  0%, 100% {{ opacity: 0.35; transform: translateY(0px); }}
  50% {{ opacity: 1.0; transform: translateY(-3px); }}
}}
text, tspan {{white-space: pre;}}
</style>
<rect width="1000px" height="{height}px" fill="{bg}" rx="15"/>

<!-- Steam Fish Graphic -->
<text x="25" y="32">""")

    for i, (kind, line) in enumerate(STEAM_FISH):
        y = 32 + i * 20
        cls = "fish" if kind == "fish" else ("bubble" if kind == "bubble" else "")
        cls_attr = f' class="{cls}"' if cls else ''
        svg.append(f'<tspan x="25" y="{y}"{cls_attr}>{escape(line)}</tspan>')

    svg.append('</text>\n')

    # Info Column
    svg.append(f'<text x="{INFO_X}" y="32" fill="{fg}">')
    
    cur_y = 32
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

with open("/Users/le/Documents/Projects/github profile/dark_mode.svg", "w", encoding="utf-8") as f:
    f.write(make_card_svg('dark'))

with open("/Users/le/Documents/Projects/github profile/light_mode.svg", "w", encoding="utf-8") as f:
    f.write(make_card_svg('light'))

print("Updated profile cards with AKA: Le!")
