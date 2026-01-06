from dash import Dash, html, dcc, Input, Output, callback
import dash
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

df_long = pd.read_excel('data/intermediate/WT25_notes_long.xlsx')
df      = pd.read_excel('data/intermediate/WT25_notes_cleaned.xlsx')

app     = Dash(__name__)


# Utility functions
def column_width(col_name):
    max_len = df_long[col_name].astype(str).map(len).max()
    return max(100, min(max_len * 10 + 20, 300))

def AgGrid_widths(df_long):
    widths = {}
    total = 39
    for col in df_long.columns:
        widths[col] = column_width(col)
        total += widths[col]
    widths["_total"] = total
    return widths


# Constants
ALL_SPINNERS        = sorted(df_long['Spinner'].unique().tolist())
ALL_JUDGES          = sorted(df_long['Judge'].unique().tolist())
ALL_CRITERIA        = sorted(df_long['Criterion'].unique().tolist())
ALL_ROUNDS          = sorted(df_long['Round'].unique().tolist())
COLUMN_WIDTHS       = AgGrid_widths(df_long)


crit_violin         = px.violin(df_long, y="Score", x="Criterion", box=True, points="all", title="Score Distribution by Criterion").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
judge_violin        = px.violin(df_long, y="Score", x="Judge", box=True, points="all", title="Score Distribution by Judge").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)

judge_violin_total  = px.violin(df, y="Total", x="Judge", box=True, points="all", title="Score Distribution by Judge").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
heatmap_crit_judge_mean = px.imshow(df_long.pivot_table(index="Judge", columns="Criterion", values="Score", aggfunc="mean"), text_auto=".2f", aspect="auto", title = "Average Score per Judge/Criterion",color_continuous_scale="Blues").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff", xaxis_title=None, yaxis_title=None)
heatmap_crit_judge_std  = px.imshow(df_long.pivot_table(index="Judge", columns="Criterion", values="Score", aggfunc="std"), text_auto=".2f", aspect="auto", title ="Standard Deviation per Judge/Criterion",color_continuous_scale="Blues").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff", xaxis_title=None, yaxis_title=None)

# Layout
app.layout = html.Div([
  # Header Section
    html.Div([
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
        html.Div(
            [
                html.Button(
                    "OVERVIEW",
                    id='overview-btn',
                    n_clicks=0,
                    className="tab-btn"
                ),
                html.Button(
                    "JUDGES",
                    id='judges-btn',
                    n_clicks=0,
                    className="tab-btn"
                ),
                html.Button(
                    "CRITERIA",
                    id='criteria-btn',
                    n_clicks=0,
                    className="tab-btn"
                ),
                html.Button(
                    "ROUNDS",
                    id='rounds-btn',
                    n_clicks=0,
                    className="tab-btn"
                ),
                html.Button(
                    "SPINNERS",
                    id='spinners-btn',
                    n_clicks=0,
                    className="tab-btn"
                ),
            ],
            className="nav-row"
        ),
    ], className="header-section"),

    # Overview tab
    # html.Div([
    #     html.Div([
    #         dag.AgGrid(
    #             id='data-table',
    #             rowData=df_long.to_dict('records'),
    #             columnDefs=[{"field": c, "width": COLUMN_WIDTHS.get(c)} for c in df_long.columns],
    #             style={
    #                 "height": "700px",
    #                 "width": f'{COLUMN_WIDTHS.get("_total", 0)}px',
    #                 "resize": False,
    #             },
    #             className="ag-theme-alpine aggrid"
    #         ),
    #         dcc.Graph(
    #             figure=crit_violin,
    #             id ='crit-violin',
    #             style={"flex": "1 1 400px", "minWidth": "300px", "height": "700px"},
    #             className="violin-plot"
    #         ),
    #     ], style={"display": "flex", "flexWrap": "wrap", "gap": "10px", "justifyContent": "center", "marginBottom": "20px","marginTop": "10px"}),
    #     dcc.Graph(
    #         figure=judge_violin,
    #         id ='judge-violin',
    #         style={"width": "100%", "height": "700px"},
    #         className="violin-plot"
    #     ),
    # ], className="body-section"),

    # Judges tab
    html.Div([
        dcc.Graph(
            figure=judge_violin,
            id ='judge-violin-notes',
            style={"width": "100%", "height": "700px"},
            className="violin-plot"
        ),
        html.Div(
            [
            dcc.Graph(
                figure=heatmap_crit_judge_mean,
                id ='heatmap-judge-criteria-mean',
                style={"height": "700px"},
                className="heatmap-plot"
            ),
            dcc.Graph(
                figure=heatmap_crit_judge_std,
                id ='heatmap-judge-criteria-std',
                style={"height": "700px"},
                className="heatmap-plot"
            ),
        ],
        className="heatmap-row"
        ),

        # Heatmap judge criteria bias
        dcc.Graph(
            figure=judge_violin_total,
            id ='judge-violin-total',
            style={"width": "100%", "height": "700px"},
            className="violin-plot"
        ),
    ], className="body-section"),
])

## Header section callbacks
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


