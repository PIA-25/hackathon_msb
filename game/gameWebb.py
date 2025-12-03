import json
import os
from nicegui import ui, app
import textwrap
from backend.app.database.database import SessionLocal
from backend.app.database.models import Scenario
from backend.app.database.crud import save_user_choice_and_update_attributes, get_scenario, get_choice_options, get_user
from ai.video_generation import get_video


# Hitta rätt sökväg till mock_data
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)  # Gå upp en nivå från game/ till projektets root
MOCK_DATA_DIR = os.path.join(PROJECT_ROOT, 'mock_data')  # Använd mock_data/ i projektets root


# -------------------------------------------------------
# LOAD JSON SCENARIOS
# -------------------------------------------------------
def load_scenarios():
    with open(os.path.join(MOCK_DATA_DIR, 'mock.json'), 'r', encoding='utf-8') as f:
        return json.load(f)["scenarios"]

def load_scenarios_from_db():
    """Laddar scenarier från databasen och formaterar dem till samma format som mock.json"""
    db = SessionLocal()
    try:
        # Sortera scenarier efter level_id och scenario_id för konsistens
        scenarios = db.query(Scenario).order_by(Scenario.level_id, Scenario.scenario_id).all()
        formatted_scenarios = []
        
        for scenario in scenarios:
            # Hämta choice_options för detta scenario, sorterade efter choice_id för konsistens
            choice_options = get_choice_options(db, scenario.scenario_id)
            choice_options = sorted(choice_options, key=lambda c: c.choice_id)
            
            # Kontrollera att vi har minst 2 val
            if len(choice_options) < 2:
                print(f"Varning: Scenario {scenario.scenario_id} har färre än 2 val, hoppar över")
                continue
            
            # Hitta korrekt och felaktigt val
            correct_choice = next((c for c in choice_options if c.is_good is True), None)
            wrong_choice = next((c for c in choice_options if c.is_good is False), None)
            
            # Bestäm vilket val som är korrekt baserat på index
            # Ta de första två valen som 'a' och 'b'
            correct_letter = 'a'
            if correct_choice and correct_choice == choice_options[1]:
                correct_letter = 'b'
            elif correct_choice and correct_choice == choice_options[0]:
                correct_letter = 'a'
            elif not correct_choice:
                # Om inget val är markerat som korrekt, använd första som default
                correct_letter = 'a'
            
            scenario_dict = {
                'id': scenario.scenario_id,
                'level_id': scenario.level_id,
                'text': scenario.scenario_text,
                'a': choice_options[0].option_text,
                'b': choice_options[1].option_text,
                'correct': correct_letter,
                'right_msg': correct_choice.outcome_text if correct_choice else '',
                'wrong_msg': wrong_choice.outcome_text if wrong_choice else ''
            }
            formatted_scenarios.append(scenario_dict)
        
        return formatted_scenarios
    finally:
        db.close()

scenarios = load_scenarios()  # Ladda från mock.json
# scenarios = load_scenarios_from_db()  # Kommenterad - används när DB är klar


# -------------------------------------------------------
# TEXT WRAPPING FUNCTION
# -------------------------------------------------------
def wrap_text(text: str, width: int = 40) -> str:
    clean = text.lstrip()
    return "\n".join(textwrap.wrap(clean, width=width))


# -------------------------------------------------------
# GAME LOGIC
# -------------------------------------------------------
class GameUI:
    def __init__(self):
        self.scenarios = scenarios
        self.index = 0
        self.finished = False
        self.last_choice_correct = None

    @property
    def current(self):
        return self.scenarios[self.index]

    VIDEO_SEQUENCE = [
    '/mock_data/video0.mp4',  # first scenario
    '/mock_data/video1.mp4',  # second scenario
    '/mock_data/video2.mp4',  # third scenario
    '/mock_data/video3.mp4',
]

    def video_path(self, correct: bool) -> str:
        return f'/mock_data/video{self.index}.mp4'

    def handle_choice(self, choice: str) -> bool:
        if self.finished:
            return False
        is_correct = choice == self.current['correct']
        self.last_choice_correct = is_correct
        return is_correct

    def advance(self):
        self.index += 1
        if self.index >= len(self.scenarios):
            self.finished = True

game = GameUI()

# Lägg till static files för videor
app.add_static_files('/mock_data', MOCK_DATA_DIR)

