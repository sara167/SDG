import dash
from dash import dcc, callback_context
from dash import html
import pandas as pd
from dash.dependencies import Output, Input, State
import numpy as np
import dash_daq as daq
import plotly.graph_objs as go
from numpy.compat import basestring

df = pd.read_csv("kiva_loans.csv")
df["Date"] = pd.to_datetime(df["posted_time"], format="%Y-%m-%d")
df.sort_values("Date", inplace=True)
df['Year'] = df['Date'].dt.year
df['Year'] = df['Year'].astype(basestring)

df_extreme = pd.read_csv("share-of-population-in-extreme-poverty.csv")
df_tweets = pd.read_csv("Final_Data1.csv")

# newCountry = list(set(df_extreme['country']).intersection(df['country']))
newCountry = list(set(df_extreme['country']).intersection(df['country'], df_tweets['country']))
# print(newCountry)
# print(len(newCountry))


i = 0
while i < len(df['country']):

    if df['country'][i] not in newCountry:
        df.at[i, 'country'] = 'None'
    i = i + 1

i = 0
while i < len(df_extreme['country']):

    if df_extreme['country'][i] not in newCountry:
        df_extreme.at[i, 'country'] = 'None'
    i = i + 1

i = 0
while i < len(df_tweets['country']):

    if df_tweets['country'][i] not in newCountry:
        df_tweets.at[i, 'country'] = 'None'
    i = i + 1

# genders row
# for i in range(len(df.borrower_genders)):
#    final_gender = ''
#    list_of_gender = df['borrower_genders'][i]
#    if type(list_of_gender) != str:
#        final_gender = 'Not answered'
#    else:
#        unique = len(pd.unique((list_of_gender.split(', '))))
#        if unique == 2:
#            final_gender = 'Both'
#        elif unique == 1:
#            if list_of_gender[0] == 'f':
#                final_gender = 'Female'
#            else:
#                final_gender = 'Male'
#
#    df.at[i, 'borrower_genders'] = final_gender

nominalOptions = ['sector', 'activity', 'repayment_interval', 'borrower_genders']
allOptions = [{"label": "Country", "value": 'country', "disabled": False},
              {"label": "Region", "value": 'region', "disabled": False},
              {"label": "Loans", "value": 'loan_amount', "disabled": False},
              {"label": "Number of Lenders", "value": 'lender_count', "disabled": False},
              {"label": "Funded Amount", "value": 'funded_amount', "disabled": False},
              {"label": "Term in Months", "value": 'term_in_months', "disabled": False},
              {"label": "Population below poverty line", "value": 'population_below_poverty', "disabled": False},
              {"label": "Tweets", "value": 'Keyword', "disabled": False},
              {"label": "Year", "value": 'Year', "disabled": False},
              {"label": "Sector", "value": 'sector', "disabled": False},
              {"label": "Activity", "value": 'activity', "disabled": False},
              {"label": "Gender", "value": 'borrower_genders', "disabled": False},
              {"label": "Repayment Interval", "value": 'repayment_interval', "disabled": False}
              ]

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Loans Analytics: Understand Poverty"

