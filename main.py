import pymysql
import dash
import dash_html_components as html
import dash_core_components as dcc
import Tab1_visualization_functions.py as tab1
import Tab2_visualization_functions.py as tab2


host = ""
port = 3306
username = ""
password = ""
dbname = ""

# setting up a connection to sql
conn = pymysql.connect(host, user=username, port=port, passwd=password, db=dbname)
conn_cursor = conn.cursor()


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# calling functions start here
country_wise_df = tab1.get_participants_country_wise()
unique_countries = country_wise_df["country"].unique()
country_wise_education_background = tab1.get_country_wise_education_background()
country_wise_job_satisfaction = tab1.get_job_avail_vs_satifaction()
hours_computer_df, hours_outside_df = tab1.get_work_life_balance()

# for education background
default_education_background_df = country_wise_education_background[
    country_wise_education_background["country"] == "India"
]
default_job_satisfaction_df = country_wise_job_satisfaction[
    country_wise_job_satisfaction["country"] == "India"
]

# for worklife balance
default_hours_computer_country_df = hours_computer_df[
    hours_computer_df["country"] == "India"
]
default_hours_outside_country_df = hours_outside_df[
    hours_outside_df["country"] == "India"
]
default_x_axis_time_bckts = default_hours_computer_country_df["time_bckt"]
default_line_hours_outside = default_hours_outside_country_df["cnt"]
default_line_hours_computer = default_hours_computer_country_df["cnt"]
# data prep for work life balance chart

################## for tab 2 ####################
# for treemap
data_treemap, layout_treemap = tab2.developer_type("India")
# for the technology comparison
# first get the default values


# for language chart
dict_curr_tech = tab2.get_tech_curr_working_df("Language")
(
    default_curr_top_10_tech_keys,
    default_curr_top_10_tech_values,
) = tab2.get_top_10_curr_tech(
    dict_curr_tech, "India", "Database administrator", "Top 10"
)
dict_future_tech = tab2.how_do_these_tech_perform_next_year("Language")
(
    default_future_top_10_future_tech_keys,
    default_future_top_10_future_tech_values,
) = tab2.get_top_10_future_tech(
    dict_future_tech, "India", "Database administrator", default_curr_top_10_tech_keys
)
# for database chart
dict_curr_db = tab2.get_tech_curr_working_df("Database")
default_curr_top_10_db_keys, default_curr_top_10_db_values = tab2.get_top_10_curr_tech(
    dict_curr_db, "India", "Database administrator", "Top 10"
)
dict_future_db = tab2.how_do_these_tech_perform_next_year("Database")
(
    default_future_top_10_future_db_keys,
    default_future_top_10_future_db_values,
) = tab2.get_top_10_future_tech(
    dict_future_db, "India", "Database administrator", default_curr_top_10_db_keys
)

# for platform chart
dict_curr_platform = tab2.get_tech_curr_working_df("Platform")
(
    default_curr_top_10_platform_keys,
    default_curr_top_10_platform_values,
) = tab2.get_top_10_curr_tech(
    dict_curr_platform, "India", "Database administrator", "Top 10"
)
dict_future_platform = tab2.how_do_these_tech_perform_next_year("Platform")
(
    default_future_top_10_platform_keys,
    default_future_top_10_platform_values,
) = tab2.get_top_10_future_tech(
    dict_future_platform,
    "India",
    "Database administrator",
    default_curr_top_10_platform_keys,
)

# the axes values have to be in the -x, 0, x range
max_value = (
    max(default_curr_top_10_platform_values)
    if max(default_curr_top_10_platform_values)
    > max(default_future_top_10_platform_values)
    else max(default_future_top_10_platform_values)
)
# x_axis_for_overlay_chart = np.linspace((-1 * max_value), max_value, num= 10, endpoint= True).tolist()
default_future_top_10_platform_values = [
    x * -1 for x in default_future_top_10_platform_values
]

# same way of calling functions for the other technologies

