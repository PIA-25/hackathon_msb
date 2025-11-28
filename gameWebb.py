from mock_data.mock import scenarios
from nicegui import ui
import textwrap

# -------------------------------------------------------
# TEXT WRAPPING FUNCTION (ADDED)
# -------------------------------------------------------
def wrap_text(text: str, width: int = 40) -> str:
    """Remove leading newlines and wrap text cleanly."""
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
        self.feedback = ''

    @property
    def current(self):
        return self.scenarios[self.index]

    @property
    def video_path(self) -> str:
        return f'mock_data/video{self.index}.mp4'

    def handle_choice(self, choice: str):
        if self.finished:
            return

        if choice == self.current['correct']:
            self.feedback = 'Rätt val, du fortsätter...'
        else:
            self.feedback = f"Fel val. {self.current['wrong_msg']}"

        self.index += 1
        if self.index >= len(self.scenarios):
            self.finished = True


game = GameUI()


# -------------------------------------------------------
# PAGE UI
# -------------------------------------------------------
@ui.page('/')
def index():

    # Load JetBrains Mono font
    ui.add_head_html("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/JetBrainsMono/2.304.0/jetbrains-mono.min.css" rel="stylesheet">
    <style>
        .font-jetbrains { font-family: 'JetBrains Mono', monospace !important; }
    </style>
    """)

    def current_video_path() -> str:
        return game.video_path

    # Background video
    with ui.element('div').classes('w-full h-screen overflow-hidden'):

        video = ui.video(current_video_path()) \
            .classes('absolute inset-0 w-full h-full object-cover') \
            .on('ended', lambda _: update_ui())

        # Overlay UI
        with ui.column().classes(
            'absolute inset-0 items-center justify-center gap-6 text-white '
            'bg-black/30 backdrop-blur-md p-10 rounded-3xl'
        ) as overlay:

            title_label = ui.label().classes('text-4xl font-bold font-jetbrains')
            text_label = ui.label().classes('text-lg max-w-3xl text-center opacity-80 font-jetbrains')
            feedback_label = ui.label().classes('text-md text-yellow-200 font-jetbrains')

            # -------------------------------------------------------
            # CHOICE A (unchanged layout)
            # -------------------------------------------------------
            with ui.row().classes(
                'items-center gap-6 bg-black/40 backdrop-blur-md rounded-2xl '
                'px-6 py-5 w-full max-w-3xl cursor-pointer hover:bg-black/60 transition-all'
            ) as block_a:

                ui.label('A').classes(
                    'text-white text-2xl font-bold font-jetbrains'
                )

                ui.element('div').classes(
                    'h-10 w-px bg-white/40'
                )

                text_a = ui.label().classes(
                    'text-white text-lg font-jetbrains leading-snug whitespace-pre-line'
                )

            block_a.on('click', lambda e: on_click('a'))

            # -------------------------------------------------------
            # CHOICE B (unchanged layout)
            # -------------------------------------------------------
            with ui.row().classes(
                'items-center gap-6 bg-black/40 backdrop-blur-md rounded-2xl '
                'px-6 py-5 w-full max-w-3xl cursor-pointer hover:bg-black/60 transition-all'
            ) as block_b:

                ui.label('B').classes(
                    'text-white text-2xl font-bold font-jetbrains'
                )

                ui.element('div').classes(
                    'h-10 w-px bg-white/40'
                )

                text_b = ui.label().classes(
                    'text-white text-lg font-jetbrains leading-snug whitespace-pre-line'
                )

            block_b.on('click', lambda e: on_click('b'))

            end_label = ui.label().classes('text-3xl font-bold mt-4 font-jetbrains')

        overlay.visible = False

    # -------------------------------------------------------
    # UPDATE UI WHEN VIDEO ENDS OR A/B CLICKED
    # -------------------------------------------------------
    def update_ui():
        if game.finished:
            title_label.text = 'The End'
            text_label.text = ''
            feedback_label.text = game.feedback
            text_a.text = ''
            text_b.text = ''
            end_label.text = 'Spelet är slut.'
            overlay.visible = True
            return

        current = game.current
        title_label.text = f"SCENARIO {game.index + 1}"
        text_label.text = current['text']
        feedback_label.text = game.feedback

        # -------------------------------------------------------
        # UPDATED: wrap and clean A/B text
        # -------------------------------------------------------
        text_a.text = wrap_text(current['a'])
        text_b.text = wrap_text(current['b'])

        end_label.text = ''
        overlay.visible = True

    # -------------------------------------------------------
    # PLAY NEXT VIDEO
    # -------------------------------------------------------
    def new_scenario():
        overlay.visible = False
        video.set_source(current_video_path())
        video.run_method('play')

    # -------------------------------------------------------
    # HANDLE USER CHOICE
    # -------------------------------------------------------
    def on_click(choice: str):
        game.handle_choice(choice)
        update_ui()
        new_scenario()


# -------------------------------------------------------
# RUN APP
# -------------------------------------------------------
if __name__ in ('__main__', '__mp_main__'):
    ui.run(title='Crisis Game')