# App layout
app.layout = html.Div(

    children=[
        html.Div(
            children=[
                html.H1(
                    children="Loans Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the loans from kiva dataset",
                    className="header-description",
                ),
                html.Div(
                    className="center",
                    # style={'margin-left': '222.5px'},
                    # 'margin-top': '90px',
                    # 'verticalAlign': 'middle'},
                    children=[
                        html.Button('All', id='display_all', className='button'),
                        html.Button('Map', id='display_map', className='button'),
                        html.Button('Bar', id='display_bar', className='button'),
                    ],
                ),
            ],
            className="header",
        ),

        html.Div(
            children=[
                html.H2("Visualization Options",
                        style={'text-align': 'center', 'color': 'grey', 'fontSize': 18, 'marginBottom': '15px',
                               'marginLeft': '5px'}),
            ],
            className="menu",
        ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Location", className="menu-title", id='location_main_title'),
                        dcc.Dropdown(id="slct_location",
                                     options=[],
                                     multi=False,
                                     value='country',
                                     clearable=False,
                                     className="dropdown",
                                     ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Specify Location", className="menu-title", id='location-subtitle'),
                        dcc.Dropdown(id="slct_specificlocation", options=[],
                                     multi=True,
                                     value='',
                                     className="dropdown-scroll",
                                     ),
                    ], className="dropdown",
                ),
            ],
            className="menu",
        ),
        html.Br(),
        html.Br(),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Measure", className="menu-title", id="measure-title"),
                        dcc.Dropdown(id="slct_find",
                                     options=[{"label": "Loans", "value": 'loan_amount'},
                                              {"label": "Number of Lender", "value": 'lender_count'},
                                              {"label": "Funded Amount", "value": 'funded_amount'},
                                              {"label": "Sector", "value": 'sector'},
                                              {"label": "Term in Months", "value": 'term_in_months'},
                                              {"label": "Activity", "value": 'activity'},
                                              {"label": "Gender", "value": 'borrower_genders'},
                                              {"label": "Repayment Interval", "value": 'repayment_interval'},
                                              {"label": "Population below poverty line",
                                               "value": 'population_below_poverty'},
                                              {"label": "Tweets", "value": 'Keyword'}
                                              ],
                                     multi=False,
                                     value='loan_amount',
                                     clearable=False,
                                     className="dropdown",

                                     ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div("Aggregate", className="menu-title"),
                        dcc.Dropdown(id="slct_aggregation",
                                     options=[],
                                     multi=False,
                                     value='sum',
                                     clearable=False,
                                     className="dropdown",
                                     ),
                    ]
                ),

            ],
            className="menu",

        ),
        html.Br(),
        html.Br(),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Additional Filter", className="menu-title"),
                        dcc.Dropdown(id="slct_specificfind_nominal", options=allOptions[6:10],
                                     multi=False,
                                     value='',
                                     clearable=True,
                                     className="dropdown",
                                     ),

                    ]
                ),

                html.Div(
                    children=[
                        html.Div(children="Filter Values", className="menu-title", id='find-subtitle'),
                        dcc.Dropdown(id="slct_specificfind", options=[],
                                     multi=True,
                                     value='',
                                     clearable=True,
                                     className="dropdown",
                                     ),
                    ]
                ),
            ],
            className="menu",
        ),

        html.Br(),
        html.Br(),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Select Sorting", className="menu-title"),
                        dcc.Dropdown(id="slct_sorting",
                                     options=[
                                         {"label": "Top", "value": 'Top'},
                                         {"label": "Bottom", "value": 'Bottom'},
                                     ],
                                     multi=False,
                                     value='',
                                     className="dropdown",
                                     ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Select Value", className="menu-title"),
                        daq.NumericInput(id='slct_nvalue',
                                         value=10,
                                         size='256px'
                                         ),
                    ],
                ),
            ],
            className="menu",
        ),

        html.Br(),
        html.Br(),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Select Order", className="menu-radio"),
                        dcc.RadioItems(id="slct_order",
                                       options=[
                                           {"label": "Ascending", "value": 'Ascending'},
                                           {"label": "Descending", "value": 'Descending'}
                                       ],
                                       value='Ascending',
                                       className="radio",
                                       )
                    ],
                ),

                html.Div(
                    children=[
                        html.Div(children="Date Range", className="menu-date"),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=df.Date.min().date(),
                            max_date_allowed=df.Date.max().date(),
                            start_date=df.Date.min().date(),
                            end_date=df.Date.max().date(),
                            className="date",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    id='map_div',
                    children=dcc.Graph(id='map', figure={}),
                    className='card',
                ),
                html.Div(
                    id='bar_div',
                    children=dcc.Graph(id='bar', figure={}, ),
                    className='card',
                ),
            ],
            className='wrapper',
        ),

    ]
)


@app.callback(
    [Output('location_main_title', 'children'),
     Output('location-subtitle', 'children'),
     Output('measure-title', 'children'),
     Output('slct_location', 'value'),
     Output('slct_find', 'value')
     ],
    [Input('display_bar', 'n_clicks'),
     Input('display_map', 'n_clicks'),
     Input('display_all', 'n_clicks')])
