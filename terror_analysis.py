import pandas as pd
import webbrowser
import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output 
import dash_core_components as dcc 
import plotly.graph_objects as go  
import plotly.express as px
from dash.exceptions import PreventUpdate

app = dash.Dash()

def load_data():
  dataset_name = "global_terror.csv"
  
  
  global df
  df = pd.read_csv(dataset_name)
  
#   print(df.head(5))
  global month_list
  month = {
         "January":1,
         "February": 2,
         "March": 3,
         "April":4,
         "May":5,
         "June":6,
         "July": 7,
         "August":8,
         "September":9,
         "October":10,
         "November":11,
         "December":12
         }
  month_list= [{"label":key, "value":values} for key,values in month.items()]

  global region_list
  region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ] 

  global country_list
  country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()

  global state_list
  state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()

  global city_list
  city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()

  global attack_type_list
  attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]

  global year_list
  year_list = sorted ( df['iyear'].unique().tolist()  )

  global year_dict
  year_dict = {str(year): str(year) for year in year_list}

  chart_values={"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
  global chart_dd_lst
  chart_dd_lst=[{"label":key,"value":value} for key,value in chart_values.items()]


def open_browser():
  webbrowser.open_new('http://127.0.0.1:8050/')

################### Page Layout
def create_app_ui():
  main_layout = html.Div(children=
    [
        html.Div(children=
        [
            html.Div(className='navbar navbar-dark bg-dark text-light',children=[
                html.H3(children='Terrorism analysis with insights',style={'font-weight':'bolder','font-size':'45px','text-shadow':'4px 4px 4px #e7ff0d'})
            ]),
            dcc.Tabs(id="Tabs", value="map",children=
            [
                #Map tool tabs
                dcc.Tab(label="Map tool" ,id="Map tool",value="map", children=
                [
                    dcc.Tabs(id = "subtabs", value = "worldMap",children = 
                    [
                    dcc.Tab(label="World Map tool", id="World", value="worldMap"),
                    dcc.Tab(label="India Map tool", id="India", value="indiaMap")
                    ])
                ]),
                #Chart tool tabs
                dcc.Tab(label = "Chart Tool", id="Chart tool", value="chart", children=
                [
                    dcc.Tabs(id = "subtabs2", value = "worldChart",children = 
                    [
                    dcc.Tab(label="World Chart tool", id="WorldC", value="worldChart"),
                    dcc.Tab(label="India Chart tool", id="IndiaC", value="indiaChart")
                    ])
                ])
            ])
        ]),
        html.Div(className='text-center bg-info p-2',children=[
            html.H3(children='Filter options')
        ]),
        html.Div(id='data')
    ])
  return main_layout

# Callback for Map tool graphs
@app.callback(
    dash.dependencies.Output('graph-object', 'children'),
    [
        dash.dependencies.Input('month', 'value'),
        dash.dependencies.Input('date', 'value'),
        dash.dependencies.Input('region-dropdown', 'value'),
        dash.dependencies.Input('country-dropdown', 'value'),
        dash.dependencies.Input('state-dropdown', 'value'),
        dash.dependencies.Input('city-dropdown', 'value'),
        dash.dependencies.Input('attacktype-dropdown', 'value'),
        dash.dependencies.Input('year-slider', 'value'), 
        dash.dependencies.Input("Tabs", "value"),
        dash.dependencies.Input("subtabs", "value")
    ]
)
def update_map(month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,tab, subtabs):
    map_figure=None
    print("Data Type of month value = " , str(type(month_value)))
    print("Data of month value = " , month_value)
    
    print("Data Type of Day value = " , str(type(date_value)))
    print("Data of Day value = " , date_value)
    
    print("Data Type of region value = " , str(type(region_value)))
    print("Data of region value = " , region_value)
    
    print("Data Type of country value = " , str(type(country_value)))
    print("Data of country value = " , country_value)
    
    print("Data Type of state value = " , str(type(state_value)))
    print("Data of state value = " , state_value)
    
    print("Data Type of city value = " , str(type(city_value)))
    print("Data of city value = " , city_value)
    
    print("Data Type of Attack value = " , str(type(attack_value)))
    print("Data of Attack value = " , attack_value)
    
    print("Data Type of year value = " , str(type(year_value)))
    print("Data of year value = " , year_value)

    print("Data of Tab value = " , tab)
    print("Data of subtabs value = " , subtabs)
  

    # year_filter
    year_range = range(year_value[0], year_value[1]+1)
    new_df = df[df["iyear"].isin(year_range)]
    
    # month_filter
    if month_value==[] or month_value is None:
        pass
    else:
        if date_value==[] or date_value is None:
            new_df = new_df[new_df["imonth"].isin(month_value)]
        else:
            new_df = new_df[new_df["imonth"].isin(month_value)
                            & (new_df["iday"].isin(date_value))]
     
    if tab == "map":
        # region, country, state, city filter
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value)) &
                                    (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                        (new_df["country_txt"].isin(country_value)) &
                                        (new_df["provstate"].isin(state_value))&
                                        (new_df["city"].isin(city_value))]

        if attack_value == [] or attack_value is None:
            pass
        else:
                new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)] 
                
        map_figure = go.Figure()
        #For cleaning new_df
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
            'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
    
        
        map_figure = px.scatter_mapbox(new_df,
                        lat="latitude", 
                        lon="longitude",
                        height=600,
                        color="attacktype1_txt",
                        animation_frame='iyear',
                        animation_group=new_df['city'],
                        hover_name="city", 
                        hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
                        zoom=1.3
                        )                       
        map_figure.update_layout(mapbox_style="open-street-map",
                    autosize=True,
                    margin=dict(l=50, r=50, t=0, b=0),
                    )
        return dcc.Graph(figure=map_figure)
    else: 
        return None

