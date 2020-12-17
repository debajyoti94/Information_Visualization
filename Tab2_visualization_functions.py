# in this program we are going to include all the functions for second tab
import pandas
import plotly.graph_objs as go
import squarify, operator
import heapq

# parameters for setting up SQL connection
host = ""
port = 3306
username = ""
password = ""
dbname = ""

# setting up a connection to sql
conn = pymysql.connect(host, user=username, port=port, passwd=password, db=dbname)
conn_cursor = conn.cursor()

# for tab 2 tree map
# Code for counting devtype of different countries with treemap
def developer_type(country_filter):
    # print('reached here')
    country_devtype_qry = (
        "select country, devtype from bs_so_answers where (devtype != 'UNANSWERED' and country != 'UNANSWERED') "
        "and country = '" + country_filter + "'"
    )
    country_devtype_df = pandas.read_sql(country_devtype_qry, con=conn)

    # start here
    devtype_country_wise_dict = {}
    i = 0
    for data in country_devtype_df.itertuples():
        i += 1
        devtype = data[2]
        country = data[1]
        for dev in devtype.split(";"):
            if data[1] in devtype_country_wise_dict:
                #             check for dev type
                if dev in devtype_country_wise_dict[country]:
                    devtype_country_wise_dict[country][dev] += 1
                elif dev not in devtype_country_wise_dict[country]:
                    devtype_country_wise_dict[data[1]][dev] = 1
                else:
                    print("Outlier case")
            else:
                devtype_country_wise_dict[country] = {}
                devtype_country_wise_dict[country][dev] = 1

    # Converting Dataframe to Dictionary
    devtype_country_wise_df = []
    i = 0
    for key, value in devtype_country_wise_dict.items():
        column = []
        for k, v in value.items():
            i += 1
            column.append(key)
            column.append(k)
            column.append(v)
            devtype_country_wise_df.append(column)
            column = []

    # Sorting the data in descending order
    devtype_country_wise_df.sort(key=operator.itemgetter(2), reverse=True)

    # Extracting only the devtype and count
    extract_list = [1, 2]
    items = operator.itemgetter(*extract_list)
    type_count = [items(x) for x in devtype_country_wise_df]


    # Extracting count of each developer
    values = [0] * (i)
    for j in range(0, i):
        values[j] = devtype_country_wise_df[j][2]

    # Extracting the type of developers
    type = [str(0)] * (i)
    for k in range(0, i):
        if devtype_country_wise_df[k][1] == "Database administrator":
            type[k] = "DB"
        elif devtype_country_wise_df[k][1] == "Data or business analyst":
            type[k] = "DA"
        elif devtype_country_wise_df[k][1] == "System administrator":
            type[k] = "SA"
        elif devtype_country_wise_df[k][1] == "DevOps specialist":
            type[k] = "DO"
        elif (
            devtype_country_wise_df[k][1]
            == "Desktop or enterprise applications developer"
        ):
            type[k] = "DT"
        elif (
            devtype_country_wise_df[k][1]
            == "Data scientist or machine learning specialist"
        ):
            type[k] = "DS"
        elif devtype_country_wise_df[k][1] == "Educator or academic researcher":
            type[k] = "ED"
        elif devtype_country_wise_df[k][1] == "QA or test developer":
            type[k] = "QA"
        elif devtype_country_wise_df[k][1] == "Game or graphics developer":
            type[k] = "GG"
        elif devtype_country_wise_df[k][1] == "Marketing or sales professional":
            type[k] = "MS"
        elif devtype_country_wise_df[k][1] == "C-suite executive (CEO, CTO, etc.)":
            type[k] = "CE"
        elif devtype_country_wise_df[k][1] == "Product manager":
            type[k] = "PM"
        elif devtype_country_wise_df[k][1] == "Engineering manager":
            type[k] = "EM"
        elif (
            devtype_country_wise_df[k][1]
            == "Embedded applications or devices developer"
        ):
            type[k] = "EA"
        elif devtype_country_wise_df[k][1] == "Back-end developer":
            type[k] = "BE"
        elif devtype_country_wise_df[k][1] == "Front-end developer":
            type[k] = "FE"
        elif devtype_country_wise_df[k][1] == "Full-stack developer":
            type[k] = "FS"
        elif devtype_country_wise_df[k][1] == "Mobile developer":
            type[k] = "MD"
        elif devtype_country_wise_df[k][1] == "Designer":
            type[k] = "DE"
        elif devtype_country_wise_df[k][1] == "Student":
            type[k] = "ST"

    x = 0.0
    y = 0.0
    width = 100.0
    height = 100.0


    normed = squarify.normalize_sizes(values, width, height)
    rects = squarify.squarify(normed, x, y, width, height)

    # Choose colors from http://colorbrewer2.org/ under "Export"
    color_brewer = [
        "#B3E6E3",
        "#ABE3E0",
        "#A3DFDC",
        "#9BDCD9",
        "#92D8D6",
        "#8AD5D3",
        "#82D1CF",
        "#7ACECC",
        "#72CAC8",
        "#6AC7C5",
        "#62C3C1",
        "#5AC0BE",
        "#51BCBB",
        "#49B9B8",
        "#41B5B4",
        "#39B2B1",
        "#31AEAD",
        "#29ABAA",
        "#21A7A6",
        "#19A4A3",
        "#009999",
    ]
    shapes = []
    annotations = []
    counter = 0

    for r in rects:
        shapes.append(
            dict(
                type="rect",
                x0=r["x"],
                y0=r["y"],
                x1=r["x"] + r["dx"],
                y1=r["y"] + r["dy"],
                line=dict(width=0),
                fillcolor=color_brewer[counter],
            )
        )
        annotations.append(
            dict(
                x=r["x"] + (r["dx"] / 2),
                y=r["y"] + (r["dy"] / 2),
                text=type[counter],
                showarrow=False,
            )
        )
        counter = counter + 1

        if counter >= len(color_brewer):
            counter = 0

    # For hover text
    trace0 = go.Scatter(
        x=[r["x"] + (r["dx"] / 2) for r in rects],
        y=[r["y"] + (r["dy"] / 2) for r in rects],
        text=[(t, v) for t, v in type_count],
        # mode='text'
    )

    layout_treemap = dict(
        title=dict(
            text="Developer Types",
            font=dict(family="Helvetica Neue", size=22.5, color="#FFFFFF"),
        ),
        height=450,
        width=500,
        xaxis=dict(
            showgrid=False, zeroline=False, showline=False, showticklabels=False
        ),
        yaxis=dict(
            showgrid=False, zeroline=False, showline=False, showticklabels=False
        ),
        shapes=shapes,
        annotations=annotations,
        font=dict(family="Helvetica Neue", size=12.5, color="#FFFFFF"),
        hovermode="closest",
        plot_bgcolor="#2D3047",
        paper_bgcolor="#2D3047",
    )
    # With hovertext
    data_treemap = [trace0]

    return data_treemap, layout_treemap