# we need to add a country wise filter
app.layout = html.Div(
    [
        # html.Div([
        dcc.Tabs(
            id="tabs",
            children=[
                dcc.Tab(
                    label="High level View",
                    children=[
                        html.Div(
                            [
                                dcc.Graph(
                                    id="geo_participants",
                                    hoverData={"points": [{"location": "India"}]},
                                    figure={
                                        "data": [
                                            dict(
                                                type="choropleth",
                                                locations=country_wise_df["country"],
                                                z=country_wise_df["freq"],
                                                locationmode="country names",
                                                text=country_wise_df["country"],
                                                textfont=dict(color="#FFFFFF"),
                                                colorscale=[
                                                    [0, "#B8EAA0"],
                                                    [0.01, "#73A65B"],
                                                    [0.09, "#90CF72"],
                                                    [0.2, "#82BA67"],
                                                    [0.5, "#7FCC57"],
                                                    [0.6, "#7FCC57"],
                                                    [0.7, "#529E29"],
                                                    [1, "#366A1C"],
                                                ],
                                            )
                                        ],
                                        "layout": dict(
                                            title=dict(
                                                text="Country-wise Survey Participants",
                                                font=dict(
                                                    family="Helvetica Neue",
                                                    size=22.5,
                                                    color="#ffffFF",
                                                ),
                                            ),  # title='Country-wise Survey Participants',
                                            automargin=True,
                                            autosize=False,
                                            font=dict(
                                                family="sans-serif",
                                                size=12,
                                                color="#ffffFF",
                                            ),
                                            # legend=dict(orientation="h"),
                                            plot_bgcolor="#2D3047",
                                            paper_bgcolor="#2D3047",
                                            geo=dict(projection=dict(type="mollweide"))
                                            # width = 500,
                                            # height = 500
                                            # margin= {'l': 10, 'b': 20, 't': 0, 'r': 0}
                                        ),
                                    },
                                )
                            ],
                            style={
                                "width": "45%",
                                "display": "inline-block",
                                "position": "relative",
                                "left": "10px",
                            },
                        ),  # , 'padding': '0 20'}),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="edu-background",
                                    figure={
                                        "data": [
                                            dict(
                                                values=default_education_background_df[
                                                    "cnt"
                                                ],
                                                labels=default_education_background_df[
                                                    "degree"
                                                ],
                                                type="pie",
                                                hole=0.3,
                                                height=10,
                                                widhth=10,
                                                colorscale="Viridis",
                                            )
                                        ],
                                        "layout": dict(
                                            title=dict(
                                                text="Education Background",
                                                font=dict(
                                                    family="Helvetica Neue",
                                                    size=22.5,
                                                    color="#ffffFF",
                                                ),
                                            ),  # title='Country-wise Survey Participants',
                                            plot_bgcolor="#c7c7c7",
                                            fontsize=200,
                                            paper_bgcolor="#7f7f7f",
                                        ),  # , legend=dict(x=4, y=4))
                                    },
                                )
                            ],
                            style={
                                "width": "40%",
                                "display": "inline-block",
                                "borderBottom": "thin lightgrey solid",
                                "position": "relative",
                                "left": "150px",
                                "right": "-30px",
                            },
                        ),
                        # job satisfaction graph
                        html.Div(
                            [
                                dcc.Graph(
                                    id="job-satisfaction",
                                    figure={
                                        "data": [
                                            dict(
                                                type="heatmap",
                                                z=country_wise_job_satisfaction["cnt"],
                                                x=country_wise_job_satisfaction[
                                                    "JobSatisfaction_up"
                                                ],
                                                y=country_wise_job_satisfaction[
                                                    "JobSearchStatus_clean"
                                                ],
                                                colorscale="Viridis",
                                            )
                                        ],
                                        "layout": dict(
                                            title="Job Satisfaction",
                                            xaxis=dict(
                                                automargin=True,
                                                title="Job Satisfaction",
                                            ),
                                            yaxis=dict(
                                                automargin=True, title="Opportunities"
                                            ),
                                            autosize=False,
                                            width=600,
                                            height=600,
                                            textfont=dict(color="#FFFFFF")
                                            # margin= {'l': 10, 'b': 20, 't': 0, 'r': 0}
                                        ),
                                    },
                                )
                            ],
                            style={
                                "width": "50%",
                                "display": "inline-block",
                                "position": "relative",
                                "left": "10px",
                                "top": "0px",
                            },
                        )  # ends here'display': 'inline-block''borderTop': 'thin lightgrey solid'
                        # new graph ends here
                        ,
                        # new graph will come up here
                        html.Div(
                            [
                                dcc.Graph(
                                    id="work-life-balance-chart",
                                    figure={
                                        "data": [
                                            dict(
                                                x=default_x_axis_time_bckts,
                                                y=default_line_hours_computer,
                                                name="Time spent on computer",
                                                line=dict(
                                                    color=("rgb(22, 96, 167)"),
                                                    width=4,
                                                    dash="dot",
                                                ),
                                            ),
                                            dict(
                                                x=default_x_axis_time_bckts,
                                                y=default_line_hours_outside,
                                                name="Time spent on outside",
                                                line=dict(
                                                    color=("rgb(205, 12, 24)"),
                                                    width=4,
                                                ),
                                            ),
                                        ],
                                        "layout": dict(
                                            title="Work Life Balance",
                                            xaxis=dict(title="Time buckets"),
                                            yaxis=dict(title="# of people"),
                                            width=450,
                                            height=500,
                                        ),
                                    },
                                )  # ends here
                            ],
                            style={
                                "width": "47.3%",
                                "display": "inline-block",
                                "position": "absolute",
                                "left": "630px",
                                "top": "533px",
                            },
                        ),  #'borderTop': 'thin lightgrey solid'
                    ],
                ),  # ,
                dcc.Tab(
                    label="Tab two",
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        #     added this part from here
                                        # html.Label(''),
                                        html.Div(
                                            [
                                                dcc.Dropdown(
                                                    id="country_filter_tab_2",
                                                    options=[
                                                        {"label": i, "value": i}
                                                        for i in unique_countries
                                                    ],
                                                    value="India",
                                                )
                                            ],
                                            style={
                                                "width": "50%",
                                                "display": "inline-block",
                                                "position": "relative",
                                                "left": "10px",
                                                "top": "5px",
                                                "borderBottom": "thin lightgrey solid",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                dcc.RadioItems(
                                                    id="top_10_bottom_10",
                                                    options=[
                                                        {"label": i, "value": i}
                                                        for i in ["Top 10", "Bottom 10"]
                                                    ],
                                                    value="Top 10",
                                                    labelStyle={
                                                        "display": "inline-block",
                                                        "left": "10px",
                                                    },
                                                )
                                            ],
                                            style={
                                                "width": "49%",
                                                "float": "right",
                                                "display": "inline-block",
                                            },
                                        ),
                                    ],
                                    style={
                                        "borderBottom": "thin lightgrey solid",
                                        "backgroundColor": "rgb(250, 250, 250)",
                                        "padding": "10px 5px",
                                    },
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="devtype_distribution",
                                            clickData={
                                                "points": [
                                                    {
                                                        "text": "('Database administrator',)"
                                                    }
                                                ]
                                            },
                                            figure={
                                                "data": data_treemap,
                                                "layout": layout_treemap,
                                            },
                                        )
                                    ],
                                    style={
                                        "width": "50%",
                                        "display": "inline-block",
                                        "position": "relative",
                                        "left": "122px",
                                        "top": "4px",
                                        "borderBottom": "thin lightgrey solid",
                                    },
                                )
                                ,
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="technology_bar_chart",
                                            figure={
                                                "data": [
                                                    {
                                                        "x": default_curr_top_10_tech_keys,
                                                        "y": default_curr_top_10_tech_values,
                                                        "type": "bar",
                                                        "name": "Year 2018",
                                                    },
                                                    {
                                                        "x": default_future_top_10_future_tech_keys,
                                                        "y": default_future_top_10_future_tech_values,
                                                        "type": "bar",
                                                        "name": "Year 2019",
                                                    },
                                                ],
                                                "layout": dict(
                                                    # xaxis=dict(tickangle=-45),
                                                    barmode="group"
                                                ),
                                            },
                                        )
                                    ],
                                    style={
                                        "width": "40%",
                                        "display": "inline-block",  #'borderBottom': 'thin lightgrey solid',
                                        "position": "relative",
                                        "left": "-5px",
                                        "top": "4px",
                                    },  #'right': '-10px'
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="database_bar_chart",
                                            figure={
                                                "data": [
                                                    {
                                                        "x": default_curr_top_10_db_keys,
                                                        "y": default_curr_top_10_tech_values,
                                                        "type": "bar",
                                                        "name": "Year 2018",
                                                    },
                                                    {
                                                        "x": default_future_top_10_future_db_keys,
                                                        "y": default_future_top_10_future_db_values,
                                                        "type": "bar",
                                                        "name": "Year 2019",
                                                    },
                                                ],
                                                "layout": dict(
                                                    # xaxis=dict(tickangle=-45),
                                                    barmode="group"
                                                ),
                                            },
                                        )
                                    ],
                                    style={
                                        "width": "39.5%",
                                        "display": "inline-block",
                                        "borderBottom": "thin lightgrey solid",
                                        "position": "relative",
                                        "left": "120px",
                                        "top": "0px",
                                        "right": "0px",
                                    },
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="platform_bar_chart",
                                            figure={
                                                "data": [
                                                    {
                                                        "x": default_curr_top_10_platform_keys,
                                                        "y": default_curr_top_10_platform_values,
                                                        "type": "bar",
                                                        "name": "Year 2018",
                                                    },
                                                    {
                                                        "x": default_future_top_10_platform_keys,
                                                        "y": default_future_top_10_platform_values,
                                                        "type": "bar",
                                                        "name": "Year 2019",
                                                    },
                                                ],
                                                "layout": dict(
                                                    # xaxis=dict(tickangle=-45),
                                                    barmode="group",
                                                    # range = [(-1* max_value), max_value],
                                                    # bargap=0.1
                                                ),
                                            },
                                        )
                                    ],
                                    style={
                                        "width": "40%",
                                        "display": "inline-block",  #'borderBottom': 'thin lightgrey solid',
                                        "position": "relative",
                                        "left": "128px",
                                        "top": "0px",
                                        "right": "-80px",
                                    },
                                )
                                # ])
                            ]
                        )
                    ],
                ),
            ],
        )
    ]
)

