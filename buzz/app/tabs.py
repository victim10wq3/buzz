"""
buzz webapp: everything needed to populate app tabs initially
"""

import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

from buzz.constants import SHORT_TO_LONG_NAME
from .strings import _make_table_name, _make_search_name
from buzz.dashview import CHART_TYPES, _df_to_figure


def _get_cols(corpus):
    """
    Make list of dicts of conll columns (for search/show)
    """
    col_order = ["file", "s", "i"] + list(corpus.columns)
    cols = [
        dict(label=SHORT_TO_LONG_NAME.get(i, i.title()).replace("_", " "), value=i)
        for i in col_order
    ]
    return cols


def _build_dataset_space(df):
    """
    Build the search interface and the conll display
    """
    cols = _get_cols(df)
    cols += [dict(label="Dependencies", value="d"), dict(label="Trees", value="t")]
    df = df.reset_index()
    df = df.drop(["parse", "text"], axis=1, errors="ignore")
    pieces = [
        dcc.Dropdown(
            id="search-target", options=cols, value="w", style={"width": "200px"}
        ),
        dcc.Input(
            id="input-box",
            type="text",
            placeholder="Enter regular expression search query...",
            size="80",
            style={"font-family": "monospace"},
        ),
        daq.BooleanSwitch(
            id="skip-switch", on=False, style={"verticalAlign": "middle"}
        ),
        html.Button("Search", id="search-button"),
    ]
    pieces = [
        html.Div(
            piece,
            style={
                "display": "table-cell",
                "verticalAlign": "middle",
                "height": "35px",
            },
        )
        for piece in pieces
    ]
    # pieces[0].style['position'] = "absolute";
    search_space = html.Div(pieces)
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    conll_table = dash_table.DataTable(
        id="conll-view",
        columns=columns,
        data=data,
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        row_deletable=True,
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=50,
    )
    return html.Div(id="dataset-container", children=[search_space, conll_table])


def _build_frequencies_space(corpus, table):
    """
    Build stuff related to the frequency table
    """
    cols = _get_cols(corpus)
    show_check = dcc.Dropdown(
        placeholder="Features to show",
        multi=True,
        id="show-for-table",
        options=cols,
        value=[],
    )
    subcorpora_drop = dcc.Dropdown(
        id="subcorpora-for-table", options=cols, placeholder="Feature for index"
    )
    relative_drop = dcc.Dropdown(
        id="relative-for-table",
        options=[
            {"label": "Absolute frequency", "value": "ff"},
            {"label": "Relative of result", "value": "tf"},
            {"label": "Relative of corpus", "value": "nf"},
            {"label": "Keyness: log likelihood", "value": "fl"},
            {"label": "Keyness: percent difference", "value": "fp"},
        ],
        placeholder="Relative/keyness calculation",
    )
    sort_drop = dcc.Dropdown(
        id="sort-for-table",
        options=[
            {"label": "Total", "value": "total"},
            {"label": "Infrequent", "value": "infreq"},
            {"label": "Alphabetical", "value": "name"},
            {"label": "Increasing", "value": "increase"},
            {"label": "Decreasing", "value": "decrease"},
            {"label": "Static", "value": "static"},
            {"label": "Turbulent", "value": "turbulent"},
        ],
        placeholder="Sort columns by...",
    )
    columns, data = _update_datatable(corpus, table, conll=False)
    freq_table = dash_table.DataTable(
        id="freq-table",
        columns=columns,
        data=data,
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        row_deletable=True,
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=50,
    )

    style = dict(
        display="inline-block", verticalAlign="middle", height="35px", width="33%"
    )
    left = html.Div(
        [html.Div(show_check, style=style), html.Div(subcorpora_drop, style=style)]
    )
    right = html.Div(
        [
            html.Div(sort_drop, style=style),
            html.Div(relative_drop, style=style),
            html.Button("Generate table", id="table-button", style=style),
        ]
    )
    toolbar = html.Div([left, right])
    return html.Div([toolbar, freq_table])


def _build_concordance_space(df):
    """
    Div representing the concordance tab
    """
    cols = _get_cols(df)
    show_check = dcc.Dropdown(
        multi=True, placeholder="Features to show", id="show-for-conc", options=cols
    )
    conc_space = html.Div([show_check])
    df = df.just.x.NOUN.conc().head(100)
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    conc = dash_table.DataTable(
        id="conctable",
        columns=columns,
        data=data,
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        row_deletable=True,
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=50,
    )

    return html.Div([conc_space, conc])


