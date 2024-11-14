from datetime import datetime, timedelta
from typing import List, Tuple
import holidays
import os

# Configuration
YEAR = 2025
CONTACT_NAME = "Dillon Dong"
CONTACT_USERNAME = "ddong"

# Styling parameters
STYLES = {
    'date_column_width': "25%",
    'content_column_width': "75%",
    'cell_padding': "15px",
    'border_color': "#E0E0E0",
    'header_bg_color': "#B8C5D9",
    'border_style': "1px solid"
}

# HTML style strings
DATE_CELL_STYLE = f"""
    width: {STYLES['date_column_width']};
    text-align: left;
    background-color: {STYLES['header_bg_color']};
    padding: {STYLES['cell_padding']};
    border: {STYLES['border_style']} {STYLES['border_color']}
""".strip()

CONTENT_CELL_STYLE = f"""
    width: {STYLES['content_column_width']};
    padding: {STYLES['cell_padding']};
    border: {STYLES['border_style']} {STYLES['border_color']}
""".strip()

# Holiday display text mapping - separate text and emoji
HOLIDAY_DISPLAY = {
    "New Year's Day": ("New Year's Day", "🎆"),
    "Martin Luther King Jr. Day": ("MLK Day", ""),
    "Washington's Birthday": ("President's Day", ""),
    "Memorial Day": ("Memorial Day", ""),
    "Juneteenth National Independence Day": ("Juneteenth", ""),
    "Independence Day": ("July 4", "🎆"),
    "Labor Day": ("Labor Day", ""),
    "Columbus Day": ("Indigenous People's Day", ""),
    "Veterans Day": ("Veterans Day", ""),
    "Thanksgiving": ("Thanksgiving", "🥧"),
    "Christmas Day": ("Christmas", "🎄"),
    "Christmas Eve": ("Christmas Eve", "🎄"),
    "New Year's Eve": ("New Year's Eve", "🎆")
}

def get_wednesdays(year: int) -> List[datetime]:
    """Get all Wednesdays for a given year."""
    start = datetime(year, 1, 1)
    
    if start.weekday() == 2:
        first_wednesday = start
    else:
        days_ahead = (2 - start.weekday()) % 7
        first_wednesday = start + timedelta(days=days_ahead)
    
    wednesdays = []
    current = first_wednesday
    while current.year == year:
        wednesdays.append(current)
        current += timedelta(days=7)
    return wednesdays

def get_federal_holidays(year: int) -> List[Tuple[datetime, str]]:
    """Get federal holidays and custom holidays that fall on Wednesdays."""
    wednesday_holidays = []
    
    us_holidays = holidays.US(years=year)
    for date, name in us_holidays.items():
        date_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=12)
        if date_time.weekday() == 2:
            wednesday_holidays.append((date_time, name))
            print(f"DEBUG: Found holiday {name} on {date_time}")
    
    custom_dates = [
        (datetime(year, 12, 24, 12, 0), "Christmas Eve"),
        (datetime(year, 12, 31, 12, 0), "New Year's Eve")
    ]
    
    for date, name in custom_dates:
        if date.weekday() == 2:
            wednesday_holidays.append((date, name))
            print(f"DEBUG: Found custom holiday {name} on {date}")
    
    return sorted(wednesday_holidays)

def format_holiday_text(holiday_name: str) -> str:
    """Format holiday text with bold text and emoji in the same paragraph."""
    display_text, emoji = HOLIDAY_DISPLAY.get(holiday_name, (holiday_name, ""))
    if not display_text and not emoji:
        return ""
    
    # Combine text and emoji in a single paragraph
    return f"<p><strong>{display_text}</strong> {emoji}</p>"