## Overview tab callbacks
@callback(
    Output('data-table', 'rowData'),
    Input('spinner-dropdown', 'value'),
    Input('judge-dropdown', 'value'),
    Input('round-dropdown', 'value'),
    Input('criteria-dropdown', 'value')
)
def update_table(selected_spinners, selected_judges, selected_rounds, selected_criteria):
    filtered_df = df_long.copy()

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
    Output('crit-violin', 'figure'),
    Output('judge-violin', 'figure'),
    Input('spinner-dropdown', 'value'),
    Input('judge-dropdown', 'value'),
    Input('round-dropdown', 'value'),
    Input('criteria-dropdown', 'value')
)
def update_violin(selected_spinners, selected_judges, selected_rounds, selected_criteria):
    filtered_df = df_long.copy() 
    
    if selected_spinners:
        filtered_df = filtered_df[filtered_df['Spinner'].isin(selected_spinners)]
    if selected_judges:
        filtered_df = filtered_df[filtered_df['Judge'].isin(selected_judges)]
    if selected_rounds:
        filtered_df = filtered_df[filtered_df['Round'].isin(selected_rounds)]
    if selected_criteria:
        filtered_df = filtered_df[filtered_df['Criterion'].isin(selected_criteria)]

    fig_crit = px.violin(filtered_df, y="Score", x="Criterion", box=True, points="all", title="Score Distribution by Criterion").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
    fig_judge = px.violin(filtered_df, y="Score", x="Judge", box=True, points="all", title="Score Distribution by Judge").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)

    return fig_crit, fig_judge


## Judges tab callbacks
@callback(
    Output('judge-violin-notes', 'figure'),
    Input('spinner-dropdown', 'value'),
    Input('judge-dropdown', 'value'),
    Input('round-dropdown', 'value'),
    Input('criteria-dropdown', 'value')
)
def update_judge_violin_notes(selected_spinners, selected_judges, selected_rounds, selected_criteria):
    filtered_df = df_long.copy() 
    
    if selected_spinners:
        filtered_df = filtered_df[filtered_df['Spinner'].isin(selected_spinners)]
    if selected_judges:
        filtered_df = filtered_df[filtered_df['Judge'].isin(selected_judges)]
    if selected_rounds:
        filtered_df = filtered_df[filtered_df['Round'].isin(selected_rounds)]
    if selected_criteria:
        filtered_df = filtered_df[filtered_df['Criterion'].isin(selected_criteria)]

    fig_judge = px.violin(filtered_df, y="Score", x="Judge", box=True, points="all", title="Score Distribution by Judge").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)

    return fig_judge

@callback(
    Output('judge-violin-total', 'figure'),
    Input('spinner-dropdown', 'value'),
    Input('judge-dropdown', 'value'),
    Input('round-dropdown', 'value'),
)
def update_judge_violin_total(selected_spinners, selected_judges, selected_rounds):
    filtered_df = df.copy() 
    
    if selected_spinners:
        filtered_df = filtered_df[filtered_df['Spinner'].isin(selected_spinners)]
    if selected_judges:
        filtered_df = filtered_df[filtered_df['Judge'].isin(selected_judges)]
    if selected_rounds:
        filtered_df = filtered_df[filtered_df['Round'].isin(selected_rounds)]

    fig_judge_total = px.violin(filtered_df, y="Total", x="Judge", box=True, points="all", title="Total Score Distribution by Judge").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)

    return fig_judge_total

@callback(
    Output('heatmap-judge-criteria-mean', 'figure'),
    Output('heatmap-judge-criteria-std', 'figure'),
    Input('judge-dropdown', 'value'),
    Input('criteria-dropdown', 'value'),
    Input('spinner-dropdown', 'value'),
    Input('round-dropdown', 'value'),
)
def update_heatmaps_judge_criteria(selected_judge, selected_criteria, selected_spinners, selected_rounds):
    filtered_df = df_long.copy() 
    
    if selected_judge:
        filtered_df = filtered_df[filtered_df['Judge'].isin(selected_judge)]
    if selected_criteria:
        filtered_df = filtered_df[filtered_df['Criterion'].isin(selected_criteria)]
    if selected_spinners:
        filtered_df = filtered_df[filtered_df['Spinner'].isin(selected_spinners)]
    if selected_rounds:
        filtered_df = filtered_df[filtered_df['Round'].isin(selected_rounds)]

    heatmap_mean    = px.imshow(filtered_df.pivot_table(index="Judge", columns="Criterion", values="Score", aggfunc="mean"), text_auto=".2f", aspect="auto", title ="Average Score per Judge/Criterion",color_continuous_scale="Blues").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff", xaxis_title=None, yaxis_title=None)
    heatmap_std     = px.imshow(filtered_df.pivot_table(index="Judge", columns="Criterion", values="Score", aggfunc="std"), text_auto=".2f", aspect="auto", title ="Standard Deviation per Judge/Criterion",color_continuous_scale="Blues").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff", xaxis_title=None, yaxis_title=None)
    return heatmap_mean, heatmap_std
    filtered_df = df_long.copy() 
    
    if selected_spinners:
        filtered_df = filtered_df[filtered_df['Spinner'].isin(selected_spinners)]
    if selected_rounds:
        filtered_df = filtered_df[filtered_df['Round'].isin(selected_rounds)]

    heatmap_std = px.imshow(
        filtered_df.pivot_table(index="Judge", columns="Criterion", values="Score", aggfunc="std"),
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues"
    )
    return heatmap_std


if __name__ == '__main__':
    app.run(debug=True)