def set_find_options(display_bar, display_map, display_all):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'display_bar' in changed_id:
        return 'X-Axis', 'Specify X-Axis', 'Y-Axis', 'country', 'loan_amount'
    else:
        return 'Location', 'Specify Location', 'Measure', 'country', 'loan_amount'


@app.callback(
    Output('slct_location', 'options'),
    [Input('location_main_title', 'children'),
     Input('slct_find', 'value')])
def set_xy_options(location_main_title, slct_find):
    barOptions = [allOptions[0], allOptions[1], allOptions[7], allOptions[8], allOptions[9], allOptions[10],
                  allOptions[11]]

    if (slct_find == 'population_below_poverty' or slct_find == ['population_below_poverty'] or len(
            slct_find) == 2 and 'population_below_poverty' in slct_find) or (
            slct_find == 'Keyword' or slct_find == ['Keyword'] or len(
        slct_find) == 2 and 'Keyword' in slct_find):

        for x in allOptions:
            if x['value'] != 'country':
                x['disabled'] = True
            else:
                x['disabled'] = False

        for x in barOptions:
            if x['value'] != 'country':
                x['disabled'] = True
            else:
                x['disabled'] = False

    else:
        for x in allOptions:
            if x['value'] != 'country':
                x['disabled'] = False
        for x in barOptions:
            if x['value'] != 'country':
                x['disabled'] = False

    if location_main_title == 'X-Axis':
        return barOptions
    else:
        return [allOptions[0], allOptions[1]]


# First options for all, map, bar
# @app.callback(
#      [Output('slct_find', 'value'),
#      Output('slct_location', 'value'),
#      Output('slct_specificlocation', 'value'),
#      Output('slct_specificfind', 'value')
#      ],
#     [Input('display_bar', 'n_clicks'),
#      Input('display_map', 'n_clicks'),
#      Input('display_all', 'n_clicks')])
# def set_xy_options(display_bar, display_map, display_all):
#     changed_id = [p['prop_id'] for p in callback_context.triggered][0]
#     barOptions = [allOptions[0], allOptions[1], allOptions[7], allOptions[8], allOptions[9], allOptions[10],
#                   allOptions[11]]
#     # if 'display_bar' in changed_id:
#     #     return 'loan_amount', 'country', '', ''
#     # else:
#     return'loan_amount', 'country', '', ''
#

@app.callback(
    [Output('slct_specificfind_nominal', 'options'),
     Output('slct_specificfind_nominal', 'value')],
    [Input('slct_location', 'value'),
     Input('slct_specificfind_nominal', 'value'),
     Input('location_main_title', 'children'),
     Input('slct_find', 'value'),

     ]
)
def set_additionalfilter_options(slct_location, slct_specificfind_nominal, location_main_title, slct_find):
    allFilters = [{"label": "Country", "value": 'country', "disabled": False},
                  {"label": "Region", "value": 'region', "disabled": False},
                  {"label": "Sector", "value": 'sector', "disabled": False},
                  {"label": "Activity", "value": 'activity', "disabled": False},
                  {"label": "Gender", "value": 'borrower_genders', "disabled": False},
                  {"label": "Repayment Interval", "value": 'repayment_interval', "disabled": False},
                  {"label": "Tweets", "value": 'Keyword', "disabled": False}]
    for x in allFilters:
        if x['value'] == slct_location:
            x['disabled'] = True
        else:
            x['disabled'] = False

    if slct_location == slct_specificfind_nominal:
        slct_specificfind_nominal = ''

    keywordCondition = (slct_find == 'Keyword' or slct_find == ['Keyword'])

    populationCondition = (slct_find == 'population_below_poverty' or slct_find == ['population_below_poverty'])

    if keywordCondition or populationCondition:
        slct_specificfind_nominal = ''

    if keywordCondition:
        for x in allFilters:
            if x['value'] == 'Keyword':
                x['disabled'] = False
            else:
                x['disabled'] = True

    elif not keywordCondition:
        for x in allFilters:
            if x['value'] == 'Keyword':
                x['disabled'] = True
            else:
                x['disabled'] = False

    if populationCondition:
        for x in allFilters:
            x['disabled'] = True

    if (len(slct_find) == 2 and 'Keyword' in slct_find) or (
            len(slct_find) == 2 and 'population_below_poverty' in slct_find):
        for x in allFilters:
            x['disabled'] = True
        slct_specificfind_nominal = ''

    if location_main_title == 'X-Axis':
        return allFilters, slct_specificfind_nominal
    else:
        return allFilters[2:7], slct_specificfind_nominal


