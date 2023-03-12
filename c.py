import pandas as pd
import dash
from dash import dash_table
from dash import dcc
from dash import html
import plotly.graph_objs as go

df_FY21 = pd.read_csv('BI_Analyst_Dataset_1_FY21.csv')
df_FY22 = pd.read_csv('BI_Analyst_Dataset_2_Expected_FY22.csv')

#---- FY21 Sums ----
FY21_nii_cad_sum = df_FY21['nii_cad'].sum()
FY21_odi_cad_sum = df_FY21['odi_cad'].sum()
FY21_payment_revenue_cad_sum = df_FY21['payment_revenue_cad'].sum()
FY21_service_revenue_cad_sum = df_FY21['service_revenue_cad'].sum()
FY21_total_revenue_sum = df_FY21['total_revenue'].sum()

#------FY22 Sums -----
FY22_nii_cad_sum = df_FY22['nii_cad'].sum()
FY22_odi_cad_sum = df_FY22['odi_cad'].sum()
FY22_payment_revenue_cad_sum = df_FY22['payment_revenue_cad'].sum()
FY22_service_revenue_cad_sum = df_FY22['service_revenue_cad'].sum()
FY22_total_revenue_sum = df_FY22['total_revenue'].sum()

# ---------------- Bar ------------------
stacked_bar = go.Figure()

stacked_bar.add_trace(go.Bar(x=['FY21', 'FY22'], y=[FY21_nii_cad_sum, FY22_nii_cad_sum], name= 'Net Interest Income (NII)'))
stacked_bar.add_trace(go.Bar(x=['FY21', 'FY22'], y=[FY21_odi_cad_sum, FY22_odi_cad_sum], name= 'Other Direct Income (ODI)'))
stacked_bar.add_trace(go.Bar(x=['FY21', 'FY22'], y=[FY21_payment_revenue_cad_sum, FY22_payment_revenue_cad_sum], name= 'Payment Revenue'))
stacked_bar.add_trace(go.Bar(x=['FY21', 'FY22'], y=[FY21_service_revenue_cad_sum, FY22_service_revenue_cad_sum], name= 'Service Revenue'))

stacked_bar.update_layout(barmode='stack', title='GTB Revenue Growth FY2021 vs FY2022', xaxis_title='Fiscal Year', yaxis_title='Revenue (CAD)')

# dash app
app = dash.Dash()

table = html.Table([
    html.Tr(
        [
            html.Th(''),
            html.Th('FY2021'),
            html.Th('FY2022'),
            html.Th('Difference')
        ]),
    html.Tr(
        [
            html.Td('Net Interest Income (NII)'),
            html.Td(format(FY21_nii_cad_sum,'.3f'), style={'border': '1px solid black', 'padding': '3px'}),
            html.Td(format(FY22_nii_cad_sum,'.3f'), style={'border': '1px solid black', 'padding': '3px'}),
            html.Td(format(FY22_nii_cad_sum - FY21_nii_cad_sum, '.3f'), style={'border': '1px solid black', 'padding': '3px'})
        ]),
    html.Tr(
        [
            html.Td('Other Direct Income (ODI)'),
            html.Td(format(FY21_odi_cad_sum,'.3f'), style={'border': '1px solid black', 'padding': '3px'}),
            html.Td(format(FY22_odi_cad_sum,'.3f'), style={'border': '1px solid black', 'padding': '3px'}),
            html.Td(format(FY22_odi_cad_sum - FY21_odi_cad_sum, '.3f'), style={'border': '1px solid black', 'padding': '3px'})
        ]),
    html.Tr(
        [
            html.Td('Payment Revenue'),
            html.Td(format(FY21_payment_revenue_cad_sum, '.3f'), style={'border': '1px solid black', 'padding': '3px'}),
            html.Td(format(FY22_payment_revenue_cad_sum, '.3f'), style={'border': '1px solid black', 'padding': '3px'}),
            html.Td(format(FY22_payment_revenue_cad_sum - FY21_payment_revenue_cad_sum, '.3f'), style={'border': '1px solid black', 'padding': '3px'})
        ]),
    html.Tr(
        [
            html.Td('Service Revenue'),
            html.Td(format(FY21_service_revenue_cad_sum, '.3f'), style={'border': '1px solid black', 'padding': '3px'}),
            html.Td(format(FY22_service_revenue_cad_sum, '.3f'), style={'border': '1px solid black', 'padding': '3px'}),
            html.Td(format(FY22_service_revenue_cad_sum - FY21_service_revenue_cad_sum, '.3f'), style={'border': '1px solid black', 'padding': '3px'})
         ]),
    html.Tr(
        [
            html.Td('Total Revenue'),
            html.Td(format(FY21_total_revenue_sum, '.3f'), style={'border': '1px solid black', 'padding': '3px'}),
            html.Td(format(FY22_total_revenue_sum, '.3f'), style={'border': '1px solid black', 'padding': '3px'}),
            html.Td(format(FY22_total_revenue_sum - FY21_total_revenue_sum, '.3f'), style={'border': '1px solid black', 'padding': '3px'})
        ])
])

app.layout = html.Div( children=[
    html.H1('GTB Revenue Growth FY2021 vs FY2022'),
    dcc.Graph(id='revenue', figure=stacked_bar),
    table
])

#running
if __name__ == '__main__':
    app.run_server(debug= True)

