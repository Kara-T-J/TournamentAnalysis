from dash import Dash, html, dcc, Input, Output, callback
import dash
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

df = pd.read_excel('data/intermediate/WT25_notes_long.xlsx')

app = Dash(__name__)


# Utility functions
def column_width(col_name):
    max_len = df[col_name].astype(str).map(len).max()
    return max(100, min(max_len * 10 + 20, 300))

def AgGrid_widths(df):
    widths = {}
    total = 17
    for col in df.columns:
        widths[col] = column_width(col)
        total += widths[col]
    widths["_total"] = total
    return widths


# Constants
ALL_SPINNERS = sorted(df['Spinner'].unique().tolist())
ALL_JUDGES = sorted(df['Judge'].unique().tolist())
ALL_CRITERIA = sorted(df['Criterion'].unique().tolist())
ALL_ROUNDS = sorted(df['Round'].unique().tolist())
COLUMN_WIDTHS = AgGrid_widths(df)


crit_violin = px.violin(df, y="Score", x="Criterion", box=True, points="all", title="Score Distribution by Criterion")
crit_violin.update_layout(plot_bgcolor="#edf5ff")
crit_violin.update_layout(paper_bgcolor="#edf5ff")
crit_violin.update_yaxes(
    showgrid=True,
    gridcolor="#d9e0e8",
    gridwidth=1,
    zeroline=False
)

# Layout
app.layout = html.Div([
    html.H1("Penspinning Tournament Analysis", className="header-title"),
    html.Div(
        [
            html.Div(
                [
                    html.Button(
                        "Reset Filters",
                        id='reset-filters',
                        n_clicks=0,
                        className="btn"
                    ),
                    html.Button(
                        "Select All",
                        id='select-all',
                        n_clicks=0,
                        className="btn"
                    ),
                ],
                className="filters-actions"
            ),
            html.Div(
                [
                    html.Div(
                        dcc.Dropdown(
                            id='spinner-dropdown',
                            options=ALL_SPINNERS,
                            multi=True,
                            placeholder="Select Spinners"
                        ),
                        className="dropdown"
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='judge-dropdown',
                            options=ALL_JUDGES,
                            multi=True,
                            placeholder="Select Judges"
                        ),
                        className="dropdown"
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='round-dropdown',
                            options=ALL_ROUNDS,
                            multi=True,
                            placeholder="Select Rounds"
                        ),
                        className="dropdown"
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='criteria-dropdown',
                            options=ALL_CRITERIA,
                            value=['Construction', 'Creativity', 'Deduction', 'Difficulty', 'Execution'],
                            multi=True,
                            placeholder="Select Criteria"
                        ),
                        className="dropdown"
                    ),
                ],
                className="filters-grid"
            ),
        ],
        className="filters-row"
    ),
    
    html.Div([
        dag.AgGrid(
            id='data-table',
            rowData=df.to_dict('records'),
            columnDefs=[{"field": c, "width": COLUMN_WIDTHS.get(c)} for c in df.columns],
            style={
                "height": "700px",
                "width": f'{COLUMN_WIDTHS.get("_total", 0)}px',
            },
            className="aggrid"
        ),
        dcc.Graph(
            figure=crit_violin,
            id ='crit-violin',
            style={"flex": "1 1 400px", "minWidth": "300px", "height": "700px"},
            className="violin-plot"
        ),
    ], style={"display": "flex", "flexWrap": "wrap", "gap": "10px", "justifyContent": "center", "marginBottom": "20px","marginTop": "10px"}),

], style={"padding": "20px"})

# Filter table with dropdowns
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

# Filter violin plot with dropdowns
@callback(
    Output('crit-violin', 'figure'), 
    Input('spinner-dropdown', 'value'),
    Input('judge-dropdown', 'value'),
    Input('round-dropdown', 'value'),
    Input('criteria-dropdown', 'value')
)
def update_violin(selected_spinners, selected_judges, selected_rounds, selected_criteria):
    filtered_df = df.copy() 
    if selected_spinners:
        filtered_df = filtered_df[filtered_df['Spinner'].isin(selected_spinners)]
    if selected_judges:
        filtered_df = filtered_df[filtered_df['Judge'].isin(selected_judges)]
    if selected_rounds:
        filtered_df = filtered_df[filtered_df['Round'].isin(selected_rounds)]
    if selected_criteria:
        filtered_df = filtered_df[filtered_df['Criterion'].isin(selected_criteria)]
    fig = px.violin(filtered_df, y="Score", x="Criterion", box=True, points="all", title="Score Distribution by Criterion")
    fig=fig.update_layout(plot_bgcolor="#edf5ff")
    fig=fig.update_layout(paper_bgcolor="#edf5ff")
    fig=fig.update_yaxes(
    showgrid=True,
    gridcolor="#d9e0e8",
    gridwidth=1,
    zeroline=False
)
    return fig

# Quickly reset or select all filters
@callback(
    Output('spinner-dropdown', 'value'),
    Output('judge-dropdown', 'value'),
    Output('round-dropdown', 'value'),
    Output('criteria-dropdown', 'value'),
    Input('reset-filters', 'n_clicks'),
    Input('select-all', 'n_clicks')
)
def control_filters(_n_clicks, _m_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'reset-filters':
        return None, None, None, None
    elif button_id == 'select-all':
        return ALL_SPINNERS, ALL_JUDGES, ALL_ROUNDS, ALL_CRITERIA

if __name__ == '__main__':
    app.run(debug=True)