# @app.callback(
#     [Output('slct_specificfind_nominal', 'disabled'),
#     Output('slct_specificfind', 'disabled')
#      ],
#     Input('slct_find', 'value'))
# def set_disable_filters(slct_find):
#     if slct_find == 'population_below_poverty' or slct_find == ['population_below_poverty'] or len(slct_find) == 2 and 'population_below_poverty' in slct_find:
#         return True, True
#     return False, False

# Aggregate dropdown options
@app.callback(
    [Output('slct_aggregation', 'options'),
     Output('slct_aggregation', 'value')],
    [Input('slct_find', 'value'),
     Input('location_main_title', 'children')],
    [State("slct_find", "options")])
def set_agg_options(slct_find, location_main_title, options):
    if location_main_title == 'X-Axis':
        if slct_find == ['population_below_poverty']:
            return [{"label": "Average", "value": 'mean'}], 'mean'
        elif slct_find == ['Keyword']:
            return [{"label": "Count", "value": 'count'}], 'count'
        elif 'population_below_poverty' in slct_find and 'Keyword' in slct_find:
            return [], ''
        elif slct_find == ['Keyword']:
            return [{"label": "Count", "value": 'count'}], 'count'
        else:

            return [{"label": "Total", "value": 'sum'},
                    {"label": "Count", "value": 'count'},
                    {"label": "Average", "value": 'mean'}], 'sum'

    else:
        the_label = [x['label'] for x in options if x['value'] == slct_find]

        if slct_find == 'population_below_poverty':
            return [{"label": "Average " + the_label[0], "value": 'mean'}], 'mean'
        elif slct_find == 'Keyword':
            return [{"label": "Count " + the_label[0], "value": 'count'}], 'count'
        else:
            return [{"label": "Total " + the_label[0], "value": 'sum'},
                    {"label": "Count " + the_label[0], "value": 'count'},
                    {"label": "Average " + the_label[0], "value": 'mean'}], 'sum'


# @app.callback(
#     [Output('slct_aggregation', 'value'),
#     Input('slct_find', 'value')])
# def set_agg_value(slct_find):
#     print(slct_find)
#     if slct_find == 'population_below_poverty':
#         return 'mean'


# Max value for sorting e.g. 87 for countries
@app.callback(
    Output('slct_nvalue', 'max'),
    Input('slct_location', 'value'))
def set_location_options(slct_location):
    return df[slct_location].nunique()


# disable/enable "select value"
@app.callback(
    Output('slct_nvalue', 'disabled'),
    Input('slct_sorting', 'value')
)
def show_nvalue(slct_sorting):
    if slct_sorting:
        if 'Top' == slct_sorting or 'Bottom' == slct_sorting:
            return False
    return True


# Show nominal values list of items e.g. Country: United States, India, ...
@app.callback(
    Output('slct_specificlocation', 'options'),
    Input('slct_location', 'value')
)
def set_location_options(slct_location):
    mask = ((df.country != 'None'))
    filtered_data = df.loc[mask, :]
    if slct_location in nominalOptions or slct_location == 'country' or slct_location == 'region' or slct_location == 'Year':
        return [{'label': c, 'value': c} for c in np.sort(filtered_data[slct_location].astype(str).unique())]
    else:
        return []


