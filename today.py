#!/usr/bin/env python3
"""
today.py - Updates Uptime dynamically in the SVG cards.
Runs daily at midnight UTC via GitHub Actions.
"""

import datetime
import os
import re

# Houze Guo's Birthday: February 28, 2007
BIRTHDAY = datetime.date(2007, 2, 28)

LINE_WIDTH = 58

def format_plural(unit, val):
    return unit + ('s' if val != 1 else '')

def calculate_uptime(born):
    today = datetime.date.today()
    years = today.year - born.year
    months = today.month - born.month
    days = today.day - born.day

    if days < 0:
        months -= 1
        prev_month = (today.month - 1) if today.month > 1 else 12
        prev_year = today.year if today.month > 1 else today.year - 1
        days_in_prev_month = (datetime.date(today.year, today.month, 1) - datetime.date(prev_year, prev_month, 1)).days
        days += days_in_prev_month

    if months < 0:
        years -= 1
        months += 12

    age_str = f"{years} {format_plural('year', years)}, {months} {format_plural('month', months)}, {days} {format_plural('day', days)}"
    if months == 0 and days == 0:
        age_str += " 🎂"
    return age_str

def update_svg_file(filepath, uptime_str):
    if not os.path.exists(filepath):
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    key_len = len("Uptime")
    val_len = len(uptime_str)
    gap = LINE_WIDTH - 2 - key_len - 1 - val_len
    if gap <= 0:
        dots = ' '
    elif gap == 1:
        dots = ' '
    elif gap == 2:
        dots = '. '
    else:
        dots = ' ' + '.' * (gap - 2) + ' '

    content = re.sub(
        r'(<tspan class="cc" id="age_data_dots">).*?(</tspan>)',
        rf'\g<1>{dots}\g<2>',
        content
    )
    content = re.sub(
        r'(<tspan class="value" id="age_data">).*?(</tspan>)',
        rf'\g<1>{uptime_str}\g<2>',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    uptime = calculate_uptime(BIRTHDAY)
    print(f"Current calculated Uptime: {uptime}")

    target_files = [
        "dark_mode.svg",
        "light_mode.svg",
        "dark_mode_tall.svg",
        "light_mode_tall.svg"
    ]

    for filename in target_files:
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        update_svg_file(full_path, uptime)
        print(f"Updated {filename}")

if __name__ == "__main__":
    main()
