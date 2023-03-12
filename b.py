import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go

df = pd.read_csv('BI_Analyst_Dataset_1_FY21.csv')

# Net New Clients = Clients [created == 2021, account_close_date == NULL] - Clients [ account_close_date != NULL ]

print(df['account_open_date'].dtype)
# we are converting the column 'account_open_date' and 'account_close_date' into a datetime value
# as the current datatype reads as 'object', this would require string parsing, conversion is easier

df['account_open_date'] = pd.to_datetime(df['account_open_date'])
df['account_close_date'] = pd.to_datetime(df['account_close_date'])

# a dataframe of all clients created in 2021
new_clients_df = df[df['account_open_date'].dt.year == 2021]
closed_clients_df = df[df['account_close_date'].dt.year == 2021]

new_clients = len(new_clients_df)
closed_clients = len(closed_clients_df)
net_new_clients = new_clients - closed_clients
current_clients = len(df) - net_new_clients

# Pie Chart
pie_chart = go.Figure(go.Pie(labels= ['Net New Clients', 'Current Clients'], values= [net_new_clients, current_clients]))

pie_chart2 = go.Figure(go.Pie(labels= ['Net New Clients', 'Closed Clients'], values= [net_new_clients, closed_clients]))


# app
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children= 'Net New Clients Pie Chart'),
    html.H5(children= '*clients that entered and stayed in FY 2021'),
    dcc.Graph(
        id = 'new-new-clients-pie-chart',
        figure = pie_chart
    ),
    html.H2(children= 'Breakdown of New Clients in FY 2021'),
    html.H5(children= 'Total new clients: '+str(new_clients)),
    dcc.Graph(
        id= 'new-client-breakdown',
        figure = pie_chart2
    )
])

if __name__ == '__main__':
    app.run_server(debug= True)