# for bubble chart language you want to work with at country and devtype level
def get_tech_curr_working_df():
    qry_for_curr_tech = (
        "select country, devtype, LanguageWorkedWith as curr_lang from bs_so_answers "
        "where  (devtype != 'UNANSWERED' and country != 'UNANSWERED' and LanguageWorkedWith != 'UNANSWERED');"
    )

    curr_tech_df = pandas.read_sql(qry_for_curr_tech, con=conn)
    # now we parse through every country and split dev type and curr_lang
    dict_curr_tech = {}
    for data in curr_tech_df.itertuples():
        # here we have to parse through every item in country_wise
        country = data[1]
        devtype_combined = data[2]
        tech_combined = data[3]
        # print(devtype_combined)
        # print(tech_combined)
        #         since this is ; sepearated value we need to split it
        local_dev_type = {}
        if country not in dict_curr_tech:
            dict_curr_tech[country] = {}
        for devtype_split in devtype_combined.split(";"):
            # print(devtype_split)
            # we are going to maintain a dict of these devtypes since we need to use only
            # these distinct values to update the main dictionary with the technology frequency

            local_dev_type[devtype_split] = 1
            if devtype_split not in dict_curr_tech[country]:
                dict_curr_tech[country][devtype_split] = {}
                dict_curr_tech[country][devtype_split]["frequency_count"] = 1
                dict_curr_tech[country][devtype_split]["tech"] = {}

            elif devtype_split in dict_curr_tech:
                dict_curr_tech[country][devtype_split]["frequency_count"] += 1
                # dict_curr_tech[devtype_split]

        # now we parse through every technology and update the global dictionary
        for tech_split in tech_combined.split(";"):
            #     now add a count of 1 for all the devtypes that are corresponding to this skill
            for dev_key in local_dev_type:
                if tech_split in dict_curr_tech[country][dev_key]["tech"]:
                    dict_curr_tech[country][dev_key]["tech"][tech_split] += 1
                elif tech_split not in dict_curr_tech[country][dev_key]["tech"]:
                    dict_curr_tech[country][dev_key]["tech"][tech_split] = 1
    return dict_curr_tech