#################################################### linked views function below ####################################################

# create pie chart
def create_edu_background(filter_value):
    # return 'You\'ve selected "{}"'.format(dropdown_value)
    country_filter_df = country_wise_education_background[
        country_wise_education_background["country"] == filter_value
    ]
    # print("At create_edu function: "+str(filter_value))
    return {
        "data": [
            dict(
                values=country_filter_df["cnt"],
                labels=country_filter_df["degree"],
                type="pie",
                hole=0.3,
                height=10,
                width=10,
                textfont=dict(color="#FFFFFF"),
                marker={
                    "colors": [
                        "#60B2E5",
                        "#A997DF",
                        "#7D82B8",
                        "#0F7173",
                        "#FFD23F",
                        "#92B4A7",
                        "#9DD9D2",
                        "#FC5130",
                        "#255957",
                    ]
                },
                # colorscale = 'Viridis'
            )
        ],
        "layout": dict(
            title=dict(
                text="Education Background",
                font=dict(family="Helvetica Neue", size=22.5, color="#ffffFF"),
            ),
            plot_bgcolor="#2D3047",
            paper_bgcolor="#2D3047",
            legend=dict(font=dict(family="sans-serif", size=12, color="#FFFFFF")),
        ),  # , legend=dict(x=4, y=4))
    }