def generate_schedule_html() -> str:
    wednesdays = get_wednesdays(YEAR)
    holidays = get_federal_holidays(YEAR)
    
    # Convert holidays to a dictionary with datetime keys normalized to noon
    holiday_dates = {}
    for date, name in holidays:
        normalized_date = datetime.combine(date.date(), datetime.min.time()) + timedelta(hours=12)
        holiday_dates[normalized_date] = name
        print(f"DEBUG: Added holiday to dict: {normalized_date} -> {name}")
    
    html = f'''<p>Wednesday Lunch is an informal lunchtime get-together with pizza to hear visitors' results as well as what staff are doing. If you or one of your visitors would like to speak at Wednesday Lunch, please contact {CONTACT_NAME} (username {CONTACT_USERNAME}) at <em>username</em>@nrao.edu.</p>

<p>Wednesday Lunch is held in the auditorium of the <a class="internal-link" href="../../../../about/socorro/maps">Domenici Science Operations Center (DSOC)</a> in Socorro, New Mexico from <span><strong>noon until 1:00 PM</strong></span> unless indicated. All are welcome.</p>

<table class="grid listing" style="width: 100%; border-collapse: collapse;">
<tbody>'''

    # Generate rows for each Wednesday
    for i, date in enumerate(wednesdays):
        row_class = "odd" if i % 2 == 0 else "even"
        formatted_date = date.strftime("%d %b %Y")
        
        # Check if it's a holiday
        normalized_date = datetime.combine(date.date(), datetime.min.time()) + timedelta(hours=12)
        content = ""
        if normalized_date in holiday_dates:
            holiday_name = holiday_dates[normalized_date]
            content = format_holiday_text(holiday_name)
            print(f"DEBUG: Generating content for {formatted_date}: {content}")
        
        html += f'''
<tr class="{row_class}">
<th style="{DATE_CELL_STYLE}">
<div>
<div class="visualClear" id="{date.strftime('%Y%m%d')}"><strong>{formatted_date}</strong></div>
<div class="visualClear"><span><span>Noon MT</span></span></div>
</div>
</th>
<td style="{CONTENT_CELL_STYLE}">
{content}
</td>
</tr>'''

    # Add footer
    html += '''
</tbody>
</table>
<p> </p>
<h2><a class="internal-link" href="overview" target="_self" title=""><span class="internal-link">Wednesday Lunch schedules from previous years</span></a></h2>
<p> </p>
<h1>Other Astrophysics Colloquia</h1>
<ul>
<li><a class="internal-link" href="../coll" target="_self" title="">NRAO Socorro Colloquia</a></li>
<li><a href="http://www.cv.nrao.edu/colloq/">NRAO Charlottesville Colloquia</a></li>
<li><a class="external-link" href="http://www.cv.nrao.edu/tuna/" target="_self" title="">NRAO Charlottesville Lunch Seminar (TUNA)</a></li>
<li><a class="external-link" href="../../../gbt/colloquia-talks/">NRAO Green Bank Colloquia</a></li>
</ul>
<ul>
<li><a class="external-link" href="http://physics.nmt.edu/events/" target="_self" title="">NMT Physics Dept. Colloquia</a> (Socorro, NM)</li>
<li><a class="external-link" href="http://panda.unm.edu/pandaweb/events/index.php?display=series&amp;series_id=6">UNM Physics &amp; Astronomy Dept. Colloquia </a>(Albuquerque, NM)</li>
<li><a href="http://astronomy.nmsu.edu/dept/html/talks.colloq.shtml">NMSU Astronomy Dept. Colloquia </a>(Las Cruces, NM)</li>
</ul>'''
    
    return html

def test_holiday_handling(year: int):
    """Test function to verify holiday handling for any year"""
    holidays = get_federal_holidays(year)
    print(f"\nHolidays falling on Wednesdays in {year}:")
    print("-" * 50)
    for date, name in sorted(holidays):
        formatted_content = format_holiday_text(name)
        print(f"{date.strftime('%Y-%m-%d')}: {name}")
        print(f"Formatted content: {formatted_content}")

if __name__ == "__main__":
    # Generate the schedule
    html_content = generate_schedule_html()
    
    os.makedirs('./lunch_talk_schedules/',exist_ok = True)
    with open(f'./lunch_talk_schedules/wednesday_lunch_{YEAR}.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nSchedule for {YEAR} has been generated!")
    
    # Test holiday handling for the current year
    test_holiday_handling(YEAR)
    
    print("\nReminder: Don't forget to add annual events such as:")
    print("- AAS Meetings")
    print("- Synthesis Imaging Workshop")
    print("- Summer Student Talks")
    print("- Scistaff Retreat")