"""
Registration Modal Component
=============================
Popup for user registration before starting the game
"""

from nicegui import ui
from config.theme import COLORS, SIZES, EFFECTS

class RegistrationModal:
    def __init__(self):
        self.dialog = None
        self.user_data = {}
        
    def show(self):
        """Shows the registration modal"""
        with ui.dialog().props('persistent') as self.dialog:
            with ui.card().style(
                f'background: {COLORS["background_card"]}; '
                f'padding: 2rem; '
                f'min-width: 700px; '
                f'max-width: 800px; '
                f'max-height: 85vh; '
                f'overflow-y: auto; '
                f'border: 2px solid {COLORS["border_card"]}; '
                f'border-radius: 16px; '
                f'box-shadow: {EFFECTS["card_shadow"]}'
            ):
                self._create_modal_content()
        
        self.dialog.open()
    
    def _create_modal_content(self):
        """Creates the content inside the modal"""
        
        # Title
        ui.label('REGISTRERA DIG').style(
            f'color: {COLORS["text_white"]}; '
            f'font-size: {SIZES["section_title"]}; '
            f'font-weight: bold; '
            f'letter-spacing: 3px; '
            f'margin-bottom: 1rem; '
            f'text-align: center; '
            f'text-shadow: {EFFECTS["text_shadow"]}'
        )
        
        # Subtitle
        ui.label('Fyll i dina uppgifter för att personalisera ditt scenario').style(
            f'color: {COLORS["text_blue"]}; '
            f'font-size: {SIZES["body"]}; '
            f'text-align: center; '
            f'margin-bottom: 2rem'
        )
        
        ui.separator().style(f'background: {COLORS["border_blue"]}; margin-bottom: 2rem')
        
        # Form fields
        with ui.column().classes('w-full gap-4'):
            
            # Användarnamn
            self._create_input_field('username', 'Användarnamn', 'Ange ditt användarnamn', 'person')
            
            # Ålder - Dropdown
            ui.label('Ålder').style(
                f'color: {COLORS["text_white"]}; '
                f'font-size: {SIZES["body"]}; '
                f'font-weight: bold; '
                f'margin-top: 1rem'
            )
            
            # Skapa en lista med åldrar från 18 till 100
            age_options = [str(i) for i in range(18, 101)]
            
            self.age = ui.select(
                age_options,
                value='25'
            ).style(
                f'background: {COLORS["background_secondary"]}; '
                f'color: {COLORS["text_white"]}; '
                f'border: 1px solid {COLORS["border_blue"]}; '
                f'border-radius: 8px; '
                f'padding: 0.5rem'
            ).props('outlined')
            
            # Kön - Dropdown
            ui.label('Kön').style(
                f'color: {COLORS["text_white"]}; '
                f'font-size: {SIZES["body"]}; '
                f'font-weight: bold; '
                f'margin-top: 1rem'
            )
            
            self.gender = ui.select(
                ['Man', 'Kvinna', 'Annat', 'Vill inte ange'],
                value='Vill inte ange'
            ).style(
                f'background: {COLORS["background_secondary"]}; '
                f'color: {COLORS["text_white"]}; '
                f'border: 1px solid {COLORS["border_blue"]}; '
                f'border-radius: 8px; '
                f'padding: 0.5rem'
            ).props('outlined')
            
            # Yrke
            ui.label('Yrke/Studieinriktning').style(
                f'color: {COLORS["text_white"]}; '
                f'font-size: {SIZES["body"]}; '
                f'font-weight: bold; '
                f'margin-top: 1rem'
            )
            
            self.occupation = ui.select(
                ['Ingenjör', 'Läkare', 'Lärare', 'Företagare', 'Konsult', 'Forskare', 'Annat'],
                value='Annat'
            ).style(
                f'background: {COLORS["background_secondary"]}; '
                f'color: {COLORS["text_white"]}; '
                f'border: 1px solid {COLORS["border_blue"]}; '
                f'border-radius: 8px; '
                f'padding: 0.5rem'
            ).props('outlined')
            
            # Ledarstil - Dropdown
            ui.label('Ledarstil').style(
                f'color: {COLORS["text_white"]}; '
                f'font-size: {SIZES["body"]}; '
                f'font-weight: bold; '
                f'margin-top: 1rem'
            )
            
            self.leadership_style = ui.select(
                ['Aggressiv', 'Defensiv', 'Diplomatisk', 'Balanserad'],
                value='Balanserad'
            ).style(
                f'background: {COLORS["background_secondary"]}; '
                f'color: {COLORS["text_white"]}; '
                f'border: 1px solid {COLORS["border_blue"]}; '
                f'border-radius: 8px; '
                f'padding: 0.5rem'
            ).props('outlined')
            
            # Prioritering - Dropdown
            ui.label('Prioritering i krissituation').style(
                f'color: {COLORS["text_white"]}; '
                f'font-size: {SIZES["body"]}; '
                f'font-weight: bold; '
                f'margin-top: 1rem'
            )
            
            self.priority = ui.select(
                ['Hjälpa andra', 'Fly/Överleva', 'Konfrontera hotet', 'Samla information'],
                value='Hjälpa andra'
            ).style(
                f'background: {COLORS["background_secondary"]}; '
                f'color: {COLORS["text_white"]}; '
                f'border: 1px solid {COLORS["border_blue"]}; '
                f'border-radius: 8px; '
                f'padding: 0.5rem'
            ).props('outlined')
            
            # Teamroll - Dropdown
            ui.label('Teamroll').style(
                f'color: {COLORS["text_white"]}; '
                f'font-size: {SIZES["body"]}; '
                f'font-weight: bold; '
                f'margin-top: 1rem'
            )
            
            self.team_role = ui.select(
                ['Ledare', 'Lagspelare', 'Ensam varg', 'Stöttande'],
                value='Lagspelare'
            ).style(
                f'background: {COLORS["background_secondary"]}; '
                f'color: {COLORS["text_white"]}; '
                f'border: 1px solid {COLORS["border_blue"]}; '
                f'border-radius: 8px; '
                f'padding: 0.5rem'
            ).props('outlined')
            
            # Riskbenägenhet - Dropdown
            ui.label('Riskbenägenhet').style(
                f'color: {COLORS["text_white"]}; '
                f'font-size: {SIZES["body"]}; '
                f'font-weight: bold; '
                f'margin-top: 1rem'
            )
            
            self.risk_tolerance = ui.select(
                ['Försiktig', 'Måttlig', 'Våghalsig'],
                value='Måttlig'
            ).style(
                f'background: {COLORS["background_secondary"]}; '
                f'color: {COLORS["text_white"]}; '
                f'border: 1px solid {COLORS["border_blue"]}; '
                f'border-radius: 8px; '
                f'padding: 0.5rem'
            ).props('outlined')
        
        # Buttons
        with ui.row().classes('w-full justify-between gap-4 mt-6'):
            # Cancel button
            ui.button('AVBRYT', on_click=self._cancel).props('flat').style(
                f'background: {COLORS["background_secondary"]} !important; '
                f'color: {COLORS["text_muted"]} !important; '
                f'font-weight: bold; '
                f'padding: 1rem 2rem; '
                f'border-radius: 8px; '
                f'border: 1px solid {COLORS["border_blue"]}'
            )
            
            # Submit button
            ui.button('STARTA SPELET', on_click=self._submit).props('flat').style(
                f'background: {COLORS["button_blue"]} !important; '
                f'color: white !important; '
                f'font-weight: bold; '
                f'padding: 1rem 2rem; '
                f'border-radius: 8px; '
                f'box-shadow: 0 10px 40px rgba(29, 78, 216, 0.3)'
            )
    
    def _create_input_field(self, field_name: str, label: str, placeholder: str, icon: str, input_type: str = 'text'):
        """Creates a styled input field with icon"""
        
        ui.label(label).style(
            f'color: {COLORS["text_white"]}; '
            f'font-size: {SIZES["body"]}; '
            f'font-weight: bold'
        )
        
        with ui.row().classes('w-full items-center gap-2'):
            ui.icon(icon).style(f'color: {COLORS["accent_bright"]}')
            
            input_field = ui.input(placeholder=placeholder).props('outlined').style(
                f'flex-grow: 1; '
                f'background: {COLORS["background_secondary"]}; '
                f'color: {COLORS["text_white"]}; '
                f'border-radius: 8px'
            )
            
            if input_type == 'number':
                input_field.props('type=number min=1 max=100')
            
            # Store reference to input field
            setattr(self, field_name, input_field)
    
    def _cancel(self):
        """Closes the modal without saving"""
        self.dialog.close()
        ui.notify('Registrering avbruten', type='warning')
    
    def _submit(self):
        """Validates and saves user data, then redirects to game"""
    
        # Collect data
        self.user_data = {
            'username': self.username.value,
            'age': self.age.value,
            'gender': self.gender.value,
            'occupation': self.occupation.value,
            'leadership_style': self.leadership_style.value,
            'priority': self.priority.value,
            'team_role': self.team_role.value,
            'risk_tolerance': self.risk_tolerance.value
        }
            
        # Basic validation
        if not self.user_data['username']:
            ui.notify('Vänligen fyll i användarnamn', type='negative')
            return
            
        # TODO: Save to database here
        print(f"User data to save: {self.user_data}")
            
        # Close modal
        self.dialog.close()
            
        # TODO: Navigate to game page
        # ui.open('/game')
        ui.notify('Registrering klar! Startar spelet...', type='positive')


# Create global instance
registration_modal = RegistrationModal()

