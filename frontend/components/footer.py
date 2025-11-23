"""
Footer Component
================
Fixed footer with copyright and social icons
"""

from nicegui import ui
from config.theme import COLORS, SIZES

def create_footer():
    """Creates fixed footer at bottom"""
    
    # Add spacer to prevent content from being hidden behind footer
    ui.element('div').style('height: 100px')
    
    with ui.footer().classes('items-center justify-center').style(
        f'background: {COLORS["background_footer"]}; '
        f'border-top: 2px solid {COLORS["border_blue"]}; '
        f'padding: 1.5rem 2rem; '
        f'position: fixed; '
        f'bottom: 0; '
        f'left: 0; '
        f'right: 0; '
        f'z-index: 1000'
    ):
        
        with ui.row().classes('items-center gap-8'):
            # Copyright text
            ui.label('© 2025 Produktnamn').style(
                f'color: {COLORS["text_muted"]}; '
                f'font-size: {SIZES["small"]}; '
                f'letter-spacing: 1px'
            )
            
            # Social icons
            with ui.row().classes('gap-4'):
                ui.icon('mail', size=SIZES['icon_small']).style(
                    f'color: {COLORS["text_muted"]}; '
                    f'cursor: pointer; '
                    f'transition: all 0.3s ease'
                ).on('click', contact_us).classes('hover:scale-125')
                
                ui.icon('share', size=SIZES['icon_small']).style(
                    f'color: {COLORS["text_muted"]}; '
                    f'cursor: pointer; '
                    f'transition: all 0.3s ease'
                ).on('click', share).classes('hover:scale-125')
                
                ui.icon('info', size=SIZES['icon_small']).style(
                    f'color: {COLORS["text_muted"]}; '
                    f'cursor: pointer; '
                    f'transition: all 0.3s ease'
                ).on('click', info).classes('hover:scale-125')


# === FUNCTIONS FOR ICONS ===
# TODO: Connect to real functions later

def contact_us():
    """Contact us"""
    ui.notify('Kontakta oss på: example@email.com')


def share():
    """Share page"""
    ui.notify('Dela med dina vänner!')


def info():
    """More information"""
    ui.notify('Mer information kommer snart!')