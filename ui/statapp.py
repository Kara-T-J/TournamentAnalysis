from dash import Dash, html, dcc, Input, Output, callback
import dash
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import numpy as np

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


judge_violin_total      = px.violin(df, y="Total", x="Judge", box=True, points="all", title="Score Distribution by Judge").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
heatmap_crit_judge_mean = px.imshow(df_long.pivot_table(index="Judge", columns="Criterion", values="Score", aggfunc="mean"), text_auto=".2f", aspect="auto", title = "Average Score per Judge/Criterion",color_continuous_scale="Blues").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff", xaxis_title=None, yaxis_title=None)
heatmap_crit_judge_std  = px.imshow(df_long.pivot_table(index="Judge", columns="Criterion", values="Score", aggfunc="std"), text_auto=".2f", aspect="auto", title ="Standard Deviation per Judge/Criterion",color_continuous_scale="Blues").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff", xaxis_title=None, yaxis_title=None)

def criteria_corr_heatmap(source_df):
    wide = source_df.pivot_table(
        index=["Spinner", "Round", "Judge"],
        columns="Criterion",
        values="Score",
        aggfunc="mean",
    )
    corr_matrix = wide.corr()
    if corr_matrix.empty:
        corr_matrix = pd.DataFrame([[np.nan]], index=["No data"], columns=["No data"])
    else:
        np.fill_diagonal(corr_matrix.values, np.nan)
    return px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Correlation between Criteria",
        color_continuous_scale="Blues",
    ).update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff", xaxis_title=None, yaxis_title=None)

def criterion_vs_total_excl_heatmap(source_df):
    wide = source_df.pivot_table(
        index=["Spinner", "Round", "Judge"],
        columns="Criterion",
        values="Score",
        aggfunc="mean",
    )
    if wide.empty:
        corr_df = pd.DataFrame([[np.nan]], index=["No data"], columns=["No data"])
    else:
        total_all = wide.sum(axis=1)
        rows = []
        judges = []
        for judge, group in wide.groupby(level="Judge"):
            group_total = total_all.loc[group.index]
            judge_corrs = []
            for col in group.columns:
                total_without = group_total - group[col]
                judge_corrs.append(total_without.corr(group[col]))
            rows.append(judge_corrs)
            judges.append(judge)
        corr_df = pd.DataFrame(rows, index=judges, columns=wide.columns)
    return px.imshow(
        corr_df,
        text_auto=".2f",
        aspect="auto",
        title="Correlation: Criterion vs Total (excluding that criterion)",
        color_continuous_scale="Blues",
    ).update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff", xaxis_title=None, yaxis_title=None)

heatmap_crit_correlation = criteria_corr_heatmap(df_long)
crit_total_corr = criterion_vs_total_excl_heatmap(df_long)


df_round_crit = df_long.groupby(['Round', 'Criterion'], as_index=False)['Score'].mean()