#Callback for chart tool graphs
@app.callback(
    dash.dependencies.Output('chart-object', 'children'),
    [
        dash.dependencies.Input('chart-dd','value'),
        dash.dependencies.Input('chart-search','value'),
        dash.dependencies.Input("Tabs", "value"),
        dash.dependencies.Input("subtabs2", "value"),
        dash.dependencies.Input('cyear_slider', 'value')
    ]
)
def update_chart(chart_dd,search,tab,subtabs2,chart_year):
    if tab=='chart':
        chart_figure = None
        year_range_c = range(chart_year[0], chart_year[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        print('Value of chart-dd: ',chart_dd)
        print('Value of chart-dd: ',search)
        print('Value of tab: ',tab)
        print('Value of subtab: ',subtabs2)
        print('Range of year: ',chart_year)

        if subtabs2=='worldChart':
            if chart_dd is not None:
                if search is not None:
                    chart_df = df.groupby("iyear")[chart_dd].value_counts().reset_index(name = "count")
                    chart_df  = chart_df[chart_df[chart_dd].str.contains(search, case = False)]
                else:
                    chart_df = df.groupby("iyear")[chart_dd].value_counts().reset_index(name="count")
            else:
                raise PreventUpdate
            chart_figure = px.area(chart_df, x= "iyear", y ="count",color = chart_dd)

        elif subtabs2=='indiaChart':
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
            if chart_dd is not None and chart_df.shape[0]:
                if search is not None:
                    chart_df = chart_df.groupby("iyear")[chart_dd].value_counts().reset_index(name = "count")
                    chart_df  = chart_df[chart_df[chart_dd].str.contains(search, case=False)]
                else:
                    chart_df = chart_df.groupby("iyear")[chart_dd].value_counts().reset_index(name="count")
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dd])
            
            chart_df.loc[0] = [0, 0,"No data"]
        chart_figure = px.area(chart_df, x="iyear", y ="count",height=500,color = chart_dd)
        return dcc.Graph(figure = chart_figure)
    else:
        return None


