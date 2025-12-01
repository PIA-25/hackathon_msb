"""
Header Component
================
Fixed header with logo and user menu
"""

from nicegui import ui
from config.theme import COLORS, SIZES

def create_header():
    """Creates a fixed header at the top"""
    
    with ui.header().classes('items-center justify-between').style(
        f'background: {COLORS["background_footer"]}; '
        f'border-bottom: 1px solid {COLORS["border_blue"]}; '
        f'padding: 0.002rem 2rem; '
        f'position: fixed; '
        f'top: 0; '
        f'left: 0; '
        f'right: 0; '
        f'z-index: 1000'
    ):
        
        # Logo/Brand (left side)
        with ui.row().classes('items-center gap-2'):
            ui.image('/assets/logo_icon.png').style('width: 60px; height: 60px') 
            
            ui.label('CRISIS MIND').style(
                f'color: {COLORS["text_white"]}; '
                f'font-size: 20px; '
                f'font-weight: bold; '
                f'letter-spacing: 2px'
            )
        
        # User icon with menu (right side)
        with ui.button(icon='account_circle').props('flat round').style(
            f'color: {COLORS["text_blue"]}; '
            f'font-size: 1.2rem'
        ):
            # Dropdown menu
            with ui.menu().props('anchor="bottom right" self="top right"') as menu:
                ui.menu_item('Logga in', on_click=lambda: ui.notify('Logga in...'))
                ui.menu_item('Registrera', on_click=lambda: ui.notify('Registrera...'))
                ui.separator()
                ui.menu_item('Inställningar', on_click=lambda: ui.notify('Inställningar...'))
                ui.menu_item('Hjälp', on_click=lambda: ui.notify('Hjälp...'))