import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import dash_table
from dash.exceptions import PreventUpdate

# Load the old data from the CSV hosted on Google Sheets
#data_source = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTV3EJy6TjvTnubFu_yZhDkRrdCjumzBIePB9zVFD5MslNF96Z7SJFkkBbyGsZciFrVXjdXBI8ckgOE/pub?gid=0&single=true&output=csv'
data = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTV3EJy6TjvTnubFu_yZhDkRrdCjumzBIePB9zVFD5MslNF96Z7SJFkkBbyGsZciFrVXjdXBI8ckgOE/pub?gid=0&single=true&output=csv')
print("old data loaded")
data.drop (['dmf_submit_date'], axis = 1, inplace = True)

# rename column names
new_columns = ['DMF_No','Company','Drug','Year','Month']
data.columns = new_columns
print(data.head())
# initiate app
app = dash.Dash(__name__)
#server = app.server

#function to create dropdown - a dictionary with labels and values
def get_options(long_list):
    dict_list = []
    unique_list = long_list.unique()
    for i in unique_list:
        dict_list.append({'label':i, 'value':i})
    return dict_list

# create lay out
app.layout = html.Div(style={'padding-top':15},children=[
    html.Div(children=[
        html.Div(className='Row',children=[
        html.H1('DRUG MASTER FILE (DMF) DATA',style = {'text-align':'center'}),
        html.Div(className = 'twelve columns div-user-controls',children = [
            html.H4('SEARCH FOR MOLECULE'),
            html.Div(className='twelve columns div-for-dropdown',children=[
                dcc.Input(id = 'searched_query', type = 'text', placeholder='')])
            ,html.Div(className = 'twelve columns div-for-charts', id='dmf_table')])
            ])
        ])
    ])

@app.callback(Output('dmf_table','children'),
              [Input('searched_query','value')])

def callback_func(searched_query):
    if searched_query is None:
        raise PreventUpdate
    filtered_data = data[data.Drug.str.match(searched_query)]
    child = html.Div(children= [dash_table.DataTable(
        data=filtered_data.to_dict('records'),
        columns = [{'id':c,'name':c} for c in filtered_data.columns],
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={'minWidth': 30, 'maxWidth': 140, 'width': 95, 'color':'green',},
        style_header={'minWidth': 30, 'maxWidth': 140, 'width': 95, 'color': 'white', 'backgroundColor': '#354','fontWeight': 'bold'},
        fixed_rows={'headers': True}
        )])
    return child

if __name__ == '__main__':
    app.run_server(debug = True)