round_line_crit = px.line(df_round_crit, x="Round", y="Score", color="Criterion", title="Score per Criterion by Round").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
round_violin_total  = px.violin(df, y="Total", x="Round", box=True, points="all", title="Total Score by Round").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
round_violin_constr = px.violin(df, y="Construction", x="Round", box=True, points="all", title="Construction Score by Round").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
round_violin_creat  = px.violin(df, y="Creativity", x="Round", box=True, points="all", title="Creativity Score by Round").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
round_violin_diff   = px.violin(df, y="Difficulty", x="Round", box=True, points="all", title="Difficulty Score by Round").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
round_violin_exe    = px.violin(df, y="Execution", x="Round", box=True, points="all", title="Execution Score by Round").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)


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
    dcc.Store(id="active-tab", data="overview"),

    # Overview tab
    html.Div([
         html.Div([
             dag.AgGrid(
                 id='data-table',
                 rowData=df_long.to_dict('records'),
                 columnDefs=[{"field": c, "width": COLUMN_WIDTHS.get(c)} for c in df_long.columns],
                 style={
                     "height": "700px",
                     "width": f'{COLUMN_WIDTHS.get("_total", 0)}px',
                     "resize": False,
                 },
                 className="ag-theme-alpine aggrid"
             ),
             dcc.Graph(
                 figure=crit_violin,
                 id ='crit-violin',
                 style={"flex": "1 1 400px", "minWidth": "300px", "height": "700px"},
                 className="violin-plot"
             ),
         ], style={"display": "flex", "flexWrap": "wrap", "gap": "10px", "justifyContent": "center", "marginBottom": "20px","marginTop": "10px"}),
         dcc.Graph(
             figure=judge_violin,
             id ='judge-violin',
             style={"width": "100%", "height": "700px"},
             className="violin-plot"
         ),
     ], id="overview-section", className="body-section"),

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
    ], id="judges-section", className="body-section"),

    # Criteria tab
    html.Div([
        html.Div([
            dcc.Graph(
                figure=crit_violin,
                id ='criteria-violin',
                style={"height": "1000px"},
                className="violin-plot"
            ),
            html.Div([
                dcc.Graph(
                    figure=heatmap_crit_correlation,
                    id ='heatmap-criteria-correlation',
                    style={"height": "500px"},
                    className="heatmap-plot"
                ),
                dcc.Graph(
                    figure=crit_total_corr,
                    id="criteria-total-corr",
                    style={"height": "500px"},
                    className="heatmap-plot"
                ),
            ],className= "filters-actions"),
        ],style={"display": "flex", "flexWrap": "wrap", "gap": "10px", "justifyContent": "center", "marginBottom": "20px","marginTop": "10px"})
    ], id="criteria-section", className="body-section"),

    # Rounds tab
    html.Div([
        html.Div(
        [
            dcc.Graph(
                figure=round_violin_total,
                id ='round_violin_total',
                style={"flex": "1 1 400px", "minWidth": "300px", "height": "700px"},
                className="violin-plot"
            ),
            dcc.Graph(
                figure=round_line_crit,
                id ='round_line_crit',
                style={"flex": "1 1 400px", "minWidth": "300px", "height": "700px"},
                className="violin-plot"
            ),
        ],
        className="heatmap-row"
        ),
        html.Div(
        [
            dcc.Graph(
                figure=round_violin_constr,
                id ='round_violin_constr',
                style={"flex": "1 1 400px", "minWidth": "300px", "height": "700px"},
                className="violin-plot"
            ),
            dcc.Graph(
                figure=round_violin_creat,
                id ='round_violin_creat',
                style={"flex": "1 1 400px", "minWidth": "300px", "height": "700px"},
                className="violin-plot"
            ),
        ],
        className="heatmap-row"
        ),
        html.Div(
        [
            dcc.Graph(
                figure=round_violin_diff,
                id ='round_violin_diff',
                style={"flex": "1 1 400px", "minWidth": "300px", "height": "700px"},
                className="violin-plot"
            ),
            dcc.Graph(
                figure=round_violin_exe,
                id ='round_violin_exe',
                style={"flex": "1 1 400px", "minWidth": "300px", "height": "700px"},
                className="violin-plot"
            ),
        ],
        className="heatmap-row"
        ),
    ], id="rounds-section", className="body-section"),

    # Spinners tab
    html.Div([
        html.H2("Spinners Analysis Coming Soon!", style={"textAlign": "center", "marginTop": "50px"})
    ], id="spinners-section", className="body-section"),
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


## Tab navigation callbacks
@callback(
    Output("active-tab", "data"),
    Input("overview-btn", "n_clicks"),
    Input("judges-btn", "n_clicks"),
    Input("criteria-btn", "n_clicks"),
    Input("rounds-btn", "n_clicks"),
    Input("spinners-btn", "n_clicks"),
)
def set_active_tab(_overview, _judges, _criteria, _rounds, _spinners):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    return ctx.triggered[0]["prop_id"].split(".")[0]

@callback(
    Output("overview-section", "style"),
    Output("judges-section", "style"),
    Output("criteria-section", "style"),
    Output("rounds-section", "style"),
    Output("spinners-section", "style"),
    Output("overview-btn", "className"),
    Output("judges-btn", "className"),
    Output("criteria-btn", "className"),
    Output("rounds-btn", "className"),
    Output("spinners-btn", "className"),
    Input("active-tab", "data"),
)
def render_tabs(active_tab):
    overview_style = {"display": "none"}
    judges_style = {"display": "none"}
    criteria_style = {"display": "none"}
    round_style = {"display": "none"}
    spinners_style = {"display": "none"}

    if active_tab == "overview-btn":
        overview_style = {"display": "block"}
    elif active_tab == "judges-btn":
        judges_style = {"display": "block"}
    elif active_tab == "criteria-btn":
        criteria_style = {"display": "block"}
    elif active_tab == "rounds-btn":
        round_style = {"display":"block"}
    elif active_tab == "spinners-btn":
        spinners_style = {"display":"block"}

    def tab_class(tab_id):
        return "tab-btn tab-btn-active" if active_tab == tab_id else "tab-btn"

    return (
        overview_style,
        judges_style,
        criteria_style,
        round_style,
        spinners_style,
        tab_class("overview-btn"),
        tab_class("judges-btn"),
        tab_class("criteria-btn"),
        tab_class("rounds-btn"),
        tab_class("spinners-btn"),
    )