# callback for pie chart
@app.callback(
    dash.dependencies.Output("edu-background", "figure"),
    [dash.dependencies.Input("geo_participants", "hoverData")],
)
def callback_edu_background(hoverData):
    actual_filter_value = hoverData["points"][0]["location"]
    return create_edu_background(actual_filter_value)


# create heatmap
def create_heatmap(filter_value):
    heatmap_colorscale = [
        [0, "#B3E6E3"],
        [0.1, "#A1DEDC"],
        [0.2, "#8FD7D4"],
        [0.3, "#7DCFCD"],
        [0.4, "#6BC7C5"],
        [0.5, "#5AC0BE"],
        [0.6, "#48B8B7"],
        [0.7, "#36B0AF"],
        [0.8, "#24A8A8"],
        [0.9, "#12A1A0"],
        [1.0, "#009999"],
    ]
    # print("At create_heatmap function: " + str(filter_value))
    country_filter_df = country_wise_job_satisfaction[
        country_wise_job_satisfaction["country"] == filter_value
    ]
    # print(country_filter_df)
    return {
        "data": [
            dict(
                type="heatmap",
                z=country_filter_df["cnt"],
                x=country_filter_df["JobSatisfaction_up"],
                y=country_filter_df["JobSearchStatus_clean"],
                colorscale=heatmap_colorscale,
                textfont=dict(color="#FFFFFF"),
            )
        ],
        "layout": dict(
            # legend = dict(font=dict(color='#FFFFFF')),
            legend=dict(font=dict(family="sans-serif", size=12, color="#FFFFFF")),
            title=dict(
                text="Job Satisfaction",
                font=dict(family="Helvetica Neue", size=22.5, color="#ffffFF"),
            ),
            width=600,
            height=600,
            xaxis=dict(
                automargin=True,
                tickfont=dict(family="Helvetica Neue", size=12, color="white"),
                title=dict(
                    text="Job Satisfaction",
                    font=dict(family="Helvetica Neue", size=18, color="#ffffFF"),
                ),
            ),
            yaxis=dict(
                automargin=True,
                tickfont=dict(family="Helvetica Neue", size=12, color="white"),
                title=dict(
                    text="Opportunities",
                    font=dict(family="Helvetica Neue", size=18, color="#ffffFF"),
                ),
            ),
            plot_bgcolor="#2d3047",
            paper_bgcolor="#2d3047",
        ),
    }


