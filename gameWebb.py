from mock_data.mock import scenarios
from nicegui import ui

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

        current = self.current
        if choice == current['correct']:
            self.feedback = 'Rätt val, du fortsätter...'
        else:
            self.feedback = f"Fel val. {current['wrong_msg']}"
        # next scenario
        self.index += 1
        if self.index >= len(self.scenarios):
            self.finished = True

game = GameUI()
show_start_overlay = True  # At the top, after game = GameUI()

@ui.page('/')
def index() -> None:
    global show_start_overlay

    with ui.element('div').classes('w-full h-screen overflow-hidden'):
        # --- Start overlay ---
        with ui.column().classes(
            'absolute inset-0 items-center justify-center gap-6 text-white bg-black/70 z-10'
        ) as start_overlay:
            ui.label('Välkommen till Crisis Game!').classes('text-4xl font-bold')
            ui.button('Starta spelet', on_click=lambda: start_game()).classes(
                'bg-green-600 text-white text-xl px-8 py-4 rounded-full mt-4'
            )
        start_overlay.visible = show_start_overlay

        # --- Main game overlay ---
        video = ui.video(
            current_video_path(),
        ).classes(
            'absolute inset-0 w-full h-full object-cover pointer-events-none'
        ).on('ended', lambda _: update_ui())

        with ui.column().classes(
            'absolute inset-0 items-center justify-center gap-4 text-white bg-black/40 p-6'
        ) as overlay:
            title_label = ui.label().classes('text-3xl font-bold')
            text_label = ui.label().classes('text-lg max-w-3xl text-center')
            feedback_label = ui.label().classes('text-md text-yellow-200')
            with ui.row().classes('gap-4'):
                btn_a = ui.button()
                btn_b = ui.button()
            end_label = ui.label().classes('text-3xl font-bold mt-4')
        overlay.visible = False

    def start_game():
        global show_start_overlay
        show_start_overlay = False
        start_overlay.visible = False
        overlay.visible = True
        update_ui()

    def update_ui():
        if game.finished:
            title_label.text = 'The End'
            text_label.text = ''
            feedback_label.text = game.feedback
            btn_a.visible = False
            btn_b.visible = False
            end_label.text = 'Spelet är slut.'
            return
        current = game.current
        title_label.text = f'Scenario {game.index + 1}'
        text_label.text = current['text']
        feedback_label.text = game.feedback
        btn_a.text = f"a) {current['a']}"
        btn_b.text = f"b) {current['b']}"
        overlay.visible = True
        btn_a.visible = True
        btn_b.visible = True
        end_label.text = ''
    def newSinario ():
        overlay.visible = False
        video.set_source(current_video_path())
        video.run_method('play')


    def on_click(choice: str):
        game.handle_choice(choice)
        update_ui()
        newSinario ()

    btn_a.on_click(lambda: on_click('a'))
    btn_b.on_click(lambda: on_click('b'))




if __name__ in ('__main__', '__mp_main__'):
    ui.run(title='Crisis Game')