## Overview tab callbacks
@callback(
    Output('data-table', 'rowData'),
    Input('spinner-dropdown', 'value'),
    Input('judge-dropdown', 'value'),
    Input('round-dropdown', 'value'),
    Input('criteria-dropdown', 'value')
)
def update_table_overview(selected_spinners, selected_judges, selected_rounds, selected_criteria):
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
def update_violin_overview(selected_spinners, selected_judges, selected_rounds, selected_criteria):
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
def update_violin_notes_judge(selected_spinners, selected_judges, selected_rounds, selected_criteria):
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
def update_violin_total_judge(selected_spinners, selected_judges, selected_rounds):
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
def update_heatmaps_criteria_judge(selected_judge, selected_criteria, selected_spinners, selected_rounds):
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


## Criteria tab callbacks
@callback(
    Output('criteria-violin', 'figure'),
    Output('heatmap-criteria-correlation', 'figure'),
    Output('criteria-total-corr', 'figure'),
    Input('spinner-dropdown', 'value'),
    Input('judge-dropdown', 'value'),
    Input('round-dropdown', 'value'),
    Input('criteria-dropdown', 'value')
)
def update_criteria_plot(selected_spinners, selected_judges, selected_rounds, selected_criteria):
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
    fig_corr = criteria_corr_heatmap(filtered_df)
    fig_total_corr = criterion_vs_total_excl_heatmap(filtered_df)

    return fig_crit, fig_corr, fig_total_corr


## Rounds tab callback
@callback(
    Output('round_line_crit', 'figure'),
    Input('spinner-dropdown', 'value'),
    Input('judge-dropdown', 'value'),
    Input('round-dropdown', 'value'),
    Input('criteria-dropdown', 'value')
)
def update_rounds_line(selected_spinners, selected_judges, selected_rounds, selected_criteria):
    filtered_df = df_long.copy() 
    
    if selected_spinners:
        filtered_df = filtered_df[filtered_df['Spinner'].isin(selected_spinners)]
    if selected_judges:
        filtered_df = filtered_df[filtered_df['Judge'].isin(selected_judges)]
    if selected_rounds:
        filtered_df = filtered_df[filtered_df['Round'].isin(selected_rounds)]
    if selected_criteria:
        filtered_df = filtered_df[filtered_df['Criterion'].isin(selected_criteria)]

    df_round_crit_filtered = filtered_df.groupby(['Round', 'Criterion'], as_index=False)['Score'].mean()

    fig_line = px.line(df_round_crit_filtered, x="Round", y="Score", color="Criterion", title="Score per Criterion by Round").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)

    return fig_line

@callback(
    Output('round_violin_total', 'figure'),
    Output('round_violin_constr', 'figure'),
    Output('round_violin_creat', 'figure'),
    Output('round_violin_diff', 'figure'),
    Output('round_violin_exe', 'figure'),
    Input('spinner-dropdown', 'value'),
    Input('judge-dropdown', 'value'),
    Input('round-dropdown', 'value'),
)
def update_rounds_violins(selected_spinners, selected_judges, selected_rounds):
    filtered_df = df.copy() 
    
    if selected_spinners:
        filtered_df = filtered_df[filtered_df['Spinner'].isin(selected_spinners)]
    if selected_judges:
        filtered_df = filtered_df[filtered_df['Judge'].isin(selected_judges)]
    if selected_rounds:
        filtered_df = filtered_df[filtered_df['Round'].isin(selected_rounds)]

    fig_total = px.violin(filtered_df, y="Total", x="Round", box=True, points="all", title="Total Score by Round").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
    fig_constr = px.violin(filtered_df, y="Construction", x="Round", box=True, points="all", title="Construction Score by Round").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
    fig_creat = px.violin(filtered_df, y="Creativity", x="Round", box=True, points="all", title="Creativity Score by Round").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
    fig_diff = px.violin(filtered_df, y="Difficulty", x="Round", box=True, points="all", title="Difficulty Score by Round").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)
    fig_exe = px.violin(filtered_df, y="Execution", x="Round", box=True, points="all", title="Execution Score by Round").update_layout(plot_bgcolor="#edf5ff", paper_bgcolor="#edf5ff").update_yaxes(showgrid=True, gridcolor="#d9e0e8", gridwidth=1, zeroline=False)

    return fig_total, fig_constr, fig_creat, fig_diff, fig_exe


if __name__ == '__main__':
    app.run(debug=True)
