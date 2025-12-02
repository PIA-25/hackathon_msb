#test 2

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nicegui import ui
import pandas as pd
import plotly.graph_objects as go
from db import get_statistics, get_question_statistics, save_user_response, get_accounts



ui.colors(
    primary='#1e293b',   
    secondary='#3b82f6', 
    accent='#14b8a6',    
    positive='#22c55e',
    negative='#ef4444',
    info='#f3f4f6'       
)


ui.add_head_html('''
    <style>
        body { background-color: #f8fafc; } /* Mycket ljus gråblå bakgrund */
        .nicegui-content { max-width: 1200px; margin: 0 auto; }
        .glass-card { 
            background: white; 
            border-radius: 12px; 
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            border: 1px solid #e2e8f0;
        }
    </style>
''')



def refresh_stats_logic(labels):

    df = get_statistics()
    acc = get_accounts()
    
    
    if df is not None and not df.empty:
        labels['resp'].set_text(str(len(df)))
        labels['users'].set_text(str(df['user_id'].nunique() if 'user_id' in df.columns else 0))
        labels['qs'].set_text(str(df['question'].nunique() if 'question' in df.columns else 0))
        labels['grid_stats'].options['rowData'] = df.to_dict('records')
        labels['grid_stats'].update()
    
    if acc is not None and not acc.empty:
        labels['grid_acc'].options['rowData'] = acc.to_dict('records')
        labels['grid_acc'].update()
    
    ui.notify('Data uppdaterad', type='positive', icon='check')

def update_chart_logic(e, container):
    """Ritar grafen"""
    container['chart'].clear()
    container['table'].clear()
    
    if not e.value:
        return

    stats_df = get_question_statistics(e.value)
    
    if stats_df is not None and not stats_df.empty:
        fig = go.Figure(data=[go.Pie(
            labels=stats_df['answer'].tolist(),
            values=stats_df['count'].tolist(),
            hole=0.4, 
            marker=dict(colors=['#3b82f6', '#14b8a6', '#f43f5e', '#f59e0b']) 
        )])
        fig.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        with container['chart']:
            ui.plotly(fig).classes('w-full h-64')
        
        with container['table']:
            ui.aggrid.from_pandas(stats_df).classes('h-64')

def save_logic(inputs):
    """Sparar användaren"""
    uid, q, ans = inputs['uid'].value, inputs['q'].value, inputs['ans'].value
    
    if uid and q and ans:
        if save_user_response(uid, q, ans):
            ui.notify('Svaret har sparats!', type='positive', icon='cloud_done')
            # Rensa formulär
            inputs['uid'].value = ''
            inputs['q'].value = ''
            inputs['ans'].value = None
        else:
            ui.notify('Kunde inte spara till databasen.', type='negative')
    else:
        ui.notify('Vänligen fyll i alla fält.', type='warning')


# --- UI LAYOUT ---


with ui.header().classes('bg-slate-900 text-white h-16 flex items-center shadow-md px-6'):
    ui.icon('analytics', size='md').classes('mr-2 text-teal-400')
    ui.label('Respondent Dashboard').classes('text-xl font-bold tracking-wide')
    ui.space()
    ui.label('v2.0').classes('text-xs text-slate-400 bg-slate-800 px-2 py-1 rounded')


