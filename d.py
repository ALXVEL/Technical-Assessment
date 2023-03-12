import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go

FY22_new_accounts = pd.read_csv('New_Account_Client_Information_FY22.csv')
FY22_information = pd.read_csv('BI_Analyst_Dataset_2_Expected_FY22.csv')

# calculating net new growth by taking the new clients and finding revenue
new_clients = pd.merge(FY22_new_accounts,FY22_information,on='account_unique_id', how='inner')

new_clients_nii_cad = new_clients['nii_cad'].sum()
new_clients_odi_cad = new_clients['odi_cad'].sum()
new_clients_payment_revenue_cad = new_clients['payment_revenue_cad'].sum()
new_clients_service_revenue_cad = new_clients['service_revenue_cad'].sum()

new_clients_total_revenue = new_clients['total_revenue'].sum()

# calculating natural growth by taking existing clients and finding revenue (total sums - new_client sums)
existing_clients_nii_cad = FY22_information['nii_cad'].sum() - new_clients_nii_cad
existing_clients_odi_cad = FY22_information['odi_cad'].sum() - new_clients_odi_cad
existing_clients_payment_revenue_cad = FY22_information['payment_revenue_cad'].sum() - new_clients_payment_revenue_cad
existing_clients_service_revenue_cad = FY22_information['service_revenue_cad'].sum() - new_clients_service_revenue_cad

existing_clients_total_revenue = FY22_information['total_revenue'].sum() - new_clients_total_revenue

# creating pie chart to see relative
pie_chart = go.Figure(go.Pie(labels=['Natural Growth (existing clients)', 'Net New Growth (New Clients)'], values=[existing_clients_total_revenue,new_clients_total_revenue]))

#4 indepth pie charts
nii_cad_pie = go.Figure(go.Pie(labels=['Natural Growth', 'Net New Growth'], values=[existing_clients_nii_cad,new_clients_nii_cad]))
nii_cad_pie.update_layout(title='Net Interest Income (NII)')
odi_cad_pie = go.Figure(go.Pie(labels=['Natural Growth', 'Net New Growth'], values=[existing_clients_odi_cad,new_clients_odi_cad]))
odi_cad_pie.update_layout(title='Other Direct Income (ODI)')
payment_revenue_pie = go.Figure(go.Pie(labels=['Natural Growth', 'Net New Growth'], values=[existing_clients_payment_revenue_cad,new_clients_payment_revenue_cad]))
payment_revenue_pie.update_layout(title='Payment Revenue')
service_revenue_pie = go.Figure(go.Pie(labels=['Natural Growth', 'Net New Growth'], values=[existing_clients_service_revenue_cad,new_clients_service_revenue_cad]))
service_revenue_pie.update_layout(title='Service Revenue')

# app
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children= 'Natural Growth vs Net New Growth (GTB FY 2022)'),
    dcc.Graph(
        id = 'pie-chart',
        figure = pie_chart
    ),
    html.Div(children=[
        dcc.Graph(
            id = 'sub-plots',
            figure = nii_cad_pie
        ),
        dcc.Graph(
            id = 'sub-plots1',
            figure = odi_cad_pie
        ),
    ], style={'display':'flex', 'height': '400px', 'width': '400px'}),
    html.Div(children=[
        dcc.Graph(
            id='sub-plots2',
            figure=payment_revenue_pie
        ),
        dcc.Graph(
            id='sub-plots3',
            figure=service_revenue_pie
        )
    ], style={'display':'flex', 'height': '400px', 'width': '400px'})
])

if __name__ == '__main__':
    app.run_server(debug= True)
