"""
Features Section Component
==========================
Shows "how it works" in 3 steps
"""

from nicegui import ui
from config.theme import COLORS, SIZES, EFFECTS

def create_features_section():
    # Creates feature-section with 3 steps
    
    with ui.column().classes('w-full items-center').props('id="features"').style(
        f'padding: 6rem 2rem; background: {COLORS["background_secondary"]}'
    ):
        
        # Section title
        ui.label('HUR DET FUNGERAR').style(
            f'color: {COLORS["text_white"]}; '
            f'font-size: {SIZES["section_title"]}; '
            f'font-weight: bold; '
            f'letter-spacing: 4px; '
            f'margin-bottom: 4rem; '
            f'text-align: center; '
            f'text-shadow: {EFFECTS["text_shadow"]}'
        )
        
        # 3 features in a row
        with ui.row().classes('gap-10 flex-wrap justify-center'):
            
            # Feature 1
            create_feature_card(
                icon='person_add',
                title='1. Skapa Profil',
                description='Mata in dina egenheter'
            )
            
            # Feature 2
            create_feature_card(
                icon='movie',
                title='2. Upplev Scenarier',
                description='AI-genererade videoscenarier'
            )
            
            # Feature 3
            create_feature_card(
                icon='analytics',
                title='3. Få Analys',
                description='Djup personlighetsanalys'
            )

def create_feature_card(icon: str, title: str, description: str):
    """
    Creates a feature card
    
    Args:
        icon: Material icon name
        title: Title on the card
        description: Description
    """
    with ui.card().style(
        f'background: {COLORS["background_card"]}; '
        f'padding: 2.5rem; '
        f'max-width: 320px; '
        f'border: 2px solid {COLORS["border_card"]}; '
        f'border-radius: 12px; '
        f'box-shadow: {EFFECTS["card_shadow"]}; '
        f'transition: all 0.3s ease'
    ).classes('hover:scale-105'):
        
        with ui.column().classes('items-center text-center'):
            # Icon
            ui.icon(icon, size=SIZES['icon_medium']).style(
                f'color: {COLORS["accent_bright"]}; '
                f'margin-bottom: 1.5rem; '
                f'filter: drop-shadow({EFFECTS["glow_subtle"]})'
            )
            
            # Title
            ui.label(title).style(
                f'color: {COLORS["text_white"]}; '
                f'font-size: {SIZES["card_title"]}; '
                f'font-weight: bold; '
                f'margin-bottom: 0.8rem; '
                f'letter-spacing: 1px'
            )
            
            # Description
            ui.label(description).style(
                f'color: {COLORS["text_blue"]}; '
                f'font-size: {SIZES["body"]}; '
                f'line-height: 1.5'
            )