# callback for heatmap
@app.callback(
    dash.dependencies.Output("job-satisfaction", "figure"),
    [dash.dependencies.Input("geo_participants", "hoverData")],
)
def callback_job_satisfaction(hoverData):
    actual_filter_value = hoverData["points"][0]["location"]
    print(hoverData)
    return create_heatmap(actual_filter_value)

    #


# create line chart
def create_work_life_balance_chart(filter_value):
    # print("At create_worklife function: " + str(filter_value))
    hours_computer_country_df = hours_computer_df[
        hours_computer_df["country"] == filter_value
    ]
    hours_outside_country_df = hours_outside_df[
        hours_outside_df["country"] == filter_value
    ]
    x_axis_time_bckts = hours_computer_country_df["time_bckt"]
    line_hours_outside = hours_outside_country_df["cnt"]
    line_hours_computer = hours_computer_country_df["cnt"]

    # print(country_filter_df)
    return {
        "data": [
            dict(
                x=x_axis_time_bckts,
                y=line_hours_computer,
                name="Time spent on computer",
                line=dict(color=("rgb(230, 127, 13)"), width=4, dash="dot"),
            ),
            dict(
                x=x_axis_time_bckts,
                y=line_hours_outside,
                name="Time spent on outside",
                line=dict(
                    color=("rgb(51, 153, 255)"),
                    width=4,
                ),
            ),
        ],
        "layout": dict(
            title=dict(
                text="Work Life Balance",
                font=dict(family="Helvetica Neue", size=22.5, color="#FFFFFF"),
            ),
            legend=dict(font=dict(family="Helvetica Neue", size=15, color="#FFFFFF")),
            xaxis=dict(
                title="Time buckets",
                tickfont=dict(
                    family="Helvetica Neue", size=12, tickangle=135, color="white"
                ),
                titlefont=dict(family="Helvetica Neue", size=18, color="#FBFCFF"),
            ),
            yaxis=dict(
                title="Frequency",
                tickfont=dict(family="Helvetica Neue", size=12, color="white"),
                titlefont=dict(family="Helvetica Neue", size=18, color="#FBFCFF"),
            ),
            plot_bgcolor="#2D3047",
            paper_bgcolor="#2D3047",
        ),
    }