def _build_chart_space(tables):
    """
    Div representing the chart tab
    """
    charts = []
    for chart_num, kind in [(1, "bar"), (2, "line"), (3, "area")]:

        table_from = [
            dict(value=i, label=_make_table_name(h)) for i, h in enumerate(tables)
        ]
        dropdown = dcc.Dropdown(
            id=f"chart-from-{chart_num}", options=table_from, value=0
        )
        types = [dict(label=i.title(), value=i) for i in sorted(CHART_TYPES)]
        chart_type = dcc.Dropdown(
            id=f"chart-type-{chart_num}", options=types, value=kind
        )
        transpose = (
            daq.BooleanSwitch(
                id=f"chart-transpose-{chart_num}",
                on=False,
                style={"verticalAlign": "middle"},
            ),
        )
        top_n = dcc.Input(
            id=f"chart-top-n-{chart_num}",
            placeholder="Results to plot",
            type="number",
            min=1,
            max=99,
            value=7,
        )

        toolbar = [
            dropdown,
            chart_type,
            top_n,
            transpose,
            html.Button("Update", id=f"figure-button-{chart_num}"),
        ]
        style = dict(display="inline-block", verticalAlign="middle")
        widths = {dropdown: "50%", chart_type: "15%"}
        tools = list()
        for component in toolbar:
            width = widths.get(component, "10%")
            nstyle = {**style, **{"width": width}}
            tools.append(html.Div(component, style=nstyle))
        toolbar = html.Div(tools)
        df = tables["initial"]
        figure = _df_to_figure(df, kind=kind)
        chart_data = dict(id=f"chart-{chart_num}", figure=figure)
        chart_space = html.Div([toolbar, dcc.Graph(**chart_data)])
        collapse = html.Details(
            [html.Summary(f"Chart space {chart_num}"), html.Div(chart_space)],
            open=chart_num == 1,
        )
        charts.append(collapse)
    return html.Div(charts)


def _update_datatable(corpus, df, conll=True):
    """
    Helper for datatables
    """
    if conll:
        col_order = ["file", "s", "i"] + list(corpus.columns)
        col_order = [i for i in col_order if i not in ["parse", "text"]]
    else:
        df.index.names = [f"_{x}" for x in df.index.names]
        col_order = list(df.index.names) + list(df.columns)
    df = df.reset_index()
    df = df[col_order]
    columns = [{"name": i.strip("_"), "id": i} for i in df.columns]
    data = df.to_dict("rows")
    return columns, data


def _make_tabs(title, searches, tables):
    """
    Generate initial layout div
    """
    dataset = _build_dataset_space(searches["corpus"])
    frequencies = _build_frequencies_space(searches["corpus"], tables["initial"])
    chart = _build_chart_space(tables)
    concordance = _build_concordance_space(searches["corpus"])

    search_from = [
        dict(value=i, label=_make_search_name(h)) for i, h in enumerate(searches)
    ]
    clear = html.Button("Clear history", id="clear-history")
    dropdown = dcc.Dropdown(id="search-from", options=search_from, value=0)
    top_bit = [
        html.Div(dropdown, style=dict(display="inline-block", width="90%")),
        html.Div(clear, style=dict(display="inline-block", width="10%")),
    ]
    top_bit = html.Div(top_bit)
    tab_headers = dcc.Tabs(
        id="tabs",
        value="dataset",
        children=[
            dcc.Tab(label="Dataset", value="dataset"),
            dcc.Tab(label="Frequencies", value="frequencies"),
            dcc.Tab(label="Chart", value="chart"),
            dcc.Tab(label="Concordance", value="concordance"),
        ],
    )

    tab_contents = [
        html.Div(
            id="tab-dataset",
            style={"display": "none"},
            children=[html.Div(id="display-dataset", children=[dataset])],
        ),
        html.Div(
            id="tab-frequencies",
            style={"display": "none"},
            children=[html.Div(id="display-frequencies", children=[frequencies])],
        ),
        html.Div(
            id="tab-chart",
            style={"display": "none"},
            children=[html.Div(id="display-chart", children=[chart])],
        ),
        html.Div(
            id="tab-concordance",
            style={"display": "none"},
            children=[html.Div(id="display-concordance", children=[concordance])],
        ),
    ]
    tab_contents = html.Div(children=tab_contents)

    return html.Div(
        [
            html.H1(children=title, style={"textAlign": "center"}),
            top_bit,
            tab_headers,
            tab_contents,
        ]
    )