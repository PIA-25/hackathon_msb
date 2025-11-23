from nicegui import ui
from config.theme import COLORS, SIZES, EFFECTS

'''
HERO Section Component

First section the user sees
'''

def create_hero_section():
    # Creates hero-section with title and buttons
    
    background_image = 'url(/assets/hero_background.jpg)'
    
    with ui.column().classes('w-full items-center justify-center').style(
        f'min-height: 100vh; '
        f'background-image: {background_image}; '
        f'background-size: cover; '           # Täcker hela området
        f'background-position: center; '      # Centrerar bilden
        f'background-repeat: no-repeat; '     # Ingen upprepning
        f'position: relative'
    ):
        
        ui.element('div').style(
            'position: absolute; '
            'top: 0; '
            'left: 0; '
            'width: 100%; '
            'height: 100%; '
            'background: rgba(1, 5, 16, 0.7); '  # Mörk overlay (70% opacity)
            'z-index: 0'
        )
    
        with ui.column().classes('items-center').style('position: relative; z-index: 1'):
            
            # Icon with blue glow
            ui.icon('psychology', size=SIZES['icon_large']).style(
                f'color: {COLORS["accent_bright"]}; '
                f'margin-bottom: 2rem; '
                f'filter: drop-shadow({EFFECTS["glow_medium"]})'
            )
            
            # Main title - bright blue!
            ui.label('PRODUKTNAMN').style(
                f'color: {COLORS["accent_bright"]}; '
                f'font-size: {SIZES["hero_title"]}; '
                f'font-weight: bold; '
                f'text-align: center; '
                f'letter-spacing: 8px; '
                f'text-shadow: {EFFECTS["glow_medium"]}; '
                f'margin-bottom: 1.5rem'
            )
            
            # Subtitle
            ui.label('AI-Driven Beslutsanalys i Krigsscenarier').style(
                f'color: {COLORS["text_blue"]}; '
                f'font-size: {SIZES["subtitle"]}; '
                f'text-align: center; '
                f'letter-spacing: 2px; '
                f'margin-bottom: 1rem'
            )
            
            # Description
            ui.label('Testa dina strategiska förmågor genom realistiska AI-genererade scenarier').style(
                f'color: {COLORS["text_muted"]}; '
                f'font-size: {SIZES["body"]}; '
                f'text-align: center; '
                f'max-width: 700px; '
                f'line-height: 1.6; '
                f'margin-bottom: 2rem'
            )
            
            # Buttons - much more visible!
            with ui.row().classes('gap-6 mt-4'):
                
                # Primary button - solid blue
                ui.button('STARTA SPEL', on_click=start_game).style(
                    f'background: {COLORS["accent_primary"]}; '
                    f'color: white; '
                    f'font-weight: bold; '
                    f'font-size: 20px; '
                    f'padding: 1.2rem 3.5rem; '
                    f'border-radius: 8px; '
                    f'letter-spacing: 2px; '
                    f'box-shadow: {EFFECTS["card_shadow"]}; '
                    f'transition: all 0.3s ease; '
                    f'border: none'
                )
                
                # Secondary button - light blue, very visible!
                ui.button('LÄR MER', on_click=learn_more).props('flat').style(
                    f'color: {COLORS["accent_bright"]}; '
                    f'border: 3px solid {COLORS["accent_bright"]}; '
                    f'font-weight: bold; '
                    f'font-size: 20px; '
                    f'padding: 1.2rem 3.5rem; '
                    f'border-radius: 8px; '
                    f'letter-spacing: 2px; '
                    f'transition: all 0.3s ease; '
                    f'background: transparent !important'
                )


# === FUNCTIONS FOR BUTTONS ===
# TODO: Connect to real pages/functions later

def start_game():
    # Navigates to the game page
    # TODO: ui.open('/game') when we have game page
    ui.notify('Spelet startas snart!', type='positive')


def learn_more():
    """Shows more information"""
    # TODO: Scroll to features section
    ui.notify('Scrolla ner för mer info!')