# Show nominal values list of items e.g. Sector: Agriculture, Arts, ...
@app.callback(
    Output('slct_specificfind', 'options'),
    [Input('slct_specificfind_nominal', 'value'),
     Input('slct_specificfind_nominal', 'options')]

)
def set_find_options(slct_find, slct_specificfind_nominal):
    if len(slct_specificfind_nominal) == 4:
        if slct_find in nominalOptions or slct_find == 'Year':
            return [{'label': c, 'value': c} for c in np.sort(df[slct_find].astype(str).unique())]
        else:
            return []

    else:
        if slct_find == 'Keyword':
            return [{'label': c, 'value': c} for c in np.sort(df_tweets[slct_find].astype(str).unique())]

        elif slct_find in nominalOptions or slct_find == 'Year' or slct_find == 'country' or slct_find == 'region':
            return [{'label': c, 'value': c} for c in np.sort(df[slct_find].astype(str).unique())]
        else:
            return []


@app.callback(
    [Output('slct_find', 'multi'),
     Output('slct_find', 'clearable')],
    Input('slct_location', 'options')

)
def set_find_options(slct_location):
    if len(slct_location) > 2:
        return True, True
    return False, False


@app.callback(
    Output('date-range', 'disabled'),
    Input('slct_find', 'value')

)
def set_date(slct_find):
    if slct_find == 'Keyword' or slct_find == ['Keyword'] or len(slct_find) == 2 and 'Keyword' in slct_find:
        return True
    return False


@app.callback(
    Output('slct_find', 'options'),
    [Input('slct_location', 'value'),
     Input('slct_find', 'value'),

     Input('slct_find', 'options')])
def set_measure_options(slct_location, slct_find, slct_find_options):
    allMeasureOptions = [{"label": "Loans", "value": 'loan_amount', "disabled": False},
                         {"label": "Number of Lenders", "value": 'lender_count', "disabled": False},
                         {"label": "Funded Amount", "value": 'funded_amount', "disabled": False},
                         {"label": "Term in Months", "value": 'term_in_months', "disabled": False},
                         {"label": "Population Below Poverty Line", "value": 'population_below_poverty',
                          "disabled": False},
                         {"label": "Tweets", "value": 'Keyword', "disabled": False}]

    if slct_location != 'country':
        for x in allMeasureOptions:
            if x['value'] == 'population_below_poverty' or x['value'] == 'Keyword':
                x['disabled'] = True
            else:
                x['disabled'] = False

    if len(slct_find) == 2:
        i = 0
        while i < len(slct_find):
            for x in allMeasureOptions:
                if x['value'] == slct_find[i]:
                    x['disabled'] = False
                else:
                    x['disabled'] = True
            i = i + 1

    return allMeasureOptions


# hide/show graph e.g. all, bar, map
@app.callback(
    [Output('bar', 'style'),
     Output('map', 'style')],
    [Input('display_bar', 'n_clicks'),
     Input('display_map', 'n_clicks'),
     Input('display_all', 'n_clicks')])
def set_find_options(display_bar, display_map, display_all):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'display_map' in changed_id:
        return {'display': 'none'}, {}
    elif 'display_bar' in changed_id:
        return {}, {'display': 'none'}
    elif 'display_all' in changed_id:
        return {}, {}
    else:
        return {}, {}