# callback for work life balance chart
@app.callback(
    dash.dependencies.Output("work-life-balance-chart", "figure"),
    [dash.dependencies.Input("geo_participants", "hoverData")],
)
def callback_work_life_balance(hoverData):
    # return 'You\'ve selected "{}"'.format(dropdown_value)
    # print("At create_worklife function callback: " + str(hoverData))
    actual_filter_value = hoverData["points"][0]["location"]
    # print(hoverData)
    return create_work_life_balance_chart(actual_filter_value)


####### for tab 2########################
@app.callback(
    dash.dependencies.Output("devtype_distribution", "figure"),
    [dash.dependencies.Input("country_filter_tab_2", "value")],
)
def create_treemap(value):
    data_treemap, layout_treemap = tab2.developer_type(value)
    return {"data": data_treemap, "layout": layout_treemap}


@app.callback(
    dash.dependencies.Output("technology_bar_chart", "figure"),
    [
        dash.dependencies.Input("devtype_distribution", "clickData"),
        dash.dependencies.Input("country_filter_tab_2", "value"),
        dash.dependencies.Input("top_10_bottom_10", "value"),
    ],
)
def update_technology_bar_chart(clickData, i_country, i_category):
    filter = clickData["points"][0]["text"]
    country_filter = i_country
    actual_filter = filter[filter.find("(") + 1 : filter.find(",")]
    actual_filter = actual_filter.replace("'", "")
    devtype_filter = actual_filter

    (
        updated_curr_top_10_tech_keys,
        updated_curr_top_10_tech_values,
    ) = tab2.get_top_10_curr_tech(
        dict_curr_tech, country_filter, devtype_filter, i_category
    )
    (
        updated_future_top_10_tech_keys,
        updated_future_top_10_tech_values,
    ) = tab2.get_top_10_future_tech(
        dict_future_tech, country_filter, devtype_filter, updated_curr_top_10_tech_keys
    )
    return {
        "data": [
            {
                "x": updated_curr_top_10_tech_keys,
                "y": updated_curr_top_10_tech_values,
                "type": "bar",
                "name": "Year 2018",
            },
            {
                "x": updated_future_top_10_tech_keys,
                "y": updated_future_top_10_tech_values,
                "type": "bar",
                "name": "Year 2019",
            },
        ],
        "layout": dict(
            title=dict(
                text="Programming Languages 2018 vs 2019",
                font=dict(family="Helvetica Neue", size=22.5, color="#FFFFFF"),
            ),
            legend=dict(font=dict(family="Helvetica Neue", size=15, color="#FFFFFF")),
            xaxis=dict(
                title="Programming Language",
                tickfont=dict(
                    family="Helvetica Neue", size=12, tickangle=135, color="white"
                ),
                titlefont=dict(family="Helvetica Neue", size=18, color="#FBFCFF"),
            ),
            yaxis=dict(
                title="Frequency",
                tickfont=dict(family="Helvetica Neue", size=12, color="white"),
                titlefont=dict(family="Helvetica Neue", size=18, color="#FBFCFF"),
            ),
            plot_bgcolor="#2D3047",
            paper_bgcolor="#2D3047",
            barmode="group"
            # height=300,
            # width=300
        ),
    }