# -------------------------------------------------------
# PAGE UI
# -------------------------------------------------------
@ui.page('/game')
def index():
    ui.add_head_html("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/JetBrainsMono/2.304.0/jetbrains-mono.min.css" rel="stylesheet">
    <style>
        .font-jetbrains { font-family: 'JetBrains Mono', monospace !important; }
    </style>
    """)

    with ui.element('div').classes('w-full h-screen overflow-hidden'):
        # TODO: fixa så att det hämtas från frontend/backend
        user_info = {
            "age": "21",
            "gender": "male",
        }
        # Frivilligt, om man vill att videosen ska sparas lokalt
        video_save_folder = "videos/"

        # Video element
        video_info = get_video(user_info, 1, video_save_folder)
        if video_info["video_exists"]:
            video = ui.video(video_info["video_bytes"]).classes('absolute inset-0 w-full h-full object-cover')
        else:
            video = ui.video(f'/mock_data/video0.mp4').classes('absolute inset-0 w-full h-full object-cover')

        # CHOICE OVERLAY
        with ui.column().classes(
            'absolute inset-0 items-center justify-center gap-6 text-white '
            'bg-black/30 backdrop-blur-md p-10 rounded-3xl'
        ) as choice_overlay:
            title_label = ui.label().classes('text-4xl font-bold font-jetbrains')
            text_label = ui.label().classes('text-lg max-w-3xl text-center opacity-80 font-jetbrains')

            # CHOICE A
            with ui.row().classes(
                'items-center gap-6 bg-black/40 backdrop-blur-md rounded-2xl '
                'px-6 py-5 w-full max-w-3xl cursor-pointer hover:bg-black/60 transition-all'
            ) as block_a:
                ui.label('A').classes('text-white text-2xl font-bold font-jetbrains')
                ui.element('div').classes('h-10 w-px bg-white/40')
                text_a = ui.label().classes('text-white text-lg font-jetbrains leading-snug whitespace-pre-line')
            block_a.on('click', lambda e: on_click('a'))

            # CHOICE B
            with ui.row().classes(
                'items-center gap-6 bg-black/40 backdrop-blur-md rounded-2xl '
                'px-6 py-5 w-full max-w-3xl cursor-pointer hover:bg-black/60 transition-all'
            ) as block_b:
                ui.label('B').classes('text-white text-2xl font-bold font-jetbrains')
                ui.element('div').classes('h-10 w-px bg-white/40')
                text_b = ui.label().classes('text-white text-lg font-jetbrains leading-snug whitespace-pre-line')
            block_b.on('click', lambda e: on_click('b'))

        choice_overlay.visible = False

        # CORRECT OVERLAY
        with ui.column().classes(
            'absolute inset-0 items-center justify-center gap-6 text-white '
            'bg-green-900/60 backdrop-blur-md p-10 rounded-3xl cursor-pointer'
        ) as correct_overlay:
            ui.label('Rätt val!').classes('text-4xl font-bold font-jetbrains text-green-300')
            correct_msg_label = ui.label().classes('text-lg max-w-3xl text-center opacity-90 font-jetbrains')
            ui.label('Klicka för att fortsätta...').classes('text-sm opacity-60 font-jetbrains mt-4')
        correct_overlay.visible = False
        correct_overlay.on('click', lambda _: proceed_to_next())

        # WRONG OVERLAY
        with ui.column().classes(
            'absolute inset-0 items-center justify-center gap-6 text-white '
            'bg-red-900/60 backdrop-blur-md p-10 rounded-3xl cursor-pointer'
        ) as wrong_overlay:
            ui.label('Fel val!').classes('text-4xl font-bold font-jetbrains text-red-300')
            wrong_msg_label = ui.label().classes('text-lg max-w-3xl text-center opacity-90 font-jetbrains')
            ui.label('Klicka för att fortsätta...').classes('text-sm opacity-60 font-jetbrains mt-4')
        wrong_overlay.visible = False
        wrong_overlay.on('click', lambda _: proceed_to_next())

        # END OVERLAY
        with ui.column().classes(
            'absolute inset-0 items-center justify-center gap-6 text-white '
            'bg-black/50 backdrop-blur-md p-10 rounded-3xl'
        ) as end_overlay:
            ui.label('Spelet är slut!').classes('text-4xl font-bold font-jetbrains')
            ui.label('Tack för att du spelade.').classes('text-lg opacity-80 font-jetbrains')
        end_overlay.visible = False

    # EVENT HANDLERS
    def on_video_ended():
        if game.finished:
            end_overlay.visible = True
            return
        update_choice_ui()
        choice_overlay.visible = True

    video.on('ended', lambda _: on_video_ended())

    def update_choice_ui():
        current = game.current
        title_label.text = f"SCENARIO {game.index + 1}"
        text_label.text = current['text']
        text_a.text = wrap_text(current['a'])
        text_b.text = wrap_text(current['b'])

    # Hämta den senaste användaren från databasen
    def get_current_user_id():
        """Hämtar den senaste användaren från databasen."""
        db = SessionLocal()
        try:
            from backend.app.database.models import User
            from sqlalchemy import desc
            latest_user = db.query(User).order_by(desc(User.user_id)).first()
            if latest_user:
                print(f"Använder senaste användaren: user_id={latest_user.user_id} ({latest_user.username})")
                return latest_user.user_id
            else:
                print("Varning: Ingen användare hittades. Spela kommer att fungera men val sparas inte.")
                return None
        finally:
            db.close()
    
    current_user_id = get_current_user_id()

    def on_click(choice: str):
        is_correct = game.handle_choice(choice)
        current = game.current

        # Spara användarens svar i databasen
        try:
            # Hantera både 'id' (mock.json) och 'scenario_id' (databas)
            scenario_id = current.get('id') or current.get('scenario_id')
            scenario_text = current.get('text', '')
            
            if not scenario_text:
                print("Varning: Scenario saknar 'text', hoppar över databas-sparning")
            else:
                db = SessionLocal()
                try:
                    print(f"Försöker spara val för scenario (text: '{scenario_text[:50]}...'), user_id={current_user_id}")
                    
                    # Försök hitta scenario i DB baserat på text (eftersom mock.json ID:n kanske inte matchar DB ID:n)
                    from backend.app.database.models import Scenario
                    scenario_db = db.query(Scenario).filter(Scenario.scenario_text == scenario_text).first()
                    
                    # Om inte hittat med text, försök med ID om det finns
                    if not scenario_db and scenario_id:
                        scenario_db = get_scenario(db, scenario_id)
                    
                    if not scenario_db:
                        # Tyst hoppa över om scenario inte finns i databasen
                        pass
                    elif not current_user_id:
                        print(f"Varning: Ingen användare hittades. Valet kommer inte att sparas.")
                        print(f"   Registrera dig först via frontend för att spara dina val.")
                    else:
                        level_id = scenario_db.level_id
                        db_scenario_id = scenario_db.scenario_id
                        print(f"Hittade scenario i DB: scenario_id={db_scenario_id}, level_id={level_id}")
                        
                        # Hämta alla choice_options för detta scenario
                        choice_options = get_choice_options(db, db_scenario_id)
                        
                        # Matcha valet ('a' eller 'b') med rätt choice_id baserat på texten
                        choice_text = current[choice]  # 'a' eller 'b' text
                        choice_id = None
                        
                        # Hitta choice_id som matchar valets text
                        for co in choice_options:
                            if co.option_text.strip() == choice_text.strip():
                                choice_id = co.choice_id
                                break
                        
                        # Om vi hittar ett matchande val, spara det
                        if choice_id:
                            # Kolla vilka attribut som kommer att påverkas
                            from backend.app.database.crud import get_choice_attributes
                            choice_attrs = get_choice_attributes(db, choice_id)
                            
                            if choice_attrs:
                                print(f"Hittat {len(choice_attrs)} attribut som kommer att påverkas för choice_id {choice_id}")
                            else:
                                print(f"Varning: Choice ID {choice_id} är inte kopplad till några attribut!")
                                print(f"   Attributen kommer inte att uppdateras. Kolla choice_attributes tabellen.")
                            
                            save_user_choice_and_update_attributes(
                                db,
                                user_id=current_user_id,
                                level_id=level_id,
                                scenario_id=db_scenario_id,
                                choice_id=choice_id
                            )
                            print(f"Sparat val: user_id={current_user_id}, scenario_id={db_scenario_id}, choice_id={choice_id}")
                        else:
                            print(f"Varning: Kunde inte hitta matchande choice_id för val '{choice}' i scenario {db_scenario_id}")
                finally:
                    db.close()
        except Exception as e:
            # Om något går fel, logga men fortsätt spelet
            print(f"Fel vid sparning till databas: {e}")
            import traceback
            traceback.print_exc()
            if 'db' in locals():
                db.close()

        choice_overlay.visible = False

        if is_correct:
            # Hantera både 'right_msg' (mock.json) och andra format
            msg = current.get('right_msg') or current.get('correct_msg') or 'Rätt val!'
            correct_msg_label.text = msg
            correct_overlay.visible = True
        else:
            # Hantera både 'wrong_msg' (mock.json) och andra format
            msg = current.get('wrong_msg') or current.get('incorrect_msg') or 'Fel val!'
            wrong_msg_label.text = msg
            wrong_overlay.visible = True

    def proceed_to_next():
        correct_overlay.visible = False
        wrong_overlay.visible = False
        game.advance()

        if game.finished:
            end_overlay.visible = True
        else:
            video_info = get_video(user_info, game.index, video_save_folder)
            if video_info["video_exists"]:
                video.set_source(video_info["video_bytes"])
            else:
                video.set_source(game.video_path(correct=True))
            video.run_method('play')

    video.run_method('play')

if __name__ in ('__main__', '__mp_main__'):
    ui.run(title='Crisis Game')