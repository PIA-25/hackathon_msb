import json
from nicegui import ui
import textwrap


# -------------------------------------------------------
# LOAD JSON SCENARIOS
# -------------------------------------------------------
def load_scenarios():
    with open('../mock_data/mock.json', 'r', encoding='utf-8') as f:
        return json.load(f)["scenarios"]

scenarios = load_scenarios()


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

    def video_path(self, correct: bool) -> str:
        # Returns correct or wrong video based on choice
        suffix = 'correct' if correct else 'wrong'
        return f'../mock_data/video{self.index}.mp4'

    def handle_choice(self, choice: str) -> bool:
        """Returns True if choice was correct, False otherwise"""
        if self.finished:
            return False

        is_correct = choice == self.current['correct']
        self. last_choice_correct = is_correct
        return is_correct

    def advance(self):
        """Move to the next scenario"""
        self.index += 1
        if self.index >= len(self.scenarios):
            self.finished = True


game = GameUI()


# -------------------------------------------------------
# PAGE UI
# -------------------------------------------------------
@ui.page('/')
def index():

    ui.add_head_html("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/JetBrainsMono/2. 304.0/jetbrains-mono. min.css" rel="stylesheet">
    <style>
        .font-jetbrains { font-family: 'JetBrains Mono', monospace ! important; }
    </style>
    """)

    with ui.element('div').classes('w-full h-screen overflow-hidden'):

        # Video element - starts with first scenario's correct path
        video = ui.video(f'../mock_data/video0.mp4') \
            .classes('absolute inset-0 w-full h-full object-cover')

        # -------------------------------------------------------
        # CHOICE OVERLAY (shown after video ends)
        # -------------------------------------------------------
        with ui.column().classes(
            'absolute inset-0 items-center justify-center gap-6 text-white '
            'bg-black/30 backdrop-blur-md p-10 rounded-3xl'
        ) as choice_overlay:

            title_label = ui. label().classes('text-4xl font-bold font-jetbrains')
            text_label = ui. label().classes('text-lg max-w-3xl text-center opacity-80 font-jetbrains')

            # ---------- CHOICE A ----------
            with ui.row().classes(
                'items-center gap-6 bg-black/40 backdrop-blur-md rounded-2xl '
                'px-6 py-5 w-full max-w-3xl cursor-pointer hover:bg-black/60 transition-all'
            ) as block_a:
                ui.label('A').classes('text-white text-2xl font-bold font-jetbrains')
                ui. element('div').classes('h-10 w-px bg-white/40')
                text_a = ui. label().classes('text-white text-lg font-jetbrains leading-snug whitespace-pre-line')

            block_a.on('click', lambda e: on_click('a'))

            # ---------- CHOICE B ----------
            with ui. row().classes(
                'items-center gap-6 bg-black/40 backdrop-blur-md rounded-2xl '
                'px-6 py-5 w-full max-w-3xl cursor-pointer hover:bg-black/60 transition-all'
            ) as block_b:
                ui.label('B').classes('text-white text-2xl font-bold font-jetbrains')
                ui.element('div').classes('h-10 w-px bg-white/40')
                text_b = ui. label().classes('text-white text-lg font-jetbrains leading-snug whitespace-pre-line')

            block_b.on('click', lambda e: on_click('b'))

        choice_overlay.visible = False

        # -------------------------------------------------------
        # CORRECT CHOICE OVERLAY (green)
        # -------------------------------------------------------
        with ui.column().classes(
            'absolute inset-0 items-center justify-center gap-6 text-white '
            'bg-green-900/60 backdrop-blur-md p-10 rounded-3xl cursor-pointer'
        ) as correct_overlay:
            ui.label('✓ Rätt val! ').classes('text-4xl font-bold font-jetbrains text-green-300')
            correct_msg_label = ui.label().classes('text-lg max-w-3xl text-center opacity-90 font-jetbrains')
            ui.label('Klicka för att fortsätta... ').classes('text-sm opacity-60 font-jetbrains mt-4')

        correct_overlay.visible = False
        correct_overlay. on('click', lambda _: proceed_to_next())

        # -------------------------------------------------------
        # WRONG CHOICE OVERLAY (red)
        # -------------------------------------------------------
        with ui.column().classes(
            'absolute inset-0 items-center justify-center gap-6 text-white '
            'bg-red-900/60 backdrop-blur-md p-10 rounded-3xl cursor-pointer'
        ) as wrong_overlay:
            ui.label('✗ Fel val!').classes('text-4xl font-bold font-jetbrains text-red-300')
            wrong_msg_label = ui.label(). classes('text-lg max-w-3xl text-center opacity-90 font-jetbrains')
            ui.label('Klicka för att fortsätta... ').classes('text-sm opacity-60 font-jetbrains mt-4')

        wrong_overlay. visible = False
        wrong_overlay.on('click', lambda _: proceed_to_next())

        # -------------------------------------------------------
        # END GAME OVERLAY
        # -------------------------------------------------------
        with ui.column(). classes(
            'absolute inset-0 items-center justify-center gap-6 text-white '
            'bg-black/50 backdrop-blur-md p-10 rounded-3xl'
        ) as end_overlay:
            ui.label('🎮 Spelet är slut!').classes('text-4xl font-bold font-jetbrains')
            ui.label('Tack för att du spelade. ').classes('text-lg opacity-80 font-jetbrains')

        end_overlay. visible = False

    # -------------------------------------------------------
    # EVENT HANDLERS
    # -------------------------------------------------------
    def on_video_ended():
        """Called when video finishes playing - show choice overlay"""
        if game.finished:
            end_overlay.visible = True
            return
        update_choice_ui()
        choice_overlay.visible = True

    video.on('ended', lambda _: on_video_ended())

    def update_choice_ui():
        """Update the choice overlay with current scenario data"""
        current = game.current
        title_label.text = f"SCENARIO {game.index + 1}"
        text_label.text = current['text']
        text_a.text = wrap_text(current['a'])
        text_b.text = wrap_text(current['b'])

    def on_click(choice: str):
        """Handle user's choice"""
        is_correct = game. handle_choice(choice)
        current = game.current

        # Hide choice overlay
        choice_overlay.visible = False

        if is_correct:
            # Show correct overlay with right_msg
            correct_msg_label.text = current['right_msg']
            correct_overlay.visible = True
        else:
            # Show wrong overlay with wrong_msg
            wrong_msg_label. text = current['wrong_msg']
            wrong_overlay.visible = True

    def proceed_to_next():
        """Proceed to next scenario after viewing feedback"""
        # Hide feedback overlays
        correct_overlay.visible = False
        wrong_overlay.visible = False

        # Advance to next scenario
        game.advance()

        if game.finished:
            end_overlay.visible = True
        else:
            # Play the next scenario's "correct path" video
            video. set_source(game.video_path(correct=True))
            video.run_method('play')

    # Start the game - play first video automatically
    video.run_method('play')


# -------------------------------------------------------
# RUN APP
# -------------------------------------------------------
if __name__ in ('__main__', '__mp_main__'):
    ui.run(title='Crisis Game')