"""
Stats Section Component
=======================
Shows project stats
"""

from nicegui import ui
from config.theme import COLORS, SIZES, EFFECTS

from backend.app.database.analytics import (
    get_choice_overview,
    get_age_behavior,
    get_attribute_impacts,
)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

def create_stats_section():
    """Creates the stats-section with three analytics charts"""
    
    # Fetch data with fallbacks for empty database
    try:
        choice_data = get_choice_overview() or [{'scenario': 1, 'good': 0, 'bad': 0}]
        age_data = get_age_behavior() or []
        attr_data = get_attribute_impacts() or [{'name': 'Ingen data', 'score': 0}]
    except Exception as e:
        print(f"Error fetching analytics data: {e}")
        # Fallback to empty data
        choice_data = [{'scenario': 1, 'good': 0, 'bad': 0}]
        age_data = []
        attr_data = [{'name': 'Ingen data', 'score': 0}]
    
    # Prepare age data for chart
    bands, good_counts, bad_counts = _prepare_age_series(age_data)
    
    with ui.column().classes('w-full items-center').style(
        f'padding: 6rem 2rem; background: {COLORS["background_primary"]}'
    ):

        # Section title
        ui.label('PROJEKTDATA').style(
            f'color: {COLORS["text_white"]}; '
            f'font-size: {SIZES["section_title"]}; '
            f'font-weight: bold; '
            f'letter-spacing: 4px; '
            f'margin-bottom: 3rem; '
            f'text-align: center; '
            f'text-shadow: {EFFECTS["text_shadow"]}'
        )
        
        # Row with three charts
        with ui.row().classes('w-full justify-center gap-8 flex-wrap'):
            
            # Chart 1: Choice overview per scenario
            _chart_card(
                'Valfördelning per scenario',
                'Visar hur många bra/dåliga beslut som tagits i varje scenario.',
                _choice_chart_options(choice_data)
            )
            
            # Chart 2: Age behavior
            _chart_card(
                'Beteende per åldersgrupp',
                'Jämför hur olika åldersband tenderar att välja.',
                _age_chart_options(bands, good_counts, bad_counts)
            )
            
            # Chart 3: Attribute impacts
            _chart_card(
                'Attributpåverkan',
                'Summerar hur spelarnas val påverkar olika attribut.',
                _attribute_chart_options(attr_data)
            )


def create_stat(number: str, label: str):
    """
    Creates a stat
    
    Args:
        number: The number to show
        label: Description text underneath
    """
    with ui.column().classes('items-center'):
        # Big number with blue glow
        ui.label(number).style(
            f'color: {COLORS["accent_bright"]}; '
            f'font-size: 72px; '
            f'font-weight: bold; '
            f'text-shadow: {EFFECTS["glow_medium"]}; '
            f'margin-bottom: 0.5rem'
        )
        
        # Label
        ui.label(label).style(
            f'color: {COLORS["text_blue"]}; '
            f'font-size: 20px; '
            f'letter-spacing: 1px'
        )
        
def _chart_card(title: str, subtitle: str, options: dict):
    with ui.card().style(
        f'background: {COLORS["background_card"]}; '
        f'border: 1px solid {COLORS["border_card"]}; '
        f'border-radius: 16px; '
        f'padding: 1.5rem; '
        f'width: 380px; '
        f'min-height: 420px; '
        f'box-shadow: {EFFECTS["card_shadow"]}'
    ):
        ui.label(title).style(
            f'color: {COLORS["text_white"]}; '
            f'font-size: 22px; '
            f'font-weight: bold; '
            f'margin-bottom: 0.5rem'
        )
        ui.label(subtitle).style(
            f'color: {COLORS["text_muted"]}; '
            f'font-size: 15px; '
            f'margin-bottom: 1rem'
        )
        ui.echart(options).style('width: 100%; height: 320px')


def _choice_chart_options(choice_data: list[dict]) -> dict:
    categories = [f'Scen {d["scenario"]}' for d in choice_data]
    good = [d['good'] for d in choice_data]
    bad = [d['bad'] for d in choice_data]

    return {
        'tooltip': {'trigger': 'axis'},
        'legend': {'data': ['Bra', 'Dåliga']},
        'xAxis': {'type': 'category', 'data': categories},
        'yAxis': {'type': 'value'},
        'series': [
            {'name': 'Bra', 'type': 'bar', 'stack': 'choices', 'data': good},
            {'name': 'Dåliga', 'type': 'bar', 'stack': 'choices', 'data': bad},
        ],
    }

def _prepare_age_series(age_rows: list[dict]):
    if not age_rows:
        return ['18-27'], [0], [0]

    bands = sorted({row['age_band'] for row in age_rows})
    good_counts = []
    bad_counts = []

    for band in bands:
        good_counts.append(
            sum(row['count'] for row in age_rows if row['age_band'] == band and row['is_good'])
        )
        bad_counts.append(
            sum(row['count'] for row in age_rows if row['age_band'] == band and row['is_good'] is False)
        )

    labels = [f'{band}-{band + 9}' for band in bands]
    return labels, good_counts, bad_counts


def _age_chart_options(bands: list[str], good: list[int], bad: list[int]) -> dict:
    return {
        'tooltip': {'trigger': 'axis'},
        'legend': {'data': ['Bra val', 'Dåliga val']},
        'xAxis': {'type': 'category', 'data': bands},
        'yAxis': {'type': 'value'},
        'series': [
            {'name': 'Bra val', 'type': 'bar', 'stack': 'age', 'data': good},
            {'name': 'Dåliga val', 'type': 'bar', 'stack': 'age', 'data': bad},
        ],
    }
    
def _attribute_chart_options(attr_data: list[dict]) -> dict:
    names = [a['name'] for a in attr_data]
    scores = [a['score'] for a in attr_data]

    return {
        'tooltip': {'trigger': 'axis'},
        'xAxis': {'type': 'value'},
        'yAxis': {'type': 'category', 'data': names},
        'series': [
            {'name': 'Poäng', 'type': 'bar', 'data': scores},
        ],
    }