with ui.column().classes('w-full gap-6 p-6'):
    
    
    with ui.tabs().classes('w-full bg-white rounded-lg shadow-sm text-slate-600') as tabs:
        tab_stats = ui.tab('Översikt', icon='dashboard')
        tab_analysis = ui.tab('Analys', icon='pie_chart')
        tab_admin = ui.tab('Administration', icon='settings')

    
    with ui.tab_panels(tabs, value=tab_stats).classes('w-full bg-transparent'):
        
       
        with ui.tab_panel(tab_stats).classes('p-0 gap-6'):
            
            
            with ui.row().classes('w-full gap-4'):
                
                def stat_card(title, icon, color_class):
                    with ui.card().classes('flex-1 glass-card p-4 flex flex-row items-center gap-4 relative overflow-hidden'):
                        
                        ui.element('div').classes(f'absolute left-0 top-0 bottom-0 w-1 {color_class}')
                        ui.icon(icon, size='lg').classes(f'text-gray-300')
                        with ui.column().classes('gap-0'):
                            ui.label(title).classes('text-xs font-bold text-gray-400 uppercase tracking-wider')
                            lbl = ui.label('0').classes('text-3xl font-black text-slate-700')
                        return lbl

                lbl_total_resp = stat_card('Totala Svar', 'folder_open', 'bg-blue-500')
                lbl_total_users = stat_card('Unika Användare', 'group', 'bg-teal-500')
                lbl_total_qs = stat_card('Unika Frågor', 'help_outline', 'bg-rose-500')

            # Datatabeller
            with ui.row().classes('w-full gap-6 mt-4'):
                with ui.column().classes('flex-[2] glass-card p-4'):
                    ui.label('Senaste Responser').classes('text-lg font-bold text-slate-700 mb-2')
                    grid_stats = ui.aggrid.from_pandas(pd.DataFrame()).classes('w-full h-64')
                
                with ui.column().classes('flex-1 glass-card p-4'):
                    ui.label('Registrerade Konton').classes('text-lg font-bold text-slate-700 mb-2')
                    grid_acc = ui.aggrid.from_pandas(pd.DataFrame()).classes('w-full h-64')

            # Uppdateringsknapp
            labels_dict = {
                'resp': lbl_total_resp, 'users': lbl_total_users, 'qs': lbl_total_qs,
                'grid_stats': grid_stats, 'grid_acc': grid_acc
            }
            ui.button('Uppdatera Data', icon='refresh', on_click=lambda: refresh_stats_logic(labels_dict))\
                .classes('bg-slate-800 text-white shadow-lg')

        
        with ui.tab_panel(tab_analysis).classes('p-0'):
            with ui.row().classes('w-full h-full gap-6'):
                # Sidebar för val
                with ui.card().classes('w-1/4 glass-card p-6 h-auto'):
                    ui.label('Filter').classes('text-lg font-bold text-slate-700 mb-4')
                    q_select = ui.select(label='Välj fråga att analysera', options={}).classes('w-full')
                    
                    # Ladda frågor knapp
                    def load_qs_click():
                        df = get_statistics()
                        if df is not None and not df.empty and 'question' in df.columns:
                            questions = df['question'].unique().tolist()
                            q_select.options = {q: q for q in questions}
                            ui.notify(f'Laddade {len(questions)} frågor', type='info')
                    
                    ui.button('Ladda Frågor', on_click=load_qs_click, icon='cloud_download').classes('w-full mt-4 bg-slate-100 text-slate-800')

                # Resultatvy
                with ui.column().classes('flex-1 gap-4'):
                    chart_ui = ui.column().classes('w-full glass-card p-4')
                    table_ui = ui.column().classes('w-full glass-card p-4')
                    
                    container_dict = {'chart': chart_ui, 'table': table_ui}
                    q_select.on_value_change(lambda e: update_chart_logic(e, container_dict))

        
        with ui.tab_panel(tab_admin).classes('p-0 flex justify-center'):
            with ui.card().classes('w-full max-w-lg glass-card p-8'):
                ui.label('Manuell Inmatning').classes('text-xl font-bold text-slate-800 mb-1')
                ui.label('Lägg till testsvar eller saknad data manuellt.').classes('text-sm text-gray-500 mb-6')
                
                with ui.column().classes('w-full gap-4'):
                    inp_uid = ui.input(label='Respondent ID').classes('w-full').props('outlined dense')
                    inp_q = ui.input(label='Fråga').classes('w-full').props('outlined dense')
                    inp_ans = ui.select(options=['Ja', 'Nej', 'Vet inte', 'Vägrar'], label='Svar').classes('w-full').props('outlined dense')
                    
                    ui.separator().classes('my-2')
                    
                    inputs_dict = {'uid': inp_uid, 'q': inp_q, 'ans': inp_ans}
                    ui.button('Spara till Databas', icon='save', on_click=lambda: save_logic(inputs_dict))\
                        .classes('w-full bg-teal-600 hover:bg-teal-700 text-white shadow-md')
                    




if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title='Respondent Dashboard',
        favicon='analytics',
        port=8080,
        reload=True
    )