#For making the dropdowns in layout
@app.callback(
    Output('data','children'),
    [Input('Tabs','value')]
)
def update_data(tab):
    data = None
    if tab =="map":
       data =  html.Div(children=[
        html.Div(className='image p-5',children=[
            html.Div(className='container p-5',children=[
                html.Div(className='row',children=[
                    html.Div(className='form-group col-6',children=[
                    dcc.Dropdown(
                    id='month', 
                    options=month_list,
                    placeholder='Select Month',
                    multi = True
                    )
                    ]),
                    html.Div(className='form-group col-6',children=[
                        dcc.Dropdown(
                            id='date', 
                            placeholder='Select Day',
                            multi = True
                        )
                    ])
                ]),
                html.Div(className='row',children=[
                    html.Div(className='form-group col-6',children=[
                        dcc.Dropdown(
                            id='region-dropdown', 
                            options=region_list,
                            placeholder='Select Region',
                            multi = True
                        )
                    ]),
                    html.Div(className='form-group col-6',children=[
                        dcc.Dropdown(
                            id='country-dropdown', 
                            options=country_list,
                            placeholder='Select Country',
                            multi = True
                        )
                    ])
                ]),
                html.Div(className='row',children=[
                    html.Div(className='form-group col-6',children=[
                        dcc.Dropdown(
                            id='state-dropdown', 
                            options=state_list,
                            placeholder='Select State or Province',
                            multi = True
                        )
                    ]),
                    html.Div(className='form-group col-6',children=[
                        dcc.Dropdown(
                            id='city-dropdown', 
                            options=city_list,
                            placeholder='Select City',
                            multi = True
                        )
                    ])
                ]),
                html.Div(className='form-group',children=[
                    dcc.Dropdown(
                        id='attacktype-dropdown', 
                        options=attack_type_list,
                        placeholder='Select Attack Type',
                        multi = True
                    )
                ])
            ])
        ]),
            html.Br(),
            html.H5('Select Year range', id='year_title',className='d-inline ml-5 p-2 bg-primary text-white'),
                html.Div(className='form-group mt-4 mx-3',children=[
                    dcc.RangeSlider(
                        id='year-slider',
                        min=min(year_list),
                        max=max(year_list),
                        value=[min(year_list),max(year_list)],
                        marks=year_dict,
                        step=None
                    )
                ]),
                html.Br(),
                html.Div(id='graph-object', children = ["World Map is loading"])
        ])

    elif tab=='chart':
        # #Code for chart
        data=html.Div(children=[
            html.Div(className='image p-5',children=[
            html.Div(className='container mt-2 p-5',children=[
                html.Br(),
                html.Div(className='form-group',children=[
                    dcc.Dropdown(
                        id='chart-dd',
                        options=chart_dd_lst,
                        placeholder='Category',
                        value='region_txt'
                    )
                ]),
                html.Div(className='form-group',children=[
                    dcc.Input(
                        id='chart-search',
                        placeholder='Search Filter',
                        type='text'
                    )
                ]),
            ])
            ]),
            html.Br(),
            html.H5('Select the Year', id='year_title',className='d-inline ml-4 p-2 bg-primary text-white'),
            html.Div(className='form-group mt-4 mx-3',children=[
                dcc.RangeSlider(
                        id='cyear_slider',
                        min=min(year_list),
                        max=max(year_list),
                        value=[min(year_list),max(year_list)],
                        marks=year_dict,
                        step=None
                        )
            ]),
            html.Div(id='chart-object', children = ["Chart is loading"])
        ])       
    return data

#Date dropdown list
@app.callback(
    Output("date", "options"),
    [Input("month", "value")]
    )
def update_date(month):
    dt_lst=[x for x in range(1,32)]
    if month is None:
        return[]
    for i in [1,3,5,7,8,10,12]:
        if i in month:
            return [{"label":m, "value":m} for m in dt_lst]
    for i in [4,6,9,11]:
        if i in month:
            return [{"label":m, "value":m} for m in dt_lst[:-1]]
    if month==[2]:
        return [{"label":m, "value":m} for m in dt_lst[:-2]]

#For india map tab
@app.callback([Output("region-dropdown", "value"),
               Output("region-dropdown", "disabled"),
               Output("country-dropdown", "value"),
               Output("country-dropdown", "disabled"),
               Output("state-dropdown", "value"),
               Output("city-dropdown", "value")],
              [Input("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    state=None
    city=None
    if tab == "worldMap":
        pass
    elif tab=="indiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c,state,city

#Country dropdown list
@app.callback(
    Output('country-dropdown', 'options'),
    [
        Input('region-dropdown', 'value'),
    ])
def set_country_options(region_value):
    option = []
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]

#State dropdown list
@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def set_state_options(country_value):
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]

#City dropdown list
@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def set_city_options(state_value):
  # Making the city Dropdown data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]

# Main function
def main():
  print('Application starting..........\n')
  load_data()  
  open_browser()
  
  global app
  app.layout = create_app_ui()
  app.title = "Forsk Terrorism Analysis"
  app.run_server()

  print("\nApplication closed.............")
  df = None
  app = None

if __name__ == '__main__':
    main()