def get_top_10_curr_tech(dict_curr_tech, i_country, i_devtype, i_category):
    print(
        "in get top 10 curr function: filter values are: "
        + str(i_country)
        + " and "
        + str(i_devtype)
    )
    print(
        "Choosing top 10 tech frorm this dictionary:"
        + str(dict_curr_tech[i_country][i_devtype])
    )
    if i_category == "Top 10":
        top_10_curr_tech_keys = heapq.nlargest(
            10,
            dict_curr_tech[i_country][i_devtype]["tech"],
            dict_curr_tech[i_country][i_devtype]["tech"].get,
        )
    elif i_category == "Bottom 10":
        top_10_curr_tech_keys = heapq.nsmallest(
            10,
            dict_curr_tech[i_country][i_devtype]["tech"],
            dict_curr_tech[i_country][i_devtype]["tech"].get,
        )
    top_10_curr_tech_values = []
    for tech in top_10_curr_tech_keys:
        # if tech in dict_curr_tech[i_country][i_devtype]['tech']:
        top_10_curr_tech_values.append(
            dict_curr_tech[i_country][i_devtype]["tech"][tech]
        )


    return top_10_curr_tech_keys, top_10_curr_tech_values


# now we want to see how do these top 10 technologies perform next year amongst the same dev_type population
def how_do_these_tech_perform_next_year():  # i_country, i_devtype, top_10_tech_list):
    qry_for_future_tech = (
        "select country, devtype, LanguageDesireNextYear as future_lang from bs_so_answers "
        "where  (devtype != 'UNANSWERED' and country != 'UNANSWERED' and LanguageDesireNextYear != 'UNANSWERED');"
    )
    future_tech_df = pandas.read_sql(qry_for_future_tech, con=conn)
    # now we parse through every country and split dev type and curr_lang
    dict_future_tech = {}
    for data in future_tech_df.itertuples():
        # here we have to parse through every item in country_wise
        country = data[1]
        devtype_combined = data[2]
        tech_combined = data[3]
        #         since this is ; sepearated value we need to split it
        local_dev_type = {}
        if country not in dict_future_tech:
            dict_future_tech[country] = {}
        for devtype_split in devtype_combined.split(";"):
            # we are going to maintain a dict of these devtypes since we need to use only
            # these distinct values to update the main dictionary with the technology frequency
            local_dev_type[devtype_split] = 1
            if devtype_split not in dict_future_tech[country]:
                dict_future_tech[country][devtype_split] = {}
                dict_future_tech[country][devtype_split]["frequency_count"] = 1
                dict_future_tech[country][devtype_split]["tech"] = {}

            elif devtype_split in dict_future_tech[country]:
                dict_future_tech[country][devtype_split]["frequency_count"] += 1

        # now we parse through every technology and update the global dictionary
        for tech_split in tech_combined.split(";"):
            #     now add a count of 1 for all the devtypes that are corresponding to this skill
            for dev_key in local_dev_type:
                # if tech_split in top_10_tech_list:

                if tech_split in dict_future_tech[country][dev_key]["tech"]:
                    dict_future_tech[country][dev_key]["tech"][tech_split] += 1
                elif tech_split not in dict_future_tech[country][dev_key]["tech"]:
                    dict_future_tech[country][dev_key]["tech"][tech_split] = 1
    #     we need to get 2 lists: one of the skills and one of the values

    return dict_future_tech


def get_top_10_future_tech(dict_future_tech, i_country, i_devtype, top_10_tech_list):
    top_10_future_tech_list_keys = top_10_tech_list
    top_10_future_tech_list_values = []

    for tech in top_10_future_tech_list_keys:
        if tech in dict_future_tech[i_country][i_devtype]["tech"]:
            top_10_future_tech_list_values.append(
                dict_future_tech[i_country][i_devtype]["tech"][tech]
            )
        else:
            top_10_future_tech_list_values.append(0)
    return top_10_future_tech_list_keys, top_10_future_tech_list_values
