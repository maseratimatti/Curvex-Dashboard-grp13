### Curvex Dash App ###
### Udarbejdet af Gruppe 13 ###
### Modul 4, delivery 5 ###

import dash                                                     
from dash import html, dcc, Input, Output, State, dash_table
import dash_table as dt
import pandas as pd                                             
import plotly.express as px
import pymongo                
import mysql.connector as sql                                  
from bson.objectid import ObjectId

# Opretter forbindelse til MongoDB database 
client = pymongo.MongoClient(
    "mongodb+srv://MaseratiMatti:Penge3333@cluster0.pxwo2.mongodb.net/?retryWrites=true&w=majority")
db = client["Curvex"]
collection = db["Scanninger"]

# Opretter forbindelse til MySQL database
db_connection = sql.connect(host='localhost', database='Curvex', 
user='root', password='Abcd12345!')
df1 = pd.read_sql('SELECT b_id, b_fornavn, b_efternavn, b_email FROM Brugere', con=db_connection)

# Eksternt layout hentes ind, som .css fil 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)
dpdown = []
for i in df1['b_id']:
   str(dpdown.append({'label':i,'value':(i)}))

# Layout til dashboardet
app.layout = html.Div([
    html.H1('ADHD Scanninger for Brugere', style={'textAlign': 'center'}),
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    html.Div(id='mongo-datatable', children=[]),
    html.Button("Gem til Mongo Database", id="save-it"),
    html.Div([
        html.Div(id='hist-graph', className='six columns'),
    ], className='row'),
    dcc.Store(id='changed-cell'),
    html.Hr(),
    html.H1("Kontakt infomation for Brugere:", style={"textAlign":"center"}),
    html.Hr(),
    html.P("Vælg Bruger:"),
    dcc.Dropdown(id='dropdown', style={'height': '30px', 'width': '100px'}, options=dpdown),
    html.Div(
        id='table-container',
        className='tableDiv'
    )
])


# Datatable med data fra Mongo database
@app.callback(Output('mongo-datatable', component_property='children'),
              Input('interval_db', component_property='n_intervals')
              )
def populate_datatable(n_intervals):
    # Laver mongoDB kollektionen om til en pandas DataFrame
    df = pd.DataFrame(list(collection.find()))
    # Formertere id fra ObjectId til en string så det kan blive læst af en DataTable
    df['_id'] = df['_id'].astype(str)
    print(df.head(20))

    return [
        dash_table.DataTable(
            id='our-table',
            data=df.to_dict('records'),
            columns=[{'id': p, 'name': p, 'editable': False} if p == '_id'
                     else {'id': p, 'name': p, 'editable': True}
                     for p in df],
        ),
    ]


# Gemmer de celler der var opdateret til Mongo Databasen
app.clientside_callback(
    """
    function (input,oldinput) {
        if (oldinput != null) {
            if(JSON.stringify(input) != JSON.stringify(oldinput)) {
                for (i in Object.keys(input)) {
                    newArray = Object.values(input[i])
                    oldArray = Object.values(oldinput[i])
                    if (JSON.stringify(newArray) != JSON.stringify(oldArray)) {
                        entNew = Object.entries(input[i])
                        entOld = Object.entries(oldinput[i])
                        for (const j in entNew) {
                            if (entNew[j][1] != entOld[j][1]) {
                                changeRef = [i, entNew[j][0]] 
                                break        
                            }
                        }
                    }
                }
            }
            return changeRef
        }
    }    
    """,
    Output('changed-cell', 'data'),
    Input('our-table', 'data'),
    State('our-table', 'data_previous')
)


# App der kan opdatere Mongo databasen og lave et histogram
@app.callback(
    Output("hist-graph", "children"),
    Input("changed-cell", "data"),
    Input("our-table", "data"),
)
def update_d(cc, tabledata):
    if cc is None:
        # Histogram over om brugerene er blevet kontaktet eller ej 
        hist_fig = px.histogram(tabledata, x='Kontaktet', title='Antal brugere kontaktet')
    else:
        print(f'changed cell: {cc}')
        print(f'Current DataTable: {tabledata}')
        x = int(cc[0])

        # Opdatere Mongo Databasen live
        row_id = tabledata[x]['_id']
        col_id = cc[1]
        new_cell_data = tabledata[x][col_id]
        collection.update_one({'_id': ObjectId(row_id)},
                              {"$set": {col_id: new_cell_data}})

        hist_fig = px.histogram(tabledata, x='Kontaktet')

    return dcc.Graph(figure=hist_fig)

# App der fremviser brugerens data fra en  MySQL databasen udfra det valgte bruger ID
@app.callback(
    dash.dependencies.Output('table-container','children'),
    [dash.dependencies.Input('dropdown', 'value')])

def display_table(dpdown):
    df_temp = df1[df1['b_id']==dpdown]
    return html.Div([
        dt.DataTable(
            id='main-table',
            columns=[{'name': i, 'id': i} for i in df_temp.columns],
            data=df_temp.to_dict('rows')
        )
    ])


if __name__ == '__main__':
    app.run_server(debug=False)