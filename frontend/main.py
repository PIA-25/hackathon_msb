"""
Landing Page
==============================
MAIN FILE - imports and combines all components
"""

from nicegui import ui, app
from components.header import create_header
from components.hero import create_hero_section
from components.features import create_features_section
from components.stats import create_stats_section
from components.footer import create_footer

# Enable dark mode
ui.dark_mode().enable()

app.add_static_files('/assets', 'assets'
)

# Covers whole screen with background color
ui.add_head_html('''
    <style>
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background: #010510 !important;
        }
        .nicegui-content {
            background: #010510 !important;
        }
    </style>
''')

# === BUILDS PAGE ===
# Every function creates its own section on the page

create_header()          
create_hero_section()
create_features_section()
create_stats_section()
create_footer()         

# Runs the app
ui.run(title='Crisis Mind', port=8080)
