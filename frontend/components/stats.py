"""
Stats Section Component
=======================
Shows project stats
"""

from nicegui import ui
from config.theme import COLORS, SIZES, EFFECTS

def create_stats_section():
    """Creates the stats-section"""
    
    with ui.column().classes('w-full items-center').style(
        f'padding: 6rem 2rem; background: {COLORS["background_primary"]}'
    ):
        
        # Section title
        ui.label('PROJEKTDATA').style(
            f'color: {COLORS["text_white"]}; '
            f'font-size: {SIZES["section_title"]}; '
            f'font-weight: bold; '
            f'letter-spacing: 4px; '
            f'margin-bottom: 4rem; '
            f'text-align: center; '
            f'text-shadow: {EFFECTS["text_shadow"]}'
        )
        
        # Row with stats
        with ui.row().classes('gap-20 flex-wrap justify-center'):
            
            create_stat(
                number='3',
                label='Scenarier per spelloop'
            )
            
            create_stat(
                number='18-29',
                label='Målgrupp (år)'
            )
            
            create_stat(
                number='∞',
                label='AI-genererade variationer'
            )


def create_stat(number: str, label: str):
    """
    Creates a stat
    
    Args:
        number: The number to show
        label: Description text underneath
    """
    with ui.column().classes('items-center'):
        # Big number with blue glow
        ui.label(number).style(
            f'color: {COLORS["accent_bright"]}; '
            f'font-size: 72px; '
            f'font-weight: bold; '
            f'text-shadow: {EFFECTS["glow_medium"]}; '
            f'margin-bottom: 0.5rem'
        )
        
        # Label
        ui.label(label).style(
            f'color: {COLORS["text_blue"]}; '
            f'font-size: 20px; '
            f'letter-spacing: 1px'
        )