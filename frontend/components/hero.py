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
        f'background-size: cover; '   
        f'background-position: center; ' 
        f'background-repeat: no-repeat; '
        f'position: relative'
    ):
        
        ui.element('div').style(
            'position: absolute; '
            'top: 0; '
            'left: 0; '
            'width: 100%; '
            'height: 100%; '
            'background: rgba(1, 5, 16, 0.88); '
            'z-index: 0'
        )
    
        with ui.column().classes('items-center').style('position: relative; z-index: 1'):
            
            # Our icon for the game
            ui.image('/assets/logo_icon.png').style(
                'width: 160px; '
                'height: 140px; '
                'margin-bottom: 2rem; '
                f'filter: drop-shadow({EFFECTS["glow_medium"]})'
            )
            
            # Main title
            ui.label('CRISIS MIND').style(
                f'color: {COLORS["hero_title"]}; '
                f'font-size: {SIZES["hero_title"]}; ' 
                'font-weight: 700; '
                'text-align: center; '
                'letter-spacing: 15px; '
                'text-shadow: 0 0 30px rgba(96, 165, 250, 0.4), 0 2px 8px rgba(0, 0, 0, 0.6); '
                'margin-bottom: 2.5rem'
            )
            
            # Subtitle
            ui.label('AI-Driven Beslutsanalys i Krissituationer').style(
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
            
            # Buttons
            with ui.row().classes('gap-6 mt-4'):
                
                # Primary button - STARTA SPEL
                ui.button('STARTA SPEL', on_click=start_game).props('flat').style(
                    f'background: {COLORS["button_blue"]} !important; '
                    'color: white !important; '
                    'font-weight: bold; '
                    'font-size: 20px; '
                    'padding: 1.2rem 3.5rem; '
                    'border-radius: 8px; '
                    'letter-spacing: 2px; '
                    'box-shadow: 0 10px 40px rgba(29, 78, 216, 0.3); '
                    'transition: all 0.3s ease; '
                    'border: none; '
                    'min-width: 250px'
                ).classes('hover:scale-110')

                # Secondary button - LÄS MER
                ui.button('LÄS MER', on_click=learn_more).props('flat').style(
                    f'background: {COLORS["button_blue"]} !important; '
                    'color: white !important; '
                    'font-weight: bold; '
                    'font-size: 20px; '
                    'padding: 1.2rem 3.5rem; '
                    'border-radius: 8px; '
                    'letter-spacing: 2px; '
                    'box-shadow: 0 10px 40px rgba(29, 78, 216, 0.3); '
                    'transition: all 0.3s ease; '
                    'border: none; '
                    'min-width: 250px'
                ).classes('hover:scale-110')


# === FUNCTIONS FOR BUTTONS ===

def start_game():
    """Opens registration modal"""
    # Import here to avoid circular imports
    from components.registration_modal import registration_modal
    registration_modal.show()


def learn_more():
    """Shows more information"""
    ui.run_javascript('document.getElementById("features").scrollIntoView({ behavior: "smooth" })')