# chart for database
@app.callback(
    dash.dependencies.Output("database_bar_chart", "figure"),
    [
        dash.dependencies.Input("devtype_distribution", "clickData"),
        dash.dependencies.Input("country_filter_tab_2", "value"),
        dash.dependencies.Input("top_10_bottom_10", "value"),
    ],
)
def update_database_horizontal_chart(clickData, i_country, i_category):
    filter = clickData["points"][0]["text"]
    country_filter = i_country
    actual_filter = filter[filter.find("(") + 1 : filter.find(",")]
    actual_filter = actual_filter.replace("'", "")
    devtype_filter = actual_filter

    (
        updated_curr_top_10_db_keys,
        updated_curr_top_10_db_values,
    ) = tab2.get_top_10_curr_tech(
        dict_curr_db, country_filter, devtype_filter, i_category
    )
    (
        updated_future_top_10_db_keys,
        updated_future_top_10_db_values,
    ) = tab2.get_top_10_future_tech(
        dict_future_db, country_filter, devtype_filter, updated_curr_top_10_db_keys
    )
    return {
        "data": [
            {
                "x": updated_curr_top_10_db_keys,
                "y": updated_curr_top_10_db_values,
                "type": "bar",
                "name": "Year 2018",
            },
            {
                "x": updated_future_top_10_db_keys,
                "y": updated_future_top_10_db_values,
                "type": "bar",
                "name": "Year 2019",
            },
        ],
        "layout": dict(
            title=dict(
                text="Databases 2018 vs 2019",
                font=dict(family="Helvetica Neue", size=22.5, color="#FFFFFF"),
            ),
            legend=dict(font=dict(family="Helvetica Neue", size=15, color="#FFFFFF")),
            xaxis=dict(
                title="Database",
                tickfont=dict(
                    family="Helvetica Neue", size=12, tickangle=135, color="white"
                ),
                titlefont=dict(family="Helvetica Neue", size=18, color="#FBFCFF"),
            ),
            yaxis=dict(
                title="Frequency",
                tickfont=dict(family="Helvetica Neue", size=12, color="white"),
                titlefont=dict(family="Helvetica Neue", size=18, color="#FBFCFF"),
            ),
            plot_bgcolor="#2D3047",
            paper_bgcolor="#2D3047",
            barmode="group",
        ),
    }


# chart for platform
@app.callback(
    dash.dependencies.Output("platform_bar_chart", "figure"),
    [
        dash.dependencies.Input("devtype_distribution", "clickData"),
        dash.dependencies.Input("country_filter_tab_2", "value"),
        dash.dependencies.Input("top_10_bottom_10", "value"),
    ],
)
def update_platform_chart(clickData, i_country, i_category):
    filter = clickData["points"][0]["text"]
    country_filter = i_country
    actual_filter = filter[filter.find("(") + 1 : filter.find(",")]
    actual_filter = actual_filter.replace("'", "")
    devtype_filter = actual_filter

    (
        updated_curr_top_10_platform_keys,
        updated_curr_top_10_platform_values,
    ) = tab2.get_top_10_curr_tech(
        dict_curr_platform, country_filter, devtype_filter, i_category
    )
    (
        updated_future_top_10_platform_keys,
        updated_future_top_10_platform_values,
    ) = tab2.get_top_10_future_tech(
        dict_future_platform,
        country_filter,
        devtype_filter,
        updated_curr_top_10_platform_keys,
    )

    return {
        "data": [
            {
                "x": updated_curr_top_10_platform_keys,
                "y": updated_curr_top_10_platform_values,
                "type": "bar",
                "name": "Year 2018",
            },
            {
                "x": updated_future_top_10_platform_keys,
                "y": updated_future_top_10_platform_values,
                "type": "bar",
                "name": "Year 2019",
            },
        ],
        "layout": dict(
            title=dict(
                text="Platforms 2018 vs 2019",
                font=dict(family="Helvetica Neue", size=22.5, color="#FFFFFF"),
            ),
            legend=dict(font=dict(family="Helvetica Neue", size=15, color="#FFFFFF")),
            xaxis=dict(
                title="Platform",
                tickfont=dict(
                    family="Helvetica Neue", size=12, tickangle=135, color="white"
                ),
                titlefont=dict(family="Helvetica Neue", size=18, color="#FBFCFF"),
            ),
            yaxis=dict(
                title="Frequency",
                tickfont=dict(family="Helvetica Neue", size=12, color="white"),
                titlefont=dict(family="Helvetica Neue", size=18, color="#FBFCFF"),
            ),
            plot_bgcolor="#2D3047",
            paper_bgcolor="#2D3047",
            barmode="group",
        ),
    }



if __name__ == "__main__":
    app.run_server(debug=True)
