from dash import Dash, html, dcc, Input, Output, callback
import dash
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

df = pd.read_excel('data/intermediate/WT25_notes_long.xlsx')

app = Dash(__name__)


ALL_SPINNERS = sorted(df['Spinner'].unique().tolist())
ALL_JUDGES = sorted(df['Judge'].unique().tolist())
ALL_CRITERIA = sorted(df['Criterion'].unique().tolist())
ALL_ROUNDS = sorted(df['Round'].unique().tolist())


app.layout = [
    html.H1("Penspinning Tournament Analysis", style={'textAlign': 'center'}),
    html.Div(html.Button("Reset Filters", id='reset-filters', n_clicks=0), style={'textAlign': 'center', 'marginBottom': '20px'}),
    html.Div([
        html.Div(dcc.Dropdown(id = 'spinner-dropdown', options = ALL_SPINNERS, multi = True, placeholder="Select Spinners"), style={"flex": "1 1 45%", "minWidth": "260px"}),
        html.Div(dcc.Dropdown(id = 'judge-dropdown', options = ALL_JUDGES, multi = True, placeholder="Select Judges"), style={"flex": "1 1 45%", "minWidth": "260px"}),
        html.Div(dcc.Dropdown(id = 'round-dropdown', options = ALL_ROUNDS, multi = True, placeholder="Select Rounds"), style={"flex": "1 1 45%", "minWidth": "260px"}),
        html.Div(dcc.Dropdown(id = 'criteria-dropdown', options = ALL_CRITERIA, multi = True, placeholder="Select Criteria"), style={"flex": "1 1 45%", "minWidth": "260px"}),
    ], style={"display": "flex", "flexWrap": "wrap", "gap": "10px", "justifyContent": "center", "marginBottom": "20px"}),

    dag.AgGrid(id='data-table', rowData=df.to_dict('records'), columnDefs=[{"field": i} for i in df.columns]) 
]


@callback(
    Output('data-table', 'rowData'),
    Input('spinner-dropdown', 'value'),
    Input('judge-dropdown', 'value'),
    Input('round-dropdown', 'value'),
    Input('criteria-dropdown', 'value')
)
def update_table(selected_spinners, selected_judges, selected_rounds, selected_criteria):
    filtered_df = df.copy()

    if selected_spinners:
        filtered_df = filtered_df[filtered_df['Spinner'].isin(selected_spinners)]
    if selected_judges:
        filtered_df = filtered_df[filtered_df['Judge'].isin(selected_judges)]
    if selected_rounds:
        filtered_df = filtered_df[filtered_df['Round'].isin(selected_rounds)]
    if selected_criteria:
        filtered_df = filtered_df[filtered_df['Criterion'].isin(selected_criteria)]
    return filtered_df.to_dict('records')

@callback(
    Output('spinner-dropdown', 'value'),
    Output('judge-dropdown', 'value'),
    Output('round-dropdown', 'value'),
    Output('criteria-dropdown', 'value'),
    Input('reset-filters', 'n_clicks')
)
def reset_filters(n_clicks):
    if n_clicks > 0:
        return None, None, None, None
    return dash.no_update

if __name__ == '__main__':
    app.run(debug=True)