@app.callback(
    [Output(component_id='map', component_property='figure'),
     Output(component_id='bar', component_property='figure'),
     Output(component_id='slct_sorting', component_property='options'), ],

    [Input(component_id='slct_location', component_property='value'),
     Input(component_id='slct_location', component_property='options'),
     Input(component_id='slct_find', component_property='value'),
     Input(component_id='slct_specificlocation', component_property='value'),
     Input(component_id='slct_sorting', component_property='value'),
     Input(component_id='slct_order', component_property='value'),
     Input(component_id='slct_nvalue', component_property='value'),
     Input(component_id='slct_aggregation', component_property='value'),
     Input(component_id='slct_specificfind', component_property='value'),
     Input(component_id='slct_specificfind_nominal', component_property='value'),
     Input(component_id="date-range", component_property="start_date"),
     Input(component_id="date-range", component_property="end_date"),
     Input('map', 'style'),
     Input(component_id="display_all", component_property="n_clicks"),
     Input(component_id="display_map", component_property="n_clicks"),
     Input(component_id="display_bar", component_property="n_clicks"),

     ],
    [State("slct_find", "options"),
     State("slct_aggregation", "options")]

)
def update_graph(slct_location, slct_location_options, slct_find, slct_specificlocation, slct_sorting, slct_order,
                 slct_nvalue,
                 slct_aggregation,
                 slct_specificfind, slct_specificfind_nominal, start_date, end_date, map_style,
                 display_all, display_map, display_bar, options, aggoptions):
    mask = ((df.Date >= start_date)
            & (df.Date <= end_date) & (df.country != 'None'))
    filtered_data = df.loc[mask, :]
    Test = filtered_data

    mask2 = ((df_extreme.Year >= pd.to_datetime(start_date, format="%Y-%m-%d").year)
             & (df_extreme.Year <= pd.to_datetime(end_date, format="%Y-%m-%d").year)
             & (df_extreme.country != 'None'))
    Test2 = df_extreme.loc[mask2, :]
    mask3 = (df_tweets.country != 'None')
    Test3 = df_tweets.loc[mask3, :]

    if slct_specificfind and slct_specificfind_nominal == 'Keyword':  # there are specific y values
        Test3 = (Test3[(Test3[slct_specificfind_nominal].isin(slct_specificfind))])

    elif slct_specificfind and slct_specificfind_nominal:  # there are specific y values
        Test = (Test[(Test[slct_specificfind_nominal].isin(slct_specificfind))])

    yAxisNum = 1
    # if len(slct_location_options) > 2:
    if len(slct_find) <= 2:
        if len(slct_find) == 0:
            slct_find = 'loan_amount'
        elif len(slct_find) == 1:
            slct_find = slct_find[0]
        elif len(slct_find) == 2:
            yAxisNum = 2

    ascending = 'Ascending' in slct_order

    if ascending:
        head = 'Bottom'
        tail = 'Top'
    else:
        head = 'Top'
        tail = 'Bottom'
    TestFinal = ['', '', '', '']
    i = 0

    if not slct_specificlocation:  ##no specific location
        if not slct_sorting:  # no sorting, by default ascending
            if yAxisNum == 1:
                if slct_location == 'country' and slct_find == 'population_below_poverty':
                    TestFinal[0] = Test2.groupby(slct_location).aggregate('mean')[slct_find].sort_values(
                        ascending=ascending)
                elif slct_location == 'country' and slct_find == 'Keyword':
                    TestFinal[0] = Test3.groupby(slct_location).aggregate('count')[slct_find].sort_values(
                        ascending=ascending)
                else:
                    TestFinal[0] = Test.groupby(slct_location).aggregate(slct_aggregation)[slct_find].sort_values(
                        ascending=ascending)
            else:
                while i < yAxisNum:
                    if slct_location == 'country' and slct_find[i] == 'population_below_poverty':
                        TestFinal[i] = Test2.groupby(slct_location).aggregate('mean')[slct_find[i]].sort_values(
                            ascending=ascending)
                    elif slct_location == 'country' and slct_find[i] == 'Keyword':
                        TestFinal[i] = Test3.groupby(slct_location).aggregate('count')[slct_find[i]].sort_values(
                            ascending=ascending)
                    else:
                        TestFinal[i] = Test.groupby(slct_location).aggregate(slct_aggregation)[
                            slct_find[i]].sort_values(
                            ascending=ascending)
                    i = i + 1

        elif head in slct_sorting:  # Top
            if yAxisNum == 1:
                if slct_location == 'country' and slct_find == 'population_below_poverty':
                    TestFinal[0] = Test2.groupby(slct_location).aggregate('mean')[slct_find].sort_values(
                        ascending=ascending).head(slct_nvalue)
                elif slct_location == 'country' and slct_find == 'Keyword':
                    TestFinal[0] = Test3.groupby(slct_location).aggregate('count')[slct_find].sort_values(
                        ascending=ascending).head(slct_nvalue)
                else:
                    TestFinal[0] = Test.groupby(slct_location).aggregate(slct_aggregation)[slct_find].sort_values(
                        ascending=ascending).head(slct_nvalue)
            else:
                while i < yAxisNum:
                    if slct_location == 'country' and slct_find[i] == 'population_below_poverty':
                        if i == 0:
                            TestFinal[i] = Test2.groupby(slct_location).aggregate('mean')[slct_find[i]].sort_values(
                                ascending=ascending).head(slct_nvalue)
                        else:
                            TestFinal[i] = Test2.groupby(slct_location).aggregate('mean')[slct_find[i]].sort_values(
                                ascending=ascending)
                    elif slct_location == 'country' and slct_find[i] == 'Keyword':
                        if i == 0:
                            TestFinal[i] = Test3.groupby(slct_location).aggregate('count')[slct_find[i]].sort_values(
                                ascending=ascending).head(slct_nvalue)
                        else:
                            TestFinal[i] = Test3.groupby(slct_location).aggregate('mean')[slct_find[i]].sort_values(
                                ascending=ascending)
                    else:
                        if i == 0:
                            TestFinal[i] = Test.groupby(slct_location).aggregate(slct_aggregation)[
                                slct_find[i]].sort_values(
                                ascending=ascending).head(slct_nvalue)
                        else:
                            TestFinal[i] = Test.groupby(slct_location).aggregate(slct_aggregation)[
                                slct_find[i]].sort_values(
                                ascending=ascending)
                    i = i + 1

        elif tail in slct_sorting:  # Bottom
            if yAxisNum == 1:
                if slct_location == 'country' and slct_find == 'population_below_poverty':
                    TestFinal[0] = Test2.groupby(slct_location).aggregate('mean')[slct_find].sort_values(
                        ascending=ascending).tail(slct_nvalue)
                elif slct_location == 'country' and slct_find == 'Keyword':
                    TestFinal[0] = Test3.groupby(slct_location).aggregate('count')[slct_find].sort_values(
                        ascending=ascending).tail(slct_nvalue)
                else:
                    TestFinal[0] = Test.groupby(slct_location).aggregate(slct_aggregation)[slct_find].sort_values(
                        ascending=ascending).tail(slct_nvalue)
            else:
                while i < yAxisNum:
                    if slct_location == 'country' and slct_find[i] == 'population_below_poverty':
                        if i == 0:
                            TestFinal[i] = Test2.groupby(slct_location).aggregate('mean')[slct_find[i]].sort_values(
                                ascending=ascending).tail(slct_nvalue)
                        else:
                            TestFinal[i] = Test2.groupby(slct_location).aggregate('mean')[slct_find[i]].sort_values(
                                ascending=ascending)
                    elif slct_location == 'country' and slct_find[i] == 'Keyword':
                        if i == 0:
                            TestFinal[i] = Test3.groupby(slct_location).aggregate('count')[slct_find[i]].sort_values(
                                ascending=ascending).tail(slct_nvalue)
                        else:
                            TestFinal[i] = Test3.groupby(slct_location).aggregate('count')[slct_find[i]].sort_values(
                                ascending=ascending)
                    else:
                        if i == 0:
                            TestFinal[i] = Test.groupby(slct_location).aggregate(slct_aggregation)[
                                slct_find[i]].sort_values(
                                ascending=ascending).tail(slct_nvalue)
                        else:
                            TestFinal[i] = Test.groupby(slct_location).aggregate(slct_aggregation)[
                                slct_find[i]].sort_values(
                                ascending=ascending)
                    i = i + 1


    else:  ##specific location
        Test = (Test[(Test[slct_location].isin(slct_specificlocation))])
        Test2 = (Test2[(Test2[slct_location].isin(slct_specificlocation))])
        Test3 = (Test3[(Test3[slct_location].isin(slct_specificlocation))])

        if yAxisNum == 1:
            if slct_location == 'country' and slct_find == 'population_below_poverty':
                TestFinal[i] = Test2.groupby(slct_location).aggregate('mean')[slct_find[i]]
            elif slct_location == 'country' and slct_find == 'Keyword':
                TestFinal[i] = Test3.groupby(slct_location).aggregate('count')[slct_find[i]]
            else:
                TestFinal[0] = Test.groupby(slct_location).aggregate(slct_aggregation)[slct_find]
        else:
            while i < yAxisNum:
                if slct_location == 'country' and slct_find[i] == 'population_below_poverty':
                    TestFinal[i] = Test2.groupby(slct_location).aggregate('mean')[slct_find[i]]
                elif slct_location == 'country' and slct_find[i] == 'Keyword':
                    TestFinal[i] = Test3.groupby(slct_location).aggregate('count')[slct_find[i]]
                else:
                    TestFinal[i] = Test.groupby(slct_location).aggregate(slct_aggregation)[slct_find[i]]
                i = i + 1

    # print(head)
    if yAxisNum > 1 and (slct_sorting is None):
        TestFinal[1] = TestFinal[1].filter(items=TestFinal[0].index.tolist(), axis=0)

    elif yAxisNum > 1 and (tail in slct_sorting or head in slct_sorting):
        TestFinal[1] = TestFinal[1].filter(items=TestFinal[0].index.tolist(), axis=0)

    the_label = ['Not shown']
    aggoptions = [{"label": "Total", "value": 'sum'},
                  {"label": "Count", "value": 'count'},
                  {"label": "Average", "value": 'mean'}]

    if yAxisNum == 1:

        # the_label = [x['label'] for x in options if x['value'] == slct_find]

        for x in aggoptions:

            if x['value'] == slct_aggregation and slct_find == 'population_below_poverty':
                the_label1 = 'Average'
            elif x['value'] == slct_aggregation:
                the_label1 = x['label']

        for x in options:
            if x['value'] == slct_find:
                the_label2 = x['label']

        the_label[0] = the_label1 + ' ' + the_label2

    print(slct_find)
    if yAxisNum > 1:
        the_label = ['', '', '', '']
        counter = 0
        for i in slct_find:
            for x in aggoptions:
                if i == 'population_below_poverty':
                    the_label0 = 'Average'

                elif i == 'Keyword':
                    the_label0 = 'Count'

                elif x['value'] == slct_aggregation:
                    the_label0 = x['label']

            for x in options:
                if x['value'] == i:
                    the_label[counter] = the_label0 + ' ' + x['label']
                    print(the_label[counter])
                    counter = counter + 1

    data = [dict(
        type='choropleth',
        locations=TestFinal[0].index,
        locationmode='country names',
        z=TestFinal[0].values,
        text=TestFinal[0].index,
        colorscale="Viridis",
        reversescale=not ascending,
        marker=dict(line=dict(width=0.7)),
        colorbar=dict(autotick=False, tickprefix='', title=the_label[0], ),
    )]
    fig = dict(data=data)

    if not ascending:
        color = 'Viridis_r'
    else:
        color = 'Viridis'

    # bar chart
    if yAxisNum == 1:
        bar_chart = go.FigureWidget(data=[
            go.Bar(
                x=TestFinal[0].index,
                y=TestFinal[0].values,
                marker={'color': TestFinal[0].values,
                        'colorscale': color})
        ],
            layout=go.Layout(
                yaxis_title=the_label[0]
            )
        )
    elif yAxisNum == 2:

        bar_chart = go.FigureWidget(data=[
            go.Bar(name=the_label[0],
                   x=TestFinal[0].index,
                   y=TestFinal[0].values,
                   yaxis='y',
                   offsetgroup=0,
                   ),
            go.Bar(name=the_label[1],
                   x=TestFinal[1].index,
                   y=TestFinal[1].values,
                   yaxis='y2',
                   offsetgroup=1,
                   )
        ],
            layout={
                'yaxis': {'title': the_label[0]},
                'yaxis2': {'title': the_label[1], 'overlaying': 'y', 'side': 'right'}
            }
        )

    top_label = {"label": "Top", "value": 'Top'}
    bottom_label = {"label": "Bottom", "value": 'Bottom'}

    options = [top_label, bottom_label]

    return fig, bar_chart, options


if __name__ == "__main__":
    app.run_server(debug